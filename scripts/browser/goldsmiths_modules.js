// Run with the Chrome javascript tool on a Goldsmiths Study Abroad module-finder page, e.g.
// https://www.gold.ac.uk/studyabroad/module-options/module-finder/?filter%5Bsubject%5D=Psychology
// Each module's details are embedded in the page (#item-<id>). Stores results in window._gold and returns a short summary;
// read window._gold in ~900-character slices if the tool output is truncated.
(() => {
  const out = [...document.querySelectorAll('article.teaser')].filter(a => a.querySelector('h3 a')).map(a => {
    const link = a.querySelector('h3 a'); const id = (link.getAttribute('href') || '').replace('#', '');
    const d = document.getElementById(id); const txt = (d ? d.innerText : a.innerText).replace(/\s*\n\s*/g, ' | ');
    const meta = (txt.match(/(Undergraduate|Postgraduate)[^|]*Term\(s\) Taught:[^|]*/) || [''])[0].trim();
    const assess = (txt.match(/Assessment[^|]*(\|[^|]*){0,2}/g) || []).map(s => s.replace(/\s*\|\s*/g, ' ').trim()).filter(s => s.length > 10);
    return { school: 'goldsmiths', title: link.innerText.trim(), meta,
      terms: ((meta.split('Term(s) Taught:')[1] || a.querySelector('.teaser__meta-term')?.innerText || '').trim()),
      year: (meta.match(/Year \d/) || [''])[0], assessment: assess.slice(0, 3),
      has_exam: /exam/i.test(assess.join(' ')), subject: decodeURIComponent((location.search.match(/subject%5D=([^&]+)|subject\]=([^&]+)/) || [])[1] || '').replace(/\+/g, ' '), item: id };
  });
  window._gold = JSON.stringify(out);
  return `${out.length} modules; spring: ${out.filter(m => /Spring/.test(m.terms)).length}; read window._gold for JSON`;
})();
