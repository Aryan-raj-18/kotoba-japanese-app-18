package com.kotoba.app

import android.app.AlarmManager
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.os.Build
import android.webkit.JavascriptInterface
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import java.util.Calendar

/**
 * Everything behind Settings -> "Daily reminder": remembering the
 * chosen time, asking AlarmManager to wake the app once a day, and
 * showing the actual notification. A WebView page can't do any of this
 * by itself (JS timers die the moment the app is closed), which is why
 * it's all native and reached from the page only through [ReminderBridge].
 */
object ReminderScheduler {
    const val PREFS_NAME = "kotoba_reminder"
    private const val KEY_ENABLED = "enabled"
    private const val KEY_HOUR = "hour"
    private const val KEY_MINUTE = "minute"
    private const val REQUEST_CODE = 1001
    const val CHANNEL_ID = "daily_reminder"

    private fun prefs(context: Context): SharedPreferences =
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    private fun pendingIntent(context: Context): PendingIntent {
        val intent = Intent(context, ReminderAlarmReceiver::class.java)
        val flags = PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        return PendingIntent.getBroadcast(context, REQUEST_CODE, intent, flags)
    }

    /** Next occurrence of hour:minute that is strictly in the future -
     *  today if that time hasn't passed yet, tomorrow otherwise. Reused
     *  both when the user first turns the reminder on and when the
     *  alarm reschedules itself right after firing (see
     *  [ReminderAlarmReceiver]), since "today's slot already passed" is
     *  true in both cases whenever it should recompute to tomorrow.
     */
    private fun nextTrigger(hour: Int, minute: Int): Long {
        val cal = Calendar.getInstance()
        cal.set(Calendar.HOUR_OF_DAY, hour)
        cal.set(Calendar.MINUTE, minute)
        cal.set(Calendar.SECOND, 0)
        cal.set(Calendar.MILLISECOND, 0)
        if (cal.timeInMillis <= System.currentTimeMillis()) {
            cal.add(Calendar.DAY_OF_YEAR, 1)
        }
        return cal.timeInMillis
    }

    fun schedule(context: Context, hour: Int, minute: Int) {
        prefs(context).edit()
            .putBoolean(KEY_ENABLED, true)
            .putInt(KEY_HOUR, hour)
            .putInt(KEY_MINUTE, minute)
            .apply()

        val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        // setAndAllowWhileIdle rather than the *Exact variants: it needs
        // no special "Alarms & reminders" permission on Android 12+ and
        // a practice reminder doesn't need to-the-minute precision - it
        // can land a little late (Doze-deferred) without anyone minding.
        alarmManager.setAndAllowWhileIdle(
            AlarmManager.RTC_WAKEUP,
            nextTrigger(hour, minute),
            pendingIntent(context)
        )
    }

    fun cancel(context: Context) {
        prefs(context).edit().putBoolean(KEY_ENABLED, false).apply()
        val alarmManager = context.getSystemService(Context.ALARM_SERVICE) as AlarmManager
        alarmManager.cancel(pendingIntent(context))
    }

    /** Re-reads the saved choice and re-arms the alarm - used after a
     *  reboot, since AlarmManager forgets everything when the phone
     *  restarts. */
    fun rescheduleIfEnabled(context: Context) {
        val p = prefs(context)
        if (p.getBoolean(KEY_ENABLED, false)) {
            schedule(context, p.getInt(KEY_HOUR, 19), p.getInt(KEY_MINUTE, 0))
        }
    }

    fun ensureChannel(context: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val manager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        if (manager.getNotificationChannel(CHANNEL_ID) != null) return
        val channel = NotificationChannel(
            CHANNEL_ID,
            "Daily reminder",
            NotificationManager.IMPORTANCE_DEFAULT
        )
        channel.description = "A once-a-day nudge to keep your Kotoba streak going."
        manager.createNotificationChannel(channel)
    }
}

/** Fires at the chosen time: shows the notification, then re-arms
 *  itself for the same time tomorrow (setAndAllowWhileIdle is one-shot,
 *  it doesn't repeat on its own the way setInexactRepeating does). */
class ReminderAlarmReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        ReminderScheduler.ensureChannel(context)

        val openApp = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        val contentIntent = PendingIntent.getActivity(
            context, 0, openApp,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(context, ReminderScheduler.CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle("Time to practice \u65e5\u672c\u8a9e")
            .setContentText("A few minutes now keeps your streak alive.")
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setAutoCancel(true)
            .setContentIntent(contentIntent)
            .build()

        // POST_NOTIFICATIONS can be denied on API 33+; NotificationManagerCompat
        // .areNotificationsEnabled() reflects that (and the pre-33 user-level
        // toggle too), so this just quietly skips showing rather than crashing
        // on a SecurityException.
        if (NotificationManagerCompat.from(context).areNotificationsEnabled()) {
            NotificationManagerCompat.from(context).notify(2001, notification)
        }

        val p = context.getSharedPreferences(ReminderScheduler.PREFS_NAME, Context.MODE_PRIVATE)
        val hour = p.getInt("hour", 19)
        val minute = p.getInt("minute", 0)
        if (p.getBoolean("enabled", false)) {
            ReminderScheduler.schedule(context, hour, minute)
        }
    }
}

/** Alarms don't survive a reboot - re-arm on boot if the reminder was on. */
class ReminderBootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            ReminderScheduler.rescheduleIfEnabled(context)
        }
    }
}

/**
 * The page's only way to reach any of the above. Installed on the
 * WebView as `window.KotobaNative` (see MainActivity.kt); methods here
 * run on a WebView-owned thread, not necessarily the UI thread, so
 * anything touching the Activity (the permission prompt) is handed off
 * via [MainActivity.runOnUiThread].
 */
class ReminderBridge(private val activity: MainActivity) {
    @JavascriptInterface
    fun scheduleReminder(hour: Int, minute: Int) {
        activity.runOnUiThread {
            activity.requestNotificationPermissionThen {
                ReminderScheduler.ensureChannel(activity)
                ReminderScheduler.schedule(activity, hour, minute)
            }
        }
    }

    @JavascriptInterface
    fun cancelReminder() {
        activity.runOnUiThread { ReminderScheduler.cancel(activity) }
    }
}
