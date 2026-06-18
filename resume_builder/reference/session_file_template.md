# Session File Template

Every JD gets a persistent session file: `output/<FolderName>/session_<name>.md`

## Template

```markdown
# Session: [Company] [Role Title]

## JD Info
- **File:** JDs/[file].txt
- **Role:** [title]
- **Company:** [company] ([context])
- **Bundle:** [role_type]
- **Format:** [Resume/CV] ([N]-page, [cls]) + [N]-page cover letter
- **Salary/Details:** [if available]

## JD Analysis
### Requirements
| # | Requirement | Match | Evidence |
|---|-------------|-------|----------|
| 1 | ... | Direct/Bridge/Gap | ... |

### ATS Keywords
- **ML/AI:** ...
- **Domain:** ...
- **Methods:** ...
- **Tools:** ...
- **Soft Skills:** ...

### Gap Assessment
- **Direct:** [list]
- **Bridge:** [list with confidence]
- **Gap:** [list -- what we can't claim]

## Company Context
- **Mission:** ...
- **This role:** Why it exists, what success looks like
- **Culture:** ...
- **"Why them" angle:** ...

## Framing Strategy
- **Lead narrative:** ...
- **Reframing map:** [domain term] → [JD term]
- **Emphasize:** ...
- **Downplay:** ...
- **CL hooks:** ...
- **User directives:** ...

## Critique Context (captured in Phase 0, used in /critique)
- **Reviewer persona:** Who reads this? Their title, daily work, what impresses/bores them
- **Competitive landscape:** Who else applies? What does the "obvious fit" have that we don't?
- **Domain vocabulary:** What terms separate insider from outsider at THIS company?

## Cover Letter Plan
- **Institution type:** Industry / National Lab / Academic
- **Paragraph count:** [N] paragraphs, [word count target]
- **P1 hook:** [specific product/paper/program to reference]
- **P2-P3 evidence:** [which achievements to highlight, how to frame]
- **Domain pivot:** [methodology bridge sentence, if pivoting]
- **Jargon level:** HR-safe / Technical / Academic
- **"Why them" hook:** [specific connection to their work]

## Bullet Plan

Note: Any FIXED positions (e.g., internships) are not included in this plan.

### Position 1 ([N] bullets, [N] rendered lines)
| # | ID | Achievement | Variant | Lines | Rationale |
|---|-----|------------|---------|-------|-----------|

### Position 2 ([N] bullets, [N] rendered lines)
[same table]

### Position 3 ([N] bullets, [N] rendered lines)
[same table]

**Budget:** [N] variable bullets, [N] rendered lines vs target [N]

## Output Files
- Resume: `output/<FolderName>/resume_<FolderName>.tex` (+ `.pdf`)
- Critique: `output/<FolderName>/critique_<name>.md`
- Cover Letter (only if `/make-cl` was run): `output/<FolderName>/cover_letter_<FolderName>.tex`

## Critique Summary
- **Score:** [N]/100
- **Key findings:** ...
- **Tier 1 fixes:** ...

## Edit History
### Edit [N] ([date]): [description]
- Changes: ...
- Source: [critique item # / user request / auto-detected]
- Verification: [gates passed]

## Phase Handoff

> **REQUIRED — overwritten at the end of EVERY phase by every skill.** A cold restart (new chat, post-/clear) reads only the session file and this block; with it, the next phase needs zero re-derivation.

- **Last completed:** [phase name, e.g., "make-resume Phase 1"]
- **Next phase:** [phase name, e.g., "make-resume Phase 2"]
- **Files the next phase needs to read (and ONLY these):**
  - [path1] — [one-line reason]
  - [path2] — [one-line reason]
- **Decisions already locked (do NOT re-derive):**
  - Role type: [value]
  - Bundle: [path]
  - Framing strategy: [1–2 lines]
  - Bullet plan: see Bullet Plan section above
- **External lookups already done (do NOT repeat):**
  - Web searches: [list of queries already run, with one-line conclusion]
  - JD: parsed, copied to [path]
- **Resume instruction for a cold new chat:** "[one-sentence command, e.g., 'Continue /make-resume Phase 2 from this session file. All prior phases are locked.']"

## Status
- Phase 0: [PENDING | DONE]
- Phase 1: [PENDING | DONE (N bullets confirmed)]
- Phase 2 Resume:
  - Summary: [PENDING | DONE]
  - Skills: [PENDING | DONE]
  - Position 1 ([N] bullets): [PENDING | DONE | IN_PROGRESS]
  - Position 2 ([N] bullets): [PENDING | DONE | IN_PROGRESS]
  - Position 3 ([N] bullets): [PENDING | DONE | IN_PROGRESS]
  - Compile: [PENDING | DONE]
- Cover Letter: [NOT REQUESTED | IN_PROGRESS | DONE]  ← stays NOT REQUESTED unless the user runs /make-cl
- Critique: [PENDING | IN_PROGRESS | CURRENT (score) | STALE]
- **Next (optional):** /critique output/<FolderName>/session_<name>.md
- **Cover letter (only if wanted):** /make-cl output/<FolderName>/session_<name>.md

## Evidence Tracking

> Populated during `/make-resume` and `/critique` when the AI identifies gaps or low-confidence claims and asks the user for evidence.

### [Date] — [Gap/Phrase Name]
**Source:** [Make-Resume Phase 1 / Critique / Edit-Resume]
**Question:** [What was asked]
**User Response:** [What the user said]
**Confidence:** high / medium / low
**Action:** kept / strengthened / reworded / removed / recorded-to-KB
```

## Context Efficiency Notes

- Session 1 (resume): resume_reference.md + experience files + bundle + support files + template. Peak depends on knowledge base size.
- Critique (optional): critique_framework.md (Part 3 only in Quick Mode) + session file + resume .tex + bundle. Moderate context.
- Cover letter (optional, only on /make-cl): cl_reference.md + significance files + session file + resume .tex + bundle S5. Light context.
- Folder created in Phase 0 — all files go to output/<FolderName>/ from the start.
