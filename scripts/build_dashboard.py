#!/usr/bin/env python3
"""Build me/dashboard.html (self-contained, read-only) from the me/ data files.
Usage: python3 scripts/build_dashboard.py [--today YYYY-MM-DD]
"""
import csv, datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import data_dir
ME = data_dir()


def load(name, default):
    try:
        return json.load(open(os.path.join(ME, name)))
    except Exception:
        return default


def main():
    today = datetime.date.today().isoformat()
    if "--today" in sys.argv:
        today = sys.argv[sys.argv.index("--today") + 1]
    try:
        expenses = list(csv.DictReader(open(os.path.join(ME, "expenses.csv"))))
    except Exception:
        expenses = []
    data = {
        "today": today,
        "profile": load("profile.json", {}),
        "requirements": load("requirements.json", []),
        "courses": load("courses.json", []),
        "deadlines": load("deadlines.json", []),
        "tasks": load("tasks.json", []),
        "bookings": load("bookings.json", []),
        "documents": load("documents.json", []),
        "contacts": load("contacts.json", []),
        "budget": load("budget.json", {}),
        "expenses": expenses,
    }
    try:
        oq = open(os.path.join(ME, "open-questions.md")).read().splitlines()
        data["questions"] = [l[2:].strip() for l in oq if l.startswith("- ")]
    except Exception:
        data["questions"] = []
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__DATA__", payload)
    out = os.path.join(ME, "dashboard.html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"wrote {out} ({len(html)//1024} KB)")


TEMPLATE = r"""<meta charset="utf-8">
<title>Abroad Planner</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Source+Sans+3:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: a departures-board summary up top, then a two-column working grid (week + courses | deadlines + money) that stacks on phones */
:root {
  --bg: #f3f5f8; --surface: #ffffff; --ink: #172033; --muted: #5b6579; --line: #d9dee8;
  --accent: #1f4fd1; --accent-soft: #e4ebfc; --brick: #b2462e;
  --good: #1d7a4c; --good-soft: #e1f3e9; --warn: #a86400; --warn-soft: #fcf0d9; --bad: #b42335; --bad-soft: #fbe3e6;
  --f-display: "Bricolage Grotesque", "Avenir Next", "Segoe UI", sans-serif;
  --f-body: "Source Sans 3", "Helvetica Neue", Arial, sans-serif;
  --f-data: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0f1420; --surface: #171e2e; --ink: #e7ebf3; --muted: #9aa4b8; --line: #2a3347;
  --accent: #7d9cff; --accent-soft: #1d2950; --brick: #e57a5f;
  --good: #5fcf96; --good-soft: #143224; --warn: #f0b552; --warn-soft: #3a2a10; --bad: #ff7a8a; --bad-soft: #3d1820; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #0f1420; --surface: #171e2e; --ink: #e7ebf3; --muted: #9aa4b8; --line: #2a3347;
  --accent: #7d9cff; --accent-soft: #1d2950; --brick: #e57a5f;
  --good: #5fcf96; --good-soft: #143224; --warn: #f0b552; --warn-soft: #3a2a10; --bad: #ff7a8a; --bad-soft: #3d1820; color-scheme: dark }
* { box-sizing: border-box }
body { background: var(--bg); color: var(--ink); font: 16px/1.5 var(--f-body); }
.wrap { max-width: 1180px; margin: 0 auto; padding-block: 20px 48px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: grid; gap: 20px }
h1, h2 { font-family: var(--f-display); text-wrap: balance; margin: 0 }
h1 { font-size: clamp(1.7rem, 4vw, 2.4rem); font-weight: 800; letter-spacing: -0.01em }
h2 { font-size: 1.05rem; font-weight: 600; display: flex; justify-content: space-between; align-items: baseline; gap: 8px }
h2 small { font: 500 .72rem var(--f-data); color: var(--muted); letter-spacing: .04em; text-transform: uppercase }
.muted { color: var(--muted) } .mono { font-family: var(--f-data); font-variant-numeric: tabular-nums }
header { display: grid; gap: 14px }
.sub { color: var(--muted) }
.board { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1px; background: var(--line);
  border: 1px solid var(--line); border-radius: 10px; overflow: hidden }
.board div { background: var(--surface); padding: 12px 14px; min-width: 0 }
.board b { display: block; font: 600 1.6rem/1.1 var(--f-display) } .board span { font-size: .8rem; color: var(--muted); text-transform: uppercase; letter-spacing: .06em }
.grid { display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr); gap: 20px; align-items: start }
@media (max-width: 860px) { .grid { grid-template-columns: minmax(0, 1fr) } }
.col { display: grid; gap: 20px; min-width: 0 }
section { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 16px; display: grid; gap: 12px; min-width: 0 }
section.alert { border-color: var(--brick); }
ul.list { list-style: none; margin: 0; padding: 0; display: grid; gap: 0 }
ul.list li { display: grid; grid-template-columns: 92px minmax(0, 1fr) auto; gap: 10px; padding: 8px 0; border-top: 1px solid var(--line); align-items: baseline }
ul.list li:first-child { border-top: 0 }
.date { font: 500 .82rem var(--f-data); color: var(--muted); font-variant-numeric: tabular-nums }
.pill { font: 500 .7rem/1 var(--f-data); padding: 4px 7px; border-radius: 99px; white-space: nowrap; letter-spacing: .02em; background: var(--accent-soft); color: var(--accent) }
.pill.good { background: var(--good-soft); color: var(--good) } .pill.warn { background: var(--warn-soft); color: var(--warn) }
.pill.bad { background: var(--bad-soft); color: var(--bad) } .pill.plain { background: transparent; border: 1px solid var(--line); color: var(--muted) }
.scroll { overflow-x: auto }
table { border-collapse: collapse; width: 100%; font-size: .92rem; min-width: 560px }
th { text-align: left; font: 500 .72rem var(--f-data); text-transform: uppercase; letter-spacing: .05em; color: var(--muted); padding: 6px 8px; border-bottom: 1px solid var(--line) }
td { padding: 8px; border-bottom: 1px solid var(--line); vertical-align: top }
tr.dropped td { color: var(--muted) } tr.dropped td:nth-child(2) { text-decoration: line-through }
.week { display: grid; grid-template-columns: 44px repeat(5, minmax(0, 1fr)); font-size: .78rem; position: relative; min-width: 520px }
.week .hd { font: 600 .75rem var(--f-data); text-align: center; padding-bottom: 6px; color: var(--muted) }
.week .hr { font: .7rem var(--f-data); color: var(--muted); height: 34px; border-top: 1px solid var(--line); padding-top: 2px }
.week .cell { border-top: 1px solid var(--line); border-left: 1px solid var(--line); height: 34px }
.slot { position: absolute; border-radius: 6px; padding: 3px 6px; overflow: hidden; background: var(--accent-soft); color: var(--accent);
  border-left: 3px solid var(--accent); font: 500 .72rem/1.25 var(--f-data) }
.slot.prov { border-left-style: dashed } .slot.drop { background: var(--bad-soft); color: var(--bad); border-left-color: var(--bad); opacity: .75 }
.slot.opt { background: transparent; color: var(--muted); border: 1px dashed var(--line); border-left: 3px dashed var(--muted) }
.legend { display: flex; flex-wrap: wrap; gap: 8px; font-size: .8rem; color: var(--muted) }
.bar { height: 8px; background: var(--line); border-radius: 99px; overflow: hidden } .bar i { display: block; height: 100%; background: var(--accent) }
.req { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 4px 10px; align-items: center; padding: 6px 0; border-top: 1px solid var(--line) }
.req:first-of-type { border-top: 0 }
.empty { color: var(--muted); font-size: .92rem }
details summary { cursor: pointer; color: var(--accent); font-weight: 600 }
a { color: var(--accent) } :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px }
footer { font-size: .82rem; color: var(--muted) }
@media (max-width: 520px) { ul.list li { grid-template-columns: 76px minmax(0, 1fr); } ul.list li .pill { grid-column: 2; justify-self: start } }
</style>
<div class="wrap" id="app"></div>
<script>
const D = __DATA__;
const $ = (h) => { const t = document.createElement('template'); t.innerHTML = h.trim(); return t.content; };
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const day = (iso) => new Date(iso + 'T12:00:00');
const diff = (iso) => Math.round((day(iso) - day(D.today)) / 864e5);
const fmt = (iso) => iso ? day(iso).toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }) : '';
const usd = (n) => '$' + Number(n || 0).toLocaleString('en-US', { maximumFractionDigits: 0 });
const when = (n) => n < 0 ? `${-n}d overdue` : n === 0 ? 'today' : n === 1 ? 'tomorrow' : `in ${n}d`;
const urg = (n) => n < 0 ? 'bad' : n <= 7 ? 'warn' : 'plain';
const P = D.profile || {};
const open = (D.deadlines || []).filter(d => d.status !== 'done').sort((a, b) => a.date.localeCompare(b.date));
const todo = (D.tasks || []).filter(t => t.status !== 'done');
const soon = open.filter(d => diff(d.date) <= 14);
const arrive = P.program_dates?.arrive_by;
const spent = (D.expenses || []).reduce((s, e) => s + Number(e.usd || 0), 0);
const expRefs = new Set((D.expenses || []).map(e => e.ref).filter(Boolean));
const booked = (D.bookings || []).filter(b => b.status !== 'cancelled' && b.cost?.usd && !expRefs.has(b.confirmation_ref)).reduce((s, b) => s + Number(b.cost.usd), 0);
const kept = (D.courses || []).filter(c => c.status === 'registered');

let h = `<header>
  <div><h1>${esc(P.name || 'Your')} · ${esc(P.host_school || 'Study abroad')}</h1>
  <div class="sub">${esc(P.term || '')} · ${esc(P.penn_school || '')} ${esc((P.majors || []).join(', '))}${P.minors?.length ? ' · minor ' + esc(P.minors.join(', ')) : ''} · updated ${fmt(D.today)}</div></div>
  <div class="board">
    <div><span>Due in 14 days</span><b>${soon.length}</b></div>
    <div><span>Open tasks</span><b>${todo.length}</b></div>
    <div><span>${arrive ? 'Arrive by' : 'Arrival'}</span><b>${arrive ? (diff(arrive) >= 0 ? diff(arrive) + 'd' : 'arrived') : '—'}</b></div>
    <div><span>Courses registered</span><b>${kept.length}</b></div>
    <div><span>Spent &amp; booked</span><b>${usd(spent + booked)}</b><small class="muted" style="font-size:.72rem">${usd(spent)} spent · ${usd(booked)} booked</small></div>
  </div></header>`;

const attn = [...soon.map(d => ({ date: d.date, t: d.title, n: diff(d.date), k: 'Deadline' })),
  ...todo.filter(t => t.priority === 'high' && !soon.some(d => d.title === t.title)).map(t => ({ date: t.due, t: t.title, n: t.due ? diff(t.due) : 99, k: 'Task' }))]
  .sort((a, b) => a.n - b.n);
h += `<section class="alert"><h2>Needs attention <small>next 14 days + high-priority tasks</small></h2>` +
  (attn.length ? `<ul class="list">${attn.map(a => `<li><span class="date">${a.date ? fmt(a.date).slice(0, 11) : 'no date'}</span><span>${esc(a.t)} <span class="muted">· ${a.k}</span></span><span class="pill ${urg(a.n)}">${a.date ? when(a.n) : 'open'}</span></li>`).join('')}</ul>` : `<p class="empty">Nothing due in the next two weeks.</p>`) + `</section>`;

// week grid
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], START = 8, END = 19, ROW = 34, HEAD = 22;
const toH = (s) => { const [a, b] = s.split(':').map(Number); return a + b / 60; };
let wk = `<div class="week" id="week"><div></div>${DAYS.map(d => `<div class="hd">${d}</div>`).join('')}`;
for (let r = START; r < END; r++) wk += `<div class="hr">${r}:00</div>` + DAYS.map(() => '<div class="cell"></div>').join('');
wk += '</div>';
const slots = [];
const myCourses = (D.courses || []).filter(c => c.status === 'registered');
const tutOptions = [];
myCourses.forEach(c => (c.days || []).forEach(s => {
  const di = DAYS.indexOf(s.day); if (di < 0) return;
  if (/option/i.test(s.type || '')) { tutOptions.push(`${c.id} ${s.day} ${s.start}`); return; }
  const drop = /DROP/.test(c.verdict || ''), opt = /option/i.test(s.type || '') || c.status === 'considering';
  slots.push({ di, top: HEAD + (toH(s.start) - START) * ROW, ht: (toH(s.end) - toH(s.start)) * ROW - 2,
    cls: drop ? 'drop' : opt ? 'opt' : (s.provisional ? 'prov' : ''), label: `${c.id} ${s.type ? '· ' + s.type.replace(' option', '?') : ''}<br>${s.start}–${s.end}` });
}));
const noTimes = myCourses.filter(c => c.host_school && !/^penn$/i.test(c.host_school) && !(c.days || []).length);
h += `<div class="grid"><div class="col">
<section><h2>Weekly timetable <small>${(D.courses || []).some(c => (c.days || []).some(d => d.provisional)) ? 'provisional' : 'confirmed'}</small></h2>
<div class="scroll">${wk}</div>
${tutOptions.length ? `<p class="muted" style="font-size:.85rem;margin:0">Tutorial slots you may be placed in (not shown on the grid): ${tutOptions.map(esc).join(' · ')}</p>` : ''}
${noTimes.length ? `<p class="muted" style="font-size:.85rem;margin:0">Not on the grid yet: ${noTimes.map(c => esc(c.id) + (c.title ? ' ' + esc(c.title) : '')).join(', ')} — class times not found yet (the host school may not have published them, or they haven\'t been looked up). Ask the planner to "look up my class times".</p>` : ''}
<div class="legend"><span class="pill">registered</span><span class="pill plain">option / considering</span><span class="pill bad">planned drop</span><span>dashed edge = provisional time</span></div></section>`;

const xs = (x) => ({ precedent: ['good', 'precedent'], approved: ['good', 'approved'], none: ['warn', 'needs XCAT'], drafted: ['plain', 'drafted'], submitted: ['plain', 'submitted'], denied: ['bad', 'denied'] }[x?.status] || ['plain', x?.status || '—']);
const vd = (v) => /^KEEP/.test(v) ? 'good' : /^DROP/.test(v) ? 'bad' : /UNLIKELY/.test(v) ? 'bad' : 'warn';
h += `<section><h2>My courses <small>${myCourses.length} registered · host → Penn</small></h2><div class="scroll"><table><thead><tr><th>Code</th><th>Module</th><th>Penn credit</th><th>XCAT</th><th>Exam May–Jun</th><th>Days</th></tr></thead><tbody>` +
  myCourses.map(c => { const [k, l] = xs(c.xcat); return `<tr class="${/DROP/.test(c.verdict || '') ? 'dropped' : ''}"><td class="mono">${esc(c.id)}</td><td>${esc(c.title)}<div class="muted" style="font-size:.8rem">L${esc(c.level)} · ${esc(c.assessment || '')}</div></td><td>${esc(c.penn_equivalent || '—')}</td><td><span class="pill ${k}">${l}</span>${c.xcat?.precedent_expires ? `<div class="muted mono" style="font-size:.72rem">exp ${c.xcat.precedent_expires}</div>` : ''}</td><td>${c.has_exam_in_exam_period ? '<span class="pill bad">yes</span>' : '<span class="pill good">no</span>'}</td><td class="mono" style="font-size:.8rem">${(c.days || []).filter(d => !/option/i.test(d.type || '')).map(d => esc(`${d.day} ${d.start}–${d.end}`)).join('<br>') || '—'}</td></tr>`; }).join('') +
  `</tbody></table></div></section>`;

const reqDone = r => (r.done_cu || 0) + (r.in_progress_cu || 0);
const reqMet = r => r.needed_cu ? reqDone(r) >= r.needed_cu : r.status === 'done';
const cuLeft = rs => rs.reduce((n, r) => n + (r.needed_cu ? Math.max(0, r.needed_cu - reqDone(r)) : (reqMet(r) ? 0 : 1)), 0);
const reqs = [...(D.requirements || [])].sort((a, b) => reqMet(a) - reqMet(b));
const reqRow = r => {
  const met = reqMet(r), pct = r.needed_cu ? Math.min(100, 100 * reqDone(r) / r.needed_cu) : (met ? 100 : 0);
  const plan = (D.courses || []).filter(c => c.penn_requirement === r.id && !/DROP|UNLIKELY/.test(c.verdict || '')).map(c => c.id);
  const pill = met ? `<span class="pill good">${r.in_progress_cu ? 'done · in progress' : 'done'}</span>` : `<span class="pill ${plan.length ? 'good' : 'plain'}">${esc(r.program)}</span>`;
  const sub = (r.satisfied_by || []).length ? 'Covered by: ' + r.satisfied_by.join(', ') : plan.length ? 'Planned abroad: ' + plan.join(', ') : (r.notes || '');
  return `<div class="req"><div><div>${esc(r.name)}</div><div class="muted" style="font-size:.82rem">${esc(sub)}</div></div>${pill}<div class="bar" style="grid-column:1/-1"><i style="width:${pct}%;${met ? 'background:var(--good)' : ''}"></i></div></div>`;
};
const GROUPS = [['major', 'Major'], ['minor', 'Minor'], ['gen-ed', 'Gen eds']];
const other = reqs.filter(r => !GROUPS.some(([k]) => k === r.program));
h += `<section><h2>Degree requirements <small>${cuLeft(reqs)} CU left · courses you're taking at Penn now count as done; planned abroad courses don't</small></h2>` +
  [...GROUPS.map(([k, label]) => [label, reqs.filter(r => r.program === k)]), ['Other', other]].filter(([, rs]) => rs.length)
    .map(([label, rs]) => `<h3 style="margin:10px 0 0;font:600 .78rem var(--f-data);text-transform:uppercase;letter-spacing:.06em;color:var(--muted)">${label} · ${cuLeft(rs)} CU left</h3>` + rs.map(reqRow).join('')).join('') + `</section></div><div class="col">`;

// timeline
let lastM = '';
h += `<section><h2>Key dates <small>${open.length} upcoming</small></h2><ul class="list">` + open.map(d => {
  const m = day(d.date).toLocaleDateString('en-GB', { month: 'long', year: 'numeric' }); const head = m !== lastM ? (lastM = m, `<li style="grid-template-columns:1fr;border:0;padding-top:12px"><b class="mono" style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em">${m}</b></li>`) : '';
  return head + `<li><span class="date">${fmt(d.date).slice(0, 7)}${d.time ? '<br>' + esc(d.time) + (d.tz === 'Europe/London' ? ' UK' : '') : ''}</span><span>${esc(d.title)}</span><span class="pill ${urg(diff(d.date))}">${esc(d.category)}</span></li>`;
}).join('') + `</ul></section>`;

h += `<section><h2>Tasks <small>${todo.length} open</small></h2><ul class="list">` + todo.map(t => `<li><span class="date">${t.due ? fmt(t.due).slice(0, 11) : '—'}</span><span>${esc(t.title)}</span><span class="pill ${t.priority === 'high' ? 'warn' : 'plain'}">${esc(t.priority)}</span></li>`).join('') + `</ul></section>`;

const cats = {}; (D.expenses || []).forEach(e => cats[e.category] = (cats[e.category] || 0) + Number(e.usd || 0));
(D.bookings || []).filter(b => b.status !== 'cancelled' && b.cost?.usd && !expRefs.has(b.confirmation_ref)).forEach(b => cats.travel = (cats.travel || 0) + Number(b.cost.usd));
const planned = D.budget?.categories || {};
const keys = [...new Set([...Object.keys(planned), ...Object.keys(cats)])];
h += `<section><h2>Budget <small>USD · spent + booked · ECB rates</small></h2>` + (keys.length ? keys.map(k => { const p = planned[k], s = cats[k] || 0, pct = p ? Math.min(100, 100 * s / p) : 0;
  return `<div class="req"><div>${esc(k)}</div><span class="mono">${usd(s)}${p ? ' / ' + usd(p) : ''}</span><div class="bar" style="grid-column:1/-1"><i style="width:${pct}%;${p && s > p ? 'background:var(--bad)' : ''}"></i></div></div>`; }).join('')
  : '') +
  (() => { const items = [...(D.expenses || []).map(e => ({ date: e.date, what: e.description, cat: e.category, usd: Number(e.usd || 0), orig: e.currency && e.currency !== 'USD' ? `${e.amount} ${e.currency}` : '', kind: 'spent' })),
      ...(D.bookings || []).filter(b => b.status !== 'cancelled' && b.cost?.usd && !(D.expenses || []).some(e => e.ref && e.ref === b.confirmation_ref)).map(b => ({ date: (b.start || '').slice(0, 10), what: `${b.provider || b.type}${b.to ? ' · ' + b.to : ''} (${b.type}, ${(b.start || '').slice(5, 10)}–${(b.end || '').slice(5, 10)})`, cat: 'travel', usd: Number(b.cost.usd), orig: b.cost.currency && b.cost.currency !== 'USD' ? `${b.cost.amount} ${b.cost.currency}` : '', kind: 'booked' }))]
      .sort((a, b) => (b.date || '').localeCompare(a.date || ''));
    return items.length ? `<ul class="list">${items.map(i => `<li><span class="date">${esc(i.date)}</span><span>${esc(i.what)}<br><span class="muted" style="font-size:.8rem">${esc(i.cat)}${i.orig ? ' · ' + esc(i.orig) : ''}</span></span><span class="mono">${usd(i.usd)} <span class="pill ${i.kind === 'booked' ? 'plain' : ''}">${i.kind}</span></span></li>`).join('')}</ul>`
      : `<p class="empty">No spending logged yet. Tell the agent "log £12 lunch" or ask it to import a bank CSV or scan receipts.</p>`; })() + `</section>`;

const liveB = (D.bookings || []).filter(b => b.status !== 'cancelled');
h += `<section><h2>Bookings <small>${liveB.length}${liveB.length !== (D.bookings || []).length ? ' · ' + ((D.bookings || []).length - liveB.length) + ' cancelled' : ''}</small></h2>` + ((D.bookings || []).length ? `<ul class="list">${D.bookings.sort((a, b) => (a.start || '').localeCompare(b.start || '')).map(b => `<li><span class="date">${fmt((b.start || '').slice(0, 10)).slice(0, 11)}</span><span>${esc(b.type)} · ${esc(b.from || '')}${b.to ? ' → ' + esc(b.to) : ''} <span class="muted">${esc(b.provider || '')}</span></span><span class="mono">${b.status === 'cancelled' ? '<span class="pill bad">cancelled</span>' : (b.cost?.usd ? usd(b.cost.usd) : '')}</span></li>`).join('')}</ul>` : `<p class="empty">No bookings yet. The agent adds flights, trains and stays it finds in your inboxes.</p>`) + `</section>`;

const docs = D.documents || [], copies = docs.filter(d => d.kind === 'copy' && d.path), notes = docs.filter(d => !(d.kind === 'copy' && d.path));
h += `<section><h2>Documents <small>${copies.length} saved · ${notes.length} notes</small></h2>` +
  (copies.length ? `<ul class="list">${copies.map(d => `<li><span class="date">${esc(d.issued || '')}</span><span><a href="${esc(d.path)}" target="_blank" rel="noopener">${esc(d.title)}</a><br><span class="muted" style="font-size:.82rem">${esc(d.type || '')}${d.expires ? ' · expires ' + esc(d.expires) : ''}</span></span><a class="pill" href="${esc(d.path)}" target="_blank" rel="noopener">Open</a></li>`).join('')}</ul>` : '<p class="empty">No saved documents yet. Ask the planner to save your offer letter, lease or ETA approval.</p>') +
  (notes.length ? `<p class="muted" style="font-size:.82rem;margin:8px 0 0">Kept as notes only (ID details are never stored):</p><ul class="list">${notes.map(d => `<li><span class="date">${d.expires ? 'exp ' + esc(d.expires) : esc(d.issued || '')}</span><span>${esc(d.title)} <span class="muted">· ${esc(d.where_original || '')}</span></span><span class="pill plain">note</span></li>`).join('')}</ul>` : '') + `</section>`;

// Open questions are kept in me/open-questions.md and answered in chat — not shown on the dashboard.

h += `<section><h2>Contacts</h2><ul class="list">${(D.contacts || []).map(c => `<li style="grid-template-columns:minmax(0,1fr)"><span><b>${esc(c.name)}</b> <span class="muted">· ${esc(c.role)}</span><br><span class="mono" style="font-size:.8rem;user-select:all">${esc(c.email)}</span> <span class="muted" style="font-size:.85rem">— ${esc(c.when_to_use)}</span></span></li>`).join('')}</ul></section>`;
h += `</div></div><footer>Read-only view. To change anything, ask the agent. Times marked provisional can still change; credit is confirmed only by an XCAT decision.</footer>`;
document.getElementById('app').append($(h));

// place week slots (needs layout)
const wkEl = document.getElementById('week');
if (wkEl) { const colW = (wkEl.clientWidth - 44) / 5;
  const groups = {}; slots.forEach(s => (groups[s.di] = groups[s.di] || []).push(s));
  Object.values(groups).forEach(g => g.forEach((s, i) => { const overl = g.filter(o => o !== s && o.top < s.top + s.ht && s.top < o.top + o.ht);
    const n = overl.length + 1, idx = [s, ...overl].sort((a, b) => a.top - b.top || a.label.localeCompare(b.label)).indexOf(s);
    const el = document.createElement('div'); el.className = 'slot ' + s.cls; el.innerHTML = s.label;
    el.style.cssText = `top:${s.top}px;height:${s.ht}px;left:calc(44px + ${s.di} * ((100% - 44px) / 5) + ${idx} * ((100% - 44px) / 5 / ${n}) + 2px);width:calc((100% - 44px) / 5 / ${n} - 4px)`;
    wkEl.append(el); })); }
</script>
"""

if __name__ == "__main__":
    main()
