# Tech Resume Kit — Patch for claude-resume-kit

This folder contains all the files needed to convert the original [claude-resume-kit](https://github.com/ARPeeketi/claude-resume-kit) from a **researcher/academic** paradigm into a **tech professional** paradigm — optimized for software engineers, ML engineers, data scientists, and similar technical roles.

## What Changed

The original repo is designed for researchers with papers, publications, Google Scholar profiles, and academic grant funding. This patch replaces that with:

- **Projects** instead of Publications
- **Technical Skills** categorized by domain (Languages, ML/DL, CV, NLP, Cloud/MLOps)
- **Certifications & Training** instead of Selected Publications
- **Leadership & Activities** instead of Honors & Awards
- **Competitions** tracked with placement and key achievements
- **Portfolio metadata** (repos, tech stacks, metrics) instead of paper metadata
- **Incremental Updates** via the `/setup-update` skill to avoid duplicating extraction work
- **Lightweight Provenance Checkpoints:** The AI asks for evidence when it spots weak claims during generation
- **Voice/Edit Signals:** The AI learns your wording preferences from cover letter and resume edits
- **Token Optimization:** Session state is isolated in `SESSIONS.md` to keep `CLAUDE.md` context small

## How to Apply

### 1. Clone the Original Repo

```bash
git clone https://github.com/ARPeeketi/claude-resume-kit
cd claude-resume-kit
```

### 2. Copy This Patch

Copy the contents of this folder **on top** of the cloned repo. All paths match the repo structure:

```bash
# From the parent directory containing both folders:
cp -r tech-resume-kit-patch/* claude-resume-kit/
cp -r tech-resume-kit-patch/.agents claude-resume-kit/
cp -r tech-resume-kit-patch/.claude claude-resume-kit/
```

On Windows (PowerShell):
```powershell
Copy-Item -Path "tech-resume-kit-patch\*" -Destination "claude-resume-kit\" -Recurse -Force
Copy-Item -Path "tech-resume-kit-patch\.agents" -Destination "claude-resume-kit\" -Recurse -Force
Copy-Item -Path "tech-resume-kit-patch\.claude" -Destination "claude-resume-kit\" -Recurse -Force
```

### 3. Clean Up Old Academic Files

```bash
# Delete the old papers directory (replaced by source_materials/)
rm -rf knowledge_base/papers/

# Delete the old pub_metadata.md (replaced by portfolio_metadata.md)
rm -f resume_builder/support/pub_metadata.md
```

### 4. Fill in Your Info

1. Open `config.md` and replace all `[YOUR ...]` placeholders with your details
2. Fill in your Provenance Flags, Role Types, and Decision Tree
3. Update `resume_builder/templates/resume_template.tex` — fill in the `[FIXED: ...]` and `[CONFIG: ...]` placeholders with your education, certifications, languages, etc.

### 5. Start Building Your Knowledge Base

```
/setup-extract path/to/your/project_readme.md     # Extract each project
/setup-build-kb                                     # Build experience files & bundles
```

## What's Included

```
tech-resume-kit-patch/
├── .agents/                          # Antigravity workflows (for Google Antigravity users)
│   ├── workflows/                    # 5 workflow files
│   ├── helpers/                      # verify_build.py
│   └── rules/                        # Anti-fabrication + Antigravity rules
├── .claude/skills/                   # Claude Code skills (for Claude Code users)
│   ├── setup-extract/SKILL.md
│   ├── setup-build-kb/SKILL.md
│   ├── setup-update/SKILL.md
│   ├── make-resume/SKILL.md
│   ├── make-cl/SKILL.md
│   ├── edit-resume/SKILL.md
│   └── critique/SKILL.md
├── resume_builder/
│   ├── reference/
│   │   ├── critique_framework.md     # Tech-focused scoring (Projects & Portfolio weight)
│   │   └── shared_ops.md            # Updated session workflow
│   ├── templates/
│   │   └── resume_template.tex      # Tech resume layout (Projects, Skills, Certs)
│   └── support/
│       ├── portfolio_metadata.md     # Template: tracks repos, competitions, certs
│       ├── skills_taxonomy.md        # Template: skill categories for tech roles
│       └── achievement_reframing_guide.md  # Template: format for role-type framing
├── knowledge_base/
│   ├── extractions/_INVENTORY.md     # Empty inventory with tech-oriented columns
│   ├── sources/                      # Organized folders for input materials
│   │   ├── project_docs/.gitkeep
│   │   ├── certificates/.gitkeep
│   │   ├── course_materials/.gitkeep
│   │   └── competition_docs/.gitkeep
│   └── notes/.gitkeep               # Any other reference material
├── config.md                         # Template with placeholders (fill in your info)
├── SESSIONS.md                       # Master tracker of active sessions
├── CLAUDE.md                         # Updated project instructions
├── DOCS.md                           # Updated documentation
└── README.md                         # This file
```

## Works With Both Claude Code and Antigravity

This patch maintains **dual workflow support**:
- **Claude Code** users: invoke skills via `/setup-extract`, `/make-resume`, etc.
- **Antigravity** users: use the `.agents/workflows/` versions

Both systems read the same knowledge base and config files. They do not interfere with each other.

## Getting Started Workflow

1. **Extract** your projects: `/setup-extract` on each project README, course syllabus, internship doc
2. **Build** your knowledge base: `/setup-build-kb` synthesizes everything into experience files and bundles
3. **Update** your knowledge base: `/setup-update` whenever you finish a new project or earn a cert
4. **Generate** a resume: `/make-resume JDs/your_jd.txt` tailors a resume to a specific job
5. **Generate** a cover letter: `/make-cl output/<Folder>/session_<name>.md`
6. **Critique** the package: `/critique output/<Folder>/session_<name>.md`
