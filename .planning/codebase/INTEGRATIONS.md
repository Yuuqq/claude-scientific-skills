# External Integrations

**Analysis Date:** 2026-04-30

## Distribution & Platform Integrations

**Claude Code Plugin Marketplace:**
- Primary distribution mechanism via `/.claude-plugin/marketplace.json`
- Registration: `/plugin marketplace add K-Dense-AI/claude-scientific-skills`
- Installation: `/plugin install scientific-skills@claude-scientific-skills`
- Manifest defines 140 skill paths across single plugin named `scientific-skills`
- Version: 2.17.0, managed by K-Dense Inc. (`contact@k-dense.ai`)

**MCP (Model Context Protocol) Server:**
- Hosted endpoint: `https://mcp.k-dense.ai/claude-scientific-skills/mcp`
- Self-hosted option: `github.com/K-Dense-AI/claude-skills-mcp`
- Enables ChatGPT, Google ADK, OpenAI Agent SDK, and other MCP-compatible clients

**Cursor IDE:**
- One-click MCP install via deep link
- Config URL: `https://mcp.k-dense.ai/claude-scientific-skills/mcp`

**K-Dense Web (Commercial Platform):**
- Skill: `scientific-skills/offer-k-dense-web/SKILL.md`
- Upsells K-Dense Web (200+ skills, cloud GPUs, publication-ready outputs)
- Website: `https://k-dense.ai`

## AI Model APIs (Used by Skills)

**OpenRouter API:**
- Gateway providing access to multiple AI models through single API key
- Env var: `OPENROUTER_API_KEY`
- Skills using it:
  - `scientific-skills/perplexity-search/` - Perplexity Sonar models (Sonar Pro, Sonar Pro Search, Sonar Reasoning Pro) for AI-powered web search
  - `scientific-skills/generate-image/` - FLUX.2 Pro and Gemini 3 Pro image generation
  - `scientific-skills/scientific-schematics/` - Nano Banana Pro diagram generation with Gemini 3 Pro quality review
  - `scientific-skills/research-lookup/` - Sonar Pro Search and Sonar Reasoning Pro for research queries

**LiteLLM:**
- Unified LLM API proxy library (Python)
- Used by perplexity-search and research-lookup for model routing
- Installed via: `uv pip install litellm`

**Perplexity Models (via OpenRouter):**
- `perplexity/sonar-pro` - General-purpose search (best cost-quality)
- `perplexity/sonar-pro-search` - Agentic multi-step reasoning search
- `perplexity/sonar` - Cost-effective simple queries
- `perplexity/sonar-reasoning-pro` - Advanced step-by-step analysis
- `perplexity/sonar-reasoning` - Basic reasoning

**Image Generation Models (via OpenRouter):**
- `google/gemini-3-pro-image-preview` - High-quality generation + editing (default)
- `black-forest-labs/flux.2-pro` - Fast generation + editing
- `black-forest-labs/flux.2-flex` - Budget generation only

**Rowan Scientific (Cloud Quantum Chemistry):**
- Skill: `scientific-skills/rowan/` (registered in marketplace.json, not on disk)
- API: `https://labs.rowansci.com`
- Capabilities: pKa prediction, docking, conformer search, geometry optimization
- Methods: DFT, GFN-xTB, neural network potentials (AIMNet2, Egret)

**EvolutionaryScale Forge API:**
- Referenced by ESM skill for cloud-based protein language model inference
- Local inference also supported with open weights

## Scientific Databases (28+ Skills)

Each database skill provides SKILL.md with API documentation, query patterns, and Python scripts for programmatic access.

### Literature & Bibliometric
- **OpenAlex** (`scientific-skills/openalex-database/`) - 240M+ scholarly works catalog. REST API, no auth required (100k req/day with email). Scripts: `scripts/` with `openalex_client.py`, query helpers.
- **PubMed** (`scientific-skills/pubmed-database/`) - 35M+ biomedical citations. E-utilities API (Entrez). No auth for basic use. NCBI API key recommended for rate limits.
- **bioRxiv** (`scientific-skills/biorxiv-database/`) - Life sciences preprints. REST API. Scripts: `scripts/biorxiv_search.py`.

### Chemical & Drug
- **ChEMBL** (`scientific-skills/chembl-database/`) - 2M+ compounds, 19M+ bioactivity measurements. REST API at `https://www.ebi.ac.uk/chembl/api/data/`. Scripts: `scripts/example_queries.py`.
- **PubChem** (`scientific-skills/pubchem-database/`) - 110M+ chemical compounds. PUG REST API at `https://pubchem.ncbi.nlm.nih.gov/rest/pug/`.
- **DrugBank** (`scientific-skills/drugbank-database/`) - 9,591+ drug entries. Requires academic license for full access.
- **ZINC** (`scientific-skills/zinc-database/`) - 230M+ purchasable compounds for virtual screening. Free access.
- **HMDB** (`scientific-skills/hmdb-database/`) - 220K+ metabolite entries. REST API.

### Genomic & Protein
- **UniProt** (`scientific-skills/uniprot-database/`) - Protein sequences and annotations. REST API at `https://rest.uniprot.org/`.
- **Ensembl** (`scientific-skills/ensembl-database/`) - 250+ vertebrate genomes. REST API at `https://rest.ensembl.org/`. Includes VEP (Variant Effect Predictor).
- **NCBI Gene** (`scientific-skills/gene-database/`) - Gene info from 500+ organisms. E-utilities API.
- **PDB** (`scientific-skills/pdb-database/`) - 200K+ 3D structures. REST API at `https://data.rcsb.org/`.
- **AlphaFold DB** (`scientific-skills/alphafold-database/`) - 200M+ predicted protein structures. REST API + Google Cloud Storage bulk downloads.
- **GEO** (`scientific-skills/geo-database/`) - 264K+ gene expression studies. E-utilities API.
- **ENA** (`scientific-skills/ena-database/`) - European Nucleotide Archive. REST API at `https://www.ebi.ac.uk/ena/browser/api/`. Rate: 50 req/sec.
- **GWAS Catalog** (`scientific-skills/gwas-database/`) - SNP-trait associations. REST API at `https://www.ebi.ac.uk/gwas/rest/api/`.
- **STRING** (`scientific-skills/string-database/`) - 20B+ protein-protein interactions. REST API.

### Clinical & Regulatory
- **ClinicalTrials.gov** (`scientific-skills/clinicaltrials-database/`) - Global clinical study registry. API v2. No auth. ~50 req/min.
- **ClinVar** (`scientific-skills/clinvar-database/`) - Genomic variant clinical significance. E-utilities API + FTP downloads.
- **COSMIC** (`scientific-skills/cosmic-database/`) - Somatic cancer mutations. Requires institutional access for full data.
- **FDA Databases** (`scientific-skills/fda-database/`) - openFDA API for drugs, devices, foods, substances. No auth required.
- **ClinPGx** (`scientific-skills/clinpgx-database/`) - Pharmacogenomics (successor to PharmGKB). Gene-drug interactions, CPIC guidelines.

### Pathways & Metabolomics
- **KEGG** (`scientific-skills/kegg-database/`) - Pathway and genome databases. REST API at `https://rest.kegg.jp/`.
- **Reactome** (`scientific-skills/reactome-database/`) - 2,825+ human pathways. Content Service + Analysis Service APIs.
- **Metabolomics Workbench** (`scientific-skills/metabolomics-workbench-database/`) - NIH metabolomics repository. REST API.
- **BRENDA** (`scientific-skills/brenda-database/`) - Enzyme information system. SOAP API. Scripts: `scripts/brenda_queries.py`.

### Targets & Patents
- **Open Targets** (`scientific-skills/opentargets-database/`) - Therapeutic target validation. GraphQL API at `https://api.platform.opentargets.org/api/v4/graphql`.
- **USPTO** (`scientific-skills/uspto-database/`) - Patent/trademark data. Multiple APIs: PatentSearch, PEDS, TSDR. Scripts: `scripts/`.

## Platform & Lab Integrations

### LIMS & R&D Platforms
- **Benchling** (`scientific-skills/benchling-integration/`) - R&D platform for lab data management. REST API + Python SDK. Supports registry entities, inventory, ELN, workflows.
- **LabArchives** (`scientific-skills/labarchive-integration/`) - Electronic Lab Notebook. REST API. Multi-regional endpoints (US, UK, AU). OAuth authentication. Third-party integrations (Protocols.io, GraphPad, SnapGene).

### Cloud Genomics Platforms
- **DNAnexus** (`scientific-skills/dnanexus-integration/`) - Cloud platform for genomics data analysis. dxpy Python SDK. Handles FASTQ/BAM/VCF processing, app deployment, workflow orchestration.
- **LatchBio** (`scientific-skills/latchbio-integration/`) - Serverless bioinformatics workflow platform. Python decorators for pipeline creation. Nextflow/Snakemake support. Pre-built workflows (RNA-seq, AlphaFold, DESeq2).

### Lab Automation
- **Opentrons** (`scientific-skills/opentrons-integration/`) - Python Protocol API v2 for Flex and OT-2 robots. Liquid handling, thermocycler, magnetic, heater-shaker module control.
- **PyLabRobot** (`scientific-skills/pylabrobot/`) - Hardware-agnostic lab automation. Hamilton STAR, Opentrons OT-2, Tecan EVO backends. 3D deck visualization.

### Microscopy & Imaging
- **OMERO** (`scientific-skills/omero-integration/`) - Microscopy data management. OMERO.py Python API. Dataset/screening retrieval, ROI management, OMERO.tables.

### Protocol Management
- **Protocols.io** (`scientific-skills/protocolsio-integration/`) - Scientific protocol discovery, creation, and sharing. REST API with OAuth. PDF generation, materials management.

### Cloud Compute
- **Modal** (`scientific-skills/modal/`) - Serverless Python with GPU support (T4 through H100). Container images, autoscaling, persistent volumes, cron scheduling. Free tier: $30/month.

### Tool Discovery
- **ToolUniverse** (referenced in `docs/scientific-skills.md`) - 600+ scientific tools/datasets/APIs. MCP integration for Claude. Semantic search for tool discovery.

## Biomedical AI Frameworks

**BIOMNI:**
- Skill: `scientific-skills/biomni/` (registered, not on disk)
- Autonomous biomedical AI agent from Stanford SNAP lab
- Integrates ~11GB of biomedical databases (Ensembl, UniProt, PDB, AlphaFold, ClinVar, OMIM, HPO, PubMed, KEGG, Reactome, GO)
- LLM providers: Claude, GPT-4, Gemini, Groq, Bedrock
- Scripts: `scripts/generate_report.py`, `scripts/setup_environment.py`

**Denario:**
- Skill: `scientific-skills/denario/`
- Multiagent AI system for end-to-end research workflows
- Built on AG2 and LangGraph frameworks
- LLM providers: Google Vertex AI, OpenAI
- Produces LaTeX papers from data analysis through publication

**HypoGeniC:**
- Skill: `scientific-skills/hypogenic/`
- Automated hypothesis generation and testing via LLMs
- Three frameworks: HypoGeniC, HypoRefine, Union methods
- Redis caching for API cost reduction

## Document Processing Integrations

**Office Documents (OOXML):**
- `scientific-skills/document-skills/docx/` - Word document creation via python-docx + OOXML manipulation. Scripts: `scripts/document.py`, `scripts/utilities.py`. Includes OOXML pack/unpack/validate tools.
- `scientific-skills/document-skills/pptx/` - PowerPoint creation via python-pptx. Includes OOXML tools.
- `scientific-skills/document-skills/xlsx/` - Excel file operations via openpyxl.

**PDF Processing:**
- `scientific-skills/document-skills/pdf/` - PDF form filling, bounding box checking, image conversion. Scripts in `scripts/` (7 Python files).

**Markdown Conversion:**
- `scientific-skills/markitdown/` - Converts 20+ formats to Markdown. Azure Document Intelligence integration for enhanced PDF tables. GPT-4o for image descriptions.

**LaTeX Generation:**
- ReportLab for programmatic PDF generation
- LaTeX templates for academic venues (Nature, Science, NeurIPS, NSF, NIH) in `scientific-skills/venue-templates/assets/`
- Beamer templates for slides in `scientific-skills/scientific-slides/assets/`
- Poster templates (beamerposter, tikzposter, baposter) in `scientific-skills/latex-posters/assets/`

## Data Storage & Caching

**Databases:**
- None - This is a content repository with no persistent data storage
- Individual skills reference their own data storage needs (e.g., LaminDB, Zarr for user workflows)

**File Storage:**
- Local filesystem only for the repository itself
- Skills reference cloud storage patterns: S3, GCS, Azure Blob (via Modal, Dask, Zarr)

**Caching:**
- Redis - Referenced by HypoGeniC skill for API response caching
- LiteLLM built-in caching - Referenced by perplexity-search
- Client-side caching in BioServices library

## Monitoring & Observability

**Error Tracking:**
- Not applicable (content repository, no runtime)

**Logging:**
- Not applicable at repository level
- Individual Python scripts use standard `logging` or `print` for user feedback

**Experiment Tracking (referenced by ML skills):**
- Weights & Biases (W&B) - Referenced by PyTorch Lightning, LaminDB
- MLflow - Referenced by LaminDB integration
- TensorBoard - Referenced by PyTorch Lightning, Stable Baselines3

## CI/CD & Deployment

**Hosting:**
- GitHub repository: `github.com/K-Dense-AI/claude-scientific-skills`
- Distribution: Claude Code Plugin Marketplace, MCP server

**CI Pipeline:**
- `.github/workflows/release.yml` - Single workflow
- Trigger: Push to `main` modifying `.claude-plugin/marketplace.json`
- Steps: Checkout (full history) -> Extract version from JSON -> Check tag existence -> Generate release notes from commits -> Create GitHub Release via `softprops/action-gh-release@v1`
- Permissions: `contents: write`
- Uses: `GITHUB_TOKEN` (automatic)

**Release Process:**
1. Bump version in `.claude-plugin/marketplace.json`
2. Commit and push to `main`
3. GitHub Actions auto-creates tag and release
4. Users update via `/plugin update scientific-skills@claude-scientific-skills`

## Environment Configuration

**Required env vars (user-configured, skill-specific):**
- `OPENROUTER_API_KEY` - Perplexity search, image generation, schematics, research lookup
- Various API keys for specific databases (most are open/no-auth)

**Secrets location:**
- GitHub repository secrets for CI/CD (`GITHUB_TOKEN`)
- User `.env` files for API keys (per skill documentation)
- `~/.modal.toml` for Modal authentication token

## Webhooks & Callbacks

**Incoming:**
- None at repository level

**Outgoing:**
- Adaptyv platform uses webhook notifications for experiment completion (referenced in skill documentation)

---

*Integration audit: 2026-04-30*
