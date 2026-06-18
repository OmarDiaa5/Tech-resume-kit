---
name: setup-update
description: Incrementally update sources, extractions, and KB outputs without duplicating existing work
user-invocable: true
---

# /setup-update

**User input:** `$ARGUMENTS`

Purpose:
Run an incremental update cycle after initial setup, avoiding duplicate extractions and unnecessary rebuilds.

Parse $ARGUMENTS:
- Empty: full incremental scan (sources + extraction candidates + selective rebuild plan)
- `sources`: intake and classify only new/changed sources
- `extract`: run/update extraction candidates only
- `build`: rebuild affected KB artifacts only
- `status`: show current delta status and source freshness

---

## Startup

1. Read `CLAUDE.md`.
2. Read `config.md` (must exist and be populated).
3. Read `knowledge_base/extractions/_INVENTORY.md` (must exist).
4. Scan these locations and build a baseline map:
   - `knowledge_base/extractions/`
   - `knowledge_base/sources/`
   - `resume_builder/experience/`
   - `resume_builder/bundles/`
   - `resume_builder/support/`

If config.md or _INVENTORY.md is missing, stop and tell user to set up first.

---

## Phase 0: Delta Detection

Classify each candidate source as one of:
- **NEW**: no matching extraction found in _INVENTORY.md
- **CHANGED**: source exists but extraction appears outdated (compare dates, content)
- **COVERED**: already extracted and up-to-date
- **UNSURE**: potential overlap; needs user confirmation

Matching heuristics:
- Extraction filename / source title similarity
- Dates in _INVENTORY.md vs source file timestamps
- Tech stack overlap between sources and existing extractions

Required output table:

| Candidate | Source Path | Status | Rationale | Recommended Action |
|-----------|-------------|--------|-----------|-------------------|
| ... | ... | NEW/CHANGED/COVERED/UNSURE | ... | extract/update/skip |

### >>>> MANDATORY STOP — DO NOT PROCEED <<<<
Present the delta table and ask:
1. Which items to extract (NEW/CHANGED)?
2. Which to skip?
3. Any items to merge as one extraction?
**You MUST wait for the user's explicit text response before continuing.**

---

## Phase 1: Selective Extraction

For each confirmed NEW/CHANGED item:
1. Run the extraction logic from `/setup-extract` (same format, same provenance rules — including the required per-item `Date:` field)
2. Update `_INVENTORY.md` **per-item router**: add or rewrite the row for this specific item with its file + line range, date, status, primary tech, and one-line summary. If line ranges of other items shifted because of the edit, refresh those too.
3. Mark the extraction date

For CHANGED items:
- Show the diff between old and new extraction
- Ask user to confirm the update before overwriting

---

## Phase 2: Selective Rebuild

After extraction, check which KB outputs are affected:

1. **Experience files** (`resume_builder/experience/`) — rebuild only files whose source extractions changed. When loading source content, use the per-item line ranges from `_INVENTORY.md` rather than reading whole extraction files.
2. **Bundles** (`resume_builder/bundles/`) — rebuild only if the priority matrix changed
3. **Skills taxonomy** (`resume_builder/support/skills_taxonomy.md`) — rebuild if new tech was extracted
4. **Portfolio metadata** (`resume_builder/support/portfolio_metadata.md`) — rebuild if new projects/certs added
5. **Achievement reframing guide** (`resume_builder/support/achievement_reframing_guide.md`) — add entries for new achievements only

Present rebuild plan:

| KB File | Affected By | Action |
|---------|-------------|--------|
| ... | [extraction that changed] | rebuild / add entries / skip |

### >>>> MANDATORY STOP — DO NOT PROCEED <<<<
Ask user to confirm rebuild plan.

---

## Phase 3: Execute Rebuild

Rebuild confirmed files following the same logic as `/setup-build-kb` but only for affected entries.

Do NOT rebuild files that aren't affected by the delta.

---

## Completion

Output summary:
- Extractions added/updated: [count]
- KB files rebuilt: [list]
- Unchanged: [list]
