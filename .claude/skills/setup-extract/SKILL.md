---
description: Extract structured information from projects, courses, competitions, internships, or other experience sources into knowledge base extractions
user-invocable: true
---

# /setup-extract

**User input:** `$ARGUMENTS`

Parse `$ARGUMENTS`:
- File path to a source (e.g., `sources/project_docs/readme.md`, `sources/certificates/cert.pdf`) → read that file
- URL to a GitHub repo (e.g., `https://github.com/user/repo`) → fetch and read repo README / docs
- Multiple paths/URLs separated by spaces → batch mode (process each sequentially)
- Empty → ask the user for the source path, URL, or paste content

---

## Startup

1. Read `CLAUDE.md` — check KB Corrections Log for known issues
2. Read `config.md` — load Personal Info (to identify user's role and involvement), Provenance Flags
3. Read `knowledge_base/extractions/_INVENTORY.md` — see what's already extracted, avoid duplicates

If the source is already in the inventory:
- Show the existing extraction path
- Ask: "This source is already extracted. Re-extract (overwrite) or skip?"
- Wait for user response before proceeding

---

## Phase 1: Read & Understand the Source

Read the source using the appropriate method:
- **PDF files:** Use the Read tool (supports PDF reading)
- **Markdown / .tex / text files:** Read directly
- **GitHub repos:** Read README.md, docs/, and key source files for context
- **If multiple formats exist:** Prefer the most detailed source (README > PDF > summary)

**While reading, collect:**
1. Project/experience title, dates, source type (project | course | competition | internship | certification)
2. Repo URL (if applicable, e.g., GitHub link)
3. Tech stack — languages, frameworks, libraries, tools, platforms
4. Team info — team size, user's role, other contributors
5. All computational methods, techniques, software, and frameworks mentioned
6. Quantitative results — accuracies, speedups, metrics, improvements over baselines
7. Novelty claims — "first-ever", "new framework", "novel approach", etc.
8. Collaboration indicators — other team members, organizations, shared resources

Progress: "Reading source... [title] ([source type])"

---

## Phase 2: Clarify User's Role

If the user's contribution is not obvious from the source (common for team projects), ask:

**Questions to ask (skip any that are already clear from the source):**
1. "What was your role? (sole developer, team lead, co-developer, contributor)"
2. "What did you build? (models, pipelines, apps, tools)"
3. "Were there other team members? What was your specific responsibility?"
4. "Any quantitative results you can personally claim? (e.g., 'I built the entire ML pipeline')"
5. "Is there anything that should NOT appear on your resume? (e.g., teammate's contribution)"

### >>>>>> MANDATORY STOP — DO NOT PROCEED <<<<<<
Present your understanding of the source and ask the clarifying questions above.
**You MUST wait for the user's explicit text response before continuing.**

---

## Phase 3: Write Extraction

Create the extraction file at `knowledge_base/extractions/<topic_descriptor>.md`

**Naming convention:** `<topic>_<2-3_word_descriptor>.md`
- Examples: `drone_capstone.md`, `aic4_tracker.md`, `depi_courses.md`, `kaggle_nlp_competition.md`
- Normalize to lowercase with underscores

**Extraction format:**

```markdown
# [Full Title]

## Metadata
- **Source type:** [project | course | competition | internship | certification]
- **Dates:** [date range]
- **Repo:** [GitHub URL or N/A]
- **Your role:** [sole developer | team lead | co-developer | contributor]
- **Team size:** [N or solo]
- **Status:** [completed | in-progress | ongoing]

## Methods & Tools
- **Computational methods:** [e.g., deep learning, NLP, computer vision, web scraping, data pipelines, etc.]
- **Software/frameworks:** [e.g., PyTorch, React, FastAPI, Docker, custom code, etc.]
- **Hardware/infrastructure:** [if mentioned — cloud, GPU resources, edge devices, etc.]
- **Key techniques:** [specific methodological details that map to resume skills]

## Key Results
[Number each result. Include quantitative metrics wherever possible.]
1. [Result with numbers — e.g., "Achieved 94% accuracy on test set, +8% over baseline"]
2. [Result — e.g., "Reduced inference latency from 200ms to 45ms"]
3. [...]

## Novelty Claims
[What's genuinely new — be precise, avoid overclaiming]
- [e.g., "First application of framework X to problem Y"]
- [e.g., "New pipeline combining A and B — no prior open-source implementation"]

## Collaboration & Scope
- **Other team members/organizations:** [teammates, mentors, partner orgs involved]
- **User's specific contribution:** [from Phase 2 clarification]
- **Shared vs. sole work:** [what the user did alone vs. with others]

## Provenance Notes
- **Completion status:** [matches config.md if listed there]
- **Safe to claim:** [what the user can put on a resume without hedging]
- **Needs hedging:** [claims that require "contributed to" or "supported" framing]
- **Do NOT claim:** [results from teammates, claims that would be overclaiming]

## Resume Bullet Seeds
[3-5 draft bullets in STAR format. These are seeds, not final text.]
[Use full-ownership verbs only for sole-contributor work. Hedge for shared work.]
1. [Action verb] + [what was done] + [quantitative result/impact]
2. [Action verb] + [method/tool developed] + [what it enabled]
3. [Action verb] + [scope — e.g., "across N systems"] + [outcome]
4. [Optional: collaboration-framed bullet]
5. [Optional: tool/infrastructure bullet]
```

Save the file. Show the user the complete extraction.

Progress: "Writing extraction for [short title]... [N] results identified, [M] bullet seeds drafted"

---

## Phase 4: Update Inventory

Read and update `knowledge_base/extractions/_INVENTORY.md`.

Add a row to the inventory table:

```
| [filename] | [short title] | [source type] | [your role] | [status] | [primary tech] | [date extracted] |
```

Present the updated inventory entry to the user.

---

## Phase 5: Next Steps

After extraction is complete, present:

1. **Extraction summary:** [N] methods, [M] quantitative results, [K] bullet seeds
2. **Provenance flags:** Any items that need special handling
3. **Suggested next action:**
   - If more sources to extract: "Run `/setup-extract [next source path]`"
   - If all sources done: "Run `/setup-build-kb` to synthesize extractions into experience files and bundles"

### >>>>>> MANDATORY STOP <<<<<<
Present extraction summary. Wait for user feedback or next source.
**You MUST wait for the user's explicit text response before continuing.**

---

## Batch Mode

If `$ARGUMENTS` contains multiple file paths or URLs:
1. Process each source through Phases 1-4 sequentially
2. Ask Phase 2 clarifying questions for ALL sources at once (grouped) before writing any extractions
3. After all extractions: present combined inventory update and summary
4. Single STOP at the end (not per source)
