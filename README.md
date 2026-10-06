# App Builder’s Workshop

A dependency-free, static, multi-page learning course for beginning a Tauri + React + FastAPI + SQLite desktop app project.

## Run locally

From the project directory:

```bash
python3 -m http.server 3000 --bind 0.0.0.0
```

Open `http://127.0.0.1:3000/` locally. The Manus Preview is configured on port 3000. Use a static server rather than opening the HTML files directly so chapter links and browser storage behave consistently.

## Contents

- `index.html` — the course map and prerequisites.
- `chapters/` — complete, linked lessons.
- `assets/site.css` — shared accessible styling.
- `assets/site.js` — local chapter progress, reading progress, and home-page filtering.
- `manus-routes.json` — route declaration required by the Webdev preview workflow.
- `plan.md` and `TODO.md` — approved design/implementation notes and project outcome tracker.

The course itself has no backend and stores only optional completion checkmarks in local browser storage. The desktop architecture examples are educational; in particular, a packaged FastAPI sidecar needs deliberate lifecycle, local networking, and security design. See Chapter 10 before selecting an architecture.
