#!/usr/bin/env python3
"""Render the standalone Python course's Markdown source modules as nested HTML lessons."""
from __future__ import annotations

import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "python-course" / "source"
LESSONS = ROOT / "python-course" / "chapters"

MODULES = [
    ("01-python-logic.md", "Advanced Python Logic & Data Wrangling", [
        ("01-domain-logic.html", "Model the domain before the endpoint"),
        ("02-control-flow-boundaries.html", "Wrangle CSV/JSON safely and cross the repository boundary"),
        ("03-data-wrangling.html", "Make processing transactional, observable, and deployable"),
    ]),
    ("02-scripting.md", "Robust Scripting, Files & Automation", [
        ("04-cli-configuration.html", "Contract-first CLI, configuration, and durable file intake"),
        ("05-durable-file-pipelines.html", "Safe local subprocesses and authorized SSH/SFTP automation"),
        ("06-remote-automation.html", "Queue boundaries, operational deployment, and production promotion"),
    ]),
    ("03-integrations.md", "Web Scraping, APIs & Browser Automation", [
        ("07-http-api-clients.html", "HTTPX API clients, schemas, pagination, and safe retries"),
        ("08-responsible-scraping.html", "API-first responsible scraping with policy checks and selector parsing"),
        ("09-playwright-automation.html", "Authorized Playwright workflows and production queue boundaries"),
    ]),
    ("04-queues.md", "Asyncio, Scheduling & Background Queues", [
        ("10-asyncio-concurrency.html", "Async foundations: event loops, cancellation, and backpressure"),
        ("11-celery-scheduling.html", "Choosing a scheduler: cron, in-process jobs, and durable background work"),
        ("12-durable-job-operations.html", "Celery in production: broker, workers, Beat, and reliable task boundaries"),
    ]),
    ("05-deployment.md", "Containers, Linux, Monitoring & Security", [
        ("13-linux-systemd-deployment.html", "Linux foundations and a reliable local service"),
        ("14-docker-cloud-deployment.html", "Containers and the API/PostgreSQL/Redis/worker/Beat layout"),
        ("15-observability-security-launch.html", "VPS production runbook: TLS, observability, security, backups, and release safety"),
    ]),
]

ALL_LESSONS = [(file, title, module_title) for _, module_title, lessons in MODULES for file, title in lessons]


def split_chapters(text: str, source_name: str):
    matches = list(re.finditer(r"(?m)^##\s+Chapter\s+(\d+)\s*[:—–-]\s*(.+?)\s*$", text))
    if len(matches) != 3:
        raise ValueError(f"{source_name}: expected exactly 3 chapter headings, found {len(matches)}")
    chapters = []
    for i, match in enumerate(matches):
        body_start = match.end()
        while body_start < len(text) and text[body_start] in "\r\n":
            body_start += 1
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = re.sub(r"\s+", " ", match.group(2)).strip()
        chapters.append((title, text[body_start:body_end].strip()))
    return chapters

def parse_reference_definitions(text: str) -> dict[str, tuple[str, str]]:
    pattern = re.compile(r'(?m)^\[(\d+)\]:\s*(\S+)(?:\s+"([^"]*)")?\s*$')
    return {m.group(1): (m.group(2), m.group(3) or m.group(2)) for m in pattern.finditer(text)}


def make_sidebar(current: str) -> str:
    parts = ['<div class="rail-label">Python · 15 chapters</div>', '<a href="../../index.html"><span class="rail-number">⌂</span>Workshop home</a>', '<a href="../index.html"><span class="rail-number">◎</span>Python course map</a>']
    for i, (filename, title, module) in enumerate(ALL_LESSONS):
        if i % 3 == 0:
            parts.append(f'<div class="rail-label">Module {i // 3 + 1} · {html.escape(module)}</div>')
        attrs = ' aria-current="page"' if filename == current else ''
        parts.append(f'<a href="{filename}"{attrs}><span class="rail-number">{i + 1:02d}</span>{html.escape(title)}</a>')
    return "\n".join(parts)


def render_chapter(i: int, title: str, body_md: str, module_title: str,
                   references: dict[str, tuple[str, str]]) -> str:
    filename = ALL_LESSONS[i][0]
    previous = ALL_LESSONS[i - 1] if i > 0 else None
    following = ALL_LESSONS[i + 1] if i + 1 < len(ALL_LESSONS) else None
    renderer = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists", "toc"])
    body_md = re.sub(r"(?ms)^##\s+References\s*.*\Z", "", body_md).strip()
    capstone = re.search(r"(?im)^(?:#{2,6}\s+[^\n]*(?:hands-on|capstone|build step)[^\n]*|\*\*Hands-on build[^\n]*)", body_md)
    if capstone:
        body_md = body_md[:capstone.start()] + '<span id="capstone-step"></span>\n\n' + body_md[capstone.start():]
    else:
        body_md += '\n\n<span id="capstone-step"></span>'
    used_references = sorted(set(re.findall(r"\[(\d+)\](?!:)", body_md)), key=int)
    definitions = "\n".join(
        f'[{number}]: {url} "{reference_title.replace(chr(34), chr(39))}"'
        for number, (url, reference_title) in references.items()
    )
    body_html = renderer.convert(body_md + "\n\n" + definitions)
    # Give external references safe new-tab behavior; internal lesson links stay in the course.
    body_html = re.sub(r'<a href="(https?://[^"]+)"([^>]*)>',
                       r'<a href="\1" target="_blank" rel="noopener noreferrer"\2>', body_html)
    reference_items = []
    for number in used_references:
        if number in references:
            url, reference_title = references[number]
            reference_items.append(
                f'<li id="ref-{number}"><a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">'
                f'{html.escape(reference_title)}</a></li>'
            )
    references_html = (f'<section class="course-references" id="references"><h2>References</h2><ol>{"".join(reference_items)}</ol></section>'
                       if reference_items else "")
    prev_link = (f'<a href="{previous[0]}"><small>Previous lesson</small><strong>← {html.escape(previous[1])}</strong></a>'
                 if previous else '<a href="../index.html"><small>Python course</small><strong>← Python course map</strong></a>')
    next_link = (f'<a href="{following[0]}"><small>Next lesson</small><strong>{html.escape(following[1])} →</strong></a>'
                 if following else '<a href="../index.html#capstone"><small>Finish the Python course</small><strong>Return to the capstone map →</strong></a>')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Chapter {i + 1}: {html.escape(title, quote=True)}. A practical Python backend and automation lesson with code, deployment context, resilience, and a capstone build step.">
<title>{i + 1:02d} — {html.escape(title)} · Python Backend &amp; Automation</title>
<link rel="icon" href="../../assets/course-mark.svg" type="image/svg+xml">
<script>(()=>{{let saved=null;try{{saved=localStorage.getItem("app-workshop-theme");}}catch{{}}const theme=saved==="dark"||saved==="light"?saved:(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light");document.documentElement.dataset.theme=theme;}})();</script>
<link rel="stylesheet" href="../../assets/site.css"></head>
<body data-track="python" data-chapter="python-{i + 1:02d}"><a class="skip-link" href="#main">Skip to lesson</a>
<header class="topbar"><div class="topbar-inner"><a class="brand" href="../../index.html"><img src="../../assets/course-mark.svg" alt=""><span>App Builder’s Workshop</span></a><nav class="topnav" aria-label="Main navigation"><a href="../index.html">Python course map</a><a href="../../index.html">Tauri course</a><button class="theme-toggle" type="button" data-theme-toggle aria-pressed="false">Dark mode: off</button></nav></div></header>
<div class="reading-progress" aria-hidden="true"><span data-reading-progress></span></div>
<main id="main" class="layout"><aside class="rail" aria-label="Python lesson navigation">{make_sidebar(filename)}</aside><div class="main">
<div class="crumbs"><a href="../../index.html">App Builder’s Workshop</a> / <a href="../index.html">Python course</a> / Chapter {i + 1:02d}</div>
<header class="lesson-header"><div class="eyebrow">Python Backend &amp; Automation · Module {i // 3 + 1}: {html.escape(module_title)}</div><h1>{html.escape(title)}</h1><p class="lead">This chapter connects practical Python/backend techniques to the capstone data-intake service. Work through the objectives, run the code locally, and then compare the operational notes before adapting the pattern to production.</p><div class="lesson-meta"><span>Chapter {i + 1:02d} of 15</span><span>Concepts · code · deployment · resilience · build</span></div></header>
<div class="lesson-tools"><a href="#lesson-content">Jump to lesson</a><a href="#capstone-step">Jump to capstone step</a><span>Use the references at the end to go deeper.</span></div>
<article id="lesson-content" class="lesson-content backend-lesson">{body_html}{references_html}</article>
<button class="mark-complete" type="button" data-complete aria-pressed="false">Mark this chapter complete</button>
<nav class="lesson-nav" aria-label="Previous and next lessons">{prev_link}{next_link}</nav>
</div></main><footer class="footer"><a href="../index.html">Python Backend &amp; Automation</a> · <a href="../../index.html">App Builder’s Workshop</a> · Progress is local to this browser.</footer><script src="../../assets/site.js" defer></script></body></html>'''


def main():
    LESSONS.mkdir(parents=True, exist_ok=True)
    rendered = 0
    global_index = 0
    for source_name, module_title, lesson_meta in MODULES:
        source_path = SOURCE / source_name
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        source_text = source_path.read_text(encoding="utf-8")
        chapter_content = split_chapters(source_text, source_name)
        module_references = parse_reference_definitions(source_text)
        if len(chapter_content) != len(lesson_meta):
            raise ValueError(f"Lesson count mismatch in {source_name}")
        for (reported_title, body_md), (filename, fallback_title) in zip(chapter_content, lesson_meta):
            title = reported_title or fallback_title
            page = render_chapter(global_index, title, body_md, module_title, module_references)
            (LESSONS / filename).write_text(page, encoding="utf-8")
            global_index += 1
            rendered += 1
    print(f"Rendered {rendered} Python course lesson pages into {LESSONS}")


if __name__ == "__main__":
    main()
