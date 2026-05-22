# Documentation

Detailed reference for claude-resume-kit. For the quick overview, see [README.md](README.md).

---

## Architecture

```
claude-resume-kit/
├── CLAUDE.md                          # Auto-loaded project instructions
├── config.md                          # Your personal configuration
├── SESSIONS.md                        # Master tracker of all active sessions
├── .claude/skills/                    # 7 Claude Code skills (invoked as /skill-name)
│   ├── setup-extract/SKILL.md         # Extract from projects/sources → structured data
│   ├── setup-build-kb/SKILL.md        # Synthesize KB from extractions
│   ├── setup-update/SKILL.md          # Incremental KB updates (detect deltas)
│   ├── make-resume/SKILL.md           # JD → tailored resume (.tex)
│   ├── make-cl/SKILL.md               # Session → cover letter (.tex)
│   ├── edit-resume/SKILL.md           # Edit from critique/feedback
│   └── critique/SKILL.md              # Independent quality review
├── .agents/workflows/                 # Antigravity workflows (same content)
│   ├── setup-extract.md
│   ├── setup-build-kb.md
│   ├── setup-update.md
│   ├── make-resume.md
│   ├── make-cl.md
│   └── critique.md
├── resume_builder/
│   ├── reference/                     # Generation rules and protocols
│   │   ├── shared_ops.md              # Session workflow (all skills read this)
│   │   ├── resume_reference.md        # Resume formatting rules
│   │   ├── cl_reference.md            # Cover letter rules
│   │   ├── critical_rules.md          # Compact re-read for generation phase
│   │   ├── session_file_template.md   # Session file format spec
│   │   └── critique_framework.md      # 8-part critique system
│   ├── templates/                     # LaTeX .cls classes + .tex templates
│   ├── helpers/                       # char_count.py, verify_build.py
│   ├── examples/                      # Fictional "Dr. Jordan Chen" — reference only
│   ├── experience/                    # YOUR experience files (built by /setup-build-kb)
│   ├── bundles/                       # YOUR role-type bundles (built by /setup-build-kb)
│   └── support/                       # Skills taxonomy, portfolio metadata, AI fingerprint rules
├── knowledge_base/
│   ├── extractions/                   # Source extractions (built by /setup-extract)
│   ├── sources/                       # Drop inputs here before running /setup-extract
│   │   ├── project_docs/              # GitHub READMEs, project reports
│   │   ├── certificates/              # Certificate PDFs, course completions
│   │   ├── course_materials/          # Syllabi, assignment specs
│   │   └── competition_docs/          # Competition briefs, results
│   └── notes/                         # Any other reference material
├── output/                            # Generated .tex files, session files, critiques
└── JDs/                               # Job descriptions (text files)
```

---

## Concepts

### Session Files

Every JD gets a session file (`output/<Folder>/session_<name>.md`) that tracks:
- JD analysis and ATS keywords
- Which bundle was selected
- Bullet plan (which achievements, in what order, at what length)
- All generation decisions and their rationale
- Cover letter plan
- Critique scores

All 4 generation skills read and update this file. It's the single source of truth for each application.

### Experience Files

One file per experience category (e.g., `experience_projects_ai.md`, `experience_internships.md`). Each achievement has:
- **Source project** with repo link
- **Methods and tools** used
- **Quantitative results**
- **Pre-written bullet variants** (2-line and 3-line)
- **Tags** for which role types this achievement is relevant to
- **Significance** context for cover letters

### Role-Type Bundles

One file per target audience (e.g., `bundle_academic.md`). Each bundle contains:
- **S1: Role Profile** — what this audience values, positioning strategy
- **S2: Summary Guide** — how to write the summary for this role type
- **S3: Achievement Reframing Map** — priority ranking of your achievements for this audience
- **S4: Skills Guide** — which tools to bold, which to include, grouping strategy
- **S5: Cover Letter Guide** — opening hooks, paragraph templates, anti-patterns

### Provenance Flags

The system enforces accuracy through provenance tracking in `config.md`. Every achievement is tagged with its completion status. The skills check this table before every output and will never:
- Claim incomplete work is completed
- Claim personal projects are peer-reviewed publications
- Use full-ownership verbs for shared work
- Inflate contribution level

### The Critique System

The `/critique` skill runs a multi-part assessment:
1. **Domain-Specialist Lens** — reviewer persona, gap analysis, competitive landscape
2. **Five-Perspective Read-Through** — ATS bot, recruiter (10s), HR (30s), hiring manager (2min), technical reviewer (10min)
3. **Eight-Dimension Scoring** — weighted score out of 100
4. **Interview Likelihood** — per-reader probability estimates
5. **Tiered Improvements** — ranked by point impact
6. **Interview Bridge Points** — resume-to-interview talking points
7. **Cover Letter Critique** — 6 sub-checks (anti-patterns, tailoring, context-specific, ATS keywords, structural, package cohesion)
8. **Post-Generation Verification** — mechanical and content checklists including AI fingerprint scan

---

## Three-Session Workflow

For best results, use a **separate Claude Code session** for each step. This gives each skill fresh context, which produces better quality (especially for critique — you want fresh eyes, not the same context that generated the resume).

```
Session 1:  /make-resume JDs/job.txt     → resume/CV .tex
            /clear
Session 2:  /make-cl                      → cover letter .tex
            /clear
Session 3:  /critique                     → critique .md with score
            /clear
            /edit-resume                  → refined .tex (if needed)
```

---

## Customization

### Everything in `config.md` (edit directly)

| Setting | What it controls | Example |
|---------|-----------------|---------|
| **Personal Info** | Name, email, phone, links on all outputs | Your contact details |
| **Document Preferences** | Page counts, bullet line variants, skills layout | `Resume: 2 pages, CV: 5 pages` |
| **Provenance Flags** | What claims are safe to make | `Drone project: in-progress → never say "completed"` |
| **Role Types** | Target audiences and their bundles | `ML Engineer (Tier 1), AI Engineer (Tier 2)` |
| **Decision Tree** | How JD keywords map to role types | `"deep learning, model training" → ML Engineer` |
| **FIXED Sections** | Template sections that never change per JD | `Education, Certifications, Awards` |
| **Output Rules** | Package formats and constraints | `Resume: 2pg + 1pg CL = 3pg package` |
| **KB Corrections** | Errors to never re-introduce | `Spearman is 0.82, not 0.85` |

### LaTeX Templates (edit directly)

- **Fonts, colors, spacing** — modify `.cls` files
- **Section order** — reorder sections in `.tex` templates
- **FIXED content** — fill in education, awards, certifications, header
- **Icons** — replace or remove icons as needed
- **Page geometry** — adjust margins in `.cls` if needed

### Knowledge Base (built by skills, then editable)

| File | How to customize |
|------|-----------------|
| **Experience files** | Edit bullet text, add/remove achievements, adjust tags |
| **Bundles** | Change priority matrices, rewrite summary guides, add role types |
| **Skills taxonomy** | Add/remove skills, change groupings, adjust bold rules |
| **Portfolio metadata** | Update project info, competition results, add new certifications |

### Reference Docs (advanced)

| File | What you'd change |
|------|-------------------|
| `resume_reference.md` | Page budgets, character limits, section specs |
| `cl_reference.md` | Cover letter paragraph templates, word count targets |
| `critical_rules.md` | Generation-time rules tables |
| `critique_framework.md` | Scoring weights, critique dimensions |
| `shared_ops.md` | Session workflow, file derivation logic |

### Skill Prompts (advanced)

Each skill exists in two places: `.claude/skills/<name>/SKILL.md` (Claude Code) and `.agents/workflows/<name>.md` (Antigravity). They share the same content. You can:
- Add STOP points for more user control
- Change the number of web searches in Phase 0
- Adjust how many bullets per position
- Modify the critique scoring weights
- Add new skills for your workflow

> **Note:** When editing skills, update BOTH copies to keep them in sync.

---

## Key Design Decisions

- **Accuracy > Relevance > Impact > ATS > Brevity** — the priority hierarchy for every generation decision
- **LaTeX-only output** — Claude generates `.tex`, you compile locally. No formatting surprises.
- **FLIPPED position format** — the bold line under each position title is a JD-customized theme, not a generic description. This is the strongest tailoring lever.
- **Structured provenance** — every achievement is tracked from source project through extraction to experience file to resume bullet
- **Character-precise budgets** — every bullet is calibrated to fit the template geometry, not "try to keep it short"
- **Session files as state** — all decisions for a JD live in one file. Skills can recover from interruptions.
- **Anti-fabrication by design** — provenance flags, verb discipline, and corrections logs prevent overclaiming even under pressure to impress
- **AI fingerprint avoidance** — a dedicated rules file is loaded by all generation and critique skills, covering banned words and phrases (with technical exceptions), structural anti-patterns, positive markers, and a 12-item post-generation checklist

---

## FAQ

**Q: Do I need to know LaTeX?**
No. Claude generates the `.tex` files. You just compile them (`pdflatex file.tex`). The templates handle all formatting.

**Q: How many projects should I extract?**
All significant projects, internships, competitions, and certifications. Quality matters more than quantity — 5 well-extracted projects beat 20 shallow ones.

**Q: Can I use this for different role types?**
Yes. The framework supports any role type — define them in `config.md`. ML Engineer, AI Engineer, Data Scientist, CV Engineer, and more. Just create appropriate bundles.

**Q: How do I add a new project?**
Run `/setup-extract` on the new source material (GitHub README, project doc, etc.), then update your experience file and bundles. Existing session files are not affected.

**Q: Can I use this with resume formats other than the included templates?**
Yes. The `.cls` files define the visual style. You can modify them or write your own. The skills generate content based on the template structure — update the `[GENERATE: ...]` and `[FIXED: ...]` markers in your template.

**Q: Can multiple people use the same kit?**
Each person needs their own clone with their own `config.md`, knowledge base, and templates. The framework itself is shared; the content is personal.

**Q: What Claude model should I use?**
The skills are designed for Claude's most capable models (Opus, Sonnet). Less capable models may skip steps or produce lower-quality output.
