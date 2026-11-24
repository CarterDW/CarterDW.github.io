# carterdw.github.io

Personal academic site. Plain HTML/CSS with no build step: edit `index.html` and push.

- `index.html`: the whole page (about, publications, talks, projects, software)
- `assets/style.css`: shared styles; the COMP2026 portfolio reuses them via `/assets/style.css`
- `assets/CV.pdf`: CV (add it)
- `assets/img/`: portrait and project thumbnails

Before launch: delete the `<meta name="robots" content="noindex">` line in `index.html` (it keeps the draft out of search engines).

Content comes from the CV (Downloads/Carter Williams CV.pdf, Nov 2026). The CV link is commented out until a phone-free `assets/CV.pdf` is added; search index.html for "CV: uncomment".

The portfolio lives in its own repo, `comp2026-portfolio`, served at
`/comp2026-portfolio/` with one sub-site per project (`solar-system/`, `defects/`, `sky-classifier/`).

Local preview: `python -m http.server` here, then open http://localhost:8000.
(The `/comp2026-portfolio/` links only resolve on GitHub Pages.)
