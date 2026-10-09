# NewsLens — Dashboard Prototype

A Django multi-page dashboard: Overview, Articles, Compare, Analysis,
Narrative Trends, Settings, and Profile. Dark, editorial, research-
instrument styling; Tailwind CSS + custom CSS; Plotly.js charts; Lucide
icons. No React/Vue/Next/Streamlit/Dash — plain Django templates and
vanilla JS, per the original brief.

## Run it

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate        # sets up the (unused) default SQLite tables
python manage.py runserver
```

Then open **http://127.0.0.1:8000/**.

## What's here

- `config/` — Django project settings/urls (the "project" package).
- `dashboard/` — the one app the whole site runs on.
  - `views.py` — one view per sidebar page. Each assembles demo data +
    the shared chart theme into a JSON payload for its template.
  - `services.py` — **demo data only**. Shaped exactly like what a real
    narrative-analysis pipeline would return, so wiring in real data later
    means changing these functions, not the templates or JS.
  - `plot_theme.py` — single source of truth for chart colors/fonts/
    layout, consumed by `static/js/newslens.js` on the client.
- `templates/` — `base.html` (shell + intro animation), `partials/`
  (sidebar, header), `dashboard/*.html` (one template per page).
- `static/css/newslens.css` — the design-system CSS Tailwind's utility
  classes don't cover: nav states, panels, badges, cards, the intro
  animation keyframes, and the button hover-fill effect.
- `static/js/newslens.js` — the intro sequence, sidebar toggle, toast
  helper (`window.NLShowToast`), and every `Plotly.newPlot(...)` call.

## Pages

| Page | Route | What it shows |
|---|---|---|
| Overview | `/` | KPI strip, narrative landscape, "same event" cards, fingerprint radar, emotional signal, topic donut, entity table, evolution line, divergence metric, recent events |
| Articles | `/articles/` | Full article table with **client-side** search/source/event/sentiment/topic filtering (no backend call — all done in `articles.html`'s inline JS against the rows already on the page) |
| Compare | `/compare/?event=<slug>` | Source comparison matrix + narrative fingerprint radar + narrative differences, swappable across 3 demo events via the dropdown (`?event=climate-summit`, `india-budget`, `ai-regulation`) |
| Analysis | `/analysis/` | Single-article deep dive: entities, keywords, emotion distribution, framing indicators, and a demo SHAP-style explainability chart |
| Narrative Trends | `/trends/` | Framing-shift timeline, semantic-similarity-over-time, and sentiment-shift charts, with filter dropdowns (UI only — see Scope) |
| Settings | `/settings/` | Profile form, notification toggles, read-only pipeline info — submit shows a toast, nothing is persisted |
| Profile | `/profile/` | Avatar, stats, bio, recent-activity feed |

## The intro animation

On first load, `#intro-overlay` in `base.html` covers the screen while
`static/js/newslens.js` reveals the "NewsLens" wordmark letter by letter
(staggered opacity/blur/translate), then fades the tagline in, then fades
the overlay out while the dashboard (`#app-shell`) scales/fades in
underneath. Total runtime is ~2.3s.

By default it only plays **once per browser tab** (`sessionStorage`), so
navigating between pages afterward is instant — only a fresh tab/session
replays it. To make it replay on every page load (handy while demoing),
open `static/js/newslens.js` and flip:

```js
var INTRO_ONCE_PER_SESSION = true; // set to false
```

## The button "fill on hover" effect

Nav links, the header buttons, and a few page buttons use `.btn-fill`
(see `newslens.css`): a color sweep expands from the left edge behind the
label when the cursor enters. Three variants are layered on top of it —
add whichever fits a given button:

- `.btn-fill-accent` — sweeps in solid accent blue, text flips dark (used where the button itself isn't already accent-colored)
- `.btn-fill-light` — sweeps a translucent white overlay (used on buttons that already have a solid accent background, like "Analyze Article")
- `.btn-fill-subtle` — sweeps a faint accent tint, text turns accent-colored (used on sidebar nav links and ghost buttons)

## Why charts are built client-side

The Python `plotly` package isn't a dependency here — `services.py`
returns plain Python data structures, and `newslens.js` renders them with
Plotly.js (loaded from a CDN). `plot_theme.py` still centralizes every
chart's design tokens; each view serializes it into the page once, and
every chart function in `newslens.js` reads from that same object.

## Scope / known limitations

- **All data is hardcoded.** Every number and chart across all seven
  pages is hand-written demo data in `services.py`, shaped the way a real
  NLP pipeline's output would be shaped — none of it is a real research
  finding.
- **No real backend actions.** "Analyze Article," Settings' "Save
  changes," Profile's "Edit profile," and Articles' row clicks all show a
  toast rather than doing something real — they're UI-complete stubs for
  a future backend.
- **Compare's event switcher** is real (a GET param swapping between 3
  hardcoded datasets); **Trends' filter dropdowns** are UI-only and don't
  currently change the charts, since there's only one hardcoded time
  series today — wire them up once there's more than one to switch
  between.
