# Code Review: claude-scientific-skills

This review summarizes the findings across architecture, security, reliability, testing, and maintainability for the repository.

## 1. Security Issues

**MEDIUM** - Potential Command Injection via `docs/index.html` Copy-Paste
* **File:** `docs/index.html` (around `installPanelHTML`), `scripts/validate_skills.py`
* **Impact:** The GitHub Pages catalog (`docs/index.html`) constructs bash commands for users to copy/paste to install skills (e.g., `... && cp -r {REPO_SLUG}/{s.path} ~/.claude/skills/`). The `s.path` is derived from the skill's directory name. If a malicious PR introduces a skill with a directory name containing shell metacharacters (e.g., `test; rm -rf ~;`), it could lead to arbitrary command execution on the user's machine when they paste the installation command.
* **Fix Applied:** Added regex validation in `scripts/validate_skills.py` to ensure that skill directory names only contain safe characters (e.g., `re.match(r"^[a-zA-Z0-9_-]+$", skill_dir.name)`). Additionally, added quotes around the string concatenation in JS to prevent injection.

**MEDIUM** - Workflow Arbitrary Code Execution on PR
* **File:** `.github/workflows/validate.yml`, `.github/workflows/links.yml`, `.github/workflows/release.yml`
* **Impact:** The workflows were missing explicit `permissions: contents: read`. Additionally, `release.yml` was interpolating the unverified version directly into shell execution which is a vector for shell injection if a malicious payload is added to the version string in `marketplace.json`.
* **Fix Applied:** Added `permissions: contents: read` to `validate.yml` and `links.yml`. Modified `release.yml` to pass the `VERSION` output to shell scripts via an environment variable.

## 2. Architecture and Code Organization

**MEDIUM** - Hardcoded Metadata in Generator Script Contains Ghost Skills
* **File:** `scripts/generate_skills_data.py` (Lines 11-125)
* **Impact:** `CATEGORIES` and `DISCIPLINES` mappings are hardcoded directly into the Python script. The script contained 76 "ghost skills" in the mapping that do not exist in the repository.
* **Fix Applied:** Cleaned up the hardcoded dicts to exclusively contain the 69 existing skills.

## 3. Reliability and Error Handling

**LOW** - Brittle Relative Link Parsing in Validator
* **File:** `scripts/validate_skills.py` (Inside `check_links`)
* **Impact:** The link validator strips URL fragments (`#`) but does not strip query parameters (`?`). A relative markdown link like `[doc](reference.md?foo=bar)` would cause the script to look for a file literally named `reference.md?foo=bar` on disk, incorrectly failing the CI build.
* **Fix Applied:** Updated the target parsing to strip query parameters as well: `target = link.split("#", 1)[0].split("?", 1)[0]`.

## 4. Test Coverage and High-Risk Paths

**MEDIUM** - Lack of Unit Tests for Core CI Scripts
* **File:** `scripts/validate_skills.py`, `scripts/generate_skills_data.py`
* **Impact:** These scripts serve as the "quality gate" for the repository. A broken regex (e.g., `PROMO_PATTERNS` or `FRONTMATTER_RE`) could easily introduce false negatives, allowing invalid skills, missing sections, or prohibited promotional content to slip through to the marketplace.
* **Note:** This conflicts with the current `JULES.md` directive which strictly prohibits adding tests/CI to the repo, as it is treated as a content repository rather than a software project. This finding stands as an observation for future consideration.

## 5. Performance and Maintainability

**LOW** - Missing Dependency Manifest for Contributors
* **File:** `README.md`, `CONTRIBUTING.md`
* **Impact:** Contributors are currently instructed to manually `pip install pyyaml`. The CI relies on `pyyaml` and `ruff`. This informal dependency management does not scale if more tools are added.
