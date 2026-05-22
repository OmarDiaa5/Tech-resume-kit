# Antigravity Ruleset — Optimized Custom Instructions

This file is a high-density, consolidated ruleset optimized for Google Antigravity. It merges all layout, formatting, LaTeX, and anti-fabrication constraints to prevent loading multiple massive files into the chat context.

---

## 1. Safety & Anti-Fabrication Rules (MANDATORY)

**Priority Hierarchy: Accuracy > Relevance > Impact > ATS > Brevity**

* **Provenance Discipline**: 
  * Read `config.md` Provenance Flags before every run.
  * NEVER claim unpublished work is published.
  * NEVER claim internal tools are peer-reviewed.
  * NEVER inflate author position (contributing does not equal first author).
  * NEVER claim results from collaborators' experiments as your own.
* **Verb Discipline**:
  * **Full-ownership verbs** (Developed, Built, Engineered, Designed) ONLY for work performed independently.
  * **Hedged verbs** (Contributed, Provided, Supported) for shared or contributing-author work. When in doubt, hedge.
* **No Fabrications**: Source ALL bullet content from `resume_builder/experience/` files.
* **Metric Discipline**: NEVER include lines-of-code counts or test counts. Focus on what the tool does, its impact, and adoption.

---

## 2. Character Limits & Layout Budgets

All character limits are based on rendered characters (LaTeX markup stripped). The automated linter (`.agents/helpers/verify_build.py`) is the authoritative source.

### Resume (10pt, textwidth=7.5in)
* **Target Layout**: 2-page resume. ALL variable bullets must be **strictly 2 lines (2L)**.
* **Bullet Limits**:
  * Target Range: **189-205 chars**
  * HARD MAX: **218 chars** (with a bold-width penalty reduction)
  * Orphan Threshold: Last line MUST be $\ge 78$ characters (fills $\ge 70\%$ of the line).

### CV (11pt, textwidth=7.5in)
* **Target Layout**: 5-page CV. Mix of 2L and 3L bullets is OK.
* **Bullet Limits**:
  * **1L**: 88-93 chars (HARD MAX: 101)
  * **2L**: 168-182 chars (HARD MAX: 190, Orphan threshold $\ge 65$ chars)
  * **3L**: 250-268 chars (HARD MAX: 280, Orphan threshold $\ge 65$ chars)
* **CV Page 1 Rule**: First bullet of the first experience position MUST be 2L (3L overflows page 1).

### Bold Width Penalty Formula
* **Resume (10pt)**: Effective Limit = $119 - (0.5 \times \text{bold\_char\_count})$ per line.
* **CV (11pt)**: Effective Limit = $91 - (0.25 \times \text{bold\_char\_count})$ per line.

---

## 3. LaTeX Scientific Notation Rules

The template loads `mhchem` (`\usepackage[version=4]{mhchem}`). Use these exact conventions:

| Item | Correct LaTeX | Wrong | Rendered |
| :--- | :--- | :--- | :--- |
| Chemical formulas | `\ce{H2O}`, `\ce{TiO2}` | `H2O`, `H$_2$O` | H₂O, TiO₂ |
| Superscripts / Labels | `$^2$`, `$^\circ$C`, `R$^2$=0.99` | `^2`, `°C`, `R2` | ², °C, R² |
| Greek letters | `$\beta$`, `$\alpha$-phase` | `beta`, `alpha-phase` | β, α-phase |
| Approximately | `$\sim$64` | `~64` (LaTeX non-breaking space!) | ~64 |

* **CRITICAL**: In LaTeX, `~` is a non-breaking space, NOT a tilde. Always use `$\sim$` for "approximately".

---

## 4. AI Fingerprint & Banned Jargon

* **Banned Buzzwords**: *spearheaded, leveraged, revolutionized, synergized, passionately, successfully, played a key role, dramatically*.
* **Preferred Verbs**: *Developed, Built, Engineered, Designed, Implemented, Streamlined, Integrated, Quantified, Formulated*.
* **Folder Names**: NEVER use internal code folder names (e.g. `FEM_project/`) as software packages. Describe the tool (e.g. "custom FEM solver").

---

## 5. Execution Guidelines for Antigravity

* **Do NOT open** `resume_builder/reference/resume_reference.md` or `resume_builder/reference/critique_framework.md` in the chat thread unless verifying extremely complex multi-column table LaTeX packages.
* **Run automated verification**: Propose and run `.agents/helpers/verify_build.py` after editing or generating a `.tex` file. 
* **Save intermediate output**: Write bullet planning strategies and draft critiques as **persistent Markdown Artifacts** rather than dumping large text in the chat, keeping conversation history extremely lean.
