# Shared Operations — All Skills

> Canonical written spec for the session/workflow system. Skills do **not** load this file at
> runtime — they inline the parts they need (see each SKILL.md) for token efficiency. This file
> is the source of truth: keep those inline copies in sync with the sections here.

---

## Workflow (resume-first, cover letter OPT-IN)

The default deliverable is a **resume**. A cover letter is generated **only if the user runs `/make-cl`** — never auto-chained.

Session 1: `/make-resume JDs/JD_xyz.txt`
  → Phase 0 (research) → STOP → Phase 1 (bullets) → STOP → Phase 2 (resume) → STOP
  → "Resume done. Optional next: `/critique output/<Folder>/session_<name>.md` (review),
     or `/make-cl output/<Folder>/session_<name>.md` ONLY if you want a cover letter."

Session 2 (optional, only if requested): `/critique output/<Folder>/session_<name>.md`
  → Critique resume (and CL if one exists) → STOP
  → If approved: finalization check → "Package complete in output/<Folder>/"

Cover letter (only when the user explicitly asks): `/make-cl output/<Folder>/session_<name>.md`

If edits needed after critique:
  /clear → /edit-resume output/<Folder>/resume_<Folder>.tex output/<Folder>/critique_<name>.md
  /clear → /critique output/<Folder>/session_<name>.md (re-critique)

Use a fresh session (`/clear`) per step for token efficiency and fresh-eyes quality.

---

## Fresh Session Startup

CLAUDE.md is auto-loaded. These files are NOT — read them at skill start:
1. `config.md` — personal info, provenance flags, KB corrections
2. `SESSIONS.md` — the mutable active-session tracker (NOT CLAUDE.md; CLAUDE.md is never written at runtime)
3. If resuming work on an existing JD: read its session file and pick up at Status → Next
4. If starting a new JD: proceed to Phase 0
5. **If invoked via `/make-resume`, the session-existence check runs FIRST** — before any web search, JD parse, or folder mkdir. See `make-resume/SKILL.md` Phase −1.

---

## Session File System

Every JD gets a persistent session file: `output/<FolderName>/session_<name>.md` — the single source of truth for all context.

**Naming:** Derive `<name>` from company/role — lowercase, underscores (e.g., `acme_engineer`, `natlab_postdoc`).

**All output files use the same key and direct naming format:**
- `output/<FolderName>/session_<name>.md` — context file
- `output/<FolderName>/resume_<FolderName>.tex` — generated document (compiles directly to `resume_<FolderName>.pdf`)
- `output/<FolderName>/cover_letter_<FolderName>.tex` — cover letter (compiles directly to `cover_letter_<FolderName>.pdf`)
- `output/<FolderName>/critique_<name>.md` — critique

**Re-read the session file at the start of EVERY phase** to restore context after compaction.

---

## Session File Derivation (for /make-cl, /critique, and /edit-resume)

**The session file is the `session_*.md` that lives in the SAME folder as the target document.** Derive by folder, never by parsing the filename into a `<name>` — the resume is named after the *folder* (`resume_Nokia.tex`) while the session is named after the *role* (`session_nokia_ni_ds_ai_trainee.md`), so they do not share a stem.

**Search order:**
1. If `$ARGUMENTS` is a `session_*.md` path → use it directly.
2. If `$ARGUMENTS` is a `.tex`/`.pdf` path → take its folder, glob `<folder>/session_*.md`.
3. If `$ARGUMENTS` is a folder or a FolderName → glob `output/<FolderName>/session_*.md`.
4. If `$ARGUMENTS` is a bare session name → glob `output/*/session_<name>.md`.
5. `SESSIONS.md` active-session pointer.
6. Last resort: glob `output/*/session_*<company>*.md`.

**NEVER scan `output/_archive/`** — it is cold storage of retired `e2e_*` builds. All globs are one level under `output/` (`output/*/…`), which excludes the two-level archive paths by construction.

**If still not found:**
- `/edit-resume`: Tell user — "No session file exists. Run `/make-resume` first, or I can create a minimal one (JD Info + Framing Strategy inferred from .tex content)."
- `/critique`: Do 1-2 web searches to build minimal context. Note in critique: "No session file — framing context is approximate."
- `/make-cl`: Tell user — "No session file exists. Run `/make-resume` first."

---

## Progress Commentary

Provide brief status updates at each major step. Minimum: what you're doing + what you found.

If a step takes more than ~30 seconds of silent processing, output a progress line. The user should never wonder if things are stuck.

Per-phase examples are in each SKILL.md.

---

## Char Count Enforcement

Run `python resume_builder/helpers/char_count.py` once after the document (or section, if mid-edit) is saved to disk — not per-bullet, not before writing.

**Never count characters in your thoughts** — the tool is fast and exact; mental counting is slow and wrong. The tool is the only authority. If the tool fails, flag: "char_count.py unavailable — verify after compile."

---

## Folder Creation (Phase 0 of /make-resume)

**Trigger:** Start of Phase 0 in `/make-resume`.

**Steps:**
1. Derive folder name from JD filename: `JDs/JD_Acme.txt` → `output/Acme/`
2. `mkdir -p output/<FolderName>/`
3. Copy JD file into output folder: `cp JDs/<filename> output/<FolderName>/`
4. Write session file to `output/<FolderName>/session_<name>.md`
5. All subsequent output files (from ALL skills) go in this folder

## Finalization (after /critique approval)

**Trigger:** User approves final output at `/critique` STOP.

**Steps:**
1. Verify the expected files exist in `output/<FolderName>/`:
   - `session_<name>.md` (always)
   - `resume_<FolderName>.tex` + `.pdf` + compile artifacts (always)
   - `critique_<name>.md` (if `/critique` was run)
   - `cover_letter_<FolderName>.tex` + `.pdf` (**only if `/make-cl` was run** — a resume-only package is complete without it)
2. No renaming needed — files are already `resume_<FolderName>.{tex,pdf}` by default.
3. **PDF naming guard:** delete any stray long-form variant (`Full_Name_Resume_*.pdf`) or legacy `e2e_*` PDF in an active folder. One resume PDF per package.
4. Confirm to user: "Package complete in output/<FolderName>/ — [N] files"

---

## Session End Protocol

Before the session ends or user does `/clear`:

1. **Update session file Status** — reflects actual state (which phase completed, what's next)
2. **Update the session row in `SESSIONS.md`** (the mutable tracker — never write to CLAUDE.md)
3. **If mid-phase:** Write a `## Resume Point` section to the session file noting exactly where you stopped and what remains
