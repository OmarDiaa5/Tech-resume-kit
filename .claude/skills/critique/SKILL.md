---
description: Re-critique existing resume output files against a JD
user-invocable: true
---

# /critique

**User input:** `$ARGUMENTS`

Parse `$ARGUMENTS`:
- Session file path (e.g., `output/Acme/session_acme_engineer.md`) → read session file, derive .tex paths from Output Files
- .tex file path(s) + JD source (existing format) → backward compatible
- Session name (e.g., `acme_engineer`) → find session file via derivation
- `quick` token anywhere in `$ARGUMENTS` → **Quick Mode** (see below)

**Resume is the default unit of critique.** A cover letter is critiqued only if a CL .tex actually exists for this session (most packages are resume-only). If none exists, run the resume-standalone path (Part 7 adjustment below) — do NOT ask the user to make a CL.

## Quick Mode (`quick`)

Lightweight pass for fast iteration. Load ONLY `critique_framework.md` Part 3 (scoring) — skip loading the rest of the framework. Produce ONLY:
1. The 8-dimension weighted score table (summing to 100) + total.
2. Tier-1 fixes (>=1 pt each), as a short numbered list.
Skip the domain lens write-up, five-perspective prose, interview-likelihood, bridge points, and full CL sub-checks. Still read the session file, the resume .tex, the JD, and run `char_count.py` + compile. Save a short `critique_<name>.md` and STOP. This is what most iterations need.

---

## Safety Rules

**Accuracy > Relevance > Impact > ATS > Brevity**

Read `config.md` Provenance Flags. Verify every claim against that table.
Check `config.md` KB Corrections Log — do not flag corrected items as errors.
Use the email from `config.md` Personal Info — flag if a different email appears in output.
FIXED sections (from `config.md` FIXED Sections) are template-locked — do not flag for editing. Flag only VARIABLE sections.

---

## User Input During Execution

If the user provides feedback, corrections, or suggestions at any point:
1. Acknowledge the input immediately
2. If it changes scoring criteria or focus: adjust the critique accordingly
3. Never restart — resume from current position

---

## Startup

Read `config.md` first, then `SESSIONS.md` (active-session tracker; CLAUDE.md is never written at runtime). Check `config.md` KB Corrections Log.

**Session file derivation** (folder-based — do NOT parse the filename into a stem; canonical spec: `shared_ops.md` § Session File Derivation — keep in sync):
- If `$ARGUMENTS` is a `session_*.md` path → use it.
- If `$ARGUMENTS` is a `.tex` path → take its folder, glob `<folder>/session_*.md`.
- If `$ARGUMENTS` is a folder/FolderName/bare session name → glob `output/<FolderName>/session_*.md` or `output/*/session_<name>.md`.
- Fallback: `SESSIONS.md` pointer, then glob `output/*/session_*<company>*.md`. **Never scan `output/_archive/`.**
- If still not found: do 1-2 web searches to build minimal context. Note in critique: "No session file — framing context is approximate."

Find and read the session file.

**Recovery check:**
- If CL not DONE in session file → "CL not yet generated. Run `/make-cl` first."
- If Critique: CURRENT → "Already critiqued (score X/100). Re-run? Waiting for confirmation."
- If Critique: STALE → "Edits made since last critique. Re-critiquing."
- If Critique: PENDING → proceed

---

## Protocol

1. **Read session file** — specifically note:
   - **Company Context** → reviewer persona, "why this company"
   - **Framing Strategy** → intentional reframing decisions (flag only execution inconsistencies, not the strategy itself)
   - **Cover Letter Plan** → CL structure rationale
   - **Critique Context** → reviewer persona, competitive landscape, domain vocabulary
   - If session file lacks Company Context or Critique Context: do 1-2 web searches to fill gaps
2. Read `resume_builder/reference/critique_framework.md` (Quick Mode: only Part 3, the scoring section)
3. Read `resume_builder/support/ai_fingerprint_rules.md` — use Section 6 checklist in Part 7 verification
4. Read the .tex file(s) — derive paths from session file Output Files, or from `$ARGUMENTS`
5. Read the JD (path from `$ARGUMENTS` or session file)
6. Read the relevant bundle (`resume_builder/bundles/bundle_[role_type].md` — from session file)
7. Run char count (resume default; `-f cv` only for a CV):
   ```bash
   python resume_builder/helpers/char_count.py -f resume [file.tex]
   ```
8. Compile and visually verify:
   ```bash
   # Copy the LaTeX class files to the output directory BEFORE compiling!
   Copy-Item resume_builder/templates/*.cls output/<FolderName>/ -Force
   
   pdflatex -interaction=nonstopmode -output-directory=output/<FolderName> [file.tex]
   ```
   Use the Read tool to view the compiled PDF — check orphans, page fill, header wrapping.
   If compile fails: note "COMPILE FAILED — visual checks could not be verified" in Part 8.
9. If a prior critique exists (`output/<FolderName>/critique_<name>.md`): read it and note previous score.
10. **Project Hook Verification:** If the resume or CL cites named projects, companies, programs, or technologies, web-search to verify accuracy. Flag factual errors as Tier 1 fixes.

11. **Run the full critique per critique_framework.md. The output MUST contain ALL 8 sections** (Quick Mode: produce only Parts 3 and 5):

    1. **Domain-Specialist Lens** — 7 elements:
       (a) Reviewer persona (b) Company context (c) JD vocabulary extraction (d) Domain vocabulary map
       (e) Gap ranking (fatal/serious/cosmetic) (f) Methodology transfer test (g) Competitive landscape
    2. **Five-Perspective Read-Through** — ATS, Recruiter (10s), HR (30s), HM (2min), Technical (10min) — each with verdict
    3. **Eight-Dimension Scoring** — weighted table summing to 100
       (ATS 15%, Summary 10%, Skills 10%, Bullets 25%, Projects & Portfolio 10%, Narrative 15%, Visual 5%, Credibility 10%)
    4. **Interview Likelihood** — per-reader probability + ceiling analysis
    5. **Tiered Improvements** — Tier 1 (>=1pt each), Tier 2 (0.3-0.9), Tier 3 (<0.3)
    6. **Interview Bridge Points** — 5-7 resume-to-interview talking points
    7. **Cover Letter Critique** — 6 sub-checks (6A anti-patterns, 6B tailoring, 6C context-specific, 6D ATS, 6E structural, 6F package cohesion)
       - **If no CL provided:** Skip 6A-6E. Run 6F as resume standalone assessment — evaluate whether the resume earns an interview without a CL. Note: "Cover letter not provided — package cohesion not assessed."
    8. **Post-Generation Verification** — mechanical + content + structural checklists

12. Save to `output/<FolderName>/critique_<name>.md`
98. **Evidence Checkpoint (Lightweight)**
    After scoring, if any dimension scored below 7/10:
    1. Identify the 1-2 weakest claims that dragged the score down
    2. Ask the user: "Before finalizing, can you provide evidence for [weak claim]? If yes, I can strengthen it. If no, I'll note it as a known gap."
    3. Record any user-provided evidence in the session file under `## Evidence Tracking`
    4. If the user says to record to KB, update the relevant extraction file with a `## Framing Evidence` section

99. **Update session file** — Critique Summary (score, findings, tier 1 fixes), Status → Critique: CURRENT
100. **Write/overwrite the Phase Handoff block** — if score passes: next phase = finalization (none); if Tier 1 fixes exist: next phase = `/edit-resume`, list the .tex + critique.md, and write the cold-restart command. See `resume_builder/reference/session_file_template.md` → Phase Handoff.
101. **Update the session row in `SESSIONS.md`** with the new score/status.

Progress: "Reading session file for framing context..." / "Running ATS keyword scan — 16/20 match..." / "Scoring 8 dimensions..." / "Score: 87.0/100"

### >>>>>> MANDATORY STOP <<<<<<
Present: score table + tier 1 actionable fixes + interview likelihood.
**You MUST wait for the user's explicit text response before continuing.**
If edits needed, tell user to run `/edit-resume`.

### When user approves / says "looks good" / finalizes:
Verify the expected files exist in `output/<FolderName>/`:
- session file, resume .tex + .pdf, critique .md (always)
- CL .tex + .pdf **only if a cover letter was generated** — a resume-only package is complete without it
- Compile artifacts (.aux, .log, .out)
Confirm to user: "Package complete in output/<FolderName>/ — [list files]"
