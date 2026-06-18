# Resume & CV Generation — Reference

> Resume rules. Read by `/make-resume` and `/edit-resume`. **Single source of truth for character limits** (the only other authority is `char_count.py`, which enforces them).
> Companion files: `cl_reference.md` (CL rules, opt-in), `cv_reference.md` (5-page CV, load only if a CV is requested).
> Shared rules (provenance, anti-fabrication, LaTeX notation): `CLAUDE.md`

---

## QUICK BUDGET CARD (read this FIRST)

```
RESUME (1-page): ~6-8 variable bullets | Skills 4 lines (compact) | Certs 3-4 | Leadership 1
RESUME (2-page): ~12-20 variable bullets | Skills 13 lines (4-3-2-2-2) | Certs 3-4 | Leadership 1

Resume bullet: max 2 rendered lines | 1L: 105-111 chars | 2L: 189-205 chars (target ~200)

Cover letter (ONLY if /make-cl was run): 1 page, 250-300 words.
```

**Page & variant selection (DEFAULT — decide this BEFORE planning bullets):**
- **Intern / trainee / new-grad / summer / student JD → 1 page, 1L bullets by default.** This is the common case. Reserve 2L for only the 1–2 strongest bullets, and only if the page still has room. Skills = 4-line compact. ~6–9 variable bullets. On a 1-page resume, **omit the Summary block** (the tagline carries it) — see Summary spec.
- **Mid/senior role, or when the content genuinely earns a second page → 2 pages, 2L by default.** Skills = Format C (13 lines). ~12–20 bullets.
- A **user directive always wins** ("make it 2-page", "make this one a 2L"). Don't mark every bullet 2L by reflex — pick the variant from the page target.
- **We cannot compile the `.tex` or see where pages break or lines orphan.** On a 1-page target, estimate line count *conservatively* and prefer cutting a bullet or dropping a 2L→1L over risking a spill. A resume that claims "1 page" but compiles to 2 pages with an orphaned section is the single biggest score-killer (it can cost several points in critique). When borderline, under-fill.

Sections, in order: (Experience — internship, FIXED) → Projects → Competitions & Hackathons → Technical Skills → Education (FIXED) → Certifications (FIXED) → Leadership (FIXED) → Languages (FIXED). **No Publications section** — this is a tech resume.

**If your bullet count doesn't match the budget above, STOP and fix before generating.**

> Generating a 5-page CV instead? Stop and load `cv_reference.md` — its budgets/char-limits differ. Resume is the default; only switch on an explicit CV request.

---

## Section-by-Section Specs

**Dates (all sections — projects, internships, competitions, certifications):** Copy verbatim from the corresponding extraction file's `Date:` field. If absent: STOP, ask the user, then backfill the extraction file before proceeding. NEVER infer or guess a year range from context.

**Project section ordering — MANDATORY:** List projects in reverse chronological order (most recent date first). If two projects share the same month, order by: (1) JD relevance (more relevant first), then (2) depth/complexity (more substantial first). Never arrange by bundle priority alone — historical order is the primary sort key and makes resume dating credible and consistent.

**One project = one rSubsection — MANDATORY:** Each distinct project gets its own `rSubsection`. Never group two separate projects under one shared sub-theme header. Sub-theme headers name a *single* project's angle — they do not collapse multiple projects.

**In-development projects — MANDATORY:** If a project's extraction marks status as IN PROGRESS or the end date is in the future, set arg 3 to `{\em <Program> --- In Development}` and use `Present` as the end date. This explains absent final metrics without apology. Do NOT claim deployment or completion.

**Project context-label rule — MANDATORY:** Never put generic context labels like `{\em University Team Project}` or `{\em Independent}` in the rSubsection's third argument. They consume vertical space without conveying signal — the reader already assumes student work absent contrary context.
- **1-page resume:** set arg 3 to `{}` (no italic line). Use the reclaimed space either for an additional useful bullet on that project, or to fit one more project entry.
- **Multi-page CV:** if the project was the deliverable for a course/certification (e.g., the HCIA capstone), don't list it as a standalone project with a generic tag — render it as a bullet under that course/cert entry instead.
- **Dataset or concrete affiliation IS useful** and may stay (e.g., `{\em IBM Telco Dataset}`, `{\em Kaggle Competition --- Top 5\%}`). The ban is on filler-only labels.


### Resume (resume.cls)

1. **Summary** (bundle Section 2): 4-5 sentences, exactly 5 body lines. 500-555 rendered chars (HARD MAX 570, floor ~490). Orphan: last line >= 78 chars.
   - **1-page resume: OMIT the Summary block entirely** — the tagline carries the positioning and you reclaim ~5 lines for bullets. Summary is a 2-page-only section.
   - **Headline Tagline:** 80-95 rendered chars, exactly 1 line. (Kept on both 1- and 2-page resumes.)
2. **Technical Skills** (bundle Section 4 + skills_taxonomy.md): **2-page** → Format C, 5 groups, 4-3-2-2-2 (13 lines); **1-page** → 4-line compact. Each dash = exactly 1 rendered line. Bold penalty: 119 - (0.5 x bold_chars).
3. **Experience & Projects** (experience files + achievement_reframing_guide.md): Write bullets FRESH per Experience Bullet Writing Protocol (below). Your primary internship/role is typically a FIXED experience entry; projects are JD-selected. Max 2 rendered lines per bullet. Run char_count.py after each section.
   - resume.cls: Args 3+4 on SAME italic line
   - **After all positions: verify total variable bullet count matches budget**

**No-duplication rule (applies to every project/experience/competition subsection):** The title, italic subtitle, and bullets must each carry *different* information. Do not repeat the model name, dataset, or technique in both the title and a bullet — if "XGBoost + SMOTE on IBM Telco" is in the title, the bullet cannot also lead with "Built XGBoost pipeline on IBM Telco." Allocate roles instead: **title** = problem domain + distinguishing angle (e.g., "Telecom Retention with Imbalance Handling"); **bullet** = specific model + dataset size + quantified result. Each line earns its space by adding new information.

4. **Competitions & Hackathons** (experience_competitions.md): reverse-chronological. Title = `Domain Project --- Competition (Nth Place)`; subtitle = `Institution --- Competition Name`. Surface the business/technical KPI.
5. **Education**: FIXED — copy from template. **NEVER include a "Relevant Coursework" line unless the user explicitly asks.** Default = degree + institution + GPA only.
6. **Certifications & Training**: FIXED list — Tier-1 compact (see Certifications Section Format below). Brand-led, date last on the right.
7. **Leadership & Activities**: FIXED — items from template.
8. **Languages**: FIXED — copy from template.

> 5-page academic **CV**? Those section specs (Research Summary, Technical Expertise, Fellowships, Presentations, etc.) live in `cv_reference.md` — load it only on an explicit CV request.

---

## Certifications Section Format

Certs are scan-fodder: the big-name brand is what HR registers in one glance. Projects and Skills carry the technical weight — don't duplicate cert details there. Default to compact Tier 1; escalate to Tier 2 only when the resume has confirmed vertical room and the extra detail earns its place.

### Tier 1 — Compact (default, 1 line per cert)
```latex
\textbf{<Famous Brand: Short Cert Name>} --- <Provider/Issuer> \hfill {\textcolor{black!60}{<date>}}
```
Rules:
- Lead with the **big-name brand** (IBM, NVIDIA, Microsoft, Huawei). That's the scan target.
- **Date is the last element on the right**, right-aligned via `\hfill`, matching every other section (Experience, Projects, Education). Nothing comes after the date.
- Short cert name only. No skill lists, no hours, no "(Coursework — 8/12)", no curriculum tail.
- Score is omitted by default. If a score is impressive AND there is real room, attach it to the brand in the title (e.g., `Huawei HCIA-AI V4.0 (98\%)`) — never after the date, never on a different cred than the one it was earned on.
- Cert names may be **rephrased / shortened** per JD relevance (e.g., "NVIDIA DLI: LLM Applications" vs "NVIDIA DLI: Generative AI" vs the full Coursera title).

### Tier 2 — Full block (only when room earns it)
```latex
\textbf{<Full Canonical Title>} \hfill {\textcolor{black!60}{<date range>}}\\
<Issuer> | <Status/Score/Hours> | <Key skills>
```

### Conventions (both tiers)
- **Date format:**
  - Both start AND end date: `Mon YYYY -- Mon YYYY`
  - Single point / under a month: `Mon YYYY`
  - Last resort (tight overflow): end date alone, `Mon YYYY`
  - Never include the day.
- **Order: reverse-chronological by end date** (newest first). In-progress items use `Present` as the effective end and sort to the top. This rule applies to **both certs and projects** for visual consistency.
- In-progress is shown by ending the date range with `Present` (e.g., `Nov 2025 -- Present`). Do **not** also add "(in progress)" — the `Present` date already says it; the parenthetical is redundant and wastes space.
- Partial completions (e.g., IBM 8/12): **omit the qualifier in Tier 1**; include only in Tier 2 when there is room.

### Canonical Naming Table (build your own)

Maintain your own version of this table from your real certifications. List in
reverse-chronological order — render in this order. The examples below show the
formatting rules, not real entries; replace them with yours.

| # | Left side (brand-led)                                    | Right side (date)   | Notes |
|---|----------------------------------------------------------|---------------------|-------|
| 1 | **[Track / Specialization]** — [Issuing Program]         | Mon YYYY – Present  | `Present` signals in-progress; no parenthetical. Spell out region-specific initiatives — a bare local acronym reads as noise to outside recruiters |
| 2 | **[Vendor Course, e.g. NVIDIA DLI]** — [Bootcamp/Provider] | Mon YYYY          | Title can flex per JD (e.g., Generative AI vs. Prompt Engineering & RAG) |
| 3 | **[Vendor Cert]** — [Co-issuer A] & [Co-issuer B]        | Mon YYYY – Mon YYYY | Use `\&` between co-issuers (not `$\times$`); a "(score%)" is optional on the vendor title only |
| 4 | **[Professional Certificate]** — [Platform]              | Mon YYYY -- Present | "(Coursework — N/M courses)" only in Tier 2 when partially complete; `Present` = in progress |

Source of truth: `knowledge_base/extractions/courses_certifications.md`. Bullet variants: `resume_builder/experience/experience_certifications.md`.

---

## Character Limits (HARD STOPS — ZERO TOLERANCE)

**DO NOT count characters in your reasoning.** Write the full draft, save to file, then run `python resume_builder/helpers/char_count.py -f [resume|cv] <path>`. The tool is the only authority on rendered char counts. Treat the target ranges below as bands the tool will check — not as values to compute mentally. Mental stripping of LaTeX markup is slow, error-prone, and burns tokens; the tool is fast and exact.

**Resume (10pt, textwidth=7.5in):**

| Target Lines | Rendered Char Range | HARD MAX | Orphan Threshold |
|-------|---------------|---------|------------------|
| 1 line | 105-111 chars | 117 | -- |
| 2 lines | 189-205 chars | 218 | Last line >= 78 chars |

> **AIM FOR THE MIDDLE OF THE TARGET RANGE — NOT THE HARD MAX.**
> A Resume-2L bullet should target ~200 chars, not 218. The hard max is a safety valve, not a target.
> Proportional fonts have variable char widths — a bullet at the hard max WILL overflow if it contains
> wide characters (m, w, W, capitals, em-dashes). Em-dash (---) counts as 1 char but renders ~2x wide;
> budget 2 extra chars per em-dash. `char_count.py` flags these as `COMPILE-RISK` — heed it.
>
> (CV-2L/3L limits live in `cv_reference.md`.)

### Variant Naming

| Variant | Document | Lines | Target Range | HARD MAX | Orphan | Word Target |
|---------|----------|-------|-------------|----------|--------|-------------|
| Resume-1L | 1/2-page resume | 1 | 105-111 | 117 | -- | ~13 words |
| Resume-2L | 2-page resume | 2 | 189-205 | 218 | >= 78 | ~23-25 words |

> **Word targets** are approximate first-draft heuristics for prose bullets (~7.9 chars/word). After drafting, always verify with precise char count. Skills dashes: NO word proxy -- use iterative char count only.

### Bold Width Penalty (COMPILE-VERIFIED)

Bold characters render wider than normal text. **Resume (10pt):** effective limit = 119 - (0.5 x bold_char_count).
- 0 bold: safe up to 119 chars/line
- 2-4 bold tools (~10-25 bold chars): 107-112 effective --> use 105-111 as default
- 5+ bold tools (~28+ bold chars): ~105 effective --> tighten to 99-105

`char_count.py` applies this penalty automatically and prints `COMPILE-RISK` when a within-tier bullet is likely to overflow due to bold/wide chars.

**Per-bullet enforcement protocol:**
1. Draft the bullet aiming for the middle of the target range (not the hard max).
2. Write the complete section to file.
3. Run `char_count.py` once on the file after the document (or section, if mid-edit) is saved. The tool reports violations.
4. **Aim for the middle of the range** during drafting, not the max. A bullet at 220 rendered chars (resume 2L) is risky — target ~200.

**Orphan rule (COMPILE-ONLY check):** For any multi-line bullet, the last rendered line must fill at least 70% of the line width (Resume-2L: last line >= 78 chars). **`char_count.py` cannot verify this** — it only knows the total char count, not where the line wraps. Confirm orphans by compiling and reading the PDF. If a last line is short, rewrite to fill it or shorten the bullet to one fewer line.

### Char Verification Protocol

Write the section. Run `python resume_builder/helpers/char_count.py -f [resume|cv] <path>` once on the saved file. If violations: ONE revision pass, re-run the tool, then accept or flag remaining over-limit lines with `% CHAR_VIOLATION: [N] chars, target [M]`. **No mental counting at any step.** The tool is fast and exact; mental counting is slow and wrong.

---

## Page Fill Budgets (Resume)

**1-page resume** (trainee/intern roles): drop the internship Experience block if space is tight; ~6-8 project/competition bullets, 4-line compact Skills, 3-4 certs, 1 leadership entry. Target a full page with <=3 lines white space.

**2-page resume:** Technical Skills uses Format C (categorized dash sub-items, 5 groups). The internship is a FIXED experience entry (its bullet is not counted in the variable budget).

**Variable Bullet Budget (Format C):** typically **12-20 variable bullets** across Projects + Competitions, depending on 1- vs 2-page and skills config. Count FIXED bullets (internship, leadership) separately.

**Adjustments:**
- Adding a skills line (e.g., 4-4-2-2-2 instead of 4-3-2-2-2): -1 variable bullet
- 1-page vs 2-page is the main lever — pick per JD seniority.

**Position header rule:** the position/project title + date must fit ONE line. If the title is too long, shorten it so the date doesn't wrap. Wrapped dates waste a vertical line and break alignment. Test by compiling.

**Page-fill verification:** compile and read the PDF. Resume: <=3 lines white space on the last page; no orphan section header alone at the top of page 2. Fix by shortening/adding VARIABLE content only (summary, skills dashes, project bullets).

> 5-page CV page budget (45 rendered lines, sub-theme rebalancing, CV Page-1 rule) lives in `cv_reference.md`.

---

## Experience Bullet Writing Protocol (Experience-File-First)

**DO NOT use pre-written bullets.** Write every bullet FRESH from experience files, reframed for the target JD.

**Required files:** Experience files (all) + achievement_reframing_guide.md + bundle Section 1 (Priority Matrix) + bundle Section 3 (Reframing Map)

**Protocol:**
1. Determine document format -> look up bullet variant (Resume-1L/2L; CV variants are in `cv_reference.md`) and budget
2. Allocate bullet count per position by JD relevance
3. For each position, consult bundle's **Priority Matrix** (Section 1) to rank achievements
4. For each achievement, consult **Achievement Reframing Guide** for role-type-specific framing directives
5. Write the bullet FRESH using target-domain vocabulary from bundle's **Reframing Map** (Section 3)
6. Verify char count per-bullet BEFORE moving to the next bullet
7. After all bullets written: run the **First-Pass Reframing Checklist** (in achievement_reframing_guide.md)

**Reframing during writing (NOT after):** Every bullet should use target-domain vocabulary from the start. Do not write in academic language and then "translate" -- write in target language directly using the Reframing Map. This is the single highest-ROI step: reframing alone moves scores from ~60 to ~85.

**Hybrid JDs (two role types):** Use primary role type's Priority Matrix for achievement ranking. Use secondary role type's Reframing Map for 1-2 bullets that bridge to the secondary domain.

---

## Position Title Format

**FLIPPED format (JD theme as bold title, role/context as subtitle):**
Bold line = JD-customized domain theme (the single most powerful JD customization lever).
Italic subtitle = formal role + organization, or `{}` for independent projects.

| Entry | Bold Line (JD-customizable) | Subtitle |
|----------|-----------------------------|----------|
| Internship | [Theme, e.g., "Edge ML \& Embedded Sensing"] | [Your Role, e.g. "Robotics Intern, Acme (FIXED)"] |
| Project | [Subject --- Method/Result angle, e.g., "Driver Monitoring System --- Real-Time Behavior Classification"] | `{}` for independent, or `{\em Org/Dataset}` |
| Competition | [Domain Project --- Competition (Nth Place)] | [Institution --- Competition Name] |

> CV conventional position format lives in `cv_reference.md` (only if a CV is requested).

---

## Immutable Elements — NEVER Modify

The following elements are set in the `.cls` files and templates. **NEVER change them in generated output:**

- **`\vspace` values** between sections — these are calibrated. Do not add, remove, or adjust.
- **`\geometry` settings** (margins, textwidth, textheight) — locked per template.
- **FIXED section content** (Education, Certifications, Leadership, Languages, Internship) — copy verbatim from template. Never rewrite, trim, or reorder.
- **`.cls` formatting** (font sizes, section rules, item separators, skill group spacing) — never override with inline LaTeX.
- **Header layout** (name, email, location, icons) — structure is template-locked. Only the email address and link URLs are configurable.

**If content spills to an extra page (orphan lines):** Fix by shortening VARIABLE content only (summary, skills dashes, project bullets). A bullet that is "2L" in the budget but renders as 3L due to character overflow is the most common cause of page spill. Before declaring any output done, compile with pdflatex and verify page count matches target (resume = 1 or 2 pages).

**When updating an existing .tex output (not generating from scratch):** Only modify VARIABLE content — summary text, skills group names/dashes, experience bullet text, sub-theme names. Never touch FIXED sections, vspaces, geometry, or cls overrides, even if a critique flags them as improvable. If a critique targets a FIXED section, note it for the next full regeneration instead.

---

## Post-Generation Verification

Run this checklist after compile gate passes, before critique. Also used as Part 7 of critique_framework.md.

Before presenting final output, verify:

- [ ] All mechanical checks pass (chars, orphans, page fill, sequences, variants)
- [ ] Em-dash count: max 2 per document. Leadership/Honors items use `. ` not `---`.
- [ ] No -ing analysis endings on bullets ("...advancing the field", "...contributing to Y"). Restructure to end with a concrete result or metric.
- [ ] All content checks pass (ATS, terms, inflation, provenance, cover letter if present)
- [ ] All narrative checks pass (scan test, per-section flow, cross-section arc)
- [ ] Company/institution name spelled correctly throughout
- [ ] .tex file has complete preamble (will compile standalone)
- [ ] Date format consistent (Mon YYYY -- Mon YYYY)

---

## Role-Type Decision Tree

The authoritative JD-keyword → role-type mapping lives in **`config.md` → Role-Type Decision Tree** (ML Engineer / CV Engineer / Data Scientist / AI Engineer). Read it there; do not duplicate it here.

**Hybrid JDs:** when a JD spans two role types, merge profiles — primary sets the Priority Matrix; secondary contributes 1-2 bridge bullets and extra ATS keywords.

---

## Gap Assessment & Bridge Mappings

For each identified gap, assess:
- **Gap description:** What the JD asks for
- **Bridge framing (if available):** Use "transferable to X" or "equivalent experience with Y" -- NEVER "experienced with X" unless directly demonstrated
- **Bridge confidence:** HIGH / MEDIUM / LOW
- **User decision:** Omit or bridge? (User decides per gap)

**Example bridge mappings** (tech):
- TensorFlow (JD) → "Deep learning framework expertise (PyTorch; directly transferable to TensorFlow)" [HIGH]
- A specific cloud (e.g., AWS SageMaker) → "MLOps tooling (Azure AI, MLflow, Docker; transferable to SageMaker)" [MEDIUM]
- A tracking framework not used → "Object tracking expertise (custom ViT tracker; transferable to [framework])" [MEDIUM]
- Production scale not yet hit → "Edge-deployment & latency optimization (12.5 GFLOPs, ~15ms; methodology transferable)" [MEDIUM]

---

## Content Density Rules

| Format | Project/Comp Bullets | Certs | Leadership |
|--------|---------|--------|------------|
| 1-page resume | ~6-8 | 3-4 | 1 |
| 2-page resume | ~12-20 | 3-4 | 1 |

(5-page CV density is in `cv_reference.md`.)

---

## Files to Upload / Read (resume)

1. `bundle_[role_type].md` — Role-specific generation content (Sections 1-5)
2. `achievement_reframing_guide.md` — Role-type framing directives (load in Phase 2 only if >2 Bridge bullets)
3. `skills_taxonomy.md` — Full skills inventory for Format C generation
4. `resume.cls` — Document class file
5. `resume_template.tex` — Structural template (contains FIXED sections)
6. Experience files from `resume_builder/experience/`

(For a CV: see the upload list in `cv_reference.md`.)

**Role type to bundle mapping:**
Bundles live in `resume_builder/bundles/`. Map each JD role type to its corresponding bundle file (e.g., `bundle_[role_type].md`).
