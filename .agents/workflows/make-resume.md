---
description: Generate a tailored resume/CV from a JD
user-invocable: true
---

# /make-resume

**User input:** `$ARGUMENTS`

Parse `$ARGUMENTS`:
- File path (e.g., `JDs/*.txt`) → read that file for the JD
- Text after the path starting with "Focus:"/"Emphasize:"/"Downplay:" → focus directive
- "Quick:" prefix → Quick Mode (see below)
- Empty → ask the user for the JD
- Inline JD text (no file path) → save to `JDs/temp_<company>.txt`, proceed normally

---

## Safety Rules (ALWAYS ENFORCED)

**Accuracy > Relevance > Impact > ATS > Brevity**

Read `config.md` Provenance Flags and `.agents/rules/antigravity-rules.md` before generating any content. Verify every claim against those rules.

- Use the email from `config.md` Personal Info in all outputs
- Resume bullets: ALL variable bullets are 2L (CV: 2L/3L mix OK, check `config.md` Document Preferences)
- Source ALL bullet content from `resume_builder/experience/` files. Never fabricate.
- Run `python3 .agents/helpers/verify_build.py -f [resume|cv] [file.tex]` — the automated linter is authoritative and checks all lengths, orphans, jargon, and metrics.

---

## User Input During Execution

If the user provides feedback, corrections, or suggestions at any point:
1. Acknowledge the input immediately
2. If it affects an already-written section: go back, fix it, re-run linter validation
3. If it changes the bullet plan: update session file Bullet Plan
4. If it's a question: answer it, then continue from current step
5. Never restart a phase — resume from current position

---

## Startup

Read `resume_builder/reference/shared_ops.md` for session startup, file derivation, and organization protocols.

Then:
1. Read `CLAUDE.md` — check Active Sessions and KB Corrections
2. Read `config.md` — load Provenance Flags, email, document preferences, role types
3. Read `.agents/rules/antigravity-rules.md` — load compact LaTeX and character limits
4. If session file exists for this JD:
   - Read session file, check Status
   - Phase 0: DONE, Phase 1: PENDING → resume at Phase 1
   - Phase 1: DONE → resume at Budget Gate
   - Phase 2: IN_PROGRESS → read .tex, check what sections exist, resume from checkpoint
   - Phase 2: DONE → "Resume already done." Show next command. Stop.
5. If no session file: proceed to Phase 0

---

## Quick Mode

Trigger: `$ARGUMENTS` starts with "Quick:"

Defaults:
- Select all HIGH priority achievements from bundle's Priority Matrix as 2L
- Fill remaining budget with MEDIUM priority in Priority Matrix order
- Default format: 2-page resume (unless JD clearly requires CV)
- Skip Phase 0 STOP and Phase 1 STOP
- Keep Budget Gate (auto-pass if within target) and end-of-resume STOP
- Run all phases with progress commentary instead of interactive stops

---

## Phase 0: Research & Session Setup

**Read these files:**
1. The JD (from `$ARGUMENTS`)
2. `.agents/rules/antigravity-rules.md` — Budget constraints, LaTeX conventions, and anti-jargon rules
3. `config.md` — Role-Type Decision Tree to identify the matching bundle

**Web Search (MANDATORY — 2-3 searches).** Load WebSearch via ToolSearch first.
1. `[Company] research & development [key JD domain]` — products, recent projects
2. `[Company] [specific technology from JD]` — concrete hooks
3. `[Company] careers [role type] culture` OR recent news — hiring context

If web search returns no results: use JD text + training knowledge. Flag: "Web search returned limited results."

**Produce all of these (reference `resume_builder/reference/session_file_template.md` for format):**
- **JD Analysis** — classify every requirement as Direct / Bridge / Gap. Extract ATS keywords by category.
- **Company Context** — mission, role purpose, culture signals
- **Framing Strategy** — lead narrative, reframing map, emphasize/downplay
- **Critique Context** — reviewer persona, competitive landscape, domain vocabulary
- **Cover Letter Plan** — (Optional, skip if cover letter is not requested by the user)

**Create output folder:**
Derive folder name from JD filename: `JDs/JD_Acme.txt` → `output/Acme/`
```bash
mkdir -p output/<FolderName>/
```
Write session file to `output/<FolderName>/session_<name>.md` (NOT flat `output/`).
All subsequent output files go in this folder.

**Verify completeness:** Re-read the session file. Confirm core sections are non-empty.

**Write memory pointer** to `CLAUDE.md` Active Sessions.

**Update session file Status:** `Phase 0: DONE`

Progress: "Searching for [company] + [domain]..." / "JD analysis done."

### >>>>>> ANTIGRAVITY OPTIMIZATION: ONE-PASS DRAFT <<<<<<
**To save API quota and speed up generation, DO NOT stop here.** Proactively proceed into **Phase 1 (Bullet Planning)**. 
Generate BOTH the **Framing Strategy** AND the **Recommended Bullet Plan Table** together. 
Render this entire combined planning layout in a single beautiful **Markdown Artifact** for the user. 
This allows the user to review the strategy and select/adjust bullets in a single conversational turn.

---

## Phase 1: Plan Bullets

**Re-read `output/<FolderName>/session_<name>.md`** — specifically Framing Strategy and ATS Keywords.

**Read:**
1. The matching bundle from `config.md` Role Types → `resume_builder/bundles/bundle_[role_type].md` — Section 1 (Priority Matrix)
2. All experience files from `resume_builder/experience/`
3. `.agents/rules/antigravity-rules.md` for spacing, layout rules, and LaTeX guidelines

**Present one table per position inside the combined Artifact:**

**[Position Name] (Budget: N-M bullets, ~X-Y rendered lines)**

| | ID | Achievement | Variant | Lines | JD Match |
|---|---|-------------|---------|-------|----------|
| * | P1-1 | [short description] | 2L | 2 | Direct |
| * | P1-5 | [short description] | 2L | 2 | Direct |
| o | P1-3 | [short description] | 2L | 2 | Bridge |
| x | P1-7 | [short description] | -- | -- | Weak |

**Legend:** `*` = recommended (HIGH on Priority Matrix + Direct JD match) | `o` = available (MEDIUM priority or Bridge match) | `x` = not recommended (LOW priority or Gap)

**After all positions, show:**
- Recommended set total vs budget (from `.agents/rules/antigravity-rules.md`)
- Remaining budget slots and what could fill them
- Forced exclusions per provenance flags
- Focus directive impact

**Update session file** — write Bullet Plan tables. Status: `Phase 1: DONE (N bullets confirmed)`

### >>>>>> MANDATORY SINGLE APPROVAL STOP <<<<<<
Present the combined Strategy + Bullet Plan Artifact. Wait for user to confirm/modify selections.
**You MUST wait for the user's explicit text response before continuing to Generation.**
Once approved, update the session file with the confirmed plan and proceed.

---

## Budget Gate (AFTER user confirms bullet plan, BEFORE Phase 2)

**Re-read session file Bullet Plan section** to verify confirmed counts.

- Check budget targets from `resume_builder/reference/resume_reference.md` Budget Card.
- Show: `Budget: [N] bullets vs target [T]. PASS/FAIL`
- **FAIL = do not proceed. Reconcile with user first.**

---

## Phase 2: Generate

**Re-read to restore context after compaction:**
1. `output/<FolderName>/session_<name>.md` (framing + confirmed bullet plan)
2. `.agents/rules/antigravity-rules.md` — Character Limits, Bold Width Penalty, LaTeX notation, and anti-jargon rules

**Read template:** `resume_builder/templates/resume_template.tex` or `cv_template.tex` + `.cls`
FIXED sections (from `config.md` FIXED Sections) are template-locked — only generate VARIABLE sections (Summary, Skills, Experience bullets/headers).

**Generate section by section**:
1. Summary → check against session framing strategy
   - Update Status → `Phase 2: Summary DONE`
2. Technical Skills
   - Update Status → `Phase 2: Skills DONE`
3. Each position's bullets
   - Position titles: bold theme + date must fit ONE line. If wrapping, shorten title.
   - After each position: Update Status → `Phase 2: [Position] DONE`

Save .tex to `output/<FolderName>/resume_<FolderName>.tex`

Update session file — add Output Files.

Progress: "Writing bullets..." / "Running automated validation linter..."

### THE ANTIGRAVITY LINT & COMPILE GATE
Run the automated verification script on the generated `.tex` file in the background:
```bash
python3 .agents/helpers/verify_build.py output/<FolderName>/resume_<FolderName>.tex -f [resume|cv] --json
```
* **If linter fails**: Read the JSON failure reports containing precise character counts, bold penalties, orphan issues, or forbidden jargon. Fix the violating bullets in the `.tex` file directly using `replace_file_content` and re-run the linter. **Do NOT prompt the user during this loop.**
* **If linter passes**: Compile the document:
```bash
pdflatex -interaction=nonstopmode -output-directory=output/<FolderName> output/<FolderName>/resume_<FolderName>.tex
```
Ensure compile matches document preferences, then proceed.

Update Status → `Phase 2: Compile DONE`

---

## End of /make-resume

Update session file Status:
- `Resume: DONE`
- `Cover Letter: PENDING`
- `Critique: PENDING`
- `Next: /make-cl output/<FolderName>/session_<name>.md`
- `Next Critique: /critique output/<FolderName>/session_<name>.md`

### Gap Check

If the JD requires a skill/domain that has NO matching extraction:
- Note the gap in the bullet plan
- Ask the user: "The JD emphasizes [skill]. Do you have related experience that could bridge to this? If yes, which project?"
- Resume bullets: ALL variable bullets are 2L (CV: 2L/3L mix OK, check `config.md` Document Preferences)
- Source ALL bullet content from `resume_builder/experience/` files. Never fabricate.
- Run `python3 .agents/helpers/verify_build.py -f [resume|cv] [file.tex]` — the automated linter is authoritative and checks all lengths, orphans, jargon, and metrics.

---

## User Input During Execution

If the user provides feedback, corrections, or suggestions at any point:
1. Acknowledge the input immediately
2. If it affects an already-written section: go back, fix it, re-run linter validation
3. If it changes the bullet plan: update session file Bullet Plan
4. If it's a question: answer it, then continue from current step
5. Never restart a phase — resume from current position

---

## Startup

Read `resume_builder/reference/shared_ops.md` for session startup, file derivation, and organization protocols.

Then:
1. Read `CLAUDE.md` — check Active Sessions and KB Corrections
2. Read `config.md` — load Provenance Flags, email, document preferences, role types
3. Read `.agents/rules/antigravity-rules.md` — load compact LaTeX and character limits
4. If session file exists for this JD:
   - Read session file, check Status
   - Phase 0: DONE, Phase 1: PENDING → resume at Phase 1
   - Phase 1: DONE → resume at Budget Gate
   - Phase 2: IN_PROGRESS → read .tex, check what sections exist, resume from checkpoint
   - Phase 2: DONE → "Resume already done." Show next command. Stop.
5. If no session file: proceed to Phase 0

---

## Quick Mode

Trigger: `$ARGUMENTS` starts with "Quick:"

Defaults:
- Select all HIGH priority achievements from bundle's Priority Matrix as 2L
- Fill remaining budget with MEDIUM priority in Priority Matrix order
- Default format: 2-page resume (unless JD clearly requires CV)
- Skip Phase 0 STOP and Phase 1 STOP
- Keep Budget Gate (auto-pass if within target) and end-of-resume STOP
- Run all phases with progress commentary instead of interactive stops

---

## Phase 0: Research & Session Setup

**Read these files:**
1. The JD (from `$ARGUMENTS`)
2. `.agents/rules/antigravity-rules.md` — Budget constraints, LaTeX conventions, and anti-jargon rules
3. `config.md` — Role-Type Decision Tree to identify the matching bundle

**Web Search (MANDATORY — 2-3 searches).** Load WebSearch via ToolSearch first.
1. `[Company] research & development [key JD domain]` — products, recent projects
2. `[Company] [specific technology from JD]` — concrete hooks
3. `[Company] careers [role type] culture` OR recent news — hiring context

If web search returns no results: use JD text + training knowledge. Flag: "Web search returned limited results."

**Produce all of these (reference `resume_builder/reference/session_file_template.md` for format):**
- **JD Analysis** — classify every requirement as Direct / Bridge / Gap. Extract ATS keywords by category.
- **Company Context** — mission, role purpose, culture signals
- **Framing Strategy** — lead narrative, reframing map, emphasize/downplay
- **Critique Context** — reviewer persona, competitive landscape, domain vocabulary
- **Cover Letter Plan** — (Optional, skip if cover letter is not requested by the user)

**Create output folder:**
Derive folder name from JD filename: `JDs/JD_Acme.txt` → `output/Acme/`
```bash
mkdir -p output/<FolderName>/
```
Write session file to `output/<FolderName>/session_<name>.md` (NOT flat `output/`).
All subsequent output files go in this folder.

**Verify completeness:** Re-read the session file. Confirm core sections are non-empty.

**Write memory pointer** to `CLAUDE.md` Active Sessions.

**Update session file Status:** `Phase 0: DONE`

Progress: "Searching for [company] + [domain]..." / "JD analysis done."

### >>>>>> ANTIGRAVITY OPTIMIZATION: ONE-PASS DRAFT <<<<<<
**To save API quota and speed up generation, DO NOT stop here.** Proactively proceed into **Phase 1 (Bullet Planning)**. 
Generate BOTH the **Framing Strategy** AND the **Recommended Bullet Plan Table** together. 
Render this entire combined planning layout in a single beautiful **Markdown Artifact** for the user. 
This allows the user to review the strategy and select/adjust bullets in a single conversational turn.

---

## Phase 1: Plan Bullets

**Re-read `output/<FolderName>/session_<name>.md`** — specifically Framing Strategy and ATS Keywords.

**Read:**
1. The matching bundle from `config.md` Role Types → `resume_builder/bundles/bundle_[role_type].md` — Section 1 (Priority Matrix)
2. All experience files from `resume_builder/experience/`
3. `.agents/rules/antigravity-rules.md` for spacing, layout rules, and LaTeX guidelines

**Present one table per position inside the combined Artifact:**

**[Position Name] (Budget: N-M bullets, ~X-Y rendered lines)**

| | ID | Achievement | Variant | Lines | JD Match |
|---|---|-------------|---------|-------|----------|
| * | P1-1 | [short description] | 2L | 2 | Direct |
| * | P1-5 | [short description] | 2L | 2 | Direct |
| o | P1-3 | [short description] | 2L | 2 | Bridge |
| x | P1-7 | [short description] | -- | -- | Weak |

**Legend:** `*` = recommended (HIGH on Priority Matrix + Direct JD match) | `o` = available (MEDIUM priority or Bridge match) | `x` = not recommended (LOW priority or Gap)

**After all positions, show:**
- Recommended set total vs budget (from `.agents/rules/antigravity-rules.md`)
- Remaining budget slots and what could fill them
- Forced exclusions per provenance flags
- Focus directive impact

### Gap Check
If the JD requires a skill/domain that has NO matching extraction:
- Note the gap in the bullet plan
- Ask the user: "The JD emphasizes [skill]. Do you have related experience that could bridge to this? If yes, which project?"
- If user provides evidence, note it in the session file `## Evidence Tracking` and use it in Phase 2
- If user says no, proceed without it — do not fabricate

Limit to 2 gap questions maximum per session.

**Update session file** — write Bullet Plan tables. Status: `Phase 1: DONE (N bullets confirmed)`

### >>>>>> MANDATORY SINGLE APPROVAL STOP <<<<<<
Present the combined Strategy + Bullet Plan Artifact. Wait for user to confirm/modify selections.
**You MUST wait for the user's explicit text response before continuing to Generation.**
Once approved, update the session file with the confirmed plan and proceed.

---

## Budget Gate (AFTER user confirms bullet plan, BEFORE Phase 2)

**Re-read session file Bullet Plan section** to verify confirmed counts.

- Check budget targets from `resume_builder/reference/resume_reference.md` Budget Card.
- Show: `Budget: [N] bullets vs target [T]. PASS/FAIL`
- **FAIL = do not proceed. Reconcile with user first.**

---

## Phase 2: Generate

**Re-read to restore context after compaction:**
1. `output/<FolderName>/session_<name>.md` (framing + confirmed bullet plan)
2. `.agents/rules/antigravity-rules.md` — Character Limits, Bold Width Penalty, LaTeX notation, and anti-jargon rules

**Read template:** `resume_builder/templates/resume_template.tex` or `cv_template.tex` + `.cls`
FIXED sections (from `config.md` FIXED Sections) are template-locked — only generate VARIABLE sections (Summary, Skills, Experience bullets/headers).

**Generate section by section**:
1. Summary → check against session framing strategy
   - Update Status → `Phase 2: Summary DONE`
2. Technical Skills
   - Update Status → `Phase 2: Skills DONE`
3. Each position's bullets
   - Position titles: bold theme + date must fit ONE line. If wrapping, shorten title.
   - After each position: Update Status → `Phase 2: [Position] DONE`

Save .tex to `output/<FolderName>/resume_<FolderName>.tex`

Update session file — add Output Files.

Progress: "Writing bullets..." / "Running automated validation linter..."

### THE ANTIGRAVITY LINT & COMPILE GATE
Run the automated verification script on the generated `.tex` file in the background:
```bash
python3 .agents/helpers/verify_build.py output/<FolderName>/resume_<FolderName>.tex -f [resume|cv] --json
```
* **If linter fails**: Read the JSON failure reports containing precise character counts, bold penalties, orphan issues, or forbidden jargon. Fix the violating bullets in the `.tex` file directly using `replace_file_content` and re-run the linter. **Do NOT prompt the user during this loop.**
* **If linter passes**: Compile the document:
```bash
pdflatex -interaction=nonstopmode -output-directory=output/<FolderName> output/<FolderName>/resume_<FolderName>.tex
```
Ensure compile matches document preferences, then proceed.

Update Status → `Phase 2: Compile DONE`

---

## End of /make-resume

Update session file Status:
- `Resume: DONE`
- `Cover Letter: PENDING`
- `Critique: PENDING`
- `Next: /make-cl output/<FolderName>/session_<name>.md`
- `Next Critique: /critique output/<FolderName>/session_<name>.md`

### >>>>>> MANDATORY STOP <<<<<<
Present: resume compilation summary (pages, char count results, any violations fixed).
**You MUST wait for the user's explicit text response before continuing.**

"Resume compiled and verified. Next steps:
1. /clear
2. [exact /make-cl command with session file path]"
