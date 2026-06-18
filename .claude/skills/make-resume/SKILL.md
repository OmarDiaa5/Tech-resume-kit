---
description: Generate a tailored resume from a JD (resume is the deliverable; cover letters are opt-in via /make-cl)
user-invocable: true
---
# /make-resume

**User input:** `$ARGUMENTS`

Parse `$ARGUMENTS`:

- File path (e.g., `JDs/*.txt`) → read that file for the JD
- Text after the path starting with "Focus:"/"Emphasize:"/"Downplay:" → focus directive
- "Quick:" prefix → Quick Mode (see below)
- `--auto` flag (or positional `auto`) anywhere in `$ARGUMENTS` → Auto Mode (see below)
- Empty → ask the user for the JD
- Inline JD text (no file path) → save to `JDs/temp_<company>.txt`, proceed normally

---

## Safety Rules (ALWAYS ENFORCED)

**Accuracy &gt; Relevance &gt; Impact &gt; ATS &gt; Brevity**

Read `config.md` Provenance Flags before generating any content. Verify every claim against that table.

- Use the email from `config.md` Personal Info in all outputs
- Resume bullets: ALL variable bullets are 2L (CV: 2L/3L mix OK, check `config.md` Document Preferences)
- Source ALL bullet content from `resume_builder/experience/` files. Never fabricate.
- Run `python resume_builder/helpers/char_count.py` after each position — authoritative

---

## User Input During Execution

If the user provides feedback or corrections at any point:

1. Acknowledge immediately
2. If it affects an already-written section: fix it, re-run char count gate
3. If it changes the bullet plan: update session file Bullet Plan
4. If it's a question: answer, then continue from current step
5. Never restart a phase — resume from current position

---

## Startup (LEAN)

Read `config.md` first, then `SESSIONS.md` (the mutable session tracker — CLAUDE.md is never written at runtime).

**File naming & output conventions** (inlined for token efficiency; canonical spec: `shared_ops.md` § Session File System — do NOT load it at runtime):

- Session file: `output/<FolderName>/session_<name>.md`
- Resume: `output/<FolderName>/resume_<FolderName>.tex`
- Critique: `output/<FolderName>/critique_<name>.md`
- Cover letter is OPT-IN — produced only by `/make-cl`. Do NOT plan, mention, or auto-chain it here.
- `<name>` = company+role, lowercase, underscores (e.g., `acme_engineer`); `<FolderName>` = CamelCase from the JD filename.
- **Session end:** Update Status in the session file + update the session row in `SESSIONS.md` before /clear.

**If session file exists for this JD:**

- Phase 0: DONE, Phase 1: PENDING → resume at Phase 1
- Phase 1: DONE → resume at Budget Gate
- Phase 2: IN_PROGRESS → read .tex, check what sections exist, resume from checkpoint
- Phase 2: DONE → "Resume already done. Optional: /critique, or /make-cl if you want a cover letter." Stop.

If no session file: proceed to Phase 0.

---

## Auto Mode (`--auto`)

Invocation: `/make-resume JDs/JD_X.txt --auto` (flag can appear anywhere in `$ARGUMENTS`).

End-to-end Phase 0 → Phase 2 with no user-approval stops. User reviews only the final compiled output.

**Behavior under** `--auto`**:**

- **Skip** the "&gt;&gt;&gt;&gt;&gt;&gt; MANDATORY SINGLE APPROVAL STOP &lt;&lt;&lt;&lt;&lt;&lt;" at end of Phase 1.
- **Resolve role type** from the JD using the Role-Type Decision Tree in `config.md` — no user question.
- **Resolve format** (1-page resume vs 2-page resume vs CV) from `config.md` Document Preferences defaults.
- **Resolve framing strategy** from the bundle's Priority Matrix.
- **Gap Check:** If the bullet plan needs a skill with no matching extraction, do NOT halt. Log it in the session file as `AUTO-SKIPPED: <skill>` and continue.
- **All other gates still fire:** CHAR COUNT GATE, PAGE FILL GATE, COMPILE GATE — these are tool-driven and need no user input.
- **All safety rules still fire:** Anti-Fabrication, Provenance Flags, char limits, AI-fingerprint scan. `--auto` only removes the user-approval stop; it does NOT bypass safety.

Without `--auto`: behavior is unchanged — the Phase 1 approval stop fires as today.

---

## Quick Mode

Trigger: `$ARGUMENTS` starts with "Quick:"

- Select all HIGH priority achievements from bundle's Priority Matrix as 2L
- Fill remaining budget with MEDIUM priority in order
- Default format: **1-page for trainee/intern/new-grad JDs (the common case); 2-page only when seniority/content earns it** (never a CV unless the JD requires one). See `resume_reference.md` § Page & variant selection.
- Skip Phase 0 STOP and Phase 1 STOP
- Keep Budget Gate (auto-pass if within target) and end-of-resume STOP
- Run all phases with progress commentary

---

## Phase −1: Session Existence Check (RUNS FIRST — BEFORE ANY WORK)

**This runs BEFORE Phase 0: before web search, before JD parse, before folder creation.** A re-run on an existing JD must NOT redo research that's already on disk.

1. Derive `FolderName` from the JD path or `$ARGUMENTS` (same rule as Phase 0).
2. Glob `output/<FolderName>/session_*.md`.
3. **If a session file exists:**
   - Read it.
   - Read its `Status:` field and `Phase Handoff` block (see Fix 5 — Phase Handoff in `session_file_template.md`).
   - Announce: "Found existing session: `<path>`. Status: `<status>`. Resuming at `<next phase>`."
   - **Jump directly to that phase. SKIP Phase 0 (folder mkdir, JD copy, web research) and SKIP any Phase 1 work already locked in the handoff block.** Those artifacts are already on disk.
4. **If no session file:** proceed to Phase 0 normally.

---

## Phase 0: Research & Session Setup

**Read these files (Phase 0 — load ONCE, not re-read in Phase 2):**

1. The JD file
2. `resume_builder/reference/resume_reference.md` — Budget Card, Section Specs, Char Limits
3. `config.md` — already loaded at Startup

**Company research — cache first, then search.**

1. Check `knowledge_base/notes/company_<slug>.md` (slug = lowercase company name). If it exists, read it and REUSE it — skip the searches unless the JD reveals a new product/team the cache doesn't cover.
2. If no cache (or stale), load WebSearch via ToolSearch and run 2-3 searches:
   - `[Company] [key JD domain]` (products, tech)
   - `[Company] [specific technology from JD]`
   - `[Company] careers [role type] culture` OR recent news
3. **Write the findings to** `knowledge_base/notes/company_<slug>.md` (mission, products, tech stack, culture signals, "why them" angle, search date) so future JDs for the same company reuse it.

If search returns no results: use JD text + training knowledge. Flag: "Web search returned limited results — company hooks may be generic."

**Produce all of these (resume-focused — NO cover-letter planning here):**

- **JD Analysis** — classify every requirement as Direct / Bridge (with confidence) / Gap. Extract ATS keywords by category.
- **Company Context** — mission, role purpose, culture signals, "why them" angle
- **Framing Strategy** — lead narrative, reframing map, emphasize/downplay, user focus directives
- **Critique Context** — reviewer persona, competitive landscape, domain vocabulary

> Do NOT write a Cover Letter Plan. CLs are opt-in — if the user later runs `/make-cl`, that skill builds the CL plan itself from Company Context + Framing Strategy + bundle S5.

**Create output folder:**

```bash
# Create the directory (use appropriate command for your OS, e.g. New-Item for Windows or mkdir -p for Linux)
# Example for Windows PowerShell:
New-Item -ItemType Directory -Force -Path output/<FolderName>/
Copy-Item JDs/<filename> output/<FolderName>/ -Force
```

**Write session file to** `output/<FolderName>/session_<name>.md` using this structure (do NOT read session_file_template.md):

```
# Session: [Company] [Role Title]
## JD Info
- File / Role / Company / Bundle / Format / Salary

## JD Analysis
### Requirements table: # | Requirement | Direct/Bridge/Gap | Evidence
### ATS Keywords: ML/AI | Domain | Methods | Tools | Soft Skills
### Gap Assessment: Direct list | Bridge list (confidence) | Gap list

## Company Context
Mission | This role | Culture | "Why them" angle

## Framing Strategy
Lead narrative | Reframing map | Emphasize | Downplay | User directives

## Critique Context
Reviewer persona | Competitive landscape | Domain vocabulary

## Bullet Plan
[filled in Phase 1]

## Output Files
[filled after generation]

## Status
- Phase 0: DONE
- Phase 1: PENDING
- Phase 2 Resume: PENDING
- Critique: PENDING
- Cover Letter: NOT REQUESTED
- Next: [exact command]
```

**Update session file Status:** `Phase 0: DONE`

**Write/overwrite the Phase Handoff block** in the session file (last action of this phase). Include: files Phase 1 needs to read, web searches already done with conclusions, JD parse status, and the one-sentence cold-restart command. See `resume_builder/reference/session_file_template.md` → Phase Handoff for structure.

Progress: "Searching for \[company\] + \[domain\]..." / "JD analysis: X direct, Y bridge, Z gap"

### &gt;&gt;&gt;&gt;&gt;&gt; CLAUDE OPTIMIZATION: ONE-PASS DRAFT &lt;&lt;&lt;&lt;&lt;&lt;

**To save API tokens and speed up generation, DO NOT stop here.** Proactively proceed into **Phase 1 (Bullet Planning)**. Generate BOTH the **Framing Strategy** AND the **Recommended Bullet Plan Table** together, and present them in a single response to the user later.

---

## Phase 1: Plan Bullets

**Read:**

1. Session file (`output/<FolderName>/session_<name>.md`) — Framing Strategy + ATS Keywords
2. Bundle: `resume_builder/bundles/bundle_[role_type].md` — Priority Matrix (Section 1) + Reframing Map (Section 3)
3. Experience files — load the synthesized files from `resume_builder/experience/` that the bundle's Priority Matrix points to. **This is the normal source for bullet planning.**
4. `knowledge_base/extractions/_INVENTORY.md` — **only consult if you need a raw extraction** (uncommon — `experience/` files cover the hot path). The inventory is grouped by section (Projects / Competitions / Internships / Courses / Leadership); look up the item and `Read` the listed line range rather than the whole extraction file.
5. `resume_builder/support/skills_taxonomy.md`

**DEFER** `achievement_reframing_guide.md` — load it in Phase 2 ONLY if &gt;2 Bridge bullets are confirmed. For Direct-match-heavy JDs, the bundle's Reframing Map (Section 3) is sufficient.

**Present one table per position:**

**\[Position Name\] (Budget: N-M bullets, \~X-Y rendered lines)**

|  | ID | Achievement | Variant | Lines | JD Match | Date |
| --- | --- | --- | --- | --- | --- | --- |
| \* | P1-1 | \[short description\] | 2L | 2 | Direct | Mar 2026 |
| \* | P1-2 | \[short description\] | 1L | 1 | Direct | Feb 2026 |
| o | P1-3 | \[short description\] | 1L | 1 | Bridge | May 2026 |
| x | P1-7 | \[short description\] | \-- | \-- | Weak | — |

**Variant follows the page target** (see `resume_reference.md` § Page & variant selection): a 1-page resume is **1L-biased** — reserve 2L for the 1–2 strongest bullets only. A 2-page resume is 2L by default. Do NOT reflexively mark every row `2L`.

**Date column rule:** Copy verbatim from the extraction file's `Date:` field. The generator reads this column straight into the `\begin{rSubsection}{Title}{Date}` LaTeX. If an extraction lacks `Date:` — STOP, ask the user, backfill the extraction file. **NEVER infer or guess.**

**Legend:** `*` = recommended | `o` = available | `x` = not recommended

**After all positions, show:**

- Recommended set total vs budget
- Remaining budget slots
- Forced exclusions per provenance flags
- Focus directive impact
- CV: confirm first bullet of first experience is 2L (page 1 rule)
- Bridge bullet count (&gt;2 → will load achievement_reframing_guide.md in Phase 2)

**Update session file** — write Bullet Plan tables. Status: `Phase 1: DONE (N bullets confirmed)`

**Write/overwrite the Phase Handoff block** (last action of Phase 1, AFTER user approval): list the 2–4 files Phase 2 will read (session file, template .tex, bundle if reframing-heavy), lock role type / bundle / framing strategy / bullet plan, and write the cold-restart command. Phase 2 must not re-read experience files or run web searches.

**TOKEN SAVE — Draft prose (MANDATORY):** For every confirmed bullet, append a one-sentence plain-English draft (no LaTeX) under the table. Phase 2 formats these into LaTeX — it does NOT re-read experience files. Format:

```
Draft prose:
- [ID]: [one sentence, metric included, ready to be turned into a LaTeX bullet]
```

Progress: "Reading experience files..." / "Recommending N bullets per position"

### Gap Check

If JD requires a skill with NO matching extraction, ask the user (max 2 questions per session).

### &gt;&gt;&gt;&gt;&gt;&gt; MANDATORY SINGLE APPROVAL STOP &lt;&lt;&lt;&lt;&lt;&lt;

Present the combined Framing Strategy + Bullet Plan. Ask user to confirm: (1) role type + bundle, (2) format, (3) framing strategy, and (4) the bullet plan. Wait for user confirmation/modifications. **Update session file with confirmed plan before continuing.**

---

## Budget Gate

- Check budget targets from resume_reference.md Budget Card (already loaded in Phase 0).
- Show: `Budget: [N] bullets vs target [T]. PASS/FAIL`
- **FAIL = do not proceed. Reconcile with user first.**

---

## Phase 2: Generate

**Read at Phase 2 start:**

1. Session file — framing + confirmed bullet plan
2. `resume_builder/templates/resume_template.tex` — **do NOT read .cls files**. (Only read `cv_template.tex` instead if the user explicitly requested a CV.)
3. If Bridge bullet count &gt; 2: read `resume_builder/support/achievement_reframing_guide.md`

**Char limits:** Enforced by `char_count.py`; do not compute them in reasoning. The CHAR COUNT GATE below is the only place char counts get verified. Aim middle-of-range during drafting and let the tool do the math.

**AI fingerprint rules (compact inline subset — canonical full list is** `resume_builder/support/ai_fingerprint_rules.md`**; keep this subset in sync if that file changes):**

Tier-1 banned words (NEVER use): delve, tapestry, multifaceted, pivotal, realm, synergy, paradigm, holistic, nuanced, foster, embark, leverage (verb), utilize, harness, spearhead, cornerstone, cutting-edge, groundbreaking.

Banned adjectives → replacement: robust→strong/reliable, comprehensive→thorough/broad, innovative→new/original (or omit), meticulous→careful/precise, diverse→varied, extensive→broad/deep.

Banned verbs → replacement: leverage→use/apply, utilize→use, harness→apply/draw on, spearhead→lead/launch, foster→support/build, facilitate→run/lead/enable, showcase→show/demonstrate, underscore→show/highlight, bolster→strengthen.

Banned adverbs: meticulously, notably, subsequently (use "then"), remarkably, seamlessly, thereby.

Banned phrases: "proven track record", "passionate about", "demonstrated ability to", "strong foundation in", "well-versed in", "adept at", "groundbreaking research", "cutting-edge methodology", "significant contributions to the field".

Structural rules:

- Bullets must NOT end with -ing analysis phrases ("...advancing the field", "...contributing to Y") — end with a concrete result or metric
- Max 2 em-dashes (`---`) in the entire document; Leadership/Honors use `. `not `---`
- No gerund fragment stacking (3+ "-ing" phrases in sequence)
- Max 2 "X, Y, and Z" triplet structures per document — use pairs or single items instead
- Vary sentence length in Summary: mix short (8-12 words) with long (20-30 words)

**Generate the ENTIRE resume in one pass** (follow Section-by-Section Specs from resume_reference.md already loaded):

1. Summary → check against session framing strategy
2. Technical Skills
3. All positions and bullets (use Draft prose from session file — do NOT re-read experience files)
   - Position title (bold theme + date) must fit ONE line — shorten if wrapping

**WRITE-FIRST RULE (MANDATORY):** Write the complete .tex first. The only acceptable place to learn a char count is `char_count.py` output. Call the Write tool immediately after composing all LaTeX. Do NOT compute char counts inline. Do NOT output the .tex content as response text. Write → then validate.

Save the complete document to: `output/<FolderName>/resume_<FolderName>.tex`Update Status: `Phase 2: Generation DONE`

Progress: "Writing complete resume..." / "Reviewing character counts..."

### CHAR COUNT GATE (run ONCE on the entire file)

```bash
python resume_builder/helpers/char_count.py -f resume output/<FolderName>/[file].tex
```

No OVER violations; no un-addressed COMPILE-RISK flags. (Last-line ≥70% orphan fill is verified at the COMPILE GATE by reading the PDF — char_count.py cannot measure it.) **CRITICAL FAIL-SAFE:** If there are violations, you are allowed ONE single revision pass — fix ALL violations in that pass, then re-run char_count.py once. If violations remain after the second run: add a `% CHAR_VIOLATION` comment on each offending `\item` line (do NOT rewrite the bullet), save the file as-is, set Status to `Phase 2: CHAR VIOLATION — user review needed`, and STOP immediately. Do NOT attempt a third pass under any circumstances.

### PAGE FILL GATE

Resume: ≤3 lines white space on the last page; no orphan section header alone atop page 2. **If FAIL: add/trim variable bullets.** (5-page CV target of 45 rendered lines: see `cv_reference.md`.)

### COMPILE GATE

```bash
# Copy the LaTeX class files to the output directory BEFORE compiling!
Copy-Item resume_builder/templates/*.cls output/<FolderName>/ -Force

# Compile the PDF
pdflatex -interaction=nonstopmode -output-directory=output/<FolderName> output/<FolderName>/resume_<FolderName>.tex
```

Verify page count matches `config.md` Document Preferences. Check orphans, header wrapping, page fill.

**Post-gen scan — run ALL 12 checks before presenting:**

- [ ] No Tier-1 banned word present

- [ ] No banned phrase from the list above

- [ ] ≤2 em-dashes (`---`) total in document

- [ ] No bullet ending with an -ing analysis phrase

- [ ] No bullet at hard max (target mid-range — risky with wide chars)

- [ ] All char count violations resolved (OVER flags cleared)

- [ ] No 3+ consecutive same-length sentences in Summary

- [ ] No more than 2 "X, Y, and Z" triplet structures

- [ ] Leadership/Honors items use `. `not `---`

- [ ] Passive voice in ≤20% of bullet verbs

- [ ] No banned adverb (meticulously, notably, subsequently, seamlessly, remarkably, thereby)

- [ ] All provenance flags respected — no inflation, no overstated completion status

Update Status → `Phase 2: Compile DONE`

**Write/overwrite the Phase Handoff block** (last action of Phase 2): mark next phase as `/critique` (optional). List files a re-critique would need (session file, finished resume .tex, bundle). Resume artifacts are now locked. Do NOT name `/make-cl` as the next step — a cover letter is produced only if the user explicitly asks.

---

## End of /make-resume

Update session file Status:

- `Resume: DONE` / `Critique: PENDING` / `Cover Letter: NOT REQUESTED`
- `Next (optional): /critique output/<FolderName>/session_<name>.md`

Update the session row in `SESSIONS.md`.

### &gt;&gt;&gt;&gt;&gt;&gt; MANDATORY STOP &lt;&lt;&lt;&lt;&lt;&lt;

Present: compilation summary (pages, char count results, any violations fixed). **Wait for user response.**

"Resume compiled and verified. Optional next steps:

- Review: `/clear` then `/critique output/<FolderName>/session_<name>.md`
- Cover letter (only if you want one): `/clear` then `/make-cl output/<FolderName>/session_<name>.md`

Otherwise the resume is ready to ship as-is."