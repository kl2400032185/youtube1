# GATE 2027 CS/IT — Subject-wise PYQ Books (Edition 3)

13 subject books + General Aptitude + master index. Every PDF is A4, printable, with a
clickable TOC, headers/footers and page numbers.

Pedagogy per book: syllabus-mapped topics → revision capsule → worked PYQs (full statement, all
options, year/set, marks, type, official answer, teaching solution) → analytics → practice test →
formula sheet → rapid-revision sheet → **COMPLETE QUESTION BANK appendix** containing *every*
question of that subject from all supplied papers.

## Deliverables (in `gate2027_pdfs/`)

| File | Subject | Qs in appendix | Pages |
|---|---|---|---|
| `00_MASTER_INDEX_GATE_2027.pdf` | Master index + full-coverage audit | — | 2 |
| `01_Programming_and_Data_Structures.pdf` | Programming & Data Structures | 174 | 32 |
| `02_Algorithms.pdf` | Algorithms | 93 | 21 |
| `03_Discrete_Mathematics.pdf` | Discrete Mathematics | 134 | 25 |
| `04_Engineering_Mathematics_Linear_Algebra.pdf` | EM — Linear Algebra | 44 | 13 |
| `05_Engineering_Mathematics_Probability_and_Statistics.pdf` | EM — Probability & Statistics | 41 | 13 |
| `06_Engineering_Mathematics_Calculus.pdf` | EM — Calculus | 26 | 11 |
| `07_Digital_Logic.pdf` | Digital Logic | 93 | 17 |
| `08_Computer_Organization_and_Architecture.pdf` | COA | 149 | 24 |
| `09_Operating_Systems.pdf` | Operating Systems | 110 | 21 |
| `10_Theory_of_Computation.pdf` | Theory of Computation | 117 | 22 |
| `11_Computer_Networks.pdf` | Computer Networks | 126 | 22 |
| `12_Databases_(DBMS).pdf` | Databases (DBMS) | 98 | 21 |
| `13_Compiler_Design.pdf` | Compiler Design | 56 | 14 |
| `14_General_Aptitude_GATE_2027.pdf` | General Aptitude (4 official sections) | 230 | 40 |
| `00_EXHAUSTIVE_PYQ_Inventory.csv` | All 1,495 questions, machine-readable | 1,495 rows | — |
| `00_COVERAGE_AUDIT.txt` | Per-paper + per-subject reconciliation | — | — |

## Coverage

All **23 supplied GATE CS papers, 2014–2026** (Set-1/Set-2/Set-3 where applicable) =
**1,495 questions (1,265 CS + 230 GA)**, i.e. 23 × 65, with **none dropped** — `00_COVERAGE_AUDIT.txt`
reports `Unrecovered stems: 0`. Each book ends with a **COMPLETE QUESTION BANK** appendix containing
the full statement, options, year/set, marks, type, official answer key and source page for every
question of that subject.

Because each question is listed exactly once across the set, the per-book counts add to exactly
1,495 (1,265 CS across 13 books + 4 out-of-syllabus legacy items shown as an `Other` row in the
index, plus 230 GA) — the master index shows that reconciliation.

## Pipeline

```
src/legacy_keys.py     # 2014 text-row + 2015 green-tick OCR answer-key parser -> data/keys_legacy.json
src/extract_pyqs.py    # PyMuPDF text layer + OCR (rapidocr) for image-only papers -> data/questions.json
src/consolidate.py     # align to official answer keys, clean text, classify subject -> data/final_questions.json
src/build_all.py       # build the 13 subject books + GA book
src/build_extras.py    # master index, CSV inventory, audit file
src/generator.py       # reportlab layout engine
```

Rebuild everything with:

```bash
python3 src/legacy_keys.py && python3 src/extract_pyqs.py && python3 src/consolidate.py \
  && python3 src/build_all.py && python3 src/build_extras.py
```

## Source and limits

Source papers: `kl2400032185/STUDY-need` (23 papers, 2014–2026) with official answer keys.

* The 2015 papers use section-local numbering (GA 1–10, CS 1–55) that does not follow the official
  order, so their blocks are matched to the answer-key question texts by content similarity
  (de-glued word + character n-gram cosine, greedy assignment with swap refinement) instead of by
  printed label.
* 2015, 2017 and 2020 question papers are image-only; their text was recovered by OCR, repaired and
  flagged in every affected entry.
* Four stems the OCR had dropped (2015 Set-1 Q24, Q30; 2015 Set-2 Q7, Q14; 2021 Set-2 Q28) were
  transcribed from the page images into `data/stem_overrides.json` — they are marked as recovered in
  the CSV, and the audit reports zero unrecovered stems.
* Figures, tables and circuits are not redrawn — each affected question says so and points to the
  source page.
* Papers before 2014 are not in the supplied repository and are therefore absent.
