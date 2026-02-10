# JR Development Skills

<div align="center">
  <img src="logo.png" alt="JR Development Skills Logo" width="200"/>
  <p><strong>A curated collection of Claude Code skills for software development workflows</strong></p>
  <p>
    <a href="README.zh.md">中文文档</a>
  </p>
</div>

## Overview

JR Development Skills is a specialized collection of Claude Code skills designed to enhance software development workflows. These skills provide structured approaches to common development tasks, from project exploration to requirements planning.

## Skills Collection

### 🗂️ Project Indexer

Generate structured indexes for quick codebase understanding in new Claude Code sessions.

**Key Features:**
- Automatic project structure analysis
- Code symbol extraction (functions, classes, exports)
- Feature map generation
- Support for 10+ programming languages
- CLAUDE.md integration for persistent context

**Use Cases:**
- Starting work on new/unfamiliar projects
- Onboarding team members
- Maintaining project documentation
- Quick codebase navigation

[📖 Read More](./project-indexer/README.md)

**Trigger Phrases:**
```
"explore the project"
"understand the codebase"
"generate index"
"了解项目"
/project-indexer
```

---

### 📋 Planning with Discovery

Structured requirements clarification and specification planning before implementation.

**Key Features:**
- Iterative requirements discovery through 10-question rounds
- Sequential spec writing with user approval
- Master plan generation
- Actionable TODO checklist creation
- Multi-language support (English/Chinese)

**Use Cases:**
- Starting new features with vague requirements
- Aligning team on project scope
- Reducing implementation rework
- Creating technical specifications

[📖 Read More](./planning-with-discovery/SKILL.md)

**Trigger Phrases:**
```
"plan this feature"
"write a spec"
"clarify requirements"
"规划功能"
/planning-with-discovery
```

---

### 🐛 Bug Diagnosis

Systematic bug diagnosis and fixing through structured problem analysis and verified fixes.

**Key Features:**
- Dual-mode operation (semi-automatic/fully automatic)
- Structured problem intake with diagnostic questions
- Index-aware code analysis with shallow-first strategy
- Hypothesis-driven diagnosis with alternatives
- Immediate fixes with optional test verification
- Lightweight tracking via diagnosis summaries

**Use Cases:**
- Diagnosing and fixing bugs systematically
- Understanding root causes before fixing
- Verifying fixes with automated tests
- Tracking bug resolutions for future reference

[📖 Read More](./bug-diagnosis/README.md)

**Trigger Phrases:**
```
"diagnose this bug"
"find the problem"
"debug this issue"
"troubleshoot"
"查找bug"
/bug-diagnosis
```

## Installation

### Manual Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/JR-Development-Skills.git
```

2. Copy desired skills to your Claude Code skills directory:
```bash
# Copy individual skills
cp -r JR-Development-Skills/project-indexer ~/.claude/skills/
cp -r JR-Development-Skills/planning-with-discovery ~/.claude/skills/
cp -r JR-Development-Skills/bug-diagnosis ~/.claude/skills/
```

3. Restart Claude Code or reload skills (if applicable)

### Verify Installation

In Claude Code, type:
```
/project-indexer
```
or
```
/planning-with-discovery
```
or
```
/bug-diagnosis
```

If the skill activates, installation was successful.

## Usage

Each skill can be triggered by:
1. **Slash command**: `/skill-name`
2. **Natural language**: Phrases listed in each skill's documentation
3. **Direct invocation**: Mention the task the skill handles

Example:
```
User: "I want to understand this codebase"
Claude: [Activates project-indexer skill]
```

## Contributing

Contributions are welcome! Here's how you can help:

### Adding New Skills

1. Fork this repository
2. Create a new directory for your skill: `skill-name/`
3. Include required files:
   - `SKILL.md` - Skill definition and documentation
   - `README.md` - User-facing documentation
   - `_meta.json` - Metadata (optional)
4. Follow existing skill structure and conventions
5. Submit a pull request

### Improving Existing Skills

1. Open an issue describing the improvement
2. Fork and make changes
3. Test thoroughly with Claude Code
4. Submit a pull request with clear description

### Skill Quality Guidelines

- **Clear trigger conditions** - Define when the skill should activate
- **Comprehensive documentation** - Both technical (SKILL.md) and user-facing (README.md)
- **Example workflows** - Show real usage scenarios
- **Error handling** - Handle edge cases gracefully
- **Multi-language support** - Consider international users where appropriate

## Project Structure

```
JR-Development-Skills/
├── README.md                          # This file (English)
├── README.zh.md                       # Chinese documentation
├── logo.png                           # Project logo
├── project-indexer/                   # Project indexing skill
│   ├── SKILL.md                       # Skill implementation guide
│   ├── README.md                      # User documentation
│   ├── _meta.json                     # Skill metadata
│   └── templates/                     # Index templates
│       ├── index-template.md
│       └── config-template.md
├── planning-with-discovery/           # Requirements planning skill
│   └── SKILL.md                       # Skill implementation guide
└── bug-diagnosis/                     # Bug diagnosis skill
    ├── SKILL.md                       # Skill implementation guide
    ├── README.md                      # User documentation
    └── _meta.json                     # Skill metadata
```

## Requirements

- Claude Code CLI or Claude Code X
- Git (for installation)
- Supported operating systems: macOS, Linux, Windows

## Compatibility

All skills in this collection are designed to work with:
- **Claude Code CLI** - Terminal-based interface
- **Claude Code X** - Enhanced IDE integration

Skills use only standard Claude Code tools (Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion) to ensure maximum compatibility.

## Roadmap

Future skills under consideration:

- [x] **Bug Diagnosis** - Systematic bug finding and fixing ✓ Added
- [ ] **Code Review Assistant** - Automated code quality checks
- [ ] **Test Generation** - Auto-generate test cases from specifications
- [ ] **Documentation Generator** - Create API docs from code
- [ ] **Refactoring Advisor** - Suggest refactoring opportunities
- [ ] **Dependency Analyzer** - Visualize and optimize dependencies

Have an idea? [Open an issue](https://github.com/yourusername/JR-Development-Skills/issues) to discuss!

## License

MIT License - See individual skill directories for specific licensing information.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/JR-Development-Skills/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/JR-Development-Skills/discussions)

## Acknowledgments

Built for the Claude Code community. Special thanks to:
- Anthropic for Claude Code
- All contributors to this skills collection

---

<div align="center">
  <p>Made with ❤️ for developers using Claude Code</p>
  <p>
    <a href="#jr-development-skills">Back to Top</a>
  </p>
</div>
