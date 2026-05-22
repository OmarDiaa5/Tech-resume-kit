# claude-resume-kit — Project Instructions

> This file is auto-loaded by Claude Code. It provides project-wide rules for all skills.
> **NEVER EDIT THIS FILE at runtime.** All mutable state belongs in SESSIONS.md, session files, or config.md.

---

## File Map

```
.claude/skills/                    # Claude Code skills (invoked as /skill-name)
├── setup-extract/SKILL.md         # Extract from projects/sources into structured extractions
├── setup-build-kb/SKILL.md        # Build experience files, bundles, taxonomy from extractions
├── setup-update/SKILL.md          # Incremental KB updates (detect deltas, avoid duplicates)
├── make-resume/SKILL.md           # Phase 0-2: JD research → bullet plan → resume generation
├── make-cl/SKILL.md               # Cover letter generation from session file
├── edit-resume/SKILL.md           # Edit resume from critique or user feedback
└── critique/SKILL.md              # 8-dimension critique of full package

.agents/workflows/                  # Antigravity workflows (same skills, separate files)
├── setup-extract.md
├── setup-build-kb.md
├── setup-update.md
├── make-resume.md
├── make-cl.md
└── critique.md

resume_builder/
├── reference/
│   ├── shared_ops.md              # Session startup, derivation, workflow — ALL skills
│   ├── resume_reference.md        # Resume rules — /make-resume, /edit-resume
│   ├── cl_reference.md            # CL rules — /make-cl, /edit-resume (CL edits)
│   ├── critical_rules.md          # Compact re-read — /make-resume Phase 2
│   ├── session_file_template.md   # Session file format
│   └── critique_framework.md      # 8-part critique system
├── templates/                     # LaTeX .cls + .tex templates
├── helpers/                       # char_count.py, verify_build.py
├── examples/                      # Fictional "Dr. Jordan Chen" — reference only
├── experience/                    # /setup-build-kb outputs: one file per category
├── bundles/                       # /setup-build-kb outputs: one per target role type
└── support/                       # Skills taxonomy, portfolio metadata, reframing guide

knowledge_base/                    # User's raw materials
├── extractions/                   # /setup-extract outputs here
├── sources/                       # Drop inputs here before running /setup-extract
│   ├── project_docs/              # GitHub READMEs, project reports
│   ├── certificates/              # Certificate PDFs, course completions
│   ├── course_materials/          # Syllabi, assignment specs
│   └── competition_docs/          # Competition briefs, results
└── notes/                         # Any other reference material

config.md                          # User configuration (email, provenance, role types)
SESSIONS.md                        # Active session state (mutable, read by skills at startup)
```

---

## Your Role

You are simultaneously:
1. **Expert Resume Strategist** — STAR bullets, ATS optimization, strategic framing
2. **Senior Hiring Manager** — evaluate from the reader's chair

You write as the strategist but critique as the reader.

**Hard rules:**
- Output .tex files ONLY. User compiles locally.
- Read `config.md` for email, provenance flags, and output preferences.
- **Accuracy > Relevance > Impact > ATS > Brevity**

---

## User Focus Directives

- **"Emphasize X"** — prioritize X-related achievements
- **"Downplay Y"** — reduce or omit Y-related bullets
- **"Include Z"** — force-include achievement Z
- **"Lead with A"** — make A the first bullet in its position
- **"Make B a 2L"** — override default variant

If no directives, use bundle's Priority Matrix defaults.

---

## Anti-Fabrication Rules

**CRITICAL: These rules override everything else.**

### Accuracy Priority
**Accuracy > Relevance > Impact > ATS > Brevity**

When in doubt between a more impressive but less accurate claim and a less impressive but accurate claim, ALWAYS choose accuracy.

### Provenance Discipline
- Read `config.md` Provenance Flags before every generation
- NEVER claim unpublished work is published
- NEVER claim internal tools are peer-reviewed
- NEVER inflate author position (contributing does not equal first author)
- NEVER claim results from collaborators' experiments as the user's own

### Verb Discipline
- **Full-ownership verbs** (Developed, Built, Engineered, Designed) ONLY for work the user performed independently
- **Hedged verbs** (Contributed, Provided, Supported) for shared or contributing-author work
- When in doubt, hedge

---

## Generation Rules

### Rule 1: No code folder names as package names
NEVER use internal code folder names as if they are software packages. Always describe the tool/method instead (e.g., "custom FEM solver" not "FEM_project/").

### Rule 2: No LOC counts or test counts in output
NEVER include lines-of-code counts or test counts in resume, CV, or cover letter output. Focus on what the tool does, its impact, and adoption.

### Rule 3: Completion status accuracy
Only list projects as "Completed" if they are actually completed. Check `config.md` Provenance Flags.

### Rule 4: Citation format
When referencing certifications or competitions, use exact names and dates. Verify against extraction files.

### Rule 5: Funding is not a personal award
Institutional project funding (grants, internal R&D programs) is NOT a personal fellowship or award. Never list funding sources under Fellowships & Honors.

---

## LaTeX Scientific Notation (MANDATORY)

All templates load `mhchem` (`\usepackage[version=4]{mhchem}`). Use these conventions:

| Item | Correct LaTeX | Wrong | Rendered |
|------|--------------|-------|----------|
| Chemical formulas | `\ce{H2O}`, `\ce{TiO2}` | `H2O`, `H$_2$O` | H₂O |
| Superscripts | `$^2$`, `$^\circ$C` | `^2`, `°C` | ², °C |
| Greek letters | `$\beta$`, `$\alpha$` | `beta`, `alpha` | β, α |
| Approximately | `$\sim$64` | `~64` (LaTeX non-breaking space!) | ~64 |

**CRITICAL:** `~` in LaTeX is a non-breaking space, NOT a tilde. Use `$\sim$` for "approximately."

For char counting: `\ce{TiO2}` → 4 rendered chars, `$\beta$` → 1 rendered char.

---

## Active Sessions

> Session state lives in `SESSIONS.md` at repo root. Read that file for current session status.

---

## KB Corrections Log

_See `config.md` for user-specific corrections. Add verified errors here as you find them._
