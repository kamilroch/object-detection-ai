import html
import textwrap

from config import FIRE_CLASS_NAME, OTHER_CLASS_NAME


CSS = '\n<style>\nhtml, body, [data-testid="stAppViewContainer"], .stApp {\n    background:\n        linear-gradient(rgba(17,44,73,.09) 1px, transparent 1px),\n        linear-gradient(90deg, rgba(17,44,73,.09) 1px, transparent 1px),\n        radial-gradient(circle at 72% -10%, rgba(26,105,214,.18), transparent 35%),\n        linear-gradient(180deg,#06101c 0%,#071321 100%) !important;\n    background-size: 42px 42px, 42px 42px, auto, auto;\n    color: #f4f7fb;\n}\n\nhtml, body { overflow-x:hidden; }\n\n[data-testid="stHeader"], [data-testid="stToolbar"], footer {\n    visibility:hidden;\n    height:0;\n}\n\n.block-container {\n    max-width:1700px !important;\n    padding:.45rem 1.25rem .45rem 1.25rem !important;\n}\n\ndiv[data-testid="stVerticalBlock"] { gap:.55rem; }\ndiv[data-testid="column"] { min-width:0; }\n\n* {\n    box-sizing:border-box;\n    font-family:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;\n}\n\n.hero-wrap {\n    display:flex;\n    align-items:center;\n    justify-content:space-between;\n    gap:20px;\n    margin-bottom:7px;\n    padding-bottom:10px;\n    border-bottom:1px solid rgba(88,147,214,.16);\n}\n.hero-left { display:flex; align-items:center; gap:14px; }\n.hero-icon {\n    width:52px;height:38px;border-radius:16px;\n    display:flex;align-items:center;justify-content:center;\n    font-size:27px;\n    background:linear-gradient(145deg,rgba(255,55,73,.18),rgba(34,135,255,.12));\n    border:1px solid rgba(116,161,216,.22);\n    box-shadow:0 0 28px rgba(255,61,82,.09),0 10px 30px rgba(0,0,0,.22);\n}\n.hero-title {\n    font-size:29px;\n    line-height:1.05;\n    font-weight:900;\n    letter-spacing:-.6px;\n}\n.hero-sub {\n    color:#93a8c2;\n    font-size:13px;\n    margin-top:5px;\n}\n.top-pills { display:flex; gap:8px; }\n.top-pill {\n    padding:9px 15px;\n    border-radius:11px;\n    border:1px solid rgba(105,151,207,.18);\n    background:rgba(10,23,38,.90);\n    color:#cbd8e8;\n    font-size:11px;\n    font-weight:800;\n}\n.top-pill.active {\n    color:#fff;\n    border-color:#238cff;\n    box-shadow:0 0 0 1px rgba(33,139,255,.16),0 0 22px rgba(33,139,255,.16);\n    background:linear-gradient(180deg,#0d2a49,#0b1e35);\n}\n\n.card {\n    position:relative;\n    margin-bottom:12px;\n    background:linear-gradient(180deg,rgba(11,25,42,.97),rgba(8,20,34,.98));\n    border:1px solid rgba(103,151,210,.18);\n    border-radius:16px;\n    box-shadow:0 12px 32px rgba(0,0,0,.18);\n    padding:13px;\n    overflow:hidden;\n}\n.card::before {\n    content:"";\n    position:absolute;\n    inset:0 auto 0 0;\n    width:2px;\n    background:linear-gradient(180deg,#2d95ff,rgba(45,149,255,0));\n    opacity:.9;\n}\n\n.section-title {\n    font-size:13px;\n    font-weight:900;\n    color:#f4f7fb;\n    margin-bottom:9px;\n    display:flex;\n    align-items:center;\n    gap:8px;\n}\n.section-title .title-icon {\n    width:26px;height:26px;border-radius:8px;\n    display:inline-flex;align-items:center;justify-content:center;\n    background:rgba(31,132,255,.10);\n    border:1px solid rgba(31,132,255,.18);\n    box-shadow:0 0 18px rgba(31,132,255,.10);\n    font-size:14px;\n}\n.small-muted { color:#8094ae; font-size:10.5px; }\n\n.file-meta {\n    background:#0d1e32;\n    border:1px solid rgba(99,148,207,.17);\n    border-radius:11px;\n    padding:9px 11px;\n    color:#dbe7f5;\n    font-size:11.5px;\n}\n\n[data-testid="stFileUploader"] { margin-bottom:0 !important; }\n[data-testid="stFileUploaderDropzone"] {\n    min-height:110px !important;\n    background:\n        radial-gradient(circle at 50% 35%,rgba(41,137,255,.06),transparent 45%),\n        #0b1b2e !important;\n    border:1px dashed rgba(77,151,238,.65) !important;\n    border-radius:13px !important;\n}\n[data-testid="stFileUploaderDropzone"] section { padding:12px !important; }\n[data-testid="stFileUploaderDropzone"] button {\n    background:#112b49 !important;\n    color:#e9f3ff !important;\n    border:1px solid rgba(91,159,240,.28) !important;\n    border-radius:9px !important;\n}\n\n.stButton > button {\n    width:100%;\n    min-height:42px;\n    border-radius:10px !important;\n    border:1px solid #4aa1ff !important;\n    color:white !important;\n    font-weight:850 !important;\n    background:linear-gradient(180deg,#2690ff,#0d6bdc) !important;\n    box-shadow:0 8px 22px rgba(28,127,240,.24);\n}\n.stButton > button:hover {\n    background:linear-gradient(180deg,#3a9cff,#1475e8) !important;\n    box-shadow:0 0 22px rgba(45,150,255,.24);\n}\n\n.stDownloadButton > button {\n    width:100%;\n    min-height:50px;\n    border-radius:12px !important;\n    border:1px solid rgba(91,159,240,.30) !important;\n    color:#edf6ff !important;\n    font-weight:800 !important;\n    background:linear-gradient(180deg,#102844,#0c1e34) !important;\n    box-shadow:0 8px 20px rgba(0,0,0,.18);\n}\n.stDownloadButton > button:hover {\n    background:linear-gradient(180deg,#16365a,#102844) !important;\n    border-color:rgba(80,164,255,.55) !important;\n}\n\nvideo {\n    border-radius:13px !important;\n    border:1px solid rgba(91,159,240,.24);\n    background:#02070d;\n    max-height:43vh !important;\n    width:100% !important;\n    object-fit:contain;\n}\n\n.video-shell {\n    background:linear-gradient(180deg,rgba(11,25,42,.97),rgba(8,20,34,.98));\n    border:1px solid rgba(100,148,207,.18);\n    border-radius:16px;\n    padding:11px;\n    box-shadow:0 12px 32px rgba(0,0,0,.18);\n}\n.video-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:7px; }\n.badges { display:flex; gap:6px; align-items:center; }\n.badge {\n    display:inline-flex;\n    padding:5px 9px;\n    border-radius:999px;\n    font-size:9.5px;\n    font-weight:900;\n    color:#b9d8ff;\n    background:rgba(32,136,255,.10);\n    border:1px solid rgba(32,136,255,.17);\n}\n.badge.green {\n    color:#78e8c2;\n    background:rgba(31,207,153,.10);\n    border-color:rgba(31,207,153,.17);\n}\n\n.placeholder {\n    min-height:42vh;\n    border-radius:13px;\n    display:flex;align-items:center;justify-content:center;\n    background:\n        radial-gradient(circle at 50% 45%,rgba(32,136,255,.08),transparent 35%),\n        #07111d;\n    border:1px dashed rgba(99,148,207,.18);\n    text-align:center;color:#7388a3;font-size:12px;\n}\n\n.summary-grid {\n    display:grid;\n    grid-template-columns:1fr 1fr;\n    gap:12px;\n}\n.stat {\n    min-height:92px;\n    border-radius:12px;\n    padding:10px;\n    background:\n        radial-gradient(circle at 85% 15%, rgba(255,255,255,.035), transparent 35%),\n        linear-gradient(180deg,#0e2035,#0a1728);\n    border:1px solid rgba(99,148,207,.14);\n    display:grid;\n    grid-template-columns:36px 1fr;\n    align-items:center;\n    gap:8px;\n}\n.stat-icon {\n    width:34px;height:34px;border-radius:10px;\n    display:flex;align-items:center;justify-content:center;\n    font-size:17px;\n    border:1px solid rgba(255,255,255,.04);\n}\n.stat-icon.red-bg{background:rgba(255,69,80,.12);box-shadow:0 0 20px rgba(255,69,80,.07)}\n.stat-icon.blue-bg{background:rgba(78,163,255,.12);box-shadow:0 0 20px rgba(78,163,255,.07)}\n.stat-icon.green-bg{background:rgba(36,213,162,.12);box-shadow:0 0 20px rgba(36,213,162,.07)}\n.stat-icon.purple-bg{background:rgba(165,122,255,.12);box-shadow:0 0 20px rgba(165,122,255,.07)}\n.stat:hover {\n    transform:translateY(-1px);\n    border-color:rgba(93,163,245,.30);\n    box-shadow:0 12px 24px rgba(0,0,0,.16),0 0 20px rgba(43,137,255,.06);\n}\n.stat { transition:.18s ease; }\n\n.detail-grid {\n    display:grid;\n    grid-template-columns:1fr 1fr;\n    gap:10px;\n}\n.detail-card {\n    min-height:78px;\n    border-radius:12px;\n    padding:11px 12px;\n    background:\n        radial-gradient(circle at 85% 15%, rgba(255,255,255,.035), transparent 38%),\n        linear-gradient(180deg,#0e2035,#0a1728);\n    border:1px solid rgba(99,148,207,.14);\n    display:flex;\n    align-items:center;\n    gap:10px;\n    transition:.18s ease;\n}\n.detail-card:hover {\n    transform:translateY(-1px);\n    border-color:rgba(93,163,245,.30);\n    box-shadow:0 12px 24px rgba(0,0,0,.16),0 0 20px rgba(43,137,255,.06);\n}\n.detail-icon {\n    flex:0 0 34px;\n    width:34px;\n    height:34px;\n    border-radius:10px;\n    display:flex;\n    align-items:center;\n    justify-content:center;\n    font-size:16px;\n    background:rgba(33,139,255,.10);\n    border:1px solid rgba(33,139,255,.17);\n    box-shadow:0 0 18px rgba(33,139,255,.08);\n}\n.detail-label {\n    font-size:9.5px;\n    color:#8fa3bd;\n    font-weight:700;\n    margin-bottom:3px;\n}\n.detail-value-big {\n    font-size:15px;\n    color:#f4f7fb;\n    font-weight:900;\n    line-height:1.1;\n}\n.section-accent {\n    height:2px;\n    width:42px;\n    border-radius:99px;\n    background:linear-gradient(90deg,#238cff,#7c4dff);\n    box-shadow:0 0 14px rgba(35,140,255,.28);\n    margin:-3px 0 10px 34px;\n}\n\n.right-stack > div {\n    margin-bottom:12px;\n}\n\n.download-shell {\n    padding:10px;\n    border-radius:14px;\n    border:1px solid rgba(100,148,207,.18);\n    background:linear-gradient(180deg,rgba(11,25,42,.96),rgba(8,20,34,.98));\n    box-shadow:0 10px 28px rgba(0,0,0,.18);\n}\n\n.stat-label { font-size:9.5px; color:#8fa3bd; font-weight:700; margin-bottom:4px; }\n.stat-value { font-size:25px; font-weight:950; line-height:1; }\n.red{color:#ff4550}.blue{color:#4ea3ff}.green-t{color:#24d5a2}.purple{color:#a57aff}\n\n.conf-row {\n    display:grid;\n    grid-template-columns:68px 1fr 38px;\n    gap:7px;\n    align-items:center;\n    margin:8px 0;\n}\n.conf-name {font-size:10px;color:#d5e1ee;font-weight:750}\n.conf-val {font-size:10px;color:#d5e1ee;text-align:right;font-weight:900}\n.bar {height:6px;border-radius:999px;background:rgba(255,255,255,.06);overflow:hidden}\n.bar > div {height:100%;border-radius:999px}\n\n.donut-wrap {display:flex;align-items:center;gap:12px}\n.donut {\n    width:84px;height:84px;border-radius:50%;\n    display:flex;align-items:center;justify-content:center;\n    background:conic-gradient(#ff4550 var(--pct), #132a45 0);\n    position:relative;\n    box-shadow:0 0 24px rgba(255,69,80,.10);\n}\n.donut::after {\n    content:"";\n    position:absolute;\n    width:58px;height:58px;border-radius:50%;\n    background:#0b1a2c;\n}\n.donut-inner {position:relative;z-index:2;text-align:center}\n.donut-num {font-size:17px;font-weight:950}\n.donut-label {font-size:7.5px;color:#8fa3bd}\n\n.detail-list {display:grid;gap:6px}\n.detail {\n    display:flex;justify-content:space-between;gap:10px;\n    padding:7px 8px;\n    border-radius:9px;\n    background:#0d1c2f;\n    border:1px solid rgba(99,148,207,.11);\n    font-size:10px;\n}\n.detail span:first-child {color:#9fb1c8}\n.detail b {color:#f4f7fb}\n\n.timeline-card {\n    position:relative;\n    background:linear-gradient(180deg,rgba(11,25,42,.97),rgba(8,20,34,.98));\n    border:1px solid rgba(100,148,207,.18);\n    border-radius:16px;\n    padding:9px 12px;\n    margin-top:2px;\n    overflow:hidden;\n}\n.timeline-card::after{\n    content:"";\n    position:absolute;right:-60px;top:-60px;\n    width:160px;height:160px;border-radius:50%;\n    background:radial-gradient(circle,rgba(33,139,255,.10),transparent 68%);\n}\n.timeline-head {\n    display:flex;align-items:center;justify-content:space-between;gap:12px;\n}\n.timeline-title-wrap{display:flex;align-items:center;gap:9px}\n.timeline-icon {\n    width:30px;height:30px;border-radius:9px;\n    display:flex;align-items:center;justify-content:center;\n    background:rgba(33,139,255,.11);\n    border:1px solid rgba(33,139,255,.18);\n    box-shadow:0 0 18px rgba(33,139,255,.10);\n}\n.timeline {\n    position:relative;\n    height:44px;\n    margin:2px 14px 0 14px;\n}\n.timeline-line {\n    position:absolute;left:0;right:0;top:20px;height:4px;border-radius:20px;\n    background:linear-gradient(90deg,#123354,#1b6cb1,#123354);\n    box-shadow:0 0 12px rgba(33,139,255,.12);\n}\n.timeline-tick {\n    position:absolute;top:15px;width:1px;height:14px;background:rgba(143,169,199,.25);\n}\n.dot {\n    position:absolute;top:13px;width:17px;height:17px;border-radius:50%;\n    transform:translateX(-50%);\n    background:#ff4550;\n    box-shadow:0 0 0 5px rgba(255,69,80,.08),0 0 18px rgba(255,69,80,.18);\n}\n.dot.blue {background:#218bff;box-shadow:0 0 0 5px rgba(33,139,255,.08),0 0 18px rgba(33,139,255,.18)}\n.tlabel {\n    position:absolute;top:31px;transform:translateX(-50%);\n    color:#8fa3bd;font-size:9px;white-space:nowrap;\n}\n.event-label {\n    position:absolute;top:-2px;transform:translateX(-50%);\n    font-size:8.5px;font-weight:900;padding:3px 6px;border-radius:6px;\n    color:#fff;background:rgba(255,69,80,.15);border:1px solid rgba(255,69,80,.20)\n}\n.event-label.blue-e {background:rgba(33,139,255,.15);border-color:rgba(33,139,255,.20)}\n\n[data-testid="stProgress"] {margin-top:3px}\n[data-testid="stProgress"] > div > div > div > div {\n    background:linear-gradient(90deg,#1b84f7,#42a5ff)\n}\n\n\n[data-testid="stSlider"] {\n    padding-top:.05rem;\n    padding-bottom:.10rem;\n}\n[data-testid="stSlider"] label {\n    color:#eaf2ff !important;\n    font-weight:800 !important;\n    font-size:11.5px !important;\n}\n[data-testid="stSlider"] [role="slider"] {\n    background:#2a90ff !important;\n    border:2px solid #dff0ff !important;\n    box-shadow:0 0 12px rgba(42,144,255,.28);\n}\n\n\n/* FINAL compact slider treatment */\n[data-testid="stSlider"] {\n    margin-top:-2px !important;\n    margin-bottom:3px !important;\n}\n[data-testid="stSlider"] > label {\n    margin-bottom:0 !important;\n}\n[data-testid="stSlider"] [data-baseweb="slider"] {\n    padding-top:7px !important;\n    padding-bottom:7px !important;\n}\n[data-testid="stSlider"] [data-baseweb="slider"] > div {\n    height:5px !important;\n    border-radius:999px !important;\n    background:#17304e !important;\n}\n[data-testid="stSlider"] [data-baseweb="slider"] > div > div {\n    height:5px !important;\n    border-radius:999px !important;\n    background:linear-gradient(90deg,#1d83ff 0%,#6d5cff 100%) !important;\n    box-shadow:0 0 12px rgba(49,137,255,.18);\n}\n[data-testid="stSlider"] [role="slider"] {\n    width:16px !important;\n    height:16px !important;\n    background:#f2f7ff !important;\n    border:3px solid #278dff !important;\n    box-shadow:0 0 0 3px rgba(39,141,255,.10),0 0 12px rgba(39,141,255,.24) !important;\n}\n[data-testid="stSlider"] [data-testid="stThumbValue"] {\n    color:#8fc4ff !important;\n    font-weight:900 !important;\n    font-size:11px !important;\n}\n\n/* headers now look like actual dashboard sections */\n.video-head {\n    padding:8px 10px;\n    border:1px solid rgba(100,148,207,.16);\n    border-radius:12px;\n    background:linear-gradient(180deg,rgba(13,31,52,.82),rgba(8,21,36,.78));\n    margin-bottom:9px;\n}\n\n\n/* stable compact controls */\n[data-testid="stSlider"] {\n    margin: 0 0 .35rem 0 !important;\n}\n[data-testid="stSlider"] label {\n    font-size: 12px !important;\n    font-weight: 800 !important;\n    color: #eef5ff !important;\n}\n[data-testid="stSlider"] [role="slider"] {\n    background: #ffffff !important;\n    border: 3px solid #258cff !important;\n    box-shadow: 0 0 0 3px rgba(37,140,255,.10), 0 0 12px rgba(37,140,255,.25) !important;\n}\n\n\n/* subtle spacing for the left control column */\n.file-meta { margin-top:4px; }\n[data-testid="stFileUploader"] { margin-bottom:5px !important; }\n\n\n\n.snapshot-head {\n    margin-top:8px;\n    margin-bottom:6px;\n    min-height:42px;\n    display:flex;\n    align-items:center;\n    gap:9px;\n    padding:7px 10px;\n    border-radius:12px;\n    border:1px solid rgba(100,148,207,.17);\n    background:linear-gradient(180deg,rgba(12,29,49,.94),rgba(8,21,36,.96));\n}\n.snapshot-icon {\n    width:28px;height:28px;border-radius:8px;\n    display:flex;align-items:center;justify-content:center;\n    color:#6eb5ff;\n    background:rgba(35,140,255,.10);\n    border:1px solid rgba(35,140,255,.18);\n}\n.snapshot-head b {\n    display:block;\n    color:#f3f8ff;\n    font-size:12px;\n}\n.snapshot-head span:not(.snapshot-icon) {\n    display:block;\n    color:#8196b0;\n    font-size:9px;\n    margin-top:1px;\n}\n.snapshot-label {\n    display:flex;\n    justify-content:space-between;\n    gap:6px;\n    align-items:center;\n    padding:5px 7px;\n    margin-bottom:4px;\n    border-radius:8px;\n    background:#0d1e32;\n    border:1px solid rgba(100,148,207,.14);\n    color:#dceaff;\n    font-size:8.5px;\n    font-weight:900;\n}\n.snapshot-label span {\n    color:#7fa0c5;\n    font-size:8px;\n    font-weight:700;\n}\n[data-testid="stImage"] img {\n    border-radius:10px !important;\n    border:1px solid rgba(100,148,207,.18);\n}\n\n\n\n/* More air between dashboard tiles */\n.summary-grid {\n    gap:14px !important;\n}\n.detail-grid {\n    gap:13px !important;\n}\n.card {\n    margin-bottom:14px !important;\n}\n\n/* Larger, cleaner snapshot presentation */\n.snapshot-head {\n    margin-top:10px !important;\n    margin-bottom:8px !important;\n}\n.snapshot-label {\n    margin-bottom:6px !important;\n    padding:6px 8px !important;\n}\n[data-testid="stImage"] {\n    margin-bottom:4px !important;\n}\n[data-testid="stImage"] img {\n    width:100% !important;\n    min-height:150px !important;\n    max-height:180px !important;\n    object-fit:cover !important;\n    border-radius:12px !important;\n    box-shadow:0 10px 24px rgba(0,0,0,.22);\n}\n\n/* Slightly more space around the right-side result cards */\n.stat {\n    padding:12px !important;\n}\n.detail-card {\n    padding:12px 13px !important;\n}\n\n\n/* classic full-width slider controls */\n[data-testid="stSlider"] {\n    margin-top:-2px !important;\n    margin-bottom:4px !important;\n}\n[data-testid="stSlider"] > label {\n    margin-bottom:0 !important;\n}\n[data-testid="stSlider"] label {\n    color:#eaf2ff !important;\n    font-size:11.5px !important;\n    font-weight:800 !important;\n}\n[data-testid="stSlider"] [data-baseweb="slider"] {\n    padding-top:7px !important;\n    padding-bottom:7px !important;\n}\n[data-testid="stSlider"] [data-baseweb="slider"] > div {\n    height:5px !important;\n    border-radius:999px !important;\n    background:#17304e !important;\n}\n[data-testid="stSlider"] [data-baseweb="slider"] > div > div {\n    height:5px !important;\n    border-radius:999px !important;\n    background:linear-gradient(90deg,#1d83ff 0%,#6d5cff 100%) !important;\n    box-shadow:0 0 12px rgba(49,137,255,.18);\n}\n[data-testid="stSlider"] [role="slider"] {\n    width:16px !important;\n    height:16px !important;\n    background:#f2f7ff !important;\n    border:3px solid #278dff !important;\n    box-shadow:0 0 0 3px rgba(39,141,255,.10),0 0 12px rgba(39,141,255,.24) !important;\n}\n[data-testid="stSlider"] [data-testid="stThumbValue"] {\n    color:#ff4e63 !important;\n    font-weight:900 !important;\n    font-size:11px !important;\n}\n\n/* plain action buttons - no surrounding download card */\n.download-shell {\n    display:none !important;\n}\n\n@media (max-width:1200px){\n    .hero-title{font-size:25px}\n    .top-pills{display:none}\n}\n</style>\n'


def esc(x):
    return html.escape(str(x))

def clean_html(value):
    return textwrap.dedent(value).strip()

def pct(v):
    return max(0.0, min(1.0, float(v)))

def class_confidences(df):
    if df is None or len(df) == 0:
        return 0.0, 0.0
    fire = df.loc[df["klasa"] == FIRE_CLASS_NAME, "confidence"]
    other = df.loc[df["klasa"] == OTHER_CLASS_NAME, "confidence"]
    fire_conf = float(fire.mean()) if len(fire) else 0.0
    other_conf = float(other.mean()) if len(other) else 0.0
    return fire_conf, other_conf

def summary_card(summary):
    return f"""
    <div class="card">
      <div class="section-title"><span class="title-icon">📊</span> Object Detection Summary</div><div class="section-accent"></div>
      <div class="summary-grid">
        <div class="stat">
          <div class="stat-icon red-bg">🚒</div>
          <div><div class="stat-label">Fire trucks</div><div class="stat-value red">{summary["fire_count"]}</div></div>
        </div>
        <div class="stat">
          <div class="stat-icon blue-bg">🚙</div>
          <div><div class="stat-label">Other vehicles</div><div class="stat-value blue">{summary["other_count"]}</div></div>
        </div>
        <div class="stat">
          <div class="stat-icon green-bg">◫</div>
          <div><div class="stat-label">Total detections</div><div class="stat-value green-t">{summary["total_count"]}</div></div>
        </div>
        <div class="stat">
          <div class="stat-icon purple-bg">◔</div>
          <div><div class="stat-label">Average confidence</div><div class="stat-value purple">{summary["avg_conf"]:.2f}</div></div>
        </div>
      </div>
    </div>
    """

def empty_summary_card():
    return """
    <div class="card">
      <div class="section-title"><span class="title-icon">📊</span> Object Detection Summary</div><div class="section-accent"></div>
      <div class="summary-grid">
        <div class="stat"><div class="stat-icon red-bg">🚒</div><div><div class="stat-label">Fire trucks</div><div class="stat-value red">—</div></div></div>
        <div class="stat"><div class="stat-icon blue-bg">🚙</div><div><div class="stat-label">Other vehicles</div><div class="stat-value blue">—</div></div></div>
        <div class="stat"><div class="stat-icon green-bg">◫</div><div><div class="stat-label">Total detections</div><div class="stat-value green-t">—</div></div></div>
        <div class="stat"><div class="stat-icon purple-bg">◔</div><div><div class="stat-label">Average confidence</div><div class="stat-value purple">—</div></div></div>
      </div>
    </div>
    """

def confidence_card(summary, df):
    fire_c, other_c = class_confidences(df)
    overall = summary["max_conf"] if summary else 0
    overall_pct = int(round(pct(overall) * 100))
    return f"""
    <div class="card">
      <div class="section-title"><span class="title-icon">🎯</span> Detection Confidence</div><div class="section-accent"></div>
      <div class="donut-wrap">
        <div class="donut" style="--pct:{overall_pct}%">
          <div class="donut-inner">
            <div class="donut-num">{overall_pct}%</div>
            <div class="donut-label">Top confidence</div>
          </div>
        </div>
        <div style="flex:1">
          <div class="conf-row">
            <div class="conf-name">Fire truck</div>
            <div class="bar"><div style="width:{pct(fire_c)*100:.1f}%;background:#ff4550"></div></div>
            <div class="conf-val">{fire_c:.2f}</div>
          </div>
          <div class="conf-row">
            <div class="conf-name">Other</div>
            <div class="bar"><div style="width:{pct(other_c)*100:.1f}%;background:#218bff"></div></div>
            <div class="conf-val">{other_c:.2f}</div>
          </div>
        </div>
      </div>
    </div>
    """

def empty_confidence_card():
    return """
    <div class="card">
      <div class="section-title"><span class="title-icon">🎯</span> Detection Confidence</div><div class="section-accent"></div>
      <div class="donut-wrap">
        <div class="donut" style="--pct:0%">
          <div class="donut-inner"><div class="donut-num">—</div><div class="donut-label">Top confidence</div></div>
        </div>
        <div style="flex:1">
          <div class="conf-row"><div class="conf-name">Fire truck</div><div class="bar"></div><div class="conf-val">—</div></div>
          <div class="conf-row"><div class="conf-name">Other</div><div class="bar"></div><div class="conf-val">—</div></div>
        </div>
      </div>
    </div>
    """

def details_card(summary):
    return (
        '<div class="card">'
        '<div class="section-title"><span class="title-icon">📋</span> Detailed Results</div>'
        '<div class="section-accent"></div>'
        '<div class="detail-grid">'
        f'<div class="detail-card"><div class="detail-icon">⭐</div><div><div class="detail-label">Highest confidence</div><div class="detail-value-big">{summary["max_conf"]:.2f}</div></div></div>'
        f'<div class="detail-card"><div class="detail-icon">📊</div><div><div class="detail-label">Average confidence</div><div class="detail-value-big">{summary["avg_conf"]:.2f}</div></div></div>'
        f'<div class="detail-card"><div class="detail-icon">⚡</div><div><div class="detail-label">First fire truck detection</div><div class="detail-value-big">{summary["first_fire_time"]}</div></div></div>'
        f'<div class="detail-card"><div class="detail-icon">🕒</div><div><div class="detail-label">Last fire truck detection</div><div class="detail-value-big">{summary["last_fire_time"]}</div></div></div>'
        f'<div class="detail-card"><div class="detail-icon">🚒</div><div><div class="detail-label">Fire trucks</div><div class="detail-value-big">{summary["fire_count"]}</div></div></div>'
        f'<div class="detail-card"><div class="detail-icon">◫</div><div><div class="detail-label">Total detections</div><div class="detail-value-big">{summary["total_count"]}</div></div></div>'
        '</div>'
        '</div>'
    )

def empty_details_card():
    return (
        '<div class="card">'
        '<div class="section-title"><span class="title-icon">📋</span> Detailed Results</div>'
        '<div class="section-accent"></div>'
        '<div class="detail-grid">'
        '<div class="detail-card"><div class="detail-icon">⭐</div><div><div class="detail-label">Highest confidence</div><div class="detail-value-big">—</div></div></div>'
        '<div class="detail-card"><div class="detail-icon">📊</div><div><div class="detail-label">Average confidence</div><div class="detail-value-big">—</div></div></div>'
        '<div class="detail-card"><div class="detail-icon">⚡</div><div><div class="detail-label">First fire truck detection</div><div class="detail-value-big">—</div></div></div>'
        '<div class="detail-card"><div class="detail-icon">🕒</div><div><div class="detail-label">Last fire truck detection</div><div class="detail-value-big">—</div></div></div>'
        '<div class="detail-card"><div class="detail-icon">🚒</div><div><div class="detail-label">Fire trucks</div><div class="detail-value-big">—</div></div></div>'
        '<div class="detail-card"><div class="detail-icon">◫</div><div><div class="detail-label">Total detections</div><div class="detail-value-big">—</div></div></div>'
        '</div>'
        '</div>'
    )

def timeline_card(summary):
    return (
        '<div class="timeline-card">'
        '<div class="timeline-head">'
        '<div class="timeline-title-wrap">'
        '<div class="timeline-icon">📈</div>'
        '<div><div class="section-title" style="margin:0">Detection Timeline</div>'
        '<div class="small-muted">Confirmed fire-truck activity across the analyzed video.</div></div>'
        '</div>'
        '<div class="badges"><span class="badge green">Tracked moments</span></div>'
        '</div>'
        '<div class="timeline">'
        '<div class="timeline-line"></div>'
        '<div style="position:absolute;left:0;right:0;top:19px;height:6px;background:linear-gradient(90deg,transparent,rgba(34,139,255,.12),transparent);filter:blur(6px);"></div>'
        '<div class="timeline-tick" style="left:0%"></div>'
        '<div class="timeline-tick" style="left:25%"></div>'
        '<div class="timeline-tick" style="left:50%"></div>'
        '<div class="timeline-tick" style="left:75%"></div>'
        '<div class="timeline-tick" style="left:100%"></div>'
        '<div class="event-label" style="left:30%">FIRST DETECTION</div>'
        '<div class="dot" style="left:30%"></div>'
        f'<div class="tlabel" style="left:30%">{summary["first_fire_time"]}</div>'
        '<div class="event-label blue-e" style="left:73%">LAST DETECTION</div>'
        '<div class="dot blue" style="left:73%"></div>'
        f'<div class="tlabel" style="left:73%">{summary["last_fire_time"]}</div>'
        '</div>'
        '</div>'
    )

