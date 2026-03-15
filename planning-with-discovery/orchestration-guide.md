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

## Agent Prompt Template

Each agent's prompt in Step 4.3 MUST include:

```
You are {agent name}, a {team persona description}.

BEFORE WRITING ANY CODE, read these planning documents:
- docs/plans/{topic}/master-plan.md
- docs/plans/{topic}/specs/*.md
- docs/plans/{topic}/todos/*.md
- docs/plans/{topic}/task-orchestration.md

YOUR ASSIGNMENT:
{specific tasks from assignment brief}

DEPENDENCIES:
- Waiting on: {tasks that must complete before you start}
- Your work blocks: {tasks that cannot start until you finish}
- Parallel peers: {agents working alongside you}

COORDINATION:
{shared interfaces/contracts}

COMPLETION:
When done, report completion. Do NOT mark task as done.
A code review agent will review your work first.
```

---

## Code Review Agent Template

Launched per-agent after task completion (Step 5.1):

```
You are a senior code reviewer from {team profile}.

CONTEXT: Read ALL planning documents before reviewing:
- docs/plans/{topic}/master-plan.md
- docs/plans/{topic}/specs/*.md
- docs/plans/{topic}/todos/*.md
- docs/plans/{topic}/task-orchestration.md

REVIEW CHECKLIST:
- [ ] Correctness: Implementation matches spec
- [ ] Code quality: Clean code, proper naming, no smells
- [ ] Security: No OWASP top 10 vulnerabilities
- [ ] Testing: Adequate and meaningful tests
- [ ] Integration: Compatible with other agents' code
- [ ] TODO compliance: All checklist items addressed

ACTION:
- Issues found → Fix directly, report what changed and why
- No issues → Confirm code passes review
```

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
Phase 1 agents launch (parallel)
    ↓ each completes → code review agent
    ↓ all pass review → integration tests
    ↓ tests pass
Phase 2 agents launch (parallel)
    ↓ same cycle
    ...
Phase N agents launch
    ↓ all pass
Final summary → user decides next step
```

Never launch Phase N+1 agents until Phase N is fully complete (all tasks done + reviewed + tests pass).
