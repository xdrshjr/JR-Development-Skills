# Orchestration & Agent Workflow Guide

Detailed reference for Phase 4-5: team assembly, agent prompts, code review, and error handling.

## Contents

- [Task Orchestration File Structure](#task-orchestration-file-structure)
- [Agent Assignment Brief Template](#agent-assignment-brief-template)
- [Agent Prompt Template](#agent-prompt-template)
- [Code Review Agent Template](#code-review-agent-template)
- [Error Handling](#error-handling)
- [Phase-Gated Execution Flow](#phase-gated-execution-flow)

## Task Orchestration File Structure

`task-orchestration.md` drives all of Phase 4-5. It contains 5 sections:

### Section 1: Dependency Graph

Mermaid `graph TD` diagram. All task units as nodes, dependency edges between them. Color-code by parallel group.

- **With TODOs:** Use TODO dependency annotations (`depends_on`, `blocks`, `parallel_group`) directly
- **Without TODOs:** Derive dependencies from spec module relationships and master plan architecture. The orchestration file becomes the SOLE source of dependency relationships

### Section 2: Execution Phases

Break tasks into ordered execution phases:

| Phase | Rule | Parallelism |
|-------|------|-------------|
| 1 | Tasks with NO dependencies | All parallel |
| 2 | Depends ONLY on Phase 1 | Parallel within phase |
| N | Depends on Phase N-1 or earlier | Parallel within phase |

Cap concurrent agents at 5-7 to avoid resource contention.

### Section 3: Critical Path

Longest dependency chain. Highlight bottleneck tasks. These determine minimum total execution time.

### Section 4: Agent Assignment Recommendations

- Recommended parallel agent count (max 5-7 concurrent)
- Task-to-agent mapping maximizing parallelism
- Coordination notes: agents sharing interfaces, APIs, or data models

### Section 5: Context Files for Agents

Every agent MUST read before coding:
- `master-plan.md`
- All `specs/*.md`
- All `todos/*.md` (if generated)
- `task-orchestration.md`

Per-agent: highlight which spec/TODO files are most relevant to their assigned tasks.

---

## Agent Assignment Brief Template

For each agent in Step 4.2, prepare:

```
Agent: {name} (e.g., google-eng-01)
Profile: {team persona — from team-profiles.md}

== Assigned Tasks ==
- {TODO/spec reference}: {brief description}
- {TODO/spec reference}: {brief description}

== Dependencies ==
Blocked by: {list tasks that must complete first}
Blocks: {list tasks waiting on this agent}
Parallel peers: {agents running in same execution phase}

== Required Reading ==
Global: master-plan.md, all specs, all TODOs, task-orchestration.md
Focus: {specific spec/TODO files for this agent's tasks}

== Coordination ==
{Shared interfaces, API contracts, data models with other agents}

== Completion Criteria ==
{Clear definition of "done" for each task}
```

---

## Development Subagent Prompt Template

Each subagent is spawned via the `Agent` tool in Step 4.3. Use `run_in_background: true` for parallel subagents.

```python
Agent(
    description="Dev: {task-summary}",
    prompt="""
You are {agent name}, a {team persona description from team-profiles.md}.

BEFORE WRITING ANY CODE, you MUST use the Read tool to read these planning documents:
- docs/plans/{topic}/master-plan.md
- docs/plans/{topic}/task-orchestration.md
- docs/plans/{topic}/specs/01-{name}.md
- docs/plans/{topic}/specs/02-{name}.md
- ... (all spec files)
- docs/plans/{topic}/todos/01-{name}.md (if generated)
- ... (all TODO files)

YOUR ASSIGNMENT:
{specific tasks from assignment brief}

DEPENDENCIES:
- Waiting on: {tasks that must complete before you start}
- Your work blocks: {tasks that cannot start until you finish}
- Parallel peers: {agents working alongside you}

COORDINATION:
{shared interfaces/contracts}

COMPLETION:
When you finish, report:
1. List of all files you created or modified
2. Summary of what you implemented
3. Any concerns or edge cases you noticed

Do NOT consider your work final. A code review subagent will automatically
review your code and fix any issues found.
""",
    run_in_background=True  # for parallel execution within same phase
)
```

---

## Code Review Subagent Template

**Auto-triggered** — the orchestrator MUST spawn this subagent immediately when any dev subagent reports completion. No user confirmation needed.

```python
Agent(
    description="Code review for {dev-agent-name}",
    prompt="""
You are a senior code reviewer from {team profile, same as the dev team}.

TASK: Review and fix the code written by {dev-agent-name}.

STEP 1 — READ CONTEXT:
Use the Read tool to read ALL planning documents:
- docs/plans/{topic}/master-plan.md
- docs/plans/{topic}/task-orchestration.md
- docs/plans/{topic}/specs/*.md (all spec files)
- docs/plans/{topic}/todos/*.md (all TODO files, if they exist)

STEP 2 — READ THE CODE:
Read all files created/modified by the dev agent:
{list of files from dev agent's completion report}

STEP 3 — REVIEW CHECKLIST:
Check each item. For every issue found, fix it directly using the Edit tool:
- [ ] Correctness: Does implementation match the spec?
- [ ] Code quality: Clean code, proper naming, no code smells?
- [ ] Security: No OWASP top 10 vulnerabilities introduced?
- [ ] Testing: Are tests adequate and meaningful?
- [ ] Integration: Will this work with code from other agents?
- [ ] TODO compliance: Are all checklist items from the TODO addressed?

STEP 4 — REPORT:
- If you fixed issues: list every change you made and why
- If no issues found: confirm the code passes review
- Rate overall quality: PASS / PASS WITH FIXES / NEEDS REWORK
""",
    mode="auto"
)
```

**NEEDS REWORK** means the review subagent found issues too severe to fix inline. In this case, the orchestrator should spawn a new dev subagent to rework the task, then re-trigger code review.

---

## Error Handling

### Agent Failure

If any agent fails (tool error, timeout, no output), ask user via `AskUserQuestion`:

| Option | Action |
|--------|--------|
| Retry with new agent | Re-launch same task, fresh agent |
| Reassign differently | Change approach or split task |
| Skip and continue | Mark as skipped, proceed with others |
| Abort to planning | Return to Phase 3 |

### Integration Test Failure (Step 5.2)

After all agents in a phase pass code review, run test suites. If tests fail:

1. Identify which agent's code caused the failure
2. Launch a fix agent with the test output and relevant planning docs
3. Re-run code review on the fix
4. Re-run tests

### No-TODO Development Warning

If user skipped TODOs but chose development: warn that TODO generation produces stronger orchestration. Offer to go back to Step 2.4 before proceeding.

---

## Phase-Gated Execution Flow

```
Phase 1: Spawn dev subagents (parallel, run_in_background=true)
    ↓ dev subagent completes
    ↓ AUTO-SPAWN: code review subagent (no user input needed)
    ↓ review subagent fixes issues or confirms pass
    ↓ ALL phase 1 subagents reviewed
    ↓ Run integration tests (Bash)
    ↓ Tests pass → report to user
Phase 2: Spawn next dev subagents (parallel)
    ↓ same auto-review cycle
    ...
Phase N: Last subagents complete + reviewed + tested
    ↓
Final summary → user decides next step (AskUserQuestion)
```

**Critical rules:**
- Never launch Phase N+1 subagents until Phase N is fully complete (all tasks done + reviewed + tests pass)
- Code review is ALWAYS auto-triggered — never ask user whether to review
- Each dev subagent gets exactly one review subagent; if review says NEEDS REWORK, spawn a new dev subagent then re-review
