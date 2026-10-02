"""Offline learner state for Kotoba.

Keeps spaced-repetition scheduling, mistakes, favorites, XP, missions,
placement results and mock history in JSON next to the rest of the app data.
Signed-in users get isolated records; guests get one device-local record.
"""
from __future__ import annotations

import json
import math
import threading
from copy import deepcopy
from datetime import date, datetime, timedelta
from pathlib import Path

_LOCK = threading.RLock()
STATE_VERSION = 1

DEFAULT_LIST = "Favorites"


def _now_iso():
    return datetime.now().replace(microsecond=0).isoformat()


def _today():
    return date.today().isoformat()


def _default_state():
    return {
        "version": STATE_VERSION,
        "xp": 0,
        "reviews": 0,
        "correct": 0,
        "srs": {},
        "mistakes": {},
        "lists": {DEFAULT_LIST: []},
        "daily": {"date": _today(), "reviews": 0, "correct": 0, "audio": 0, "speaking": 0, "lessons": 0, "mock": 0, "explore": 0},
        "japan_visited": {},
        "placement": None,
        "mock_history": [],
        "history": [],
    }


def _merge_defaults(raw):
    base = _default_state()
    if not isinstance(raw, dict):
        return base
    for key, value in raw.items():
        base[key] = value
    if not isinstance(base.get("srs"), dict): base["srs"] = {}
    if not isinstance(base.get("mistakes"), dict): base["mistakes"] = {}
    if not isinstance(base.get("lists"), dict): base["lists"] = {DEFAULT_LIST: []}
    base["lists"].setdefault(DEFAULT_LIST, [])
    if not isinstance(base.get("mock_history"), list): base["mock_history"] = []
    if not isinstance(base.get("history"), list): base["history"] = []
    if not isinstance(base.get("japan_visited"), dict): base["japan_visited"] = {}
    daily = base.get("daily") if isinstance(base.get("daily"), dict) else {}
    if daily.get("date") != _today():
        daily = {"date": _today(), "reviews": 0, "correct": 0, "audio": 0, "speaking": 0, "lessons": 0, "mock": 0, "explore": 0}
    else:
        for k in ("reviews", "correct", "audio", "speaking", "lessons", "mock", "explore"):
            daily.setdefault(k, 0)
    base["daily"] = daily
    return base


def _read_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return deepcopy(default)


def _write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
    tmp.replace(path)


def _paths(data_dir):
    data_dir = Path(data_dir)
    return data_dir / "learner_state.json", data_dir / "user_learner_state.json"


def load_state(data_dir, user=None):
    guest_path, users_path = _paths(data_dir)
    with _LOCK:
        if user is None:
            return _merge_defaults(_read_json(guest_path, {}))
        all_states = _read_json(users_path, {})
        return _merge_defaults(all_states.get(str(user["id"]), {}))


def save_state(data_dir, state, user=None):
    guest_path, users_path = _paths(data_dir)
    state = _merge_defaults(state)
    state["version"] = STATE_VERSION
    with _LOCK:
        if user is None:
            _write_json(guest_path, state)
        else:
            all_states = _read_json(users_path, {})
            all_states[str(user["id"])] = state
            _write_json(users_path, all_states)


def item_key(kind, item_id):
    return f"{str(kind or 'item').strip().lower()}::{str(item_id or '').strip()}"


def _stage(item):
    reviews = int(item.get("reviews", 0))
    interval = float(item.get("interval", 0) or 0)
    accuracy = (item.get("correct", 0) / reviews) if reviews else 0
    if reviews == 0: return "New"
    if accuracy < 0.55 or int(item.get("lapses", 0)) >= 3: return "Weak"
    if interval >= 21 and accuracy >= 0.82: return "Mastered"
    if interval >= 7 and accuracy >= 0.72: return "Familiar"
    return "Learning"


def _next_interval(item, is_correct, quality=4):
    old = max(0, float(item.get("interval", 0) or 0))
    ease = float(item.get("ease", 2.35) or 2.35)
    if not is_correct:
        return 1, max(1.3, ease - 0.2)
    quality = max(3, min(int(quality or 4), 5))
    ease = max(1.3, ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
    # record_answer increments the success streak before scheduling, so
    # streak 1/2/3 correspond to the learner's first/second/third correct
    # recall. Keep the early spacing predictable before expanding by ease.
    streak = int(item.get("streak", 0))
    if old < 1 or streak <= 1: interval = 1
    elif streak == 2: interval = 3
    elif streak == 3: interval = 7
    else: interval = min(365, max(old + 1, round(old * ease)))
    return interval, ease


def _trim_history(state):
    # Enough for useful recent stats while keeping the on-device JSON small.
    if len(state["history"]) > 1000:
        state["history"] = state["history"][-1000:]
    if len(state["mock_history"]) > 60:
        state["mock_history"] = state["mock_history"][-60:]


def record_answer(data_dir, user, payload):
    """Record one scored learning interaction and schedule its next review."""
    with _LOCK:
        state = load_state(data_dir, user)
        kind = str(payload.get("kind") or "practice")
        iid = str(payload.get("id") or payload.get("front") or payload.get("prompt") or "unknown")
        key = item_key(kind, iid)
        right = bool(payload.get("correct"))
        now = datetime.now().replace(microsecond=0)
        item = state["srs"].get(key, {
            "kind": kind, "id": iid, "front": payload.get("front") or payload.get("prompt") or iid,
            "answer": payload.get("answer") or payload.get("correct_answer") or "",
            "reading": payload.get("reading") or "", "meaning": payload.get("meaning") or "",
            "sub": payload.get("sub") or "", "reviews": 0, "correct": 0, "lapses": 0,
            "streak": 0, "interval": 0, "ease": 2.35,
        })
        # Refresh presentation data whenever a richer event arrives.
        for src, dst in (("front","front"),("prompt","front"),("answer","answer"),("correct_answer","answer"),
                         ("reading","reading"),("meaning","meaning"),("sub","sub"),("level","level"),
                         ("explanation","explanation"),("source_url","source_url")):
            if payload.get(src): item[dst] = payload.get(src)
        item["reviews"] = int(item.get("reviews", 0)) + 1
        if right:
            item["correct"] = int(item.get("correct", 0)) + 1
            item["streak"] = int(item.get("streak", 0)) + 1
        else:
            item["lapses"] = int(item.get("lapses", 0)) + 1
            item["streak"] = 0
        interval, ease = _next_interval(item, right, payload.get("quality", 4 if right else 1))
        item["interval"] = interval
        item["ease"] = round(ease, 3)
        item["last_review"] = now.isoformat()
        item["next_review"] = (now + timedelta(days=interval)).date().isoformat()
        item["mastery"] = _stage(item)
        state["srs"][key] = item

        state["reviews"] = int(state.get("reviews", 0)) + 1
        if right: state["correct"] = int(state.get("correct", 0)) + 1
        state["xp"] = int(state.get("xp", 0)) + (12 if right else 3)
        state["daily"]["reviews"] += 1
        if right: state["daily"]["correct"] += 1

        if not right:
            m = state["mistakes"].get(key, {
                "key": key, "kind": kind, "id": iid, "count": 0, "recovered": 0,
            })
            m["count"] = int(m.get("count", 0)) + 1
            # Recovery is measured after the latest miss, not over the entire
            # lifetime of the item. A new miss restarts the recovery streak.
            m["recovered"] = 0
            m["prompt"] = payload.get("prompt") or payload.get("front") or item.get("front", "")
            m["chosen"] = payload.get("chosen") or ""
            m["correct_answer"] = payload.get("answer") or payload.get("correct_answer") or item.get("answer", "")
            m["explanation"] = payload.get("explanation") or item.get("explanation", "")
            m["level"] = payload.get("level") or item.get("level", "")
            m["last_missed"] = now.isoformat()
            m["mastered"] = False
            state["mistakes"][key] = m
        elif key in state["mistakes"]:
            m = state["mistakes"][key]
            m["recovered"] = int(m.get("recovered", 0)) + 1
            # Two correct encounters after the latest miss marks it mastered,
            # but it remains visible in the notebook's mastered view.
            if m["recovered"] >= 2:
                m["mastered"] = True
            state["mistakes"][key] = m

        state["history"].append({
            "at": now.isoformat(), "kind": kind, "id": iid, "correct": right,
            "front": item.get("front", ""), "answer": item.get("answer", ""),
        })
        _trim_history(state)
        save_state(data_dir, state, user)
        return summary(state)


def record_action(data_dir, user, action, amount=1):
    with _LOCK:
        state = load_state(data_dir, user)
        action = str(action or "").lower()
        amount = max(1, int(amount or 1))
        if action in ("audio", "speaking", "lessons", "mock"):
            state["daily"][action] += amount
        xp_gain = {"audio": 1, "speaking": 5, "lessons": 25, "mock": 40}.get(action, 0) * amount
        state["xp"] += xp_gain
        state["history"].append({"at": _now_iso(), "kind": "action", "id": action, "correct": True})
        _trim_history(state)
        save_state(data_dir, state, user)
        return summary(state)


def toggle_favorite(data_dir, user, item, list_name=DEFAULT_LIST):
    with _LOCK:
        state = load_state(data_dir, user)
        name = (list_name or DEFAULT_LIST).strip()[:60] or DEFAULT_LIST
        state["lists"].setdefault(name, [])
        key = item_key(item.get("kind"), item.get("id") or item.get("front") or item.get("word"))
        items = state["lists"][name]
        idx = next((i for i,x in enumerate(items) if x.get("key") == key), None)
        if idx is None:
            clean = {
                "key": key,
                "kind": item.get("kind") or "item",
                "id": item.get("id") or item.get("front") or item.get("word") or "",
                "front": item.get("front") or item.get("word") or item.get("pattern") or "",
                "reading": item.get("reading") or "",
                "meaning": item.get("meaning") or item.get("answer") or "",
                "url": item.get("url") or "",
                "added": _now_iso(),
            }
            items.append(clean); added = True
        else:
            items.pop(idx); added = False
        save_state(data_dir, state, user)
        return {"ok": True, "added": added, "list": name, "count": len(items)}


def add_list(data_dir, user, name):
    with _LOCK:
        state=load_state(data_dir,user)
        clean=(name or '').strip()[:60]
        if not clean: return False
        state['lists'].setdefault(clean,[])
        save_state(data_dir,state,user)
        return True



def copy_favorite(data_dir, user, source_name, target_name, key):
    with _LOCK:
        state=load_state(data_dir,user)
        source=state.get('lists',{}).get(str(source_name or DEFAULT_LIST),[])
        target=(target_name or DEFAULT_LIST).strip()[:60] or DEFAULT_LIST
        state['lists'].setdefault(target,[])
        item=next((x for x in source if x.get('key')==key),None)
        if not item: return {"ok":False,"error":"item not found"}
        if not any(x.get('key')==key for x in state['lists'][target]):
            state['lists'][target].append(deepcopy(item))
        save_state(data_dir,state,user)
        return {"ok":True,"list":target,"count":len(state['lists'][target])}


def remove_favorite(data_dir, user, list_name, key):
    with _LOCK:
        state=load_state(data_dir,user)
        name=(list_name or DEFAULT_LIST).strip() or DEFAULT_LIST
        items=state.get('lists',{}).get(name)
        if items is None: return False
        before=len(items); state['lists'][name]=[x for x in items if x.get('key')!=key]
        if len(state['lists'][name])==before: return False
        save_state(data_dir,state,user); return True

def save_placement(data_dir, user, result):
    with _LOCK:
        state=load_state(data_dir,user)
        state['placement']={**result,'at':_now_iso()}
        state['xp'] += 50
        save_state(data_dir,state,user)
        return summary(state)


def save_mock(data_dir, user, result):
    with _LOCK:
        state=load_state(data_dir,user)
        state['mock_history'].append({**result,'at':_now_iso()})
        state['daily']['mock'] += 1
        state['xp'] += 40
        _trim_history(state)
        save_state(data_dir,state,user)
        return summary(state)


def record_japan_visit(data_dir, user, place_id, label=""):
    """Record a Japan Explorer stop. XP is awarded only on the first visit."""
    with _LOCK:
        state = load_state(data_dir, user)
        pid = str(place_id or "").strip()
        if not pid:
            return {"ok": False, "first_time": False, "visited_count": len(state.get("japan_visited", {})), "visited_ids": sorted(state.get("japan_visited", {}).keys()), "summary": summary(state)}
        visits = state.setdefault("japan_visited", {})
        first = pid not in visits
        row = visits.get(pid, {"first_visited": _now_iso(), "visits": 0, "label": label or pid})
        row["visits"] = int(row.get("visits", 0)) + 1
        row["last_visited"] = _now_iso()
        if label:
            row["label"] = label
        visits[pid] = row
        xp_awarded = 12 if first else 0
        if first:
            state["xp"] = int(state.get("xp", 0)) + xp_awarded
            state["daily"]["explore"] = int(state["daily"].get("explore", 0)) + 1
        state["history"].append({"at": _now_iso(), "kind": "japan-explorer", "id": pid, "correct": True, "first": first})
        _trim_history(state)
        save_state(data_dir, state, user)
        return {
            "ok": True, "first_time": first, "xp_awarded": xp_awarded,
            "visited_count": len(visits), "visited_ids": sorted(visits.keys()),
            "summary": summary(state),
        }


def due_items(state, limit=30):
    today=_today()
    rows=[]
    for key,item in state.get('srs',{}).items():
        due=item.get('next_review') or today
        if due <= today:
            rows.append({"key":key,**item})
    # Weak and overdue first, then normal due items.
    rank={'Weak':0,'Learning':1,'Familiar':2,'Mastered':3,'New':4}
    rows.sort(key=lambda x:(rank.get(x.get('mastery','Learning'),9), x.get('next_review',''), x.get('reviews',0)))
    return rows[:max(1,min(int(limit or 30),100))]


def achievements(state, streak_current=0):
    reviews=int(state.get('reviews',0)); xp=int(state.get('xp',0));
    mastered=sum(1 for x in state.get('srs',{}).values() if x.get('mastery')=='Mastered')
    recovered=sum(1 for x in state.get('mistakes',{}).values() if x.get('mastered'))
    favs=sum(len(v) for v in state.get('lists',{}).values())
    japan=len(state.get('japan_visited',{}))
    specs=[
        ('first-step','First Step','Complete your first scored review.',reviews>=1,'🌱'),
        ('ten-reviews','Getting Warm','Complete 10 scored reviews.',reviews>=10,'🔥'),
        ('hundred-reviews','Century','Complete 100 scored reviews.',reviews>=100,'💯'),
        ('master-25','Memory Builder','Master 25 scheduled items.',mastered>=25,'🧠'),
        ('mistake-fixer','Comeback Kid','Master 10 past mistakes.',recovered>=10,'🔁'),
        ('streak-7','Seven-Day Rhythm','Reach a 7-day streak.',streak_current>=7,'🗓️'),
        ('collector','Collector','Save 20 favorites.',favs>=20,'⭐'),
        ('xp-2500','Kotoba Explorer','Earn 2,500 XP.',xp>=2500,'🏯'),
        ('japan-5','Japan Starter','Explore 5 places on the Japan map.',japan>=5,'🗾'),
        ('japan-20','Regional Explorer','Explore 20 places on the Japan map.',japan>=20,'🚅'),
        ('japan-47','Japan Passport','Explore all 47 prefectural-capital stops.',japan>=47,'🛂'),
    ]
    return [{'id':i,'title':t,'description':d,'unlocked':u,'icon':ic} for i,t,d,u,ic in specs]


def missions(state):
    d=state.get('daily',{})
    rows=[
        {'id':'review-10','title':'Review 10 items','current':min(d.get('reviews',0),10),'target':10},
        {'id':'correct-8','title':'Get 8 answers correct','current':min(d.get('correct',0),8),'target':8},
        {'id':'listen-5','title':'Listen to Japanese 5 times','current':min(d.get('audio',0),5),'target':5},
    ]
    for r in rows: r['done']=r['current']>=r['target']
    return rows


def summary(state, streak_current=0):
    state=_merge_defaults(state)
    reviews=int(state.get('reviews',0)); correct=int(state.get('correct',0)); xp=int(state.get('xp',0))
    mastery={k:0 for k in ('New','Learning','Weak','Familiar','Mastered')}
    for item in state.get('srs',{}).values(): mastery[_stage(item)] = mastery.get(_stage(item),0)+1
    due=len(due_items(state,100000))
    level=1 + xp//500
    next_level=level*500
    return {
        'xp':xp,'level':level,'xp_into_level':xp%500,'xp_per_level':500,'next_level_xp':next_level,
        'reviews':reviews,'correct':correct,'accuracy':round(100*correct/reviews) if reviews else 0,
        'due':due,'mastery':mastery,
        'mistakes_open':sum(1 for m in state.get('mistakes',{}).values() if not m.get('mastered')),
        'favorites':sum(len(v) for v in state.get('lists',{}).values()),
        'japan_visited':len(state.get('japan_visited',{})),
        'daily':state.get('daily',{}),'missions':missions(state),
        'achievements':achievements(state,streak_current),
        'placement':state.get('placement'),
        'mock_history':state.get('mock_history',[])[-12:],
    }
