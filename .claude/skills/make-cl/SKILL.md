---
description: Generate a tailored cover letter from an existing session file and finished resume
user-invocable: true
---

# /make-cl

**User input:** `$ARGUMENTS`

> Cover letters are OPT-IN. This skill runs only when the user explicitly invokes `/make-cl`. `/make-resume` never auto-chains here.

Parse `$ARGUMENTS`:
- Session file path (e.g., `output/Acme/session_acme_engineer.md`) → read that session file
- Session name (e.g., `acme_engineer`) → find session file via derivation below
- Empty → check `SESSIONS.md` for the latest active session

---

## Safety Rules (ALWAYS ENFORCED)

**Accuracy > Relevance > Impact > ATS > Brevity**

Read `config.md` Provenance Flags before generating any content. Verify every claim against that table.

- Use the email from `config.md` Personal Info in all outputs
- CL deepens what resume presents — never introduces new claims not traceable to resume bullets
- Source field context from `resume_builder/support/significance_*.md` files
- **Word/line counts go through tools, not mental tallying.** Use `wc -w` on the CL .tex (or `char_count.py` for resume-style bullets). Never compute word/char counts in reasoning.

---

## User Input During Execution

If the user provides feedback, corrections, or suggestions at any point:
1. Acknowledge the input immediately
2. If it affects already-written content: fix it, re-verify word count and anti-patterns
3. If it changes the framing: note the change in session file Framing Strategy
4. Never restart — resume from current position

---

## Startup

Read `config.md` first, then `SESSIONS.md` (active-session tracker; CLAUDE.md is never written at runtime).

**Session file derivation** (folder-based — do NOT parse the filename into a stem; canonical spec: `shared_ops.md` § Session File Derivation — keep in sync):
- If `$ARGUMENTS` is a `session_*.md` path → use it.
- If `$ARGUMENTS` is a `.tex` path → take its folder, glob `<folder>/session_*.md`.
- If `$ARGUMENTS` is a folder/FolderName/bare session name → glob `output/<FolderName>/session_*.md` or `output/*/session_<name>.md`.
- Fallback: `SESSIONS.md` pointer, then glob `output/*/session_*<company>*.md`.
- **Never scan `output/_archive/`** (retired `e2e_*` storage). All globs stay one level under `output/`.

Find and read the session file.

**Recovery check:**
   - If Resume Status is not DONE → "Resume not yet generated. Run `/make-resume` first." Stop.
   - If CL Status is DONE → "CL already generated. Optionally run `/critique`." Show command. Stop.
   - If CL Status is IN_PROGRESS → check if CL .tex exists, offer to resume or regenerate
   - If CL Status is NOT REQUESTED or PENDING → proceed to Phase 1 (the user explicitly invoked `/make-cl`, so generate it now)

---

## Phase 1: Load Context

Read in this order:
1. **Session file** — specifically: Company Context, Framing Strategy, ATS Keywords. (There is normally **no** pre-written Cover Letter Plan — `/make-resume` does not produce one. **Build the CL plan now** from Company Context + Framing Strategy + bundle S5: institution type, paragraph structure, P1 hook, jargon level, "why them" angle. If Company Context is thin, do 1-2 quick web searches.)
2. **Finished resume .tex** — path from session file Output Files. Read to understand what the CL must complement.
3. `resume_builder/reference/cl_reference.md` — CL format rules, paragraph templates, anti-patterns
4. `resume_builder/support/ai_fingerprint_rules.md` — Banned words, structural rules (CLs are most vulnerable)
5. The matching bundle from session file role type → `resume_builder/bundles/bundle_[role_type].md` — Section 5 (Cover Letter)
6. All significance files from `resume_builder/support/significance_*.md`

Update session file Status: `Cover Letter: IN_PROGRESS`

Progress: "Loading CL context — [company], [role type] bundle, [institution type]..."

---

## Phase 2: Generate Cover Letter

Read `resume_builder/templates/coverletter_template.tex`.

**Institution type** (from the CL plan you built in Phase 1):
- Industry → 3 paragraphs, 250-300 words
- Startup → 3 paragraphs, 200-250 words (shorter, more direct)

**Generate CL following cl_reference.md paragraph structure:**
- Use significance files for field-context depth (NOT resume bullet text)
- Use the "why them" angle and hooks from your Phase 1 plan / session Framing Strategy
- Ensure every major claim is traceable to a resume bullet
- Open with a specific reference to their work — no generic openers
- Weave credentials into body paragraphs, not closing

Save to `output/<FolderName>/cover_letter_<FolderName>.tex`

Progress: "Writing [institution type] cover letter — [N] paragraphs, targeting [N] words..."

### CL Hook Verification Gate (MANDATORY before presenting to user)

Web-search every hook used in the CL:
- Industry: product, technology, or company news referenced
- Startup: product, funding stage, or tech stack referenced

Present evidence as:
> **Claim:** [what the CL says] → **Evidence:** [what the search found] → **Source:** [URL]

Flag any unverified item: **"UNVERIFIED — please confirm"**

Do NOT present the CL draft to the user until all hooks are verified or flagged.

---

## Phase 3: Compile & Verify

```bash
pdflatex -interaction=nonstopmode -output-directory=output/<FolderName> output/<FolderName>/cover_letter_<FolderName>.tex
```

Use Read tool to view compiled PDF. Verify:

| Gate | Check | If FAIL |
|------|-------|---------|
| Word count | Industry 250-300, Startup 200-250 | Trim/expand |
| Page count | Resume package: 1 page | Adjust content |
| Page fill | 1pg: well-filled. 2pg: page 2 >= half filled before signature | Adjust |
| Anti-patterns | No generic opener, no defensive framing, no credential dump | Rewrite |
| Package cohesion | CL claims traceable to resume bullets, no contradictions | Fix |
| Compile | Clean pdflatex | Fix LaTeX errors |

Update session file:
- Add CL to Output Files
- Status: `Cover Letter: DONE`
- Add Next Critique command
- **Write/overwrite the Phase Handoff block** — next phase = `/critique`; list files `/critique` needs (session file, finished resume .tex, finished CL .tex, bundle); write the cold-restart command.

Progress: "Compiled — 1 page, 278 words. Package cohesion verified."

### >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<
Present: CL summary (word count, page count, key hooks used).
**You MUST wait for the user's explicit text response before continuing.**

If user requests changes: apply them, re-compile, re-verify. Update session file.
If user approves: update Status, present next command.

**Do NOT trigger file organization** — that happens after `/critique` approval.

"Cover letter done. Next steps:
1. /clear
2. [exact /critique command with session file path]"

## Voice Signal Capture

If the user corrects any CL phrasing during this session:
- Append an entry to `output/CL_VOICE_SIGNALS.md` (create if missing)
- Format: see `resume_builder/support/cl_voice_signals.md` for schema
- Capture the user's exact preferred wording so future CLs match their voice
