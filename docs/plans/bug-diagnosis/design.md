# Bug Diagnosis Skill - Design Document

**Date:** 2026-02-10
**Status:** Approved
**Target:** Claude Code / Code X agents

---

## Overview

A systematic bug diagnosis and fixing skill that guides coding agents through structured problem analysis, root cause identification using project context, and verified fixes with optional test execution.

### Core Capabilities

- **Dual-mode operation:** Semi-automatic (interactive) and Fully automatic
- **Structured problem intake:** Standard diagnostic questions + context-specific follow-ups
- **Index-aware diagnosis:** Leverages project structure for efficient code navigation
- **Hypothesis-driven analysis:** Presents alternatives and welcomes user input
- **Verified fixes:** Optional test execution with results reporting
- **Lightweight tracking:** Auto-generated diagnosis summaries

---

## Skill Metadata

**Name:** `bug-diagnosis`
**Slash command:** `/bug-diagnosis`

**Trigger phrases:**
- "diagnose this bug"
- "find the problem"
- "debug this issue"
- "troubleshoot"
- "查找bug" / "诊断问题" (Chinese)

**Description:**
*"Systematic bug diagnosis and fixing through structured problem analysis. Guides agents through problem intake, root cause analysis using project context, and verified fixes with optional test execution."*

---

## Architecture: Linear State Machine

The skill follows a clear 4-phase linear flow with mode-dependent behavior:

```
Phase 0: Initialization
├─ Ask: Language preference (English/Chinese)
└─ Ask: Mode (Semi-automatic/Fully automatic)

Phase 1: Problem Intake
├─ Get problem description
├─ Round 1: 5 standard diagnostic questions
└─ Round 2: 5 context-specific follow-up questions
    (Skip rounds in fully automatic mode)

Phase 2: Diagnosis
├─ Check for project index (standard locations)
├─ Offer to create index if missing (semi-auto: ask, full-auto: create)
├─ Analyze problem with shallow code reading
├─ If unclear: Expand search scope
├─ Present root cause hypothesis
└─ Semi-auto: Get user confirmation (with alternatives)
    Full-auto: Proceed directly

Phase 3: Fix & Verify
├─ Implement fix immediately
├─ Show changes to user
├─ Semi-auto: Ask about running tests
    Full-auto: Run tests automatically
└─ Create lightweight diagnosis summary in .claude/diagnoses/
```

---

## Mode Behavior Matrix

| Action | Semi-Automatic | Fully Automatic |
|--------|---------------|-----------------|
| Language selection | Ask | Ask |
| Mode selection | Ask | Ask |
| Problem description | Ask | Ask |
| Diagnostic questions | Ask 2 rounds | Skip |
| Create index | Ask permission | Create automatically |
| Root cause confirmation | Present alternatives + ask | Proceed with best hypothesis |
| Run tests | Ask | Run automatically |

---

## Phase 0: Initialization

### Step 1: Language Selection

```
Present to user:
"Which language would you like to use for this diagnosis session?
A) English
B) Chinese (中文)"

Store choice, use for all subsequent interactions and generated files.
```

### Step 2: Mode Selection

```
Present to user:
"How would you like to proceed?
A) Semi-automatic - I'll ask questions and confirm decisions with you
B) Fully automatic - I'll handle everything after you describe the problem"

Store mode, affects all subsequent phase behaviors.
```

---

## Phase 1: Problem Intake

### Step 1: Get Problem Description

```
Ask: "Please describe the problem you're experiencing. Include:
- What's happening (the symptom)
- What you expected to happen
- Any error messages or unexpected behavior"

Wait for user response.
Parse and store the problem description.
```

### Step 2: Round 1 - Standard Diagnostic Questions

**Semi-automatic mode only.** Ask these 5 questions as a batch:

1. **Error Evidence:** "Do you have error messages, stack traces, or logs? If yes, please share them."
2. **Reproduction:** "Can you reliably reproduce this issue? If yes, what are the exact steps?"
3. **Timing:** "When did this start happening? (Always broken / Started recently / After a specific change)"
4. **Frequency:** "How often does it occur? (Every time / Sometimes / Rarely)"
5. **Scope:** "What parts of the system are affected? (Single feature / Multiple features / Entire application)"

Wait for answers. Store responses.

### Step 3: Round 2 - Context-Specific Questions

**Semi-automatic mode only.** Based on the problem description and Round 1 answers, dynamically generate 5 follow-up questions.

**Example questions:**
- If it's a recent regression: "What changed recently? (Code, dependencies, config, environment)"
- If it's intermittent: "Are there any patterns? (Time of day, specific users, data conditions)"
- If error messages exist: "What happens right before the error? What's the user flow?"
- If it affects multiple features: "What do the affected features have in common?"
- If environment-related: "Does it happen in all environments or just specific ones?"

The agent should use judgment to ask the most relevant questions based on what's been learned so far.

**Fully automatic mode:** Skip both rounds entirely, proceed to Phase 2 with only the initial problem description.

---

## Phase 2: Diagnosis

### Step 1: Project Index Check

**Check standard locations in order:**
1. `docs/PROJECT_INDEX.md`
2. `CLAUDE.md` (look for index section)
3. `.claude/project-index.md`
4. `docs/project-index.md`

**If index found:**
- Read it
- Use it to identify relevant subsystems/files

**If index NOT found:**
- **Semi-auto mode:** Ask user: "No project index found. Would you like me to create one using the project-indexer skill? This will help me understand the codebase structure. (Yes/No)"
- **Full-auto mode:** Automatically invoke project-indexer skill to create index
- After creation, read and use the index

### Step 2: Initial Code Analysis (Shallow)

**Strategy:**
1. Use the problem description to identify keywords (feature names, file names, error messages, function names)
2. Use Grep to search for these keywords in the codebase
3. Use the project index (if available) to narrow down to relevant subsystems
4. Read only the files that are directly related to the problem
5. Analyze the code to form initial hypotheses

**Limit:** Start with reading 3-5 files maximum

### Step 3: Root Cause Hypothesis

**If a clear root cause is identified:**
- Formulate the hypothesis clearly
- Identify the specific code location (file:line)
- Explain why this is causing the observed problem

**If root cause is unclear:**
- **Expand search scope:**
  - Look at adjacent files (imports, dependencies)
  - Check configuration files
  - Examine test files for clues
  - Read up to 5-10 more files
- **Re-analyze** with broader context
- If still unclear after expansion, proceed to "uncertain diagnosis" flow

### Step 4: Present Findings

**Semi-automatic mode:**

Present the diagnosis in this format:
```
## Root Cause Analysis

**Primary Hypothesis:**
[Most likely cause with file:line reference]

**Why this causes the problem:**
[Explanation linking the code to the observed symptom]

**Alternative Possibilities:**
1. [Second most likely cause]
2. [Third possibility if relevant]

Do you agree with this diagnosis, or would you like to:
A) Proceed with the primary hypothesis
B) Investigate one of the alternatives
C) Share your own hypothesis for me to investigate
```

Wait for user response. Handle A/B/C accordingly.

**Fully automatic mode:**
- Proceed directly with the primary hypothesis
- Log the diagnosis to internal state (will be saved in Phase 3)

---

## Phase 3: Fix & Verify

### Step 1: Implement the Fix

**Actions:**
1. Make the necessary code changes using Edit or Write tools
2. Fix only what's needed - no refactoring or "improvements"
3. Ensure the fix directly addresses the identified root cause

**Output to user:**
```
## Fix Applied

**Files modified:**
- path/to/file1.js:42 - [brief description of change]
- path/to/file2.py:15 - [brief description of change]

**What changed:**
[Concise explanation of the fix and how it resolves the root cause]
```

### Step 2: Test Verification

**Semi-automatic mode:**
```
Ask user: "Would you like me to run tests to verify the fix?
A) Yes, run relevant tests
B) No, I'll test manually
C) Run all tests"
```

**Fully automatic mode:**
- Automatically attempt to run relevant tests
- Look for test commands in package.json, Makefile, or common patterns
- If tests exist: run them
- If no tests found: skip and note in summary

**Test execution:**
- Use Bash to run tests
- Capture output
- Report results to user (pass/fail/errors)

### Step 3: Create Diagnosis Summary

**Location:** `.claude/diagnoses/YYYY-MM-DD-HHMM-<issue-slug>.md`

**Content format:**
```markdown
# Bug Diagnosis: <issue-slug>

**Date:** YYYY-MM-DD HH:MM
**Mode:** [Semi-automatic | Fully automatic]
**Status:** [Fixed | Partially fixed | Needs verification]

## Problem Description
[User's original problem description]

## Root Cause
[The identified root cause with file:line references]

## Fix Applied
[List of changes made]

## Verification
[Test results or verification status]

## Notes
[Any additional context, alternative hypotheses considered, or follow-up needed]
```

**Create the directory if it doesn't exist:**
- Use Bash: `mkdir -p .claude/diagnoses`

### Step 4: Completion

**Present to user:**
```
## Diagnosis Complete ✓

**Summary:**
- Problem: [one-line summary]
- Root cause: [one-line summary]
- Fix: [one-line summary]
- Tests: [passed/failed/not run]

**Diagnosis report saved to:** .claude/diagnoses/YYYY-MM-DD-HHMM-<issue-slug>.md

Would you like me to:
A) Commit these changes
B) Diagnose another issue
C) Nothing else, we're done
```

Wait for user response and handle accordingly.

---

## Edge Cases & Error Handling

### 1. Multiple Bugs in Problem Description
- Acknowledge multiple issues detected
- Ask user (semi-auto) or decide automatically (full-auto) which to tackle first
- After fixing one, offer to diagnose the next

### 2. Cannot Reproduce/Understand the Problem
- After expanding search, if still unclear:
  - Semi-auto: Ask for more details, suggest adding debug logging, or request a minimal reproduction
  - Full-auto: Document uncertainty in the summary, make best-effort fix with caveats

### 3. Fix Requires Breaking Changes or Major Refactoring
- Always alert the user before making large-scale changes
- Present the scope and ask for confirmation (even in full-auto mode)
- Offer alternative smaller fixes if possible

### 4. Tests Fail After the Fix
- Don't panic - analyze test failures
- Determine if tests are outdated or if fix introduced new issues
- Semi-auto: Present findings and ask how to proceed
- Full-auto: Attempt to fix test failures, but limit to 1 retry attempt

### 5. No Project Index and project-indexer Skill Not Available
- Proceed without index
- Use Glob and Grep more extensively
- Document in summary that diagnosis was done without project context

### 6. User Disagrees with All Presented Hypotheses
- Ask user to describe their hypothesis
- Investigate their suggested angle
- Update diagnosis based on new direction

---

## Tool Usage Guidelines

### Primary Tools

- `AskUserQuestion` - For structured choices (language, mode, confirmations)
- `Glob` - Finding files by pattern
- `Grep` - Searching code content
- `Read` - Reading source files
- `Edit` - Making targeted fixes
- `Write` - Creating diagnosis summaries
- `Bash` - Running tests, creating directories
- `Skill` - Invoking project-indexer when needed

### Tool Usage Principles

- Use Grep before Read (search before reading)
- Use Edit over Write for existing files
- Batch Read calls when reading multiple files
- Keep Bash usage minimal (tests and directory creation only)

---

## File Naming Conventions

### Diagnosis Summaries
- **Format:** `YYYY-MM-DD-HHMM-<issue-slug>.md`
- **Issue slug:** kebab-case, max 50 chars, derived from problem description
- **Example:** `2026-02-10-1430-login-timeout-error.md`

### Standard Index Locations (Priority Order)
1. `docs/PROJECT_INDEX.md`
2. `CLAUDE.md`
3. `.claude/project-index.md`
4. `docs/project-index.md`

---

## Language Support

### Supported Languages
English, Chinese (extensible to others)

### What Gets Translated
- All user-facing prompts and questions
- Diagnosis summary content
- Error messages and status updates

### What Stays in English
- Code comments in fixes (unless original code uses another language)
- File paths and technical identifiers
- Tool invocations and internal logic

---

## Compatibility

### Works With
- Claude Code CLI
- Claude Code X
- Any environment with standard Claude Code tools

### Dependencies
- **Optional:** project-indexer skill (gracefully degrades if unavailable)
- **No external tools or APIs required**

---

## Implementation Notes

### Key Principles
- **Start shallow, go deep only if needed** - Efficient code reading strategy
- **Present alternatives** - Never force a single hypothesis on the user
- **Fix immediately, show changes** - Direct and transparent
- **Mode-appropriate automation** - Respect user's chosen interaction level
- **Lightweight documentation** - Track without cluttering

### Success Criteria
- Agent can diagnose and fix bugs with minimal user input (full-auto mode)
- Agent provides clear explanations and alternatives (semi-auto mode)
- Diagnosis summaries are useful for future reference
- Integration with project-indexer enhances efficiency
- Works reliably across different project types and languages

---

## Next Steps

1. **Write SKILL.md** - Implement the skill prompt following this design
2. **Write README.md** - Create user-facing documentation
3. **Create _meta.json** - Add skill metadata
4. **Test with real bugs** - Validate the workflow with actual debugging scenarios
5. **Update main README** - Add bug-diagnosis to the skills collection list
