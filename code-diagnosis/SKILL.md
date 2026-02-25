---
name: code-diagnosis
description: Multi-agent code scanning and project diagnosis tool with three-way confirmation (Scanner, Reviewer, QA). Deploys a team of Google Core Team engineers to systematically scan, review, and diagnose code issues across security, performance, quality, architecture, and more. Use this skill when the user wants to scan a project, audit code quality, review a codebase, find potential issues, or run a diagnostic check on their code. Also trigger when the user mentions "code review", "code audit", "project health check", "scan for issues", "code scan", "diagnose project", "code quality", or wants a comprehensive analysis of their codebase, even if they don't explicitly ask for a "diagnosis". Also use when the user mentions "代码诊断", "代码扫描", "代码审计", "项目扫描", or "代码检查" in Chinese.
---

# Code Diagnosis — Multi-Agent Project Scanning

A structured code scanning workflow that deploys a team of three Google Core Team engineers to independently verify every finding through a three-way confirmation process: Scanner identifies issues, Reviewer verifies independently, and QA Lead makes the final call.

## Why Three-Way Confirmation?

Code scanning tools often produce noisy results — false positives waste developer time and erode trust. By requiring three independent assessments from experienced engineers, this workflow ensures that every reported issue is real, properly categorized, and actionable. The separation of powers (Scanner → Reviewer → QA) prevents blind spots and catches both false positives and false negatives.

## The Team

All agents adopt Google Core Team engineer personas. These personas shape the review lens — thoroughness, evidence-based reasoning, and pragmatic severity assessment — rather than being decorative.

### Scanner — Alex Chen
- **Role**: Senior Software Engineer, Google Core Infrastructure Team
- **Strengths**: Deep code analysis, edge case detection, security awareness
- **Approach**: Methodical file-by-file scanning; never flags an issue without exact code location and evidence

### Reviewer — Sarah Kim
- **Role**: Staff Software Engineer, Google Code Health Team
- **Strengths**: False positive elimination, severity calibration, practical trade-off analysis
- **Approach**: Independent verification of each finding against actual code; if she can't reproduce the concern, it's not real

### QA Lead — Marcus Johnson
- **Role**: Principal Engineer, Google Engineering Productivity Team
- **Strengths**: Cross-cutting pattern recognition, strategic prioritization, final arbitration
- **Approach**: Holistic review of both assessments; sees the forest for the trees

## When to Use

- User wants a comprehensive code review or quality audit
- User asks to scan a project for issues, vulnerabilities, or code smells
- User wants a health check before a release or handoff
- User mentions code diagnosis, code audit, or project scanning
- User wants to understand the overall quality of a codebase
- User is onboarding to a new project and wants to assess code health

**Do NOT use when:**
- User is reporting a specific bug (use bug-diagnosis instead)
- User wants to add a new feature (use planning-with-discovery instead)
- User wants to understand project structure without diagnosis (use project-indexer instead)
- User wants a quick fix for one issue — this skill is for broad scanning, not targeted fixes

---

## Phase 0: Initialization & Configuration

### Step 1: Language Selection

Use AskUserQuestion:
- **question**: "Which language would you like to use for this session? / 您希望使用哪种语言进行本次会话？"
- **header**: "Language"
- **options**:
  1. label: "English (Default)", description: "All interaction and output in English"
  2. label: "中文 (Chinese)", description: "所有交互和输出使用中文"

Store the chosen language as SESSION_LANG. All subsequent prompts, questions, and generated report files follow this language. The SKILL.md itself stays in English — only user-facing content changes.

### Step 2: Scan Scope

Use AskUserQuestion (in SESSION_LANG):
- **question**: "What would you like to scan and diagnose?"
- **header**: "Scope"
- **options**:
  1. label: "Entire project (Default)", description: "Scan all source code in the project"
  2. label: "Specific directories", description: "Scan only selected directories"
  3. label: "Specific files", description: "Scan only selected files"
  4. label: "By feature/module", description: "Scan code related to a specific feature"

If the user selects anything other than "Entire project", follow up to get the specific paths or feature description. Accept freeform input here — the user knows their project best.

### Step 3: Scan Categories

Use AskUserQuestion (in SESSION_LANG, multiSelect: true):
- **question**: "Which diagnostic categories should the team focus on?"
- **header**: "Categories"
- **options**:
  1. label: "All categories (Default)", description: "Security, Bugs, Performance, Quality, Architecture, Error Handling, Testing, Documentation"
  2. label: "Security & Bugs", description: "Focus on vulnerabilities and potential bugs"
  3. label: "Quality & Architecture", description: "Focus on maintainability, design patterns, structure"
  4. label: "Performance & Scalability", description: "Focus on efficiency, resource usage, scaling"

Store selected categories as SCAN_CATEGORIES.

### Step 4: Output Configuration

Use AskUserQuestion with 4 questions in a single call (in SESSION_LANG):

**Question 1 — Scan depth:**
- **question**: "How deep should the scan go?"
- **header**: "Depth"
- **options**:
  1. label: "Standard (Default)", description: "All source files, common issue patterns"
  2. label: "Surface", description: "Key files only, obvious issues — faster but less thorough"
  3. label: "Deep", description: "Every file including configs, edge cases, subtle issues"
  4. label: "Exhaustive", description: "Line-by-line analysis of every file — slowest but most complete"

**Question 2 — Number of output files:**
- **question**: "How many report files should be generated?"
- **header**: "Files"
- **options**:
  1. label: "Auto (Default)", description: "Determined by findings — typically 3-6 files"
  2. label: "Compact (1-2)", description: "Everything in minimal files"
  3. label: "Detailed (5-8)", description: "One file per diagnostic category"
  4. label: "Comprehensive (8+)", description: "Maximum granularity with sub-categories"

**Question 3 — Output language:**
- **question**: "What language should the report files use?"
- **header**: "Report lang"
- **options**:
  1. label: "Same as session (Default)", description: "Follow the language chosen in Step 1"
  2. label: "English", description: "Reports always in English"
  3. label: "Chinese", description: "Reports always in Chinese"

**Question 4 — Detail level:**
- **question**: "How detailed should each finding be?"
- **header**: "Detail"
- **options**:
  1. label: "Moderate (Default)", description: "Issue description, location, evidence, and recommendation"
  2. label: "Brief", description: "Issue description and location only"
  3. label: "Comprehensive", description: "Full analysis with code examples, impact assessment, and alternative approaches"

Store all configuration values. These shape scanning prompts and report generation.

---

## Phase 1: Project Analysis

### Step 1: Discover Project Structure

Use Glob and Grep to understand the project:

1. **Identify tech stack**: Glob for config files — `**/package.json`, `**/pom.xml`, `**/Cargo.toml`, `**/go.mod`, `**/requirements.txt`, `**/pyproject.toml`, `**/*.csproj`, `**/build.gradle`, etc. Read key configs to understand dependencies and frameworks.

2. **Map the codebase**: Glob for source files matching the detected tech stack. Count files, estimate project size, identify entry points, test directories, and configuration.

3. **Check for project index**: Look for `.claude-index/index.md`. If it exists, Read it for a pre-built feature map. If no index exists and the project has >100 source files, suggest running `/project-indexer` first — it dramatically improves scan quality.

### Step 2: Define Scan Targets

Based on the scope from Phase 0 Step 2:

- **Entire project**: All source files, excluding build artifacts, `node_modules`, `vendor`, `.git`, and other generated directories.
- **Specific directories/files**: Validate paths exist, then scope.
- **By feature/module**: Use Grep to find related files, confirm with user.

**If zero scannable files are found** after applying filters, halt and ask the user to verify the scope paths or project root before continuing.

Partition files into **scan groups** of 5-15 files each, organized by directory or module. This keeps subagent context focused and manageable. Limit the total number of scan groups to 20 — if more groups are needed, merge smaller groups or ask the user to narrow scope.

### Step 3: Present Scan Plan

Show the user (in SESSION_LANG):
- Total files to scan
- Number of scan groups
- Categories being checked
- Scan depth setting

Use AskUserQuestion:
- **question**: "Ready to begin scanning? Here is the plan: [summary]. Proceed?"
- **header**: "Confirm"
- **options**:
  1. label: "Proceed (Default)", description: "Start the multi-agent scan"
  2. label: "Adjust scope", description: "Modify scan targets before starting"
  3. label: "Add focus areas", description: "Highlight specific concerns to prioritize"

---

## Phase 2: Multi-Agent Code Scanning

This is the core phase. Process each scan group through the three-way confirmation pipeline.

### Execution Strategy

For efficiency, parallelize where possible:
1. Launch Scanner agents for **all scan groups simultaneously** (parallel Task calls)
2. Once all Scanners complete, launch Reviewer agent with **all findings at once**
3. Once Reviewer completes, launch QA agent with **all findings and reviews**

This minimizes total wall-clock time while maintaining the three-way confirmation integrity.

### Step 1: Deploy Scanners (Alex Chen)

For each scan group, spawn a subagent using the Task tool:
- **subagent_type**: "Explore"
- **description**: "Scan code group N"

**Prompt template:**
```
You are Alex Chen, a Senior Software Engineer on Google's Core Infrastructure team. You have 8 years of experience working on large-scale systems like Borg and Spanner. Your code reviews are known for being thorough and evidence-based. You never flag an issue without providing the exact code location and a clear explanation of why it matters.

## Task
Scan the following files for issues in these categories: {SCAN_CATEGORIES}
Scan depth: {SCAN_DEPTH}

## Files
{list of file paths in this scan group}

## Project Context
- Tech stack: {detected tech stack}
- Frameworks: {detected frameworks}

## Instructions
1. Read each file carefully
2. For every issue, output a structured finding:

### Finding [SCAN-NNN]
- **Category**: BUG | SECURITY | PERFORMANCE | QUALITY | ARCHITECTURE | ERROR_HANDLING | TESTING | DOCUMENTATION
- **Severity**: CRITICAL | HIGH | MEDIUM | LOW | INFO
- **File**: {file path}
- **Line(s)**: {line numbers}
- **Title**: {one-line summary}
- **Description**: {why this is an issue}
- **Evidence**: {the problematic code snippet}
- **Impact**: {what could go wrong}
- **Recommendation**: {how to fix}

3. Only flag genuine issues with clear evidence
4. Consider the project's tech stack and framework conventions
5. If a file has no issues, state that explicitly
6. Cap at 50 findings for this scan group — prioritize by severity if you hit the cap, and note that more issues may exist
```

Collect all Scanner findings from all groups. Merge and renumber if needed.

### Step 2: Deploy Reviewer (Sarah Kim)

Spawn a single subagent with ALL Scanner findings:
- **subagent_type**: "Explore"
- **description**: "Review scanner findings"

**Prompt template:**
```
You are Sarah Kim, a Staff Software Engineer leading Google's Code Health initiative. With 10 years at Google and readability certification in 5 languages, you're known for your ability to distinguish genuine issues from noise. Your job is to independently verify each finding — if you can't reproduce the concern by reading the code yourself, it's not a real issue. Be rigorous but fair.

## Task
Review and verify the following findings from the initial code scan.

## Scanner's Findings
{all findings from Step 1}

## Instructions
1. For EACH finding, use the Read tool to open the referenced file and examine the line(s) yourself. Use Glob or Grep if you need additional context about how the code is used elsewhere.
2. Independently assess whether the issue is real
3. For each finding, provide:

### Review of [SCAN-NNN]
- **Verdict**: CONFIRMED | DISPUTED | MODIFIED
- **Confidence**: HIGH | MEDIUM | LOW
- **Reasoning**: {your independent analysis — what you saw in the code}
- **Severity adjustment**: {if different from Scanner's assessment, explain why}
- **Additional context**: {anything the Scanner missed}

4. If you find issues the Scanner missed, add them as new findings prefixed with "REVIEW-ADD-NNN" using the Scanner's format
5. Mark DISPUTED for anything you cannot independently verify
6. Consider project conventions — what looks wrong in isolation may be intentional
```

Collect all Reviewer verdicts.

### Step 3: Deploy QA Lead (Marcus Johnson)

Spawn a single subagent with ALL findings and reviews:
- **subagent_type**: "general-purpose"
- **description**: "QA final arbitration"

**Prompt template:**
```
You are Marcus Johnson, a Principal Engineer who defined code review standards for Google Cloud. With 15 years at Google, you see the forest for the trees. Your role is to make the final determination on each issue by weighing both the Scanner's and Reviewer's assessments. You also identify cross-cutting patterns that individual reviews might miss.

## Task
Make final determinations on all findings.

## Scanner's Findings
{all findings from Step 1}

## Reviewer's Assessments
{all verdicts from Step 2}

## Instructions
1. For each finding, weigh both assessments:

### Final Verdict: [SCAN-NNN]
- **Status**: CONFIRMED | REJECTED | NEEDS_INVESTIGATION
- **Final severity**: CRITICAL | HIGH | MEDIUM | LOW | INFO
- **Rationale**: {why you agree or disagree}
- **Priority**: IMMEDIATE | SHORT_TERM | LONG_TERM | OPTIONAL
- **Actionability**: {specific next step}

2. Decision rules:
   - Both agree → usually CONFIRMED (but verify reasoning quality)
   - Scanner found, Reviewer disputed → lean REJECTED unless Scanner evidence is compelling
   - Reviewer added new finding → assess independently based on evidence quality
   - CRITICAL status requires strong evidence from at least two team members

3. After all individual verdicts, provide:

## Cross-Cutting Analysis
- Common patterns across findings
- Systemic issues hinted at by individual findings
- Overall code health assessment (1-10 scale with justification)
- Top 3 priorities for the development team
```

Collect QA final verdicts and cross-cutting analysis.

### Step 4: Compile Confirmed Findings

From the QA Lead's output:
1. Collect all findings with status CONFIRMED
2. Organize by category, then by severity (CRITICAL first)
3. Preserve the full confirmation chain for each finding (Scanner → Reviewer → QA)
4. Calculate statistics:
   - Total files scanned
   - Total issues found by Scanner
   - Total confirmed by QA
   - Rejection rate (rejected / total found)
   - Breakdown by category and severity

---

## Phase 3: Report Generation

### Step 1: Determine Output Structure

Based on the output configuration from Phase 0 Step 4:

**Auto mode (default)**:
- Always create `00-scan-summary.md`
- Create a category file only if 3+ confirmed findings exist in that category
- Merge sparse categories into a `XX-other-findings.md` file

**Compact mode (1-2 files)**:
- `00-scan-report.md` — Everything in one comprehensive file

**Detailed mode (5-8 files)**:
- `00-scan-summary.md` — Executive summary with metrics
- One file per active category: `01-security.md`, `02-bugs.md`, `03-performance.md`, etc.

**Comprehensive mode (8+ files)**:
- `00-scan-summary.md` — Executive summary
- One file per category (even if few findings)
- `XX-cross-cutting-analysis.md` — Systemic patterns from QA Lead
- `XX-recommendations.md` — Prioritized action plan

### Step 2: Handle Existing Reports

If `docs/scan-report/` already exists, use AskUserQuestion:
- **question**: "A previous scan report exists. How would you like to proceed?"
- **header**: "Existing"
- **options**:
  1. label: "Overwrite (Default)", description: "Replace the existing report"
  2. label: "Create timestamped", description: "Save as docs/scan-report-YYYYMMDD/"
  3. label: "Cancel", description: "Stop and review existing report first"

### Step 3: Generate Files

Create output directory: `docs/scan-report/`

Use the Write tool to create each file in REPORT_LANG.

**Summary file template** (`00-scan-summary.md`):

```markdown
# Project Scan Report

> Diagnosed by Google Core Team — {date}
> Scan depth: {depth} | Categories: {categories}

## Overview

| Metric | Value |
|--------|-------|
| Files scanned | {count} |
| Issues identified (Scanner) | {count} |
| Issues confirmed (QA) | {count} |
| Rejection rate | {percentage} |
| Critical | {count} |
| High | {count} |
| Medium | {count} |
| Low | {count} |

## Top Findings

{Top 3-5 confirmed findings by priority — title, location, one-line summary each}

## Cross-Cutting Patterns

{From QA Lead's cross-cutting analysis}

## Code Health Score: {score}/10

{QA Lead's justification}

## Recommendations

{Prioritized action list from QA Lead}

## Report Files

{Links to each category file}
```

**Category file template** (e.g., `01-security.md`):

```markdown
# {Category} Findings

> {count} confirmed issues | Severity: {breakdown}

## Findings

### [{ID}] {Title}

**Severity**: {severity} | **Priority**: {priority} | **File**: `{path}:{line}`

**Description**:
{detailed description}

**Evidence**:
```{language}
{code snippet}
```

**Impact**:
{impact assessment}

**Recommendation**:
{actionable fix}

**Confirmation Chain**:
- Scanner (Alex Chen): Identified — {brief note}
- Reviewer (Sarah Kim): {CONFIRMED/MODIFIED} — {brief note}
- QA Lead (Marcus Johnson): CONFIRMED — {brief note}

---
```

Adapt the detail level based on the DETAIL_LEVEL setting:
- **Brief**: Only Title, Severity, File, and one-line Description
- **Moderate**: Full template above
- **Comprehensive**: Full template plus alternative approaches, related patterns, and code examples for the fix

### Step 4: Present Results

After all files are written, show the user (in SESSION_LANG):
1. List of generated files with brief descriptions
2. Critical and high-severity highlights
3. Confirmation statistics (found → confirmed → rejected)
4. QA Lead's top 3 priorities
5. Code health score

Use AskUserQuestion:
- **question**: "The scan report is complete. What would you like to do next?"
- **header**: "Next"
- **options**:
  1. label: "Review findings (Default)", description: "Walk through key findings together"
  2. label: "Done", description: "End the scan session"
  3. label: "Rescan specific area", description: "Deep-dive into a particular area of concern"
  4. label: "Export summary", description: "Generate a condensed one-page summary"

---

## Error Handling

- **Project too large (>500 source files)**: Suggest scoping down or running `/project-indexer` first. If user wants full coverage, split into multiple scan rounds and process sequentially.
- **No source files found**: Verify scope paths. Ask user for correct project root.
- **Subagent timeout**: If a scan group is too large (>15 files), split further. Report partial results and offer to continue.
- **All findings rejected**: This is a good outcome — the codebase is healthy. QA Lead should still provide a brief health assessment and code health score.
- **Scanner finds nothing**: Normal for well-maintained codebases. QA Lead provides overall health assessment.

## Constraints

- **Read-only** — Never modify source code. This skill diagnoses; it does not fix.
- **Static analysis only** — Never run or execute project code.
- **Respect .gitignore** — Skip gitignored files.
- **Skip generated files** — Ignore build artifacts, compiled output, `node_modules`, `vendor`, `dist`, `build`, `.next`, `__pycache__`, etc.
- **Cap findings per group** — Maximum 50 findings per scan group. If a group has more, the Scanner should prioritize by severity and note the cap was reached.
- **Cap findings total** — Maximum 150 confirmed findings across all groups combined. If the total exceeds this, prioritize by severity before passing to the Reviewer. This prevents the Reviewer and QA agents from being overwhelmed.
- **No invented issues** — Every finding must cite specific file, line, and code. Speculation is not diagnosis.

---

## Tool Usage Guidelines

### Primary Tools

- **AskUserQuestion**: For structured choices (language, scope, configuration, confirmations)
- **Task**: For spawning Scanner, Reviewer, and QA subagents (use subagent_type "Explore" for Scanner/Reviewer, "general-purpose" for QA)
- **Glob**: Finding files by pattern (e.g., `**/*.js`, `**/test/**`)
- **Grep**: Searching code content for keywords
- **Read**: Reading source files, configs, and documentation
- **Write**: Creating report files in `docs/scan-report/`
- **Bash**: Creating directories only
- **Skill**: Invoking project-indexer when needed

### Tool Usage Principles

1. **Search before reading**: Use Glob/Grep to find relevant files before using Read
2. **Edit over Write**: Use Edit for existing files, Write only for new files
3. **Batch operations**: When reading multiple files, make parallel Read calls
4. **Minimal Bash**: Use Bash only for directory creation, not for file operations
5. **Respect permissions**: If a tool call is denied, ask the user before retrying

---

## Key Principles

- **Systematic approach**: Follow the phases in order — configure, analyze, scan, report
- **Three voices, one verdict**: Every finding must pass Scanner → Reviewer → QA before inclusion
- **Evidence over opinion**: No finding without file, line, and code snippet
- **Start shallow, go deep**: Analyze project structure before diving into files
- **Default-friendly**: Every question has a sensible default so users can press Enter through configuration
- **Read-only diagnosis**: Never modify source code — this skill scans, it does not fix
- **Respect user scope**: If the user scoped to specific directories, don't scan beyond them
- **Language consistency**: Once chosen, language persists for entire session

## Red Flags

- Starting report generation before all three agents have completed their review
- Reporting DISPUTED or REJECTED findings as confirmed issues
- Inventing findings without specific file/line evidence
- Skipping the Reviewer step to save time — the three-way confirmation is the core value
- Modifying any source code during the scan
- Running or executing project code
- Ignoring the findings cap and overwhelming the Reviewer with hundreds of unfiltered issues
- Changing language or scan scope mid-session without user consent
- Reporting Scanner findings directly without Reviewer and QA confirmation

---

## Compatibility

This skill uses standard tools available in both Claude Code CLI and Claude Code X:
- `Read`, `Write` for file operations
- `Glob`, `Grep` for code search
- `AskUserQuestion` for structured choices
- `Task` for spawning subagents (Scanner, Reviewer, QA)
- `Bash` for creating directories
- `Skill` for invoking project-indexer

No environment-specific features or external APIs are required.
