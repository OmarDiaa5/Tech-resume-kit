# CV (5-page) — Reference

> **OPT-IN ONLY.** Load this file *only* when a JD explicitly asks for a multi-page academic CV.
> The default deliverable is a resume — see `resume_reference.md`. Most tech JDs never need this file.
> Companion: `resume_reference.md` (shared section/provenance/LaTeX rules apply here too).

---

## CV Budget Card

```
CV (5-page, cv.cls): 19-21 variable bullets (45 rendered lines) | Skills 17 lines (4-4-3-3-3)
CV bullet: max 3 rendered lines | 2L: 168-182 chars | 3L: 250-268 chars (target ~175 / ~260)
CV + cover letter (if requested): 6-7 pages total
```

## CV Character Limits (11pt, textwidth=7.5in) — verified by `char_count.py -f cv`

| Target Lines | Rendered Char Range | HARD MAX | Orphan Threshold |
|-------|---------------|---------|------------------|
| 1 line | 88-93 chars | 101 | -- |
| 2 lines | 168-182 chars | 190 | Last line >= 65 chars |
| 3 lines | 250-268 chars | 280 | Last line >= 65 chars |

**Bold width penalty (CV, 11pt):** Effective limit = 91 - (0.25 x bold_char_count).
Aim for the middle of the range, never the hard max — wide chars (m, w, capitals, em-dashes) overflow a max-length line.

## CV Section Specs (cv.cls)

1. **Research Summary** (bundle S2): exactly 6 body lines, 500-540 rendered chars (HARD MAX 545, floor ~490). Orphan: last line >= 62 chars. Technical identity, not narrative.
2. **Education**: FIXED — copy verbatim from `cv_template.tex`.
3. **Technical Expertise** (bundle S4 + skills_taxonomy): 4-4-3-3-3 ALWAYS (17 body lines).
4. **Research Experience**: exactly **45 rendered bullet lines** across 19-21 bullets, plus sub-theme lines.
   - cv.cls: args 3+4 on SEPARATE italic lines.
   - Max 3 rendered lines per bullet.
5-10. **Fellowships & Honors, Presentations, Mentorship, Collaborations, Computing**: all FIXED — copy verbatim from `cv_template.tex`.

> This early-career profile has **no Publications section** — do not add one to the CV.

## CV Page Budget — LOCKED

Total: ~209 rendered text lines across 5 pages; 1-2 lines slack at the bottom of page 5 is acceptable.

| Category | Status |
|----------|--------|
| Header, Education, Honors, Presentations, etc. | FIXED (count from template) |
| Research Summary | JD-dependent (typically 7 lines: 1 heading + 6 body) |
| Technical Expertise | JD-dependent (typically 18 lines: 1 heading + 17 body) |
| Experience bullets | JD-dependent (**target 45 rendered lines**, 19-21 bullets, 2L/3L mix) |

**Bullet mix options (45 rendered lines):** 18×2L + 3×3L = 21 | 15×2L + 5×3L = 20 | 12×2L + 7×3L = 19.
Allocate more bullets to JD-relevant positions.

**Sub-theme rebalancing:** to shift weight toward a more JD-relevant sub-theme: (a) drop the weakest bullet from a less-relevant sub-theme (-2L), or (b) split a high-content 3L into two 2L bullets (+1L). Never split a 2L bullet.

**CV Page 1 rule:** the FIRST bullet of the FIRST experience position MUST be 2L (not 3L). A 3L first bullet pushes content below the page-1 fold. Plan this in bullet planning.

**Position header rule:** position title + date must fit ONE line; shorten the title if the date wraps.

## Files to Upload (CV)

1. `bundle_[role_type].md` (Sections 1-5)
2. `achievement_reframing_guide.md`
3. `skills_taxonomy.md`
4. `cv.cls` + `cv_template.tex`
5. Experience files from `resume_builder/experience/`
