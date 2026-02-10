# Bug Diagnosis

A Claude Code skill that systematically diagnoses and fixes bugs through structured problem analysis, index-aware code exploration, and verified fixes.

## Problem

When bugs occur, developers often jump straight to fixing without fully understanding the root cause. This leads to:
- Incomplete fixes that don't address the real issue
- New bugs introduced by hasty changes
- Wasted time investigating the wrong areas
- Lack of documentation about what was fixed and why

## Solution

Bug Diagnosis provides a systematic approach to finding and fixing bugs:
- **Structured problem intake** - Gather comprehensive information before diving into code
- **Index-aware analysis** - Leverage project structure for efficient code navigation
- **Hypothesis-driven diagnosis** - Present clear root causes with alternatives
- **Immediate fixes** - Apply changes and show what was modified
- **Test verification** - Run tests to confirm the fix works
- **Lightweight tracking** - Auto-generate diagnosis summaries for future reference

## Usage

### Trigger the Skill

Say any of these to Claude Code:
- "diagnose this bug"
- "find the problem"
- "debug this issue"
- "troubleshoot"
- "查找bug" / "诊断问题" (Chinese)
- `/bug-diagnosis`

### Choose Your Mode

**Semi-automatic mode** (Interactive):
- Claude asks diagnostic questions to understand the problem
- You confirm the root cause before fixes are applied
- You decide whether to run tests
- Best for: Complex bugs, learning, or when you want control

**Fully automatic mode** (Autonomous):
- Claude handles everything after you describe the problem
- Automatically creates project index if needed
- Applies fixes and runs tests without asking
- Best for: Clear bugs, time pressure, or when you trust the agent

### Example Session (Semi-automatic)

```
You: "The login form isn't working - users can't sign in"

Claude: "Which language would you like to use?
A) English
B) Chinese"

You: "A"

Claude: "How would you like to proceed?
A) Semi-automatic - I'll ask questions and confirm decisions
B) Fully automatic - I'll handle everything after you describe the problem"

You: "A"

Claude: "Please describe the problem you're experiencing..."

You: "When users click the login button, nothing happens. No error message,
just no response. This started yesterday after we deployed the new UI update."

Claude: [Asks 5 standard diagnostic questions]
1. Do you have error messages, stack traces, or logs?
2. Can you reliably reproduce this issue?
...

You: [Answers questions]

Claude: [Asks 5 context-specific follow-up questions based on your answers]

Claude: [Analyzes code using project index]

Claude: "## Root Cause Analysis

**Primary Hypothesis:**
src/components/LoginForm.tsx:45 - Event handler not properly bound

**Why this causes the problem:**
The onClick handler was changed to an arrow function but 'this' context
is lost, preventing form submission.

**Alternative Possibilities:**
1. API endpoint changed and form is hitting wrong URL
2. Validation logic blocking submission silently

Do you agree with this diagnosis, or would you like to:
A) Proceed with the primary hypothesis
B) Investigate one of the alternatives
C) Share your own hypothesis"

You: "A"

Claude: [Applies fix]

Claude: "## Fix Applied

**Files modified:**
- src/components/LoginForm.tsx:45 - Restored proper event handler binding

**What changed:**
Changed arrow function back to bound method to preserve 'this' context

Would you like me to run tests to verify the fix?
A) Yes, run relevant tests
B) No, I'll test manually
C) Run all tests"

You: "A"

Claude: [Runs tests]

Claude: "## Diagnosis Complete ✓

**Summary:**
- Problem: Login button not responding after UI update
- Root cause: Event handler lost 'this' context (LoginForm.tsx:45)
- Fix: Restored proper method binding
- Tests: ✓ All 12 login tests passed

**Diagnosis report saved to:** .claude/diagnoses/2026-02-10-1430-login-button-not-responding.md

Would you like me to:
A) Commit these changes
B) Diagnose another issue
C) Nothing else, we're done"
```

### Example Session (Fully automatic)

```
You: "The API returns 500 errors when fetching user profiles"

Claude: "Which language would you like to use?
A) English
B) Chinese"

You: "A"

Claude: "How would you like to proceed?
A) Semi-automatic
B) Fully automatic"

You: "B"

Claude: "Please describe the problem..."

You: "GET /api/users/:id returns 500 error. Started after we added
the new profile fields to the database schema."

Claude: [Automatically creates project index if needed]
Claude: [Analyzes code]
Claude: [Identifies root cause]
Claude: [Applies fix]
Claude: [Runs tests automatically]

Claude: "## Diagnosis Complete ✓

**Summary:**
- Problem: API 500 errors on user profile fetch
- Root cause: Database query missing new schema fields (api/users.py:78)
- Fix: Updated query to include new profile fields
- Tests: ✓ 8/8 API tests passed

**Diagnosis report saved to:** .claude/diagnoses/2026-02-10-1445-api-500-user-profiles.md

Would you like me to:
A) Commit these changes
B) Diagnose another issue
C) Nothing else, we're done"
```

## Generated Files

### Diagnosis Summaries

Each diagnosis creates a lightweight summary in `.claude/diagnoses/`:

```
.claude/diagnoses/
└── 2026-02-10-1430-login-button-not-responding.md
```

**Content:**
```markdown
# Bug Diagnosis: login-button-not-responding

**Date:** 2026-02-10 14:30
**Mode:** Semi-automatic
**Status:** Fixed

## Problem Description
Login button not responding after UI update deployment

## Root Cause
src/components/LoginForm.tsx:45 - Event handler lost 'this' context
when changed to arrow function

## Fix Applied
**Files modified:**
- src/components/LoginForm.tsx:45 - Restored proper method binding

## Verification
✓ All 12 login tests passed

## Notes
Alternative hypotheses considered: API endpoint change, validation blocking
```

## Features

### Structured Problem Intake

**Round 1 - Standard Questions:**
- Error evidence (messages, stack traces, logs)
- Reproduction steps
- Timing (when it started)
- Frequency (how often)
- Scope (what's affected)

**Round 2 - Context-Specific:**
- Dynamically generated based on your answers
- Targets the most relevant information gaps
- Adapts to the type of bug (UI, API, data, etc.)

### Index-Aware Diagnosis

- Checks for existing project index in standard locations
- Offers to create index using project-indexer skill if missing
- Uses index to quickly identify relevant code areas
- Starts with shallow reading (3-5 files), expands if needed

### Hypothesis-Driven Analysis

- Presents primary hypothesis with clear file:line references
- Explains why the code causes the observed problem
- Offers 1-2 alternative possibilities
- Welcomes user's own hypotheses for investigation

### Verified Fixes

- Applies fixes immediately and shows what changed
- Runs tests to verify the fix works (mode-dependent)
- Handles test failures gracefully
- No refactoring or "improvements" - just fixes the bug

### Lightweight Tracking

- Auto-generates diagnosis summaries in `.claude/diagnoses/`
- Includes problem, root cause, fix, and verification
- Useful for future reference and team knowledge sharing
- Doesn't clutter main documentation

## Edge Cases Handled

### Multiple Bugs
- Detects when problem description mentions multiple issues
- Asks which to tackle first (or chooses automatically)
- Offers to diagnose remaining issues after fixing one

### Unclear Root Cause
- Expands search scope automatically
- Asks for more information if still unclear
- Makes best-effort fix with documented uncertainty

### Breaking Changes Required
- Alerts user before making large-scale changes
- Asks for confirmation even in fully automatic mode
- Offers alternative smaller fixes when possible

### Test Failures
- Analyzes why tests failed after the fix
- Determines if tests need updating or fix needs revision
- Attempts one retry in fully automatic mode

### No Project Index
- Proceeds without index if unavailable
- Uses Glob and Grep more extensively
- Documents that diagnosis was done without project context

## Integration

### Works With project-indexer

If project-indexer skill is installed:
- Automatically offers to create index if missing
- Uses index for efficient code navigation
- Gracefully degrades if skill is unavailable

### Standalone Operation

Works perfectly fine without any other skills:
- Uses Glob and Grep for code search
- Still provides systematic diagnosis
- All core features remain functional

## Language Support

**Supported languages:** English, Chinese (extensible)

**What gets translated:**
- All prompts and questions
- Diagnosis summaries
- Status messages

**What stays in English:**
- Code and file paths
- Technical identifiers
- Tool invocations

## Tips

1. **Use semi-automatic for learning** - See how systematic diagnosis works
2. **Use fully automatic for speed** - When you trust the agent and have clear bugs
3. **Provide error logs** - The more information upfront, the faster the diagnosis
4. **Keep diagnosis summaries** - Useful for tracking recurring issues
5. **Regenerate index after refactoring** - Keeps diagnosis efficient

## Compatibility

Works with:
- Claude Code CLI
- Claude Code X
- Any environment with standard Claude Code tools

No external dependencies or APIs required.

## License

MIT
