# GATE 2027 CS/IT — Subject-wise PYQ Books (Edition 2)

13 subject books + General Aptitude + master index. Every PDF is A4, printable, with a
clickable TOC, headers/footers and page numbers.

## Deliverables (in `gate2027_pdfs/`)

| File | Subject | Qs in appendix | Pages |
|---|---|---|---|
| `00_MASTER_INDEX_GATE_2027.pdf` | Master index + 100% coverage audit | — | 2 |
| `01_Programming_and_Data_Structures.pdf` | Programming & Data Structures | 132 | 27 |
| `02_Algorithms.pdf` | Algorithms | 68 | 19 |
| `03_Discrete_Mathematics.pdf` | Discrete Mathematics | 98 | 22 |
| `04_Engineering_Mathematics_Linear_Algebra.pdf` | EM — Linear Algebra | 31 | 12 |
| `05_Engineering_Mathematics_Probability_and_Statistics.pdf` | EM — Probability & Statistics | 31 | 12 |
| `06_Engineering_Mathematics_Calculus.pdf` | EM — Calculus | 14 | 10 |
| `07_Digital_Logic.pdf` | Digital Logic | 70 | 15 |
| `08_Computer_Organization_and_Architecture.pdf` | COA | 109 | 20 |
| `09_Operating_Systems.pdf` | Operating Systems | 82 | 18 |
| `10_Theory_of_Computation.pdf` | Theory of Computation | 98 | 20 |
| `11_Computer_Networks.pdf` | Computer Networks | 89 | 19 |
| `12_Databases_(DBMS).pdf` | Databases (DBMS) | 71 | 18 |
| `13_Compiler_Design.pdf` | Compiler Design | 42 | 13 |
| `14_General_Aptitude_GATE_2027.pdf` | General Aptitude (4 official sections) | 170 | 32 |
| `00_EXHAUSTIVE_PYQ_Inventory.csv` | All 1,105 questions, machine-readable | 1,105 rows | — |
| `00_COVERAGE_AUDIT.txt` | Per-paper + per-subject reconciliation | — | — |

## Coverage

All **17 supplied GATE CS papers, 2016–2026** (Set-1/Set-2 where applicable) = **1,105 questions
(935 CS + 170 GA)**, i.e. 17 × 65, with none dropped. Each book ends with a **COMPLETE QUESTION
BANK** appendix containing the full statement, options, year/set, marks, type, official answer key
and source page for every question of that subject.

Because each question is listed exactly once across the set, the per-book counts add to exactly
1,105 — the master index shows that reconciliation.

## Pipeline

```
src/extract_pyqs.py    # PyMuPDF text layer + OCR (rapidocr) for image-only papers -> data/questions.json
src/consolidate.py     # align to official answer keys, clean text, classify subject -> data/final_questions.json
src/build_all.py       # build the 13 subject books + GA book
src/build_extras.py    # master index, CSV inventory, audit file
src/generator.py       # reportlab layout engine
```

Rebuild everything with:

```bash
python3 src/extract_pyqs.py && python3 src/consolidate.py && python3 src/build_all.py && python3 src/build_extras.py
```

## Source and limits

Source papers: `kl2400032185/STUDY-need` (18 files, 17 papers, 2016–2026) with official answer keys.

* 2017 and 2020 question papers are image-only; their text was recovered by OCR and is flagged in
  every affected entry.
* 1 stem (2021 Set-2, Q47) could not be recovered from the scan; it is still listed with its answer
  key and a pointer to the source page.
* Figures, tables and circuit diagrams are not redrawn — each affected question says so.
* Pre-2016 papers (1991–2015) are not in the supplied repository and are therefore absent.
