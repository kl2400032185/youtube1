# Rankroom · GATE CS 2027

A static, interactive preparation dashboard for the GATE Computer Science syllabus supplied in the brief.

## What is included

- A complete 10-section syllabus checklist with **must know**, **high yield**, and **build next** priorities.
- High-yield question archetypes and solving lenses for every section.
- A four-phase preparation playbook: coverage, retrieval, mixed timed practice, and mock refinement.
- Coverage and question-pattern progress tracking saved locally in the browser.
- Search, filters, keyboard navigation, answer reveals, and a mock-analysis loop.

The question bank is deliberately framed as recurring question shapes rather than guaranteed predictions. Confirm the official GATE 2027 brochure, syllabus, dates, and any exam-pattern details through the organizing institute before making final scheduling decisions.

## Run locally

This is a dependency-free static site. From the repository root:

```bash
python3 -m http.server 4173 --bind 0.0.0.0
```

Then open `http://localhost:4173`.
