#!/usr/bin/env python3
"""Validate the repository structure. Run: python3 scripts/validate.py

Checks:
- every skill folder has SKILL.md with matching name and a description
- the always-on rule stays under Antigravity's 12,000-character limit
- every workflow has a description
- every shared/ or templates/ path mentioned in docs exists
- skills named in workflows exist, and each skill's references/playbook.md exists
- client data is excluded from Git
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".agent" / "skills"
RULES = ROOT / ".agent" / "rules"
WORKFLOWS = ROOT / ".agent" / "workflows"
errors = []


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    data = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.split("#")[0].strip() if k.strip() == "status" else v.strip()
    return data


# Skills
skill_names = set()
for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
    f = d / "SKILL.md"
    if not f.exists():
        errors.append(f"{d.name}: missing SKILL.md")
        continue
    fm = frontmatter(f)
    if not fm:
        errors.append(f"{d.name}: SKILL.md has no frontmatter")
        continue
    if fm.get("name") != d.name:
        errors.append(f"{d.name}: frontmatter name '{fm.get('name')}' does not match folder")
    desc = fm.get("description", "")
    if not desc:
        errors.append(f"{d.name}: missing description")
    elif len(desc) > 1024:
        errors.append(f"{d.name}: description is {len(desc)} chars (max 1024)")
    if not (d / "references" / "playbook.md").exists():
        errors.append(f"{d.name}: missing references/playbook.md")
    skill_names.add(d.name)

# Rules
for r in RULES.glob("*.md"):
    n = len(r.read_text(encoding="utf-8"))
    if n > 12000:
        errors.append(f"{r.name}: {n} chars exceeds the 12,000 limit")

# Workflows
for w in WORKFLOWS.glob("*.md"):
    fm = frontmatter(w)
    if not fm or not fm.get("description"):
        errors.append(f"workflow {w.name}: missing description frontmatter")
    for ref in re.findall(r"`([a-z]+(?:-[a-z]+)+)`", w.read_text(encoding="utf-8")):
        if ref in {"chief-of-staff", "chief-growth-officer", "growth-strategist",
                   "business-development-manager", "chief-strategy-officer",
                   "revenue-growth-manager", "head-of-growth", "chief-operating-officer",
                   "chief-financial-officer", "risk-compliance-officer"} and ref not in skill_names:
            errors.append(f"workflow {w.name}: references missing skill {ref}")

# Path references in markdown files
path_re = re.compile(r"\b((?:shared|templates)/[A-Za-z0-9_./-]+\.md)\b")
for md in ROOT.rglob("*.md"):
    if "clients" in md.relative_to(ROOT).parts[:1]:
        continue
    for ref in set(path_re.findall(md.read_text(encoding="utf-8"))):
        if not (ROOT / ref).exists():
            errors.append(f"{md.relative_to(ROOT)}: references missing file {ref}")

# Privacy guard
gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
if "clients/*" not in gi:
    errors.append(".gitignore must exclude clients/* to protect client data")

if errors:
    print("FAILED:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"OK: {len(skill_names)} skills, {len(list(WORKFLOWS.glob('*.md')))} workflows, rules within limit.")
