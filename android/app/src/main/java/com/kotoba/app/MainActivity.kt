package com.kotoba.app

import android.Manifest
import android.app.Activity
import android.content.ActivityNotFoundException
import android.content.Intent
import android.content.pm.PackageManager
import android.content.res.Configuration
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.tts.TextToSpeech
import android.util.Log
import android.webkit.JavascriptInterface
import android.webkit.PermissionRequest
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import java.net.HttpURLConnection
import java.net.URL
import java.util.Locale

/**
 * Hosts the whole app as a single full-screen WebView pointed at a
 * Flask server that this same process starts locally via Chaquopy
 * (Python-for-Android). Nothing here talks to the network - the
 * "server" is just Python code running inside this app, listening on
 * the loopback address so the WebView can load it like any other page.
 */
class MainActivity : AppCompatActivity() {

    companion object {
        private const val TAG = "Kotoba"

        // Process-wide, deliberately NOT a per-Activity field. Android can
        // destroy and recreate this Activity while the process (and the
        // Flask server thread inside it) stays alive: back-then-reopen, the
        // reminder notification, fold/unfold, font or locale changes. Each
        // fresh onCreate() used to start a second server on port 5000, which
        // dies with "Address already in use" and - because it happened on a
        // bare Thread - took the whole app down with it.
        @Volatile
        private var serverThreadRunning = false
    }

    private lateinit var webView: WebView
    private val serverUrl = "http://127.0.0.1:5000/"
    private val handler = Handler(Looper.getMainLooper())
    private var startupAttempts = 0
    private val maxStartupAttempts = 80 // ~20s at 250ms apart; Flask's first import can be slow on first launch

    // Bridges the page's <input type="file"> (wallpaper upload) to the
    // system photo picker. A plain WebView never shows a picker on its
    // own for file inputs - that only happens once a WebChromeClient
    // implements onShowFileChooser, below. Must be registered before
    // the activity reaches STARTED, so it's a property, not something
    // created lazily inside the callback.
    private var pendingFileChooserCallback: ValueCallback<Array<Uri>>? = null
    private val fileChooserLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            val callback = pendingFileChooserCallback
            pendingFileChooserCallback = null
            if (callback == null) return@registerForActivityResult

            if (result.resultCode != Activity.RESULT_OK) {
                callback.onReceiveValue(null)
                return@registerForActivityResult
            }
            val data = result.data
            val clip = data?.clipData
            val uris: Array<Uri> = when {
                clip != null -> Array(clip.itemCount) { i -> clip.getItemAt(i).uri }
                data?.data != null -> arrayOf(data.data!!)
                else -> emptyArray()
            }
            callback.onReceiveValue(if (uris.isEmpty()) null else uris)
        }

    // Android 13+ (API 33) requires runtime consent to post notifications
    // at all. Below that this permission is granted automatically at
    // install time, so requesting it there is a harmless no-op.
    // pendingReminderAction runs either right away (permission already
    // granted, or not needed pre-33) or once the user answers the
    // system prompt - either way the alarm still gets scheduled even
    // on "deny", since a silenced notification is a smaller problem
    // than a reminder that silently never got armed.
    private var pendingReminderAction: (() -> Unit)? = null
    private val notificationPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) {
            pendingReminderAction?.invoke()
            pendingReminderAction = null
        }

    // WebRTC microphone requests from the local WebView must pass both
    // Android's runtime permission gate and WebView's PermissionRequest.
    // We never grant camera or other protected WebView resources here.
    private var pendingAudioPermissionRequest: PermissionRequest? = null
    private val microphonePermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            val request = pendingAudioPermissionRequest
            pendingAudioPermissionRequest = null
            if (request == null) return@registerForActivityResult
            if (granted) {
                request.grant(arrayOf(PermissionRequest.RESOURCE_AUDIO_CAPTURE))
            } else {
                request.deny()
            }
        }

    private lateinit var speechBridge: SpeechBridge

    /** Called from [ReminderBridge] before scheduling/showing anything
     *  notification-related, so the OS prompt (Android 13+ only) has a
     *  chance to appear first. */
    fun requestNotificationPermissionThen(action: () -> Unit) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU) {
            action()
            return
        }
        val granted = ContextCompat.checkSelfPermission(
            this, Manifest.permission.POST_NOTIFICATIONS
        ) == PackageManager.PERMISSION_GRANTED
        if (granted) {
            action()
        } else {
            pendingReminderAction = action
            notificationPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }

        webView = findViewById(R.id.webview)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true

        // The page synthesises its own sound effects with the Web Audio
        // API. Android blocks audio until a user gesture by default,
        // which would swallow the first chime of every session.
        webView.settings.mediaPlaybackRequiresUserGesture = false

        // Match the WebView's own backdrop to the system light/dark
        // setting so there's no white flash before the page paints.
        webView.setBackgroundColor(if (isSystemDark()) 0xFF13161A.toInt() else 0xFFEFE7D6.toInt())

        webView.webViewClient = KotobaWebViewClient()
        webView.webChromeClient = KotobaWebChromeClient()
        // Exposes window.KotobaNative.{scheduleReminder,cancelReminder} to
        // the page's settings panel (see static/js/reminder.js). Only the
        // app-bundled page ever runs in this WebView, so there's no
        // untrusted-page risk in exposing it.
        webView.addJavascriptInterface(ReminderBridge(this), "KotobaNative")

        // Native Japanese TTS gives vocabulary, grammar, story and dialogue
        // playback an offline path inside the APK. The JavaScript layer uses
        // this bridge first and falls back to browser speechSynthesis on web.
        speechBridge = SpeechBridge()
        webView.addJavascriptInterface(speechBridge, "KotobaSpeechNative")

        requestHighRefreshRate()

        startFlaskServer()
        pollUntilServerReady()
    }

    /**
     * Asks Android to run this window at the display's fastest available
     * refresh rate (120Hz on most modern phones) instead of the 60Hz a
     * WebView-hosted app otherwise defaults to. This only *requests* the
     * mode - the OS can still decline (battery saver, an older/60Hz-only
     * panel, etc.), so it's a no-op rather than a crash on those devices.
     * Re-applied in onResume() too: some OEM skins reset window
     * attributes like this when an activity comes back to the foreground.
     */
    private fun requestHighRefreshRate() {
        if (!::webView.isInitialized) return
        val display = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            display
        } else {
            @Suppress("DEPRECATION")
            windowManager.defaultDisplay
        } ?: return

        val supportedModes = display.supportedModes ?: return
        val bestMode = supportedModes.maxByOrNull { it.refreshRate } ?: return
        if (bestMode.refreshRate <= display.refreshRate) return // already on the fastest mode

        window.attributes = window.attributes.apply {
            preferredDisplayModeId = bestMode.modeId
        }
    }

    override fun onResume() {
        super.onResume()
        requestHighRefreshRate()
    }

    override fun onDestroy() {
        // Stop the startup poll from touching a dead WebView.
        handler.removeCallbacksAndMessages(null)
        pendingAudioPermissionRequest?.deny()
        pendingAudioPermissionRequest = null
        if (::speechBridge.isInitialized) speechBridge.shutdown()
        super.onDestroy()
    }

    private fun isSystemDark(): Boolean {
        val mode = resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK
        return mode == Configuration.UI_MODE_NIGHT_YES
    }

    /**
     * Everything the app itself serves stays in the WebView. Anything
     * else - in practice the Feedback page's mailto: link - is handed to
     * whichever app on the phone handles it, because a WebView can't
     * open a mail composer and would just show an error page.
     */
    private inner class KotobaWebViewClient : WebViewClient() {

        override fun shouldOverrideUrlLoading(
            view: WebView?,
            request: WebResourceRequest?
        ): Boolean {
            val url = request?.url ?: return false
            return handleExternal(url)
        }

        @Deprecated("Needed for API < 24, which minSdk still allows")
        override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
            if (url == null) return false
            return handleExternal(Uri.parse(url))
        }

        private fun handleExternal(uri: Uri): Boolean {
            val scheme = uri.scheme?.lowercase() ?: return false
            if (scheme == "http" || scheme == "https") {
                // Local Flask pages load in place; a genuinely remote URL
                // has no business opening inside the app shell.
                return if (uri.host == "127.0.0.1" || uri.host == "localhost") {
                    false
                } else {
                    launch(Intent(Intent.ACTION_VIEW, uri))
                }
            }
            return launch(Intent(Intent.ACTION_VIEW, uri))
        }

        private fun launch(intent: Intent): Boolean {
            return try {
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                startActivity(intent)
                true
            } catch (e: ActivityNotFoundException) {
                Toast.makeText(
                    this@MainActivity,
                    "No app on this phone can open that.",
                    Toast.LENGTH_SHORT
                ).show()
                true
            }
        }
    }

    /**
     * Handles the wallpaper picker's <input type="file"> in the page.
     * Without this, tapping "Upload image / GIF" fires the input click
     * exactly as expected, but a bare WebView has no built-in file
     * picker to show, so nothing visibly happens.
     */
    private inner class KotobaWebChromeClient : WebChromeClient() {
        override fun onPermissionRequest(request: PermissionRequest?) {
            val req = request ?: return
            runOnUiThread {
                // Only the bundled local Flask origin may request microphone
                // capture, and only the microphone resource is eligible.
                val host = req.origin?.host?.lowercase()
                val localOrigin = host == "127.0.0.1" || host == "localhost"
                val asksForAudio = req.resources.contains(PermissionRequest.RESOURCE_AUDIO_CAPTURE)
                if (!localOrigin || !asksForAudio) {
                    req.deny()
                    return@runOnUiThread
                }

                val granted = ContextCompat.checkSelfPermission(
                    this@MainActivity, Manifest.permission.RECORD_AUDIO
                ) == PackageManager.PERMISSION_GRANTED
                if (granted) {
                    req.grant(arrayOf(PermissionRequest.RESOURCE_AUDIO_CAPTURE))
                } else {
                    pendingAudioPermissionRequest?.deny()
                    pendingAudioPermissionRequest = req
                    microphonePermissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
                }
            }
        }

        override fun onPermissionRequestCanceled(request: PermissionRequest?) {
            if (request != null && pendingAudioPermissionRequest === request) {
                pendingAudioPermissionRequest = null
            }
        }

        override fun onShowFileChooser(
            view: WebView?,
            filePathCallback: ValueCallback<Array<Uri>>?,
            fileChooserParams: FileChooserParams?
        ): Boolean {
            // Only one chooser can be in flight at a time; cancel any
            // stale one so its Promise on the JS side doesn't hang.
            pendingFileChooserCallback?.onReceiveValue(null)
            pendingFileChooserCallback = filePathCallback

            val intent = fileChooserParams?.createIntent()
                ?: Intent(Intent.ACTION_GET_CONTENT).apply {
                    type = "image/*"
                    addCategory(Intent.CATEGORY_OPENABLE)
                }

            return try {
                fileChooserLauncher.launch(intent)
                true
            } catch (e: ActivityNotFoundException) {
                pendingFileChooserCallback = null
                Toast.makeText(
                    this@MainActivity,
                    "No app on this phone can pick a photo.",
                    Toast.LENGTH_SHORT
                ).show()
                false
            }
        }
    }

    /** Native offline Japanese text-to-speech exposed as
     *  window.KotobaSpeechNative to the app's bundled pages. */
    private inner class SpeechBridge : TextToSpeech.OnInitListener {
        private var tts: TextToSpeech? = TextToSpeech(this@MainActivity, this)
        @Volatile private var ready = false

        override fun onInit(status: Int) {
            if (status != TextToSpeech.SUCCESS) return
            val engine = tts ?: return
            val result = engine.setLanguage(Locale.JAPAN)
            ready = result != TextToSpeech.LANG_MISSING_DATA &&
                result != TextToSpeech.LANG_NOT_SUPPORTED
        }

        @JavascriptInterface
        fun speak(text: String?, rate: Double) {
            val clean = text?.trim().orEmpty()
            if (clean.isEmpty()) return
            runOnUiThread {
                val engine = tts ?: return@runOnUiThread
                if (!ready) {
                    Toast.makeText(
                        this@MainActivity,
                        "Japanese speech data is not ready on this device.",
                        Toast.LENGTH_SHORT
                    ).show()
                    return@runOnUiThread
                }
                engine.setSpeechRate(rate.coerceIn(0.55, 1.35).toFloat())
                engine.speak(clean, TextToSpeech.QUEUE_FLUSH, null, "kotoba-${System.nanoTime()}")
            }
        }

        @JavascriptInterface
        fun stop() {
            runOnUiThread { tts?.stop() }
        }

        fun shutdown() {
            tts?.stop()
            tts?.shutdown()
            tts = null
            ready = false
        }
    }

    private fun startFlaskServer() {
        // Flask's app.run() blocks the calling thread forever, so it
        // must never run on the UI thread - this app has exactly one
        // background thread whose only job is to keep it alive.
        // If one is already running (this Activity was recreated), reuse it.
        synchronized(MainActivity::class.java) {
            if (serverThreadRunning) return
            serverThreadRunning = true
        }
        Thread {
            try {
                val py = Python.getInstance()
                val module = py.getModule("kotoba_app.app")
                module.callAttr("run_server")
            } catch (t: Throwable) {
                // An uncaught exception on any thread kills the whole
                // process on Android. Log it instead; the startup poll
                // below will then show Flask's own error page rather
                // than the app vanishing.
                Log.e(TAG, "Flask server thread failed", t)
            } finally {
                serverThreadRunning = false
            }
        }.start()
    }

    private fun pollUntilServerReady() {
        Thread {
            val up = isServerRespondingNow()
            handler.post {
                // The Activity may have been destroyed while we were polling.
                if (isFinishing || isDestroyed) return@post
                if (up) {
                    webView.loadUrl(serverUrl)
                } else if (startupAttempts < maxStartupAttempts) {
                    startupAttempts++
                    handler.postDelayed({ pollUntilServerReady() }, 250)
                } else {
                    // Something's genuinely wrong (not just "still starting up") -
                    // show whatever Flask/Chaquopy last had to say rather than a
                    // silent blank screen.
                    webView.loadUrl(serverUrl)
                }
            }
        }.start()
    }

    private fun isServerRespondingNow(): Boolean {
        return try {
            val conn = URL(serverUrl).openConnection() as HttpURLConnection
            conn.connectTimeout = 200
            conn.readTimeout = 200
            conn.requestMethod = "GET"
            val ok = conn.responseCode == 200
            conn.disconnect()
            ok
        } catch (e: Exception) {
            false
        }
    }

    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
