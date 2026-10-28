#!/usr/bin/env python3
from datetime import date, timedelta
from pathlib import Path
import calendar
import html

ROOT = Path(__file__).resolve().parent
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
DOW = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

def week_id(mon: date) -> str:
    return f"w{mon.isoformat()}"

def week_path(mon: date) -> str:
    return f"weeks/{week_id(mon)}.html"

def month_path(m: int) -> str:
    return f"months/2027-{m:02d}.html"

d0 = date(2027, 1, 1)
start = d0 - timedelta(days=d0.weekday())
end = date(2027, 12, 31)
last = end - timedelta(days=end.weekday())
weeks = []
cur = start
while cur <= last:
    weeks.append(cur)
    cur += timedelta(days=7)
week_index = {w: i for i, w in enumerate(weeks)}

def nav(depth=0):
    p = "../" * depth
    return f'''<nav class="nav" aria-label="Planner nav">
  <a class="brand" href="{p}index.html">ADHD 2027 Planner</a>
  <a href="{p}index.html">Year</a>
  <a href="{p}how-to.html">How to use</a>
  <a href="{p}example/filled-week.html">EXAMPLE week</a>
  <a href="{p}weekly-review.html">Weekly review</a>
  <a href="{p}templates/day.html">Day template</a>
</nav>'''

def footer(depth=0):
    p = "../" * depth
    return f'''<footer class="footer">
  Free sample · MIT License · Methods: time blocking · MIT / Top 3 · Pomodoro (Cirillo) · optional Eisenhower<br/>
  Trust hub: <a href="https://sirmem.github.io/freelancer-money-sheets/">sirmem.github.io/freelancer-money-sheets</a>
  · <a href="{p}README.md">README</a>
</footer>'''

def page(title, body, depth=0):
    p = "../" * depth
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <meta name="description" content="Free 2027 ADHD hyperlinked digital planner sample — time blocking, Top 3 (MIT), Pomodoro. Open in browser or print." />
  <link rel="stylesheet" href="{p}css/planner.css" />
</head>
<body>
<div class="wrap">
{nav(depth)}
{body}
{footer(depth)}
</div>
</body>
</html>
'''

def day_section(d: date, filled=None):
    label = f"{DOW[d.weekday()]} {MONTHS[d.month-1][:3]} {d.day}, {d.year}"
    mits = ["", "", ""]
    blocks = {"Morning": "", "Afternoon": "", "Evening": ""}
    pomo = 0
    dump = ""
    done = [False, False, False]
    if filled and d in filled:
        f = filled[d]
        mits = (f.get("mits", []) + ["", "", ""])[:3]
        blocks = {**blocks, **f.get("blocks", {})}
        pomo = int(f.get("pomo", 0))
        dump = f.get("dump", "")
        done = (f.get("done", []) + [False, False, False])[:3]
    mit_items = []
    for i in range(3):
        bx = "box done" if done[i] else "box"
        content = html.escape(mits[i]) if mits[i] else "&nbsp;"
        mit_items.append(f'<li><span class="{bx}"></span><span>{content}</span></li>')
    ticks = []
    for i in range(4):
        cls = "tick on" if i < pomo else "tick"
        ticks.append(f'<span class="{cls}"></span>')
    block_parts = []
    for name in ("Morning", "Afternoon", "Evening"):
        val = html.escape(blocks[name]) if blocks.get(name) else "&nbsp;"
        block_parts.append(
            f'<div class="slot"><div class="label">{name} block</div><div>{val}</div></div>'
        )
    dump_html = html.escape(dump) if dump else "&nbsp;"
    return f'''<section class="day-card" id="d{d.isoformat()}">
  <h3><span>{label}</span><a href="../templates/day.html" class="muted" style="font-size:.8rem;font-weight:400">day template</a></h3>
  <p style="margin:.2rem 0;font-size:.85rem;color:var(--muted)"><strong>MIT / Top 3</strong></p>
  <ul class="mit">{"".join(mit_items)}</ul>
  <div class="blocks">{"".join(block_parts)}</div>
  <div class="pomo"><span>Pomodoro:</span>{"".join(ticks)}</div>
  <p style="margin:.7rem 0 .2rem;font-size:.85rem;color:var(--muted)"><strong>Brain dump</strong></p>
  <div class="lined" style="border:0;min-height:1.5rem">{dump_html}</div>
</section>'''

def week_mits_html(filled):
    if filled and "_week" in filled:
        wm = filled["_week"]
        items = []
        done_n = int(wm.get("done", 0))
        for j, t in enumerate(wm.get("mits", [])[:3]):
            bx = "box done" if j < done_n else "box"
            items.append(f'<li><span class="{bx}"></span><span>{html.escape(t)}</span></li>')
        while len(items) < 3:
            items.append('<li><span class="box"></span><span>&nbsp;</span></li>')
        return "<ul class='mit'>" + "".join(items) + "</ul>"
    return '''<ul class="mit">
      <li><span class="box"></span><span>&nbsp;</span></li>
      <li><span class="box"></span><span>&nbsp;</span></li>
      <li><span class="box"></span><span>&nbsp;</span></li>
    </ul>'''

def write_week(mon: date, filled=None, out_path=None, depth=1, extra_banner=""):
    i = week_index[mon]
    if i > 0:
        prev_link = f'<a href="{week_id(weeks[i-1])}.html">← Prev week</a>'
    else:
        prev_link = '<span class="muted">← Prev week</span>'
    if i < len(weeks) - 1:
        next_link = f'<a href="{week_id(weeks[i+1])}.html">Next week →</a>'
    else:
        next_link = '<span class="muted">Next week →</span>'
    days = [mon + timedelta(days=k) for k in range(7)]
    in_2027 = [d.month for d in days if d.year == 2027]
    if in_2027:
        primary = max(set(in_2027), key=lambda m: in_2027.count(m))
        month_hub = f'<a href="../{month_path(primary)}">→ {MONTHS[primary-1]} hub</a>'
    elif all(d.year == 2026 for d in days):
        month_hub = f'<a href="../{month_path(1)}">→ Jan 2027 hub</a>'
    else:
        month_hub = f'<a href="../{month_path(12)}">→ Dec 2027 hub</a>'
    sun = mon + timedelta(days=6)
    title = f"Week of {mon.isoformat()} – {sun.isoformat()}"
    days_html = "\n".join(day_section(d, filled) for d in days)
    body = f'''
{extra_banner}
<p class="muted"><span class="tag">week spread</span> 7 days · Top 3 + time blocks + Pomodoro</p>
<h1>{html.escape(title)}</h1>
<div class="week-nav">{prev_link}{month_hub}{next_link}</div>
<div class="card">
  <strong>This week’s Top 3</strong> (optional theme — keep daily MITs tighter)
  {week_mits_html(filled)}
  <p style="margin:.5rem 0 0"><a href="../weekly-review.html">Weekly review (Eisenhower)</a></p>
</div>
<div class="days">
{days_html}
</div>
'''
    path = out_path or (ROOT / "weeks" / f"{week_id(mon)}.html")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(page(title + " — ADHD 2027 Planner", body, depth=depth), encoding="utf-8")

# ---- index ----
month_cards = []
for m in range(1, 13):
    month_cards.append(
        f'<a href="{month_path(m)}">{MONTHS[m-1]} 2027<span>Open month hub → weeks</span></a>'
    )

index_body = f'''
<p><span class="tag">free sample</span><span class="tag">2027</span><span class="tag">hyperlinked</span></p>
<h1>ADHD 2027 Hyperlinked Planner — free sample</h1>
<p><strong>What:</strong> A working <strong>2027</strong> hyperlinked HTML planner: <strong>12</strong> month hubs → <strong>{len(weeks)}</strong> week spreads → day template. Each day screen: <strong>Top 3</strong> (MIT), <strong>3</strong> time blocks, <strong>4</strong> Pomodoro ticks.</p>
<p><strong>Who for:</strong> Adults with ADHD (self-described) who lose the plan by late morning and want one screen per day — not a 200-page aesthetic dump.</p>
<p class="muted">Open in any browser. Print-friendly CSS. For GoodNotes/Notability: print to PDF or import pages. No signup.</p>

<div class="card">
  <h2 style="margin-top:0">Start here (60 seconds)</h2>
  <ol>
    <li>Open <a href="how-to.html">How to use</a> once (methods credited).</li>
    <li>Peek the <a href="example/filled-week.html">EXAMPLE filled week</a> (fake person “Alex Rivera”).</li>
    <li>Jump to a month below → click a week link → fill Top 3 + blocks.</li>
  </ol>
</div>

<div class="gap card">
  <strong>If this free sample is missing something you need, say which one-word gap fits</strong> (open a GitHub issue with that word — no pitch required):
  <ul>
    <li><code>YEARLY</code> — full-year goals / theme map beyond month hubs</li>
    <li><code>HABITS</code> — habit tracker grid tied to weeks</li>
    <li><code>BODY-DOUBLE</code> — body-doubling / focus-session partner checklist pages</li>
  </ul>
</div>

<h2>2027 months</h2>
<div class="grid-months">
{"".join(month_cards)}
</div>

<h2>Quick links</h2>
<ul>
  <li><a href="{week_path(weeks[1])}">First full week of Jan 2027</a> (Mon {weeks[1].isoformat()})</li>
  <li><a href="weekly-review.html">Weekly review</a> (Eisenhower optional)</li>
  <li><a href="templates/day.html">Blank day template</a> (duplicate as needed)</li>
</ul>
'''
(ROOT / "index.html").write_text(page("ADHD 2027 Hyperlinked Planner — free sample", index_body), encoding="utf-8")

howto_body = '''
<h1>How to use this planner</h1>
<p class="muted">Recognized public methods only. We do not claim medical advice or ADHD treatment.</p>

<div class="card howto">
  <h2 style="margin-top:0">Methods credited</h2>
  <table class="cal" style="margin-top:.5rem">
    <thead><tr><th>Method</th><th>How it appears here</th></tr></thead>
    <tbody>
      <tr><td><strong>Time blocking</strong> (Cal Newport–style framing as a method name)</td><td>Each day has Morning / Afternoon / Evening blocks — put one job in a block, not a floating to-do list</td></tr>
      <tr><td><strong>MIT / Top 3</strong>（一日三件事）</td><td>Three checkboxes max per day. If everything is #1, nothing is</td></tr>
      <tr><td><strong>Pomodoro</strong> (Francesco Cirillo)</td><td>Four tick circles ≈ four 25-min focus sessions; take a break after a tick</td></tr>
      <tr><td><strong>Eisenhower</strong> (optional weekly)</td><td>On <a href="weekly-review.html">Weekly review</a>: Urgent/Important quadrants for Sunday reset</td></tr>
    </tbody>
  </table>
</div>

<div class="card howto">
  <h2 style="margin-top:0">Daily loop (under 5 minutes to set)</h2>
  <ol>
    <li>From Year → Month → Week.</li>
    <li>Write at most <strong>3</strong> MITs for today.</li>
    <li>Drop each MIT into a time block (or park one in Brain dump).</li>
    <li>Run Pomodoro ticks; mark boxes when done.</li>
    <li>Sunday: open Weekly review once.</li>
  </ol>
</div>

<div class="card">
  <h2 style="margin-top:0">Browser / GoodNotes / print</h2>
  <ul>
    <li><strong>Browser:</strong> open <code>index.html</code> (or the GitHub Pages URL). Links are relative — keep the folder intact.</li>
    <li><strong>Print / PDF:</strong> File → Print → Save as PDF (print CSS reduces clutter).</li>
    <li><strong>GoodNotes / Notability:</strong> import the PDF, or screenshot week spreads. Hyperlinks work best in browser; PDF may flatten some links depending on your app.</li>
  </ul>
</div>

<div class="gap">
  <strong>Gap words</strong> (free→paid signal): open a GitHub issue with <code>YEARLY</code>, <code>HABITS</code>, or <code>BODY-DOUBLE</code> if that is what you came for and this sample lacks it.
</div>
'''
(ROOT / "how-to.html").write_text(page("How to use — ADHD 2027 Planner", howto_body), encoding="utf-8")

review_body = '''
<h1>Weekly review (optional Eisenhower)</h1>
<p class="muted">Use once per week (often Sunday). Not medical advice — a sorting grid.</p>
<div class="card">
  <p><strong>Week of:</strong> <span class="lined" style="display:inline-block;min-width:12rem"></span></p>
  <p><strong>Wins (max 3):</strong></p>
  <div class="lined"></div><div class="lined"></div><div class="lined"></div>
  <p><strong>Carry over to next week:</strong></p>
  <div class="lined"></div><div class="lined"></div>
</div>
<h2>Eisenhower grid</h2>
<div class="eisen">
  <div class="q"><strong>1 · Urgent + Important — do</strong><div class="lined"></div><div class="lined"></div><div class="lined"></div></div>
  <div class="q"><strong>2 · Not urgent + Important — schedule</strong><div class="lined"></div><div class="lined"></div><div class="lined"></div></div>
  <div class="q"><strong>3 · Urgent + Not important — delegate / shrink</strong><div class="lined"></div><div class="lined"></div><div class="lined"></div></div>
  <div class="q"><strong>4 · Neither — drop</strong><div class="lined"></div><div class="lined"></div><div class="lined"></div></div>
</div>
<p class="muted" style="margin-top:1rem">Then open next week’s spread and write only Top 3 per day.</p>
'''
(ROOT / "weekly-review.html").write_text(page("Weekly review — ADHD 2027 Planner", review_body), encoding="utf-8")

day_body = '''
<h1>Blank day template</h1>
<p class="muted">Duplicate this page (Save As) or print copies. Date is blank on purpose.</p>
<div class="day-card">
  <h3><span>Date: _______________ · Day: ________</span><span class="muted">Top 3 + blocks + Pomodoro</span></h3>
  <p style="margin:.2rem 0;font-size:.85rem;color:var(--muted)"><strong>MIT / Top 3</strong></p>
  <ul class="mit">
    <li><span class="box"></span><span class="lined" style="border:0;min-height:1.4rem"></span></li>
    <li><span class="box"></span><span class="lined" style="border:0"></span></li>
    <li><span class="box"></span><span class="lined" style="border:0"></span></li>
  </ul>
  <div class="blocks">
    <div class="slot"><div class="label">Morning block</div><div class="lined"></div><div class="lined"></div></div>
    <div class="slot"><div class="label">Afternoon block</div><div class="lined"></div><div class="lined"></div></div>
    <div class="slot"><div class="label">Evening block</div><div class="lined"></div><div class="lined"></div></div>
  </div>
  <div class="pomo"><span>Pomodoro (Cirillo):</span>
    <span class="tick"></span><span class="tick"></span><span class="tick"></span><span class="tick"></span>
    <span class="muted">25 on / 5 off</span>
  </div>
  <p style="margin:.7rem 0 .2rem;font-size:.85rem;color:var(--muted)"><strong>Brain dump</strong> (parking lot — not commitments)</p>
  <div class="lined"></div><div class="lined"></div><div class="lined"></div>
</div>
'''
(ROOT / "templates" / "day.html").write_text(page("Day template — ADHD 2027 Planner", day_body, depth=1), encoding="utf-8")

for w in weeks:
    write_week(w)

cal = calendar.Calendar(firstweekday=0)
for m in range(1, 13):
    mons = []
    seen = set()
    for day in cal.itermonthdates(2027, m):
        if day.month == m:
            mon = day - timedelta(days=day.weekday())
            if mon not in seen:
                seen.add(mon)
                mons.append(mon)
    rows = []
    for week_days in cal.monthdatescalendar(2027, m):
        cells = []
        mon = week_days[0]
        for d in week_days:
            if d.month == m:
                href = f"../{week_path(mon)}#d{d.isoformat()}"
                week_href = f"../{week_path(mon)}"
                cells.append(
                    f'<td><a class="day" href="{href}">{d.day}</a>'
                    f'<a class="weeklink" href="{week_href}">week</a></td>'
                )
            else:
                cells.append(f'<td class="out">{d.day}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    week_list = "".join(
        f'<li><a href="../{week_path(mon)}">Week of {mon.isoformat()}</a> → {(mon + timedelta(days=6)).isoformat()}</li>'
        for mon in mons
    )
    prev_m = f'<a href="2027-{m-1:02d}.html">← {MONTHS[m-2]}</a>' if m > 1 else '<span class="muted">←</span>'
    next_m = f'<a href="2027-{m+1:02d}.html">{MONTHS[m]} →</a>' if m < 12 else '<span class="muted">→</span>'
    body = f'''
<p class="muted"><span class="tag">month hub</span> Click a day or “week” to open the week spread</p>
<h1>{MONTHS[m-1]} 2027</h1>
<div class="week-nav">{prev_m}<a href="../index.html">Year</a>{next_m}</div>
<table class="cal" aria-label="{MONTHS[m-1]} 2027 calendar">
  <thead><tr>{"".join(f"<th>{x}</th>" for x in DOW)}</tr></thead>
  <tbody>
{"".join(rows)}
  </tbody>
</table>
<div class="card">
  <strong>Weeks touching {MONTHS[m-1]}</strong>
  <ul>{week_list}</ul>
</div>
'''
    (ROOT / month_path(m)).write_text(
        page(f"{MONTHS[m-1]} 2027 — ADHD Planner", body, depth=1), encoding="utf-8"
    )

# EXAMPLE filled week
ex_mon = date(2027, 1, 11)
filled = {
    "_week": {
        "mits": [
            "Ship client draft to Nora Blake by Thu",
            "Doctor form + pharmacy refill",
            "Protect two deep-work mornings (no Slack)",
        ],
        "done": 1,
    },
    date(2027, 1, 11): {
        "mits": ["Outline Nora Blake draft (sections only)", "Book pharmacy refill online", "20-min walk after lunch"],
        "done": [True, True, False],
        "blocks": {
            "Morning": "09:00–11:00 Outline draft (phone in other room)",
            "Afternoon": "13:30 Pharmacy order + email triage 30m",
            "Evening": "Low stim: dishes + plan Tue Top 3",
        },
        "pomo": 3,
        "dump": "Buy oat milk · reply Discord later · idea: template for kickoff calls",
    },
    date(2027, 1, 12): {
        "mits": ["Write draft body 800 words", "Send calendar invite to Sam Okonkwo", "Laundry start"],
        "done": [True, True, True],
        "blocks": {
            "Morning": "09:00–11:30 Draft body (2 Pomodoros+)",
            "Afternoon": "Invite Sam · laundry · snack",
            "Evening": "TV only after Top 3 checked",
        },
        "pomo": 4,
        "dump": "Mom birthday Mar 3 · fix bike light",
    },
    date(2027, 1, 13): {
        "mits": ["Edit draft for clarity", "Grocery: protein + greens", "Pay electric bill"],
        "done": [False, True, True],
        "blocks": {
            "Morning": "Edit pass (headphones, one tab)",
            "Afternoon": "Errands loop 60m max",
            "Evening": "Rest — no new commitments",
        },
        "pomo": 2,
        "dump": "Feeling scattered after lunch — shorten Thursday",
    },
    date(2027, 1, 14): {
        "mits": ["Send draft to Nora Blake", "Admin: invoice #1042", "Stretch 10 min"],
        "done": [True, False, True],
        "blocks": {
            "Morning": "Final polish + send before noon",
            "Afternoon": "Invoice #1042 in Aging sheet",
            "Evening": "Friend call (optional)",
        },
        "pomo": 3,
        "dump": "Celebrate send with coffee out",
    },
    date(2027, 1, 15): {
        "mits": ["Light admin only", "Prep weekend groceries list", "Early bedtime target 22:30"],
        "done": [True, True, False],
        "blocks": {
            "Morning": "Inbox zero attempt 45m",
            "Afternoon": "Buffer / open",
            "Evening": "Screens off 22:00 if possible",
        },
        "pomo": 1,
        "dump": "Protect Sat morning for hobby",
    },
    date(2027, 1, 16): {
        "mits": ["Hobby block: sketch 45m", "Meal prep 2 lunches", "Text Sam confirm Mon"],
        "done": [True, False, True],
        "blocks": {
            "Morning": "Sketch — timer on",
            "Afternoon": "Meal prep or skip without guilt",
            "Evening": "Social optional",
        },
        "pomo": 2,
        "dump": "No work Slack on Sat",
    },
    date(2027, 1, 17): {
        "mits": ["Weekly review 20 min", "Set Mon–Wed Top 3", "Return library book"],
        "done": [True, True, False],
        "blocks": {
            "Morning": "Weekly review page",
            "Afternoon": "Library + groceries",
            "Evening": "Wind down",
        },
        "pomo": 1,
        "dump": "Tomorrow: deep work morning protected",
    },
}

write_week(ex_mon, filled=filled)

i = week_index[ex_mon]
days = [ex_mon + timedelta(days=k) for k in range(7)]
days_html = "\n".join(day_section(d, filled) for d in days)
banner = '''<p><span class="tag">EXAMPLE</span><span class="tag">fake person</span></p>
<div class="card" style="border-color:#e8d4a8;background:#fff8e8">
  <strong>Filled example — not real client data.</strong>
  Persona: <strong>Alex Rivera</strong> (freelance designer). Week of Mon 2027-01-11.
  Shows how Top 3 + time blocks + Pomodoro ticks look when used. Blank weeks elsewhere are empty on purpose.
</div>'''
ex_body = f'''
{banner}
<h1>EXAMPLE week: 2027-01-11 – 2027-01-17</h1>
<div class="week-nav">
  <a href="../{week_path(weeks[i-1])}">← Blank prev week</a>
  <a href="../{month_path(1)}">→ January hub</a>
  <a href="../{week_path(weeks[i+1])}">Blank next week →</a>
</div>
<div class="card">
  <strong>This week’s Top 3</strong>
  {week_mits_html(filled)}
</div>
<div class="days">
{days_html}
</div>
<p class="muted">Day-template links above go to the blank template. To use a real week, open any month hub.</p>
'''
(ROOT / "example" / "filled-week.html").write_text(
    page("EXAMPLE filled week — ADHD 2027 Planner", ex_body, depth=1), encoding="utf-8"
)

print("weeks:", len(weeks))
print("html files:", len(list(ROOT.rglob("*.html"))))
print("ok")
