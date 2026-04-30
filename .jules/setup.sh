#!/bin/bash
# Jules Environment Setup Script
# This runs once when Jules first clones the repo. Environment is snapshotted after.
set -e

echo "=== Claude Scientific Skills - Environment Setup ==="
echo ""

# 1. Verify we're in the right directory
if [ ! -f "JULES.md" ]; then
    echo "ERROR: JULES.md not found. Are you in the repo root?"
    exit 1
fi
echo "[OK] Repository root verified"

# 2. Verify Python (needed for catalog generator only)
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "WARN: Python not found. Catalog regeneration (generate_skills_data.py) will not work."
    echo "      This is fine for SKILL.md editing tasks."
    PYTHON=""
fi

if [ -n "$PYTHON" ]; then
    PY_VERSION=$($PYTHON --version 2>&1)
    echo "[OK] $PY_VERSION"
fi

# 3. Count skills
SKILL_COUNT=$(find scientific-skills -maxdepth 2 -name "SKILL.md" | wc -l)
echo "[OK] Found $SKILL_COUNT SKILL.md files"

# 4. Regenerate catalog if Python available
if [ -n "$PYTHON" ]; then
    echo "Regenerating skills.json..."
    $PYTHON scripts/generate_skills_data.py
    echo "[OK] Catalog updated"
fi

# 5. Print summary
echo ""
echo "=== Setup Complete ==="
echo ""
echo "This is a CONTENT repository (no build, no tests, no runtime)."
echo "Jules edits Markdown files under scientific-skills/."
echo ""
echo "Key files:"
echo "  JULES.md              - Read this for all instructions"
echo "  DEVELOPMENT-PLAN.md   - Iteration plan"
echo "  .jules/env.md         - Human-readable environment docs"
echo ""
echo "After editing skills, run: python scripts/generate_skills_data.py"
