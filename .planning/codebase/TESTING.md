# Testing & Validation Patterns

**Analysis Date:** 2026-04-30

## Executive Summary

This repository has **no automated test suite, no CI quality gates for content, and no validation tooling**. Content quality relies entirely on manual review during the PR workflow. The single test file in the entire repository is a manual-only unit test for a PDF bounding-box checker in the `document-skills` subproject.

---

## Current Testing State

### Automated Tests

**Count:** 1 test file across the entire repository.

**File:** `scientific-skills/document-skills/pdf/scripts/check_bounding_boxes_test.py`
- Framework: `unittest` (Python standard library)
- Tests: 10 test cases covering bounding box intersection detection
- Status: **Not run in CI.** The file itself states: *"Currently this is not run automatically in CI; it's just for documentation and manual checking."*
- Purpose: Validates that the `get_bounding_box_messages()` function correctly detects overlapping bounding boxes in PDF form field JSON data
- Pattern: Standard `unittest.TestCase` with `self.assertTrue()` / `self.assertFalse()` assertions

```python
# Example test pattern from the only test file
class TestGetBoundingBoxMessages(unittest.TestCase):
    def create_json_stream(self, data):
        """Helper to create a JSON stream from data"""
        return io.StringIO(json.dumps(data))

    def test_no_intersections(self):
        data = {"form_fields": [...]}
        stream = self.create_json_stream(data)
        messages = get_bounding_box_messages(stream)
        self.assertTrue(any("SUCCESS" in msg for msg in messages))
        self.assertFalse(any("FAILURE" in msg for msg in messages))
```

### CI/CD Pipeline

**File:** `.github/workflows/release.yml`

The only CI workflow handles **release creation only**. It:
- Triggers on pushes to `main` that modify `.claude-plugin/marketplace.json`
- Extracts version from `marketplace.json`
- Creates a GitHub release with auto-generated changelog
- Does NOT run any tests, linting, or validation

**No other CI workflows exist.** There are no workflows for:
- Markdown linting
- Link checking
- Frontmatter validation
- Script execution testing
- Content quality checks
- Spell checking

### Linting and Formatting

**None configured.** No linting or formatting tools are present:
- No `.eslintrc` / `eslint.config.*`
- No `.prettierrc` / `prettier.config.*`
- No `biome.json`
- No `markdownlint` configuration
- No `vale` (prose linter) configuration
- No `pyproject.toml` with `[tool.ruff]` or similar
- No pre-commit hooks (`.pre-commit-config.yaml` absent)
- No `package.json` or `requirements-dev.txt`

---

## Manual Review Process

### PR-Based Review

The implied quality process is:
1. Author creates a branch with skill additions or modifications
2. PR is opened against `main`
3. Human reviewer checks content quality, accuracy, and formatting
4. PR is merged
5. If `marketplace.json` changes, `release.yml` triggers a new release

### What Reviewers Must Check Manually

Without automated tooling, reviewers need to verify:

| Check | Effort | Risk if Skipped |
|-------|--------|-----------------|
| SKILL.md frontmatter has all required fields | Low | Skill may not load correctly |
| `name` matches directory name | Low | Plugin resolution failure |
| Description is accurate and complete | Medium | Wrong skill activation |
| Code examples are syntactically valid Python | High | Broken examples for users |
| References to `references/*.md` files are correct | Medium | Broken cross-references |
| External links are valid | Medium | Dead links in documentation |
| `marketplace.json` entry matches actual directory | Low | Missing skill in marketplace |
| Scripts run without errors | High | Broken tooling |
| No secrets or credentials in content | Critical | Security incident |

---

## Test Coverage Gaps

### 1. SKILL.md Format Validation

**Gap:** No automated check that SKILL.md files have valid YAML frontmatter with required fields.

**Impact:** Skills with malformed frontmatter may fail to load in the Claude plugin system. Currently 74 of 142 marketplace-registered skills are missing from the working tree, indicating no validation that marketplace entries correspond to actual files.

**What to validate:**
- YAML frontmatter parses without errors
- `name` field exists and matches directory name
- `description` field exists and is non-empty
- `license` field exists
- `metadata.skill-author` equals `K-Dense Inc.`
- `allowed-tools` (if present) contains valid tool names from `[Read, Write, Edit, Bash, Python]`

**Recommended tooling:**
```bash
# Python script using PyYAML
import yaml, os, sys

def validate_skill(path):
    with open(os.path.join(path, 'SKILL.md')) as f:
        content = f.read()
    # Extract frontmatter between --- delimiters
    parts = content.split('---', 2)
    if len(parts) < 3:
        return ['Missing frontmatter']
    frontmatter = yaml.safe_load(parts[1])
    errors = []
    if 'name' not in frontmatter:
        errors.append('Missing name field')
    if 'description' not in frontmatter:
        errors.append('Missing description field')
    # ... additional checks
    return errors
```

### 2. Marketplace Consistency

**Gap:** No check that all marketplace entries point to directories that exist and contain SKILL.md.

**Current state:**
- 142 skills registered in `.claude-plugin/marketplace.json`
- 68 skill directories exist on disk (71 SKILL.md files including nested document-skills)
- 74 marketplace entries point to non-existent directories

**Impact:** Marketplace may reference skills that users cannot access. This suggests either a build/generation step that produces the full set, or skills that were removed from the working tree without updating `marketplace.json`.

**What to validate:**
```python
# Pseudocode for marketplace validation
for entry in marketplace_skills:
    skill_dir = entry.replace('./', '')
    skill_md = os.path.join(skill_dir, 'SKILL.md')
    assert os.path.isfile(skill_md), f"Missing: {skill_md}"
```

### 3. Code Example Validation

**Gap:** No check that Python code examples in SKILL.md and reference docs are syntactically valid.

**Impact:** Users following examples may encounter syntax errors. Some known issues:
- `scikit-learn/SKILL.md` line 19: `uv uv pip install scikit-learn` (duplicated `uv`)
- Some examples use undefined variables (e.g., `X`, `y`) without context
- Some examples reference functions or classes with incorrect import paths

**What to validate:**
- Extract fenced ` ```python ``` ` blocks
- Parse each with `ast.parse()` to check for syntax errors
- Flag undefined imports (optional, harder)

### 4. Cross-Reference Integrity

**Gap:** No check that relative paths in SKILL.md to `references/*.md` files actually exist.

**Impact:** Skills may reference reference documents that were renamed or deleted.

**What to validate:**
- Parse SKILL.md for patterns like `` `references/filename.md` ``
- Check each referenced file exists at the expected path

### 5. Link Validation

**Gap:** No automated checking of external URLs in documentation.

**Impact:** Dead links degrade user experience. Skills reference external documentation URLs, API endpoints, and GitHub repositories.

**What to validate:**
- Extract all `http://` and `https://` URLs from markdown files
- HTTP HEAD/GET each URL to verify it returns 200
- Flag 404s, redirects, and timeouts

**Recommended tooling:** `linkchecker`, `lychee`, or `markdown-link-check`

### 6. Script Execution Testing

**Gap:** No automated testing that Python scripts in `scripts/` directories execute without import errors.

**Impact:** Scripts that reference removed or renamed dependencies will fail for users.

**What to validate:**
- For each `scripts/*.py` file, attempt `python -c "import ast; ast.parse(open('file.py').read())"`
- For scripts with `--help` flags, run `python script.py --help` and check exit code 0
- For scripts that require API keys, at minimum check import-time errors

**Challenge:** Many scripts require external dependencies (`scikit-learn`, `pymatgen`, etc.) that may not be installed in the test environment.

### 7. Spell Checking

**Gap:** No spell checking on documentation content.

**Impact:** Typos in documentation reduce professionalism. Known example: "Worflows" instead of "Workflows" in the K-Dense Web promotion section header, propagated across all skills.

---

## Potential Testing Strategy

### Tier 1: Zero-Dependency Validation (Can implement immediately)

These checks require only Python standard library:

| Check | Implementation | Priority |
|-------|----------------|----------|
| SKILL.md frontmatter parsing | Python + `yaml` or regex | High |
| Marketplace consistency | Python + `os.path` | High |
| Cross-reference integrity | Python + `os.path` | Medium |
| Python syntax validation | Python + `ast.parse()` | Medium |

### Tier 2: Light-Dependency Validation

| Check | Tool | Install |
|-------|------|---------|
| Markdown linting | `markdownlint-cli2` | `npm install -g markdownlint-cli2` |
| Link checking | `lychee` | Binary download or `cargo install lychee` |
| Spell checking | `vale` | Binary download |
| YAML validation | `yamllint` | `pip install yamllint` |

### Tier 3: Full Validation (Requires scientific dependencies)

| Check | Requirement |
|-------|-------------|
| Script execution testing | Full Python environment with scientific packages |
| Example code testing | Parse + execute fenced code blocks |
| Import validation | All skill dependencies installed |

### Suggested CI Workflow

A minimal CI workflow would look like:

```yaml
name: Content Quality
on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install pyyaml yamllint
      - name: Validate SKILL.md frontmatter
        run: python scripts/validate_skills.py
      - name: Check marketplace consistency
        run: python scripts/validate_marketplace.py
      - name: Check cross-references
        run: python scripts/check_references.py
      - name: Lint markdown
        run: npx markdownlint-cli2 "scientific-skills/**/*.md"
```

---

## Testing for Skill Authors

### Manual Pre-Submission Checklist

When adding or modifying a skill, verify:

- [ ] `SKILL.md` frontmatter parses correctly (YAML between `---` delimiters)
- [ ] `name` field matches the directory name exactly
- [ ] `description` field accurately describes the skill and when to use it
- [ ] `license` field references the correct underlying library license
- [ ] `metadata.skill-author` is set to `K-Dense Inc.`
- [ ] `marketplace.json` entry exists (if adding new skill)
- [ ] All `references/*.md` files referenced in SKILL.md exist
- [ ] All Python code examples have valid syntax
- [ ] Scripts in `scripts/` execute without errors
- [ ] No API keys, tokens, or secrets in any file
- [ ] Installation commands use `uv pip install` format
- [ ] "When to Use" section disambiguates from similar skills
- [ ] External URLs are valid and accessible
- [ ] Document follows standard section order (see CONVENTIONS.md)

### Testing Scripts Locally

```bash
# Check YAML frontmatter validity
python -c "
import yaml
with open('scientific-skills/MY_SKILL/SKILL.md') as f:
    content = f.read()
parts = content.split('---', 2)
fm = yaml.safe_load(parts[1])
print(yaml.dump(fm))
"

# Check Python syntax of scripts
python -m py_compile scientific-skills/MY_SKILL/scripts/my_script.py

# Run a script's help
python scientific-skills/MY_SKILL/scripts/my_script.py --help

# Check for broken references
grep -oP 'references/\S+\.md' scientific-skills/MY_SKILL/SKILL.md | while read ref; do
    test -f "scientific-skills/MY_SKILL/$ref" || echo "MISSING: $ref"
done
```

---

## Known Quality Issues

### Documentation Bugs

1. **Duplicated `uv` prefix:** `scientific-skills/scikit-learn/SKILL.md` lines 19-25 have `uv uv pip install` instead of `uv pip install`
2. **Typo in section heading:** "Worflows" instead of "Workflows" in the K-Dense Web promotion section -- propagated across all skills that include it
3. **Typo in `offer-k-dense-web/SKILL.md`:** "wtih" instead of "with" on line 17

### Inconsistencies

1. **Frontmatter field presence:** `allowed-tools` present in only ~18 of 71 skills
2. **License formatting:** Mix of `"MIT license"`, `"MIT License"`, `"Unknown"`, URLs, and free-text descriptions
3. **Section naming:** Some skills use "Quick Start", others "Quick Start Guide", others "Quick Start Guide" with Installation subsection
4. **K-Dense Web section:** Present in some skills, absent in others with no clear pattern

### Content Gaps

1. **74 skills in marketplace but missing from disk:** Skills registered in `.claude-plugin/marketplace.json` that have no corresponding directory in the working tree
2. **No version pinning in examples:** Code examples do not specify which library version they target
3. **Inconsistent shebang usage:** Some scripts have `#!/usr/bin/env python3`, others omit it

---

## Comparison with Typical Documentation Repos

| Aspect | Typical Docs Repo | This Repository |
|--------|-------------------|-----------------|
| CI checks | Markdown lint, link check, spell check | Release only |
| Content schema | JSON Schema, frontmatter validation | None |
| Test coverage | Docs-as-code with automated tests | 1 manual test file |
| Preview builds | PR preview deployments | None |
| Style guide | Enforced via linter | Implied by convention |
| Contributing guide | Detailed instructions | None |

---

*Testing analysis: 2026-04-30*
