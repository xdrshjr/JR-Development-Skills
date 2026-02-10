---
name: bug-diagnosis
description: Systematic bug diagnosis and code fixing through structured problem analysis. Use when the user reports a bug, error, unexpected behavior, or asks to "diagnose", "debug", "troubleshoot", "find the problem", or "fix this issue". Also use when the user mentions "查找bug", "诊断问题", or "修复错误" in Chinese.
---

# Bug Diagnosis & Fixing

## Overview

Guide coding agents through systematic bug diagnosis and fixing using structured problem intake, index-aware code analysis, hypothesis-driven root cause identification, and verified fixes with optional test execution.

**Core principle:** Diagnose systematically before fixing. Understand the problem deeply through structured questions, leverage project context for efficient analysis, present clear hypotheses with alternatives, then fix immediately with verification.

## When to Use

- User reports a bug, error, or unexpected behavior
- User asks to diagnose, debug, troubleshoot, or find a problem
- User describes something that "doesn't work" or "is broken"
- User mentions error messages, crashes, or incorrect output
- User wants to investigate why something is failing

**Do NOT use when:**
- User wants to add a new feature (use planning-with-discovery instead)
- User wants general code review or refactoring
- User is asking conceptual questions without a specific bug

## The Process

### Phase 0: Initialization

#### Step 1: Language Selection

Ask the user which language to use for this diagnosis session:

```
Which language would you like to use for this diagnosis session?
A) English
B) Chinese (中文)
```

Store the choice and use it for all subsequent interactions and generated files.

#### Step 2: Mode Selection

Ask the user how they want to proceed:

```
How would you like to proceed?
A) Semi-automatic - I'll ask questions and confirm decisions with you
B) Fully automatic - I'll handle everything after you describe the problem
```

Store the mode. This affects all subsequent phase behaviors:
- **Semi-automatic:** Interactive with user confirmations at key decision points
- **Fully automatic:** Autonomous operation after initial problem description

---

### Phase 1: Problem Intake

#### Step 1: Get Problem Description

Ask the user to describe the problem:

```
Please describe the problem you're experiencing. Include:
- What's happening (the symptom)
- What you expected to happen
- Any error messages or unexpected behavior
```

Wait for the user's response. Parse and store the problem description carefully.

#### Step 2: Round 1 - Standard Diagnostic Questions

**Semi-automatic mode only.** Present these 5 questions as a batch:

1. **Error Evidence:** "Do you have error messages, stack traces, or logs? If yes, please share them."
2. **Reproduction:** "Can you reliably reproduce this issue? If yes, what are the exact steps?"
3. **Timing:** "When did this start happening? (Always broken / Started recently / After a specific change)"
4. **Frequency:** "How often does it occur? (Every time / Sometimes / Rarely)"
5. **Scope:** "What parts of the system are affected? (Single feature / Multiple features / Entire application)"

Wait for answers. Store all responses for analysis.

#### Step 3: Round 2 - Context-Specific Questions

**Semi-automatic mode only.** Based on the problem description and Round 1 answers, dynamically generate 5 follow-up questions. Use your judgment to ask what's most important.

**Example questions to consider:**
- If it's a recent regression: "What changed recently? (Code, dependencies, config, environment)"
- If it's intermittent: "Are there any patterns? (Time of day, specific users, data conditions)"
- If error messages exist: "What happens right before the error? What's the user flow?"
- If it affects multiple features: "What do the affected features have in common?"
- If environment-related: "Does it happen in all environments or just specific ones?"
- If data-related: "What data or inputs trigger the issue?"
- If UI-related: "What browser/device are you using?"
- If API-related: "What's the request/response? Any network issues?"

Present your 5 most relevant questions as a batch. Wait for answers.

**Fully automatic mode:** Skip both question rounds entirely. Proceed directly to Phase 2 with only the initial problem description.

---

### Phase 2: Diagnosis

#### Step 1: Check for Project Index

Look for an existing project index in these standard locations (in order):

1. `docs/PROJECT_INDEX.md`
2. `CLAUDE.md` (check if it contains an index section)
3. `.claude/project-index.md`
4. `docs/project-index.md`

**If index found:**
- Read it completely
- Use it to identify relevant subsystems, modules, and files related to the problem

**If index NOT found:**

- **Semi-automatic mode:** Ask the user:
  ```
  No project index found. Would you like me to create one using the project-indexer skill?
  This will help me understand the codebase structure and diagnose more efficiently.

  A) Yes, create an index
  B) No, proceed without it
  ```

  If user chooses A, invoke the project-indexer skill, then read the generated index.

- **Fully automatic mode:** Automatically invoke the project-indexer skill to create an index, then read it.

**If project-indexer skill is not available:**
- Proceed without an index
- Use Glob and Grep more extensively
- Note in the final summary that diagnosis was performed without project context

#### Step 2: Initial Code Analysis (Shallow First)

**Strategy:**

1. **Extract keywords** from the problem description:
   - Feature names, component names, function names
   - Error messages, exception types
   - File names or paths mentioned by the user
   - Technology-specific terms (API endpoints, database tables, etc.)

2. **Search the codebase:**
   - Use Grep to search for these keywords
   - Use the project index (if available) to narrow down to relevant subsystems
   - Identify 3-5 files that are most likely related to the problem

3. **Read the identified files:**
   - Use Read tool to examine the code
   - Look for the specific functionality mentioned in the problem
   - Analyze the code flow and logic
   - Form initial hypotheses about the root cause

**Important:** Start with reading only 3-5 files maximum. Don't read extensively yet.

#### Step 3: Form Root Cause Hypothesis

**If a clear root cause is identified:**

- Formulate a clear hypothesis
- Identify the specific code location (file:line)
- Explain why this code is causing the observed problem
- Consider 1-2 alternative possibilities if they exist

**If root cause is unclear after initial analysis:**

**Expand the search scope:**
1. Look at files imported by or importing the suspicious files
2. Check configuration files (package.json, .env, config files)
3. Examine test files for clues about expected behavior
4. Search for related error handling code
5. Read up to 5-10 additional files

**Re-analyze** with the broader context and attempt to form a hypothesis.

**If still unclear after expansion:**
- Acknowledge the uncertainty
- Present the most likely possibilities based on available evidence
- In semi-automatic mode: ask for user input (see Step 4)
- In fully automatic mode: proceed with the best hypothesis and document uncertainty

#### Step 4: Present Findings and Get Confirmation

**Semi-automatic mode:**

Present the diagnosis in this format:

```
## Root Cause Analysis

**Primary Hypothesis:**
[Most likely cause with file:line reference]

**Why this causes the problem:**
[Clear explanation linking the code to the observed symptom]

**Alternative Possibilities:**
1. [Second most likely cause, if relevant]
2. [Third possibility, if relevant]

Do you agree with this diagnosis, or would you like to:
A) Proceed with the primary hypothesis
B) Investigate one of the alternatives (specify which)
C) Share your own hypothesis for me to investigate
```

Wait for user response:
- **If A:** Proceed to Phase 3
- **If B:** Investigate the chosen alternative, then re-present findings
- **If C:** Ask user to describe their hypothesis, investigate it, then re-present findings

**Fully automatic mode:**
- Skip user confirmation
- Proceed directly to Phase 3 with the primary hypothesis
- Log the diagnosis internally (will be saved in Phase 3)

---

### Phase 3: Fix & Verify

#### Step 1: Implement the Fix

**Actions:**

1. Make the necessary code changes using Edit or Write tools
2. Fix only what's needed to address the root cause
3. Do NOT refactor, add features, or make "improvements" beyond the fix
4. Ensure the fix directly resolves the identified problem

**Present the changes to the user:**

```
## Fix Applied

**Files modified:**
- path/to/file1.js:42 - [brief description of change]
- path/to/file2.py:15 - [brief description of change]

**What changed:**
[Concise explanation of the fix and how it resolves the root cause]
```

#### Step 2: Test Verification

**Semi-automatic mode:**

Ask the user:
```
Would you like me to run tests to verify the fix?
A) Yes, run relevant tests
B) No, I'll test manually
C) Run all tests
```

Wait for response and act accordingly.

**Fully automatic mode:**

Automatically attempt to run tests:
1. Look for test commands in common locations:
   - `package.json` scripts (npm test, npm run test)
   - `Makefile` (make test)
   - Common patterns (pytest, jest, go test, cargo test, etc.)
2. If tests are found, run them
3. If no tests found, skip and note in the summary

**Test execution:**
- Use Bash to run the test command
- Capture the output
- Report results to the user:
  - ✓ Tests passed
  - ✗ Tests failed (show failures)
  - ⚠ No tests found

**If tests fail after the fix:**
- Analyze the test failures
- Determine if:
  - Tests are outdated and need updating
  - The fix introduced a new issue
  - Tests were already failing (unrelated)
- **Semi-automatic mode:** Present findings and ask how to proceed
- **Fully automatic mode:** Attempt to fix test failures (1 retry only), then report final status

#### Step 3: Create Diagnosis Summary

**Always create a lightweight summary** in `.claude/diagnoses/`

1. Create the directory if it doesn't exist:
   ```bash
   mkdir -p .claude/diagnoses
   ```

2. Generate a filename:
   - Format: `YYYY-MM-DD-HHMM-<issue-slug>.md`
   - Issue slug: kebab-case, max 50 chars, derived from problem description
   - Example: `2026-02-10-1430-login-timeout-error.md`

3. Write the summary file with this content:

```markdown
# Bug Diagnosis: <issue-slug>

**Date:** YYYY-MM-DD HH:MM
**Mode:** [Semi-automatic | Fully automatic]
**Status:** [Fixed | Partially fixed | Needs verification]

## Problem Description

[User's original problem description]

## Root Cause

[The identified root cause with file:line references]

**Explanation:**
[Why this code caused the problem]

## Fix Applied

**Files modified:**
- path/to/file1.js:42 - [description]
- path/to/file2.py:15 - [description]

**Changes:**
[Summary of what was changed]

## Verification

[Test results or verification status]

## Notes

[Any additional context, alternative hypotheses considered, uncertainties, or follow-up needed]
```

#### Step 4: Completion

Present the final summary to the user:

```
## Diagnosis Complete ✓

**Summary:**
- Problem: [one-line summary]
- Root cause: [one-line summary with file:line]
- Fix: [one-line summary of changes]
- Tests: [passed/failed/not run]

**Diagnosis report saved to:** .claude/diagnoses/YYYY-MM-DD-HHMM-<issue-slug>.md

Would you like me to:
A) Commit these changes
B) Diagnose another issue
C) Nothing else, we're done
```

Wait for user response:
- **If A:** Use git to stage and commit the changes with an appropriate message
- **If B:** Start over from Phase 1 with a new problem
- **If C:** End the session

---

## Edge Cases & Special Situations

### Multiple Bugs Detected

If the problem description suggests multiple distinct issues:

1. Acknowledge that multiple issues were detected
2. List them briefly
3. **Semi-automatic mode:** Ask which to tackle first
4. **Fully automatic mode:** Choose the most critical or first-mentioned issue
5. After fixing one, offer to diagnose the next

### Cannot Identify Root Cause

If after expanding the search scope, the root cause is still unclear:

**Semi-automatic mode:**
- Present what you've learned so far
- Ask for more information:
  - Request more detailed error logs
  - Suggest adding debug logging to gather more data
  - Ask if user can provide a minimal reproduction case
- Offer to investigate specific areas the user suspects

**Fully automatic mode:**
- Document the uncertainty in the summary
- Make a best-effort fix based on the most likely hypothesis
- Mark status as "Needs verification" in the summary
- Suggest next steps in the completion message

### Fix Requires Breaking Changes

If the proper fix would require breaking changes or major refactoring:

1. **Always alert the user** (even in fully automatic mode)
2. Present the scope of changes required
3. Ask for confirmation before proceeding
4. Offer alternative smaller fixes if possible:
   - Workarounds
   - Partial fixes
   - Temporary solutions

### Tests Fail After Fix

If tests fail after applying the fix:

1. Analyze the test failures carefully
2. Determine the cause:
   - Are tests outdated?
   - Did the fix introduce a new issue?
   - Were tests already failing?

**Semi-automatic mode:**
- Present the analysis
- Ask: "Should I update the tests, revise the fix, or investigate further?"

**Fully automatic mode:**
- Attempt to fix the issue (1 retry only)
- If still failing, report the situation and mark as "Needs verification"

### No Project Index Available

If no index exists and project-indexer skill is not available:

1. Proceed without an index
2. Use Glob and Grep more extensively:
   - Search for common patterns
   - Look in standard directories (src/, lib/, app/, etc.)
3. Document in the summary that diagnosis was performed without project context
4. Suggest creating an index for future diagnoses

### User Disagrees with Diagnosis

If the user disagrees with all presented hypotheses (semi-automatic mode):

1. Ask the user to describe their hypothesis or suspicion
2. Investigate the area they suggest
3. Read relevant code and analyze
4. Either confirm their hypothesis or present new findings
5. Update the diagnosis based on the investigation

---

## Tool Usage Guidelines

### Primary Tools

- **AskUserQuestion:** For structured choices (language, mode, confirmations)
- **Glob:** Finding files by pattern (e.g., `**/*.js`, `**/test/**`)
- **Grep:** Searching code content for keywords
- **Read:** Reading source files, configs, and documentation
- **Edit:** Making targeted fixes to existing files
- **Write:** Creating diagnosis summaries
- **Bash:** Running tests, creating directories
- **Skill:** Invoking project-indexer when needed

### Tool Usage Principles

1. **Search before reading:** Use Grep to find relevant files before using Read
2. **Edit over Write:** Use Edit for existing files, Write only for new files
3. **Batch operations:** When reading multiple files, make parallel Read calls
4. **Minimal Bash:** Use Bash only for tests and directory creation, not for file operations
5. **Respect permissions:** If a tool call is denied, ask the user before retrying

---

## Key Principles

- **Systematic approach:** Follow the phases in order, don't skip steps
- **Start shallow, go deep:** Read 3-5 files first, expand only if needed
- **Present alternatives:** Never force a single hypothesis without alternatives
- **Fix immediately:** Once diagnosis is confirmed, fix right away and show changes
- **Mode-appropriate automation:** Respect the user's chosen interaction level
- **Lightweight documentation:** Track diagnoses without cluttering the project
- **No over-engineering:** Fix the bug, don't refactor or add features
- **Test when possible:** Verify fixes with tests when available

## Red Flags

- Starting to fix code before understanding the root cause
- Reading dozens of files without a clear search strategy
- Making changes beyond what's needed to fix the bug
- Skipping user confirmation in semi-automatic mode
- Forcing a diagnosis when evidence is weak
- Not documenting the diagnosis process
- Ignoring test failures after applying a fix
- Changing the mode or language mid-session without user consent

## Compatibility

This skill uses only standard tools available in both Claude Code CLI and Claude Code X:
- `Read`, `Write`, `Edit` for file operations
- `Glob`, `Grep` for code search
- `AskUserQuestion` for structured choices
- `Bash` for running tests and creating directories
- `Skill` for invoking project-indexer

No environment-specific features or external APIs are required.
