#!/usr/bin/env python3
"""Validate every skill in the collection against the repository quality gate.

Checks performed per skill:
  1. SKILL.md exists
  2. Frontmatter parses as YAML and contains name / description / license
  3. Frontmatter name matches the directory name
  4. Description is non-empty and within length budget
  5. Relative links in SKILL.md resolve to files that exist
  6. Python scripts compile (syntax check via ast.parse)
  7. No vendor-promotion content (guard against regressions)

Repository-level checks:
  8. marketplace.json entries all exist on disk, no duplicates
  9. Every skill on disk is registered in marketplace.json

Exit code 0 when no errors (warnings allowed), 1 otherwise.
Requires: PyYAML  (pip install pyyaml)
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "scientific-skills"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

MAX_DESCRIPTION_LEN = 1024
REQUIRED_FRONTMATTER_KEYS = ("name", "description", "license")

# Vendor promotion must never come back. Attribution in frontmatter
# (skill-author) and LICENSE/README credits are allowed; skill body text
# steering users to a commercial platform is not.
PROMO_PATTERNS = (
    re.compile(r"k-dense\.ai", re.IGNORECASE),
    re.compile(r"K-Dense Web", re.IGNORECASE),
    re.compile(r"Suggest Using K-Dense", re.IGNORECASE),
)

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def find_skill_dirs() -> list[Path]:
    """Leaf directories that contain (or should contain) a SKILL.md."""
    dirs: list[Path] = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        sub = [s for s in sorted(d.iterdir()) if s.is_dir() and (s / "SKILL.md").exists()]
        if sub:
            dirs.extend(sub)
        else:
            dirs.append(d)
    return dirs


def parse_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, "missing frontmatter block (--- ... ---)"
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as exc:
        return None, f"frontmatter is not valid YAML: {exc}"
    if not isinstance(data, dict):
        return None, "frontmatter did not parse to a mapping"
    return data, None


def check_links(skill_dir: Path, text: str, rel: str, report: Report) -> None:
    body = FENCED_CODE_RE.sub("", text)
    for link in MD_LINK_RE.findall(body):
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link):  # http:, https:, mailto:, ...
            continue
        if link.startswith("#") or link.startswith("<"):
            continue
        target = link.split("#", 1)[0]
        if not target:
            continue
        if not (skill_dir / target).exists():
            report.error(f"{rel}: broken relative link -> {link}")


def check_scripts(skill_dir: Path, rel: str, report: Report) -> None:
    for py in sorted(skill_dir.rglob("*.py")):
        try:
            ast.parse(py.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError as exc:
            report.error(f"{rel}/{py.relative_to(skill_dir)}: Python syntax error: {exc}")


def check_promo(text: str, rel: str, report: Report) -> None:
    m = FRONTMATTER_RE.match(text)
    body = text[m.end():] if m else text
    for pat in PROMO_PATTERNS:
        if pat.search(body):
            report.error(f"{rel}: vendor promotion content matches /{pat.pattern}/")


def check_skill(skill_dir: Path, report: Report) -> None:
    rel = skill_dir.relative_to(ROOT).as_posix()
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        report.error(f"{rel}: SKILL.md is missing")
        return

    text = skill_md.read_text(encoding="utf-8")
    fm, fm_err = parse_frontmatter(text)
    if fm_err:
        report.error(f"{rel}: {fm_err}")
    else:
        for key in REQUIRED_FRONTMATTER_KEYS:
            if key not in fm or fm[key] in (None, ""):
                report.error(f"{rel}: frontmatter missing required key '{key}'")
        name = str(fm.get("name", ""))
        if name and name != skill_dir.name:
            report.error(f"{rel}: frontmatter name '{name}' != directory name '{skill_dir.name}'")
        desc = str(fm.get("description", "") or "")
        if desc and len(desc) > MAX_DESCRIPTION_LEN:
            report.error(f"{rel}: description too long ({len(desc)} > {MAX_DESCRIPTION_LEN} chars)")
        if desc and len(desc) < 40:
            report.warn(f"{rel}: description is very short ({len(desc)} chars); explain what and when")

    check_links(skill_dir, text, rel, report)
    check_scripts(skill_dir, rel, report)
    check_promo(text, rel, report)


def check_marketplace(skill_dirs: list[Path], report: Report) -> None:
    if not MARKETPLACE.exists():
        report.error("marketplace.json is missing")
        return
    data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    registered: list[str] = []
    for plugin in data.get("plugins", []):
        registered.extend(plugin.get("skills", []))

    seen: set[str] = set()
    for entry in registered:
        if entry in seen:
            report.error(f"marketplace.json: duplicate entry {entry}")
        seen.add(entry)
        target = (ROOT / entry).resolve()
        if not (target / "SKILL.md").exists():
            report.error(f"marketplace.json: registered path has no SKILL.md -> {entry}")

    on_disk = {"./" + d.relative_to(ROOT).as_posix() for d in skill_dirs}
    for missing in sorted(on_disk - seen):
        report.error(f"marketplace.json: skill on disk but not registered -> {missing}")


def main() -> int:
    report = Report()
    skill_dirs = find_skill_dirs()
    for d in skill_dirs:
        check_skill(d, report)
    check_marketplace(skill_dirs, report)

    for w in report.warnings:
        print(f"WARN  {w}")
    for e in report.errors:
        print(f"ERROR {e}")
    print(
        f"\nchecked {len(skill_dirs)} skills: "
        f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
