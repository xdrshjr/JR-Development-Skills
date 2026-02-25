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

### The Five Skills

| Skill | Slash Command | Purpose |
|-------|--------------|---------|
| **project-indexer** | `/project-indexer` | Scans codebases and generates `.claude-index/` with navigable feature maps |
| **planning-with-discovery** | `/planning-with-discovery` | Iterative requirements Q&A → specs → optional TODO files |
| **spec-to-tasks** | `/spec-to-tasks` | Converts spec documents (Markdown/Word) into structured TODO task plans |
| **code-diagnosis** | `/code-diagnosis` | Multi-agent code scanning with three-way confirmation (Scanner → Reviewer → QA) |
| **bug-diagnosis** | `/bug-diagnosis` | Hypothesis-driven bug diagnosis with dual-mode (semi-auto/full-auto) operation |

### Shared Design Patterns

All skills share these architectural patterns:

- **Phase-based workflows**: Each skill progresses through numbered phases with clear gates
- **Language selection first**: Users choose English or Chinese at skill start; all generated content follows that choice
- **AskUserQuestion for decisions**: Structured questions with candidate answers at critical decision points
- **Standard tools only**: Skills use only Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Skill, and Task (for subagent spawning) — no external dependencies
- **Search before read**: Use Glob/Grep to locate files before reading them
- **Edit over Write**: Use Edit for existing files, Write only for new files

### Output Locations

- **project-indexer** → `.claude-index/index.md` and `.claude-index/config.md` in target project
- **planning-with-discovery** → `docs/plans/<topic-name>/` (master plan, specs, optional TODOs)
- **spec-to-tasks** → `docs/plans/<topic-name>/TODO-*.md` files
- **code-diagnosis** → `docs/scan-report/` structured diagnostic reports
- **bug-diagnosis** → `.claude/diagnoses/` summaries in target project

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
4. Update the root `README.md` (both English and `README.zh.md`) to list the new skill
5. Add trigger phrases in the README and ensure the SKILL.md defines clear activation conditions

### Conventions

- Skill directory names use kebab-case
- SKILL.md files define `name:` and `description:` in a YAML-like frontmatter block
- Generated output paths use `docs/plans/` for planning artifacts
- The `.gitignore` excludes `docs/plans/bug-diagnosis/` to avoid committing diagnosis traces
