# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JR Development Skills is a collection of Claude Code skills — structured AI-guided workflows for software development tasks. This is **not an application codebase**; it contains no executable code, build system, or test framework. Each skill is a set of Markdown-based workflow definitions that Claude Code loads and follows.

**Repository:** https://github.com/xdrshjr/JR-Development-Skills.git

## Architecture

### Skill Structure

Each skill lives in its own top-level directory with this layout:

```
skill-name/
├── SKILL.md        # Required: Full workflow definition (the "source code")
├── README.md       # Optional: User-facing documentation
├── _meta.json      # Optional: Version, tags, publication metadata
└── templates/      # Optional: Template files used during execution
```

`SKILL.md` is the primary artifact — it contains the complete phase-by-phase workflow that Claude Code executes when the skill is invoked. Think of it as the skill's implementation.

### Skills

| Skill | Slash Command | Purpose |
|-------|--------------|---------|
| **project-indexer** | `/project-indexer` | Scans codebases and generates `.claude-index/` with navigable feature maps |
| **planning-with-discovery** | `/planning-with-discovery` | Iterative requirements Q&A → specs → dependency-aware TODOs → optional multi-agent development with code review |
| **spec-to-tasks** | `/spec-to-tasks` | Converts spec documents (Markdown/Word) into structured TODO task plans |
| **code-diagnosis** | `/code-diagnosis` | Multi-agent code scanning with three-way confirmation (Scanner → Reviewer → QA) |
| **bug-diagnosis** | `/bug-diagnosis` | Hypothesis-driven bug diagnosis with dual-mode (semi-auto/full-auto) operation |
| **security-scan** | `/security-scan` | Multi-phase security vulnerability scanning with team personas, verification rounds, and PoC validation |
| **nano-banana-draw** | `/nano-banana-draw` | AI image generation & editing using Gemini 3 Pro Image (text-to-image, image editing, multi-resolution) |

### Shared Design Patterns

All skills share these architectural patterns:

- **Phase-based workflows**: Each skill progresses through numbered phases with clear gates
- **Language selection first**: Users choose English or Chinese at skill start; all generated content follows that choice
- **AskUserQuestion for decisions**: Structured questions with candidate answers at critical decision points
- **Standard tools only**: Skills use only Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Skill, and Task/TeamCreate/SendMessage (for multi-agent workflows) — no external dependencies
- **Search before read**: Use Glob/Grep to locate files before reading them
- **Edit over Write**: Use Edit for existing files, Write only for new files
- **Project index awareness**: bug-diagnosis and security-scan check for `.claude-index/` and `CLAUDE.md`, optionally invoking project-indexer first
- **Multi-agent pipelines**: code-diagnosis (Scanner → Reviewer → QA), security-scan (Discovery → Verification → Validation), and planning-with-discovery (Development Team → Code Review, Phase 4-5) spawn parallel subagent teams via Task/TeamCreate

### Output Locations

- **project-indexer** → `.claude-index/index.md` and `.claude-index/config.md` in target project
- **planning-with-discovery** → `docs/plans/<topic-name>/` (master plan, specs, optional TODOs, task-orchestration.md); Phase 4-5 generates source code in project directories
- **spec-to-tasks** → `docs/plans/<topic-name>/TODO-*.md` files
- **code-diagnosis** → `docs/scan-report/` structured diagnostic reports
- **security-scan** → `docs/security-scan/` with phase subdirectories (`phase1/`, `phase2/`, `phase3/`, plus index)
- **bug-diagnosis** → `.claude/diagnoses/` summaries in target project
- **nano-banana-draw** → `img/` directory in user's working directory (timestamped PNG files)

## Working in This Repo

There are no build, lint, or test commands. Changes are validated by:

1. Reading the SKILL.md to verify workflow logic and phase transitions
2. Checking that AskUserQuestion calls include proper candidate answers
3. Ensuring consistent structure across skills (language selection, phase numbering, approval gates)
4. Testing skills by invoking them in Claude Code against real projects

### Adding a New Skill

1. Create a directory: `skill-name/`
2. Write `SKILL.md` following the phase-based workflow pattern used by existing skills
3. Add `README.md` for user documentation and `_meta.json` for metadata
4. Optionally add `references/` for supporting documents (see security-scan for example)
5. Update the root `README.md` (both English and `README.zh.md`) to list the new skill
6. Update this `CLAUDE.md` — add the skill to the table, output locations, and any new `.gitignore` entries
7. Add trigger phrases in the README and ensure the SKILL.md defines clear activation conditions

### Conventions

- Skill directory names use kebab-case
- SKILL.md files define `name:` and `description:` in a YAML-like frontmatter block
- Generated output paths use `docs/plans/` for planning artifacts, `docs/scan-report/` for diagnostics, `docs/security-scan/` for security reports
- The `.gitignore` excludes `docs/plans/bug-diagnosis/`, `docs/scan-report/`, and `docs/scan-report-*/` to avoid committing generated reports
- Skills with multi-agent workflows (code-diagnosis, security-scan) use structured agent personas with named identities and role-specific prompts
