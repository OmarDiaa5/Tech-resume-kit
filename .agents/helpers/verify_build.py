#!/usr/bin/env python3
"""
Automated validation and linting script for LaTeX resume/CV builds.
Optimized for Google Antigravity to perform autonomous, turn-free corrections.

Usage:
  python3 .agents/helpers/verify_build.py output/ElectroPi/e2e_electropi_intern_resume.tex -f resume
  python3 .agents/helpers/verify_build.py output/Ericsson/e2e_ericsson_cv.tex -f cv
"""

import re
import sys
import json
import argparse
from pathlib import Path


# ==============================================================================
# LaTeX Stripping & Char Counting Engine (Aligned with char_count.py)
# ==============================================================================

def strip_latex(text):
    """Strip LaTeX markup to get rendered text (exactly what a reader sees)."""
    # Remove \item[] prefix
    text = re.sub(r'\\item\s*(\[\s*\])?\s*', '', text)
    # \href{url}{text} -> text
    text = re.sub(r'\\href\{[^}]*\}\{([^}]*)\}', r'\1', text)
    # \textbf{X} -> X
    text = re.sub(r'\\textbf\{([^}]*)\}', r'\1', text)
    # \textit{X} -> X
    text = re.sub(r'\\textit\{([^}]*)\}', r'\1', text)
    # \underline{X} -> X
    text = re.sub(r'\\underline\{([^}]*)\}', r'\1', text)
    # \emph{X} -> X
    text = re.sub(r'\\emph\{([^}]*)\}', r'\1', text)
    # \ce{X} -> X (subscript digits still count as 1 char each)
    text = re.sub(r'\\ce\{([^}]*)\}', r'\1', text)
    # Greek letters -> 1 char each
    greeks = [
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta',
        'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'pi', 'rho', 'sigma',
        'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega',
        'Alpha', 'Beta', 'Gamma', 'Delta', 'Theta', 'Lambda', 'Sigma',
        'Phi', 'Psi', 'Omega',
    ]
    for g in greeks:
        text = text.replace(f'$\\{g}$', 'G')
        text = text.replace(f'\\{g}', 'G')
    # $^\circ$ -> 1 char
    text = re.sub(r'\$\^\{?\\circ\}?\$', 'D', text)
    # $^\dagger$ -> 1 char
    text = re.sub(r'\$\^\{?\\dagger\}?\$', 'D', text)
    # Superscripts: $^{2}$ or $^2$ -> content
    text = re.sub(r'\$\^\{([^}]*)\}\$', r'\1', text)
    text = re.sub(r'\$\^(.)\$', r'\1', text)
    # Subscripts: $_{2}$ or $_2$ -> content
    text = re.sub(r'\$_\{([^}]*)\}\$', r'\1', text)
    text = re.sub(r'\$_(.)\$', r'\1', text)
    # \sim -> 1 char (~)
    text = text.replace('$\\sim$', '~')
    text = text.replace('\\sim', '~')
    text = text.replace('\\textasciitilde', '~')
    # $<$ $>$ -> 1 char
    text = re.sub(r'\$([<>])\$', r'\1', text)
    # --- -> em-dash (1 char but ~2x wide)
    text = text.replace('---', '\u2014')
    # -- -> en-dash (1 char)
    text = text.replace('--', '\u2013')
    # Remove remaining $ (math mode delimiters)
    text = text.replace('$', '')
    # Remove remaining \commands
    text = re.sub(r'\\[a-zA-Z]+\s*', '', text)
    # Remove remaining braces
    text = text.replace('{', '').replace('}', '')
    # Collapse multiple spaces
    text = re.sub(r'  +', ' ', text)
    return text.strip()


def count_bold_chars(text):
    """Count characters inside \\textbf{} commands."""
    return sum(len(m) for m in re.findall(r'\\textbf\{([^}]*)\}', text))


def count_em_dashes(text):
    """Count em-dashes (---) which render ~2x wide."""
    return len(re.findall(r'---', text))


# ==============================================================================
# Validation Engine
# ==============================================================================

def validate_bullet(raw, index, position_name, fmt):
    """Check a single experience bullet against character, bold, and orphan rules."""
    rendered = strip_latex(raw)
    n = len(rendered)
    bold = count_bold_chars(raw)
    
    # Check parameters based on format
    if fmt == 'resume':
        base_limit = 119
        penalty = 0.5
        # Resume strictly supports 2L
        target_lo, target_hi, hard_max, orphan_threshold = 189, 205, 218, 78
        expected_variant = "2L"
    else:  # cv
        # CV allows 1L, 2L, or 3L (we classify and check based on closest tier)
        base_limit = 91
        penalty = 0.25
        if n <= 120:
            expected_variant = "1L"
            target_lo, target_hi, hard_max, orphan_threshold = 88, 93, 101, 0
        elif n <= 220:
            expected_variant = "2L"
            target_lo, target_hi, hard_max, orphan_threshold = 168, 182, 190, 65
        else:
            expected_variant = "3L"
            target_lo, target_hi, hard_max, orphan_threshold = 250, 268, 280, 65

    effective_limit = base_limit - (penalty * bold)
    
    bullet_errors = []

    # 1. Hard character limit check
    if n > hard_max:
        bullet_errors.append({
            "type": "OVER_LIMIT",
            "message": f"Rendered chars ({n}) exceeds the hard maximum ({hard_max}) for {expected_variant} bullet.",
            "fix": f"Trim by {n - hard_max} characters."
        })
    # 2. Short character check (underfill)
    elif n < target_lo and expected_variant != "1L":
        bullet_errors.append({
            "type": "SHORT",
            "message": f"Rendered chars ({n}) is below the target minimum ({target_lo}) for {expected_variant} bullet.",
            "fix": f"Add {target_lo - n} characters of professional detail to fill the line."
        })
    # 3. Orphan threshold check
    elif expected_variant in ("2L", "3L") and orphan_threshold > 0:
        # For a 2L bullet, the last line rendered char count is approximately the remainder of full lines
        # Total line width is ~105-111 chars for resume, ~88-93 chars for CV
        line_width = 111 if fmt == 'resume' else 93
        total_lines_approx = int(expected_variant[0])
        chars_on_last_line = n - ((total_lines_approx - 1) * line_width)
        
        if chars_on_last_line < orphan_threshold and chars_on_last_line > 0:
            bullet_errors.append({
                "type": "ORPHAN",
                "message": f"Bullet risks creating an orphan (only ~{chars_on_last_line} chars on the last line; needs >= {orphan_threshold}).",
                "fix": f"Add {orphan_threshold - chars_on_last_line} characters to fill out the last line, or shorten to 1 line."
            })

    # 4. Banned Jargon scan
    banned_words = [
        'spearheaded', 'leveraged', 'revolutionized', 'synergized', 
        'passionately', 'successfully', 'played a key role', 'dramatically',
        'utilizing'
    ]
    for word in banned_words:
        if re.search(r'\b' + re.escape(word) + r'\b', raw.lower()):
            bullet_errors.append({
                "type": "BANNED_JARGON",
                "message": f"Contains forbidden corporate buzzword: '{word}'.",
                "fix": "Replace with a high-ownership action verb (e.g., 'Engineered', 'Developed', 'Streamlined')."
            })

    # 5. Metric and LOC scans (No LOC/Test count rules)
    if re.search(r'\b\d+\s*(?:LOC|lines of code)\b', raw, re.IGNORECASE):
        bullet_errors.append({
            "type": "METRIC_VIOLATION",
            "message": "Contains forbidden lines-of-code (LOC) metric.",
            "fix": "Describe the core features, adoption, or performance optimization instead of LOC."
        })
    if re.search(r'\b\d+\s*(?:unit|integration|functional)?\s*tests?\s*(?:written|run|created)?\b', raw, re.IGNORECASE):
        bullet_errors.append({
            "type": "METRIC_VIOLATION",
            "message": "Contains forbidden raw test count.",
            "fix": "Focus on reliability improvements, coverage percentages, or integration achievements."
        })

    # 6. LaTeX Scientific notation scans
    # Approx check: raw ~ preceding a number (e.g. ~15ms or ~64)
    if re.search(r'(?<!\$\\sim\$)(?<!\\textasciitilde)(?<!\\)~\d', raw):
        bullet_errors.append({
            "type": "LATEX_STYLE",
            "message": "Uses raw tilde '~' for 'approximately' instead of correct '$\\sim$'.",
            "fix": "Replace '~' with '$\\sim$' (e.g. '$\\sim$15ms'). Remember that raw ~ is a LaTeX non-breaking space."
        })

    # Return results
    if bullet_errors:
        return {
            "status": "FAILED",
            "position": position_name,
            "bullet_index": index,
            "raw": raw,
            "rendered": rendered,
            "char_count": n,
            "expected_variant": expected_variant,
            "errors": bullet_errors
        }
    return {
        "status": "PASSED",
        "position": position_name,
        "bullet_index": index,
        "char_count": n,
        "expected_variant": expected_variant
    }


def parse_tex_file(filepath):
    """
    Parse a LaTeX resume file, keeping track of sections, subsections, and items.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    
    parsed_bullets = []
    current_section = "Unknown"
    current_position = "Unknown"
    bullet_index = 0

    section_regex = re.compile(r'\\begin\{rSection\}(\{[^}]*\})|\\begin\{rSection2\}(\{[^}]*\})')
    subsection_regex = re.compile(r'\\begin\{rSubsection\}\{([^}]*)\}')
    item_regex = re.compile(r'^\s*\\item\s+(.*)')

    for line in lines:
        line_strip = line.strip()
        
        # Check Section
        sec_match = section_regex.search(line_strip)
        if sec_match:
            sec_name = sec_match.group(1) or sec_match.group(2)
            current_section = sec_name.strip('{} ')
            # Reset position context inside new section unless it's Subsection
            current_position = "Unknown"
            continue
            
        # Check Subsection (Position)
        sub_match = subsection_regex.search(line_strip)
        if sub_match:
            current_position = sub_match.group(1).strip()
            bullet_index = 0
            continue
            
        # Check Bullet
        item_match = item_regex.match(line)
        if item_match:
            bullet_index += 1
            raw_text = line_strip
            parsed_bullets.append({
                "raw": raw_text,
                "index": bullet_index,
                "section": current_section,
                "position": current_position if current_position != "Unknown" else current_section
            })

    return parsed_bullets


def main():
    parser = argparse.ArgumentParser(description="Lints LaTeX resume/CV bullets for Antigravity automated corrections.")
    parser.add_argument("tex_file", help="Path to the generated LaTeX (.tex) file")
    parser.add_argument("-f", "--format", choices=["resume", "cv"], required=True, help="Document format constraint")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON log")
    args = parser.parse_args()

    tex_path = Path(args.tex_file)
    if not tex_path.exists():
        print(f"Error: File '{args.tex_file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    bullets = parse_tex_file(tex_path)
    
    all_reports = []
    failed_bullets = []
    total_rendered_lines = 0

    first_exp_bullet_checked = False
    cv_page1_error = None

    for b in bullets:
        # Ignore non-experience/project bullets (like Skills or Languages listings) for strict length checks
        is_experience_or_project = b["section"].lower() in ("experience", "projects", "research experience", "professional experience")
        
        # Validate bullet
        report = validate_bullet(b["raw"], b["index"], b["position"], args.format)
        
        if is_experience_or_project:
            # Check CV Page 1 rule: First bullet of first experience cannot be 3L
            if args.format == 'cv' and not first_exp_bullet_checked and b["section"].lower() in ("experience", "professional experience"):
                first_exp_bullet_checked = True
                if report["expected_variant"] == "3L":
                    cv_page1_error = {
                        "type": "CV_PAGE1_OVERFLOW",
                        "message": "First bullet of first experience is 3L. This violates the 'CV Page 1 Rule' and will overflow the page boundary.",
                        "fix": "Reduce this first experience bullet to strictly 2 lines (2L)."
                    }
                    if report["status"] == "PASSED":
                        report["status"] = "FAILED"
                        report["errors"] = [cv_page1_error]
                    else:
                        report["errors"].append(cv_page1_error)

            if report["status"] == "FAILED":
                failed_bullets.append(report)
            
            # Count expected lines
            if report.get("expected_variant") in ("1L", "2L", "3L"):
                total_rendered_lines += int(report["expected_variant"][0])
        
        all_reports.append(report)

    # Compile overall status
    has_failed = len(failed_bullets) > 0
    
    # Formulate JSON output
    final_output = {
        "status": "FAILED" if has_failed else "PASSED",
        "total_bullets_checked": len(bullets),
        "total_experience_bullets": sum(1 for b in bullets if b["section"].lower() in ("experience", "projects", "research experience", "professional experience")),
        "total_rendered_lines_estimate": total_rendered_lines,
        "failures": failed_bullets
    }

    if args.json:
        print(json.dumps(final_output, indent=2))
    else:
        # Print a beautiful console report
        print("=" * 80)
        print(f" ANTIGRAVITY BUILD VALIDATOR: {tex_path.name.upper()} ")
        print("=" * 80)
        print(f"Format Constraint : {args.format.upper()}")
        print(f"Total Bullets      : {len(bullets)}")
        print(f"Rendered Lines Est.: {total_rendered_lines}")
        print("-" * 80)

        if not has_failed:
            print("[PASS] SUCCESS: All bullets adhere to character limits, LaTeX styles, and anti-jargon rules!")
        else:
            print(f"[FAIL] FAILED: Found {len(failed_bullets)} experience bullets violating constraints.\n")
            for f in failed_bullets:
                print(f"Position: {f['position']} | Bullet Index: {f['index']}")
                print(f"  Raw: {f['raw']}")
                print(f"  Rendered Length: {f['char_count']} chars (Expected {f['expected_variant']})")
                print("  Violations:")
                for err in f["errors"]:
                    print(f"    - [{err['type']}] {err['message']}")
                    print(f"      Fix: {err['fix']}")
                print("-" * 80)
        print("=" * 80)

    # Exit with code 1 if errors exist, else 0
    sys.exit(1 if has_failed else 0)


if __name__ == "__main__":
    main()
