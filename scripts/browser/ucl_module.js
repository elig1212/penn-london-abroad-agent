// Run with the Chrome javascript tool on a UCL module page (ucl.ac.uk/module-catalogue/modules/<slug>-<CODE>).
// UCL blocks scripted downloads (403), so this runs inside the user's browser. Returns one JSON line.
(() => {
  const t = document.body.innerText.replace(/\n+/g, ' | ');
  const grab = (label, stop) => { const i = t.indexOf(label); if (i < 0) return ''; const s = t.slice(i + label.length, i + label.length + 600).replace(/^\s*\|\s*/, ''); return stop ? s.split(stop)[0] : s.split(' | ')[0]; };
  const code = (document.title.match(/\(([A-Z]{4}\d{4})\)/) || [])[1] || '';
  const deliv = t.slice(t.indexOf('Module deliveries'));
  const terms = [...new Set((deliv.match(/Intended teaching term: ([^|]+?)\s{2,}|Intended teaching term: ([^|]+)/g) || []).map(s => s.replace('Intended teaching term:', '').trim()))];
  const levels = [...new Set(deliv.match(/FHEQ Level \d/g) || [])];
  const assess = (deliv.match(/Methods of assessment \| (.*?) \| Mark scheme/) || [])[1] || '';
  return JSON.stringify({ school: 'ucl', code, title: document.title.split(' (')[0], credits: grab('Credit value'),
    terms, levels, assessment: assess.split(' | '), has_exam: /Exam/i.test(assess),
    restrictions: grab('Restrictions', ' | Timetable').slice(0, 300), contact: grab('Who to contact for more information'),
    affiliate_note: /affiliate students may be different/.test(t) ? 'Assessment for affiliates may differ — confirm with department' : '',
    url: location.href, checked: new Date().toISOString().slice(0, 10) });
})();
