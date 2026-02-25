# Code Diagnosis

Multi-agent code scanning and project diagnosis with three-way confirmation from Google Core Team engineers.

## What It Does

Code Diagnosis deploys a team of three Google Core Team engineer personas to systematically scan your codebase for issues. Every finding goes through a three-way confirmation process — Scanner identifies, Reviewer verifies independently, QA Lead makes the final call — ensuring high-confidence results with minimal false positives.

## How It Works

```
Phase 0: Configuration
  ├── Language selection (English / Chinese)
  ├── Scan scope (entire project / specific dirs / specific files / feature)
  ├── Diagnostic categories (security, bugs, quality, performance, etc.)
  └── Output settings (depth, file count, language, detail level)

Phase 1: Project Analysis
  ├── Discover project structure and tech stack
  ├── Partition files into scan groups
  └── Present scan plan for approval

Phase 2: Multi-Agent Scanning (three-way confirmation)
  ├── Scanner (Alex Chen) — Identifies issues with evidence
  ├── Reviewer (Sarah Kim) — Independently verifies each finding
  └── QA Lead (Marcus Johnson) — Final arbitration + cross-cutting analysis

Phase 3: Report Generation
  └── Writes structured MD files to docs/scan-report/
```

## The Team

| Role | Persona | Focus |
|------|---------|-------|
| Scanner | Alex Chen, Senior SWE | Thorough code analysis, evidence-based findings |
| Reviewer | Sarah Kim, Staff SWE | False positive elimination, severity calibration |
| QA Lead | Marcus Johnson, Principal Engineer | Final arbitration, systemic patterns, prioritization |

## Output

Reports are generated as Markdown files in `docs/scan-report/`:

- `00-scan-summary.md` — Executive summary with metrics and code health score
- Category-specific files (e.g., `01-security.md`, `02-bugs.md`) based on findings
- Each finding includes: location, evidence, impact, recommendation, and the full confirmation chain

## Configuration Options

All options have sensible defaults — just press Enter to accept them:

| Setting | Options | Default |
|---------|---------|---------|
| Language | English, Chinese | English |
| Scope | Entire project, Directories, Files, Feature | Entire project |
| Categories | All, Security & Bugs, Quality & Architecture, Performance | All |
| Scan depth | Surface, Standard, Deep, Exhaustive | Standard |
| Output files | Auto, Compact (1-2), Detailed (5-8), Comprehensive (8+) | Auto |
| Report language | Same as session, English, Chinese | Same as session |
| Detail level | Brief, Moderate, Comprehensive | Moderate |

## Trigger Phrases

```
"scan this project"
"code diagnosis"
"audit the codebase"
"find issues in this code"
"project health check"
"review code quality"
/code-diagnosis
```

## Requirements

- Claude Code CLI or Claude Code X
- Standard Claude Code tools only (no external dependencies)
- Works best with projects that have a `.claude-index/` (run `/project-indexer` first for large projects)
