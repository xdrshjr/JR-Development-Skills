---
name: planning-with-discovery
description: Use when starting a new project, feature, or task that needs requirements clarification and spec planning before implementation. Also use when the user mentions "plan", "spec", "requirements", "design doc", or wants to discuss what to build before coding.
---

# Requirements Discovery & Spec Planning

## Overview

Guide developers through structured requirements discovery via iterative Q&A rounds, then generate a complete spec plan with master plan, detailed design documents, and actionable TODO files - all before any code is written.

**Core principle:** Never start coding without a clear, validated plan. Discover requirements through conversation, write specs incrementally with user approval, then produce actionable tasks.

## When to Use

- Starting a new project or significant feature
- Requirements are vague, incomplete, or only exist as a rough idea
- The team needs alignment on what to build before implementation
- User wants to "think through" a feature before coding

**Do NOT use when:**
- The task is a simple bug fix or minor tweak
- Requirements are already fully documented
- User explicitly says "just do it" for a small, clear task

## The Process

### Phase 0: Initialization

1. Read the user's initial task description carefully
2. Auto-generate a short kebab-case topic name from the description (e.g., `user-auth-system`, `payment-flow`)
3. Ask the user which language to use for conversation and generated documents:
   - Present as a simple choice: English or Chinese (or other if user specifies)
   - The skill prompt itself stays in English; conversation and output files follow user's chosen language
4. Confirm the output directory: `docs/plans/<topic-name>/`

### Phase 1: Requirements Discovery (Iterative Q&A)

**Each round:**
1. Present exactly 10 numbered questions as a batch
2. Questions should be driven entirely by the agent's judgment - ask whatever is most important to clarify based on:
   - The original task description
   - All previous answers from the user
   - Gaps, ambiguities, or risks identified so far
3. Wait for the user to answer (they may answer all, some, or add extra context)
4. Digest the answers and update your internal understanding

**After each round, evaluate readiness:**
- If enough information has been gathered to write a meaningful spec, ask: "I believe I have enough information to start writing the plan. Ready to proceed, or would you like another round of questions?"
- If significant gaps remain, proceed directly with another round of 10 questions
- The user can override at any time by typing keywords like "start writing", "generate plan", "begin spec", "write the plan", or similar - honor this immediately

**Question quality guidelines:**
- Mix question types: clarifying, exploring edge cases, confirming assumptions, probing constraints
- Avoid repeating questions already answered
- Build on previous answers - go deeper, not wider, as rounds progress
- Ask about risks, failure modes, and "what if" scenarios in later rounds
- Cover both functional and non-functional aspects naturally

### Phase 2: Spec Writing (Sequential with Review)

Once the user agrees to start writing, proceed in this exact order:

#### Step 2.1: Master Plan

1. Write `docs/plans/<topic-name>/master-plan.md` containing:
   - Project/feature overview and goals
   - Scope definition (what's in, what's out)
   - High-level architecture or approach
   - Key design decisions and rationale
   - Dependencies and assumptions
   - Risk assessment
   - Table of contents linking to all spec files that will be created
2. Present the full content of `master-plan.md` to the user
3. Ask for approval or edits
4. If the user requests changes, apply them and re-present until approved
5. Only proceed to spec files after the master plan is approved

#### Step 2.2: Planning Configuration

After the master plan is approved, configure the planning scope with **two** `AskUserQuestion` calls:

1. **Spec file count** — Analyze the master plan and recommend a number of spec files with a brief rationale, then ask:
   - Option 1: `"N files (Recommended)"` — the agent's recommended count with a one-line reason
   - Option 2: `"1-3 files (Compact)"` — for simple projects
   - Option 3: `"4-7 files (Balanced)"` — for moderate complexity
   - Option 4: `"8-10 files (Comprehensive)"` — for large projects
   - (User can always enter a custom number via the automatic "Other" option)
   - If the user selects a range, follow up to confirm the exact number within that range

2. **TODO file preference** — Ask whether to generate TODO files after specs are complete:
   - Option 1: `"Yes, generate TODO files"` — create actionable task checklists after spec approval
   - Option 2: `"No, specs only"` — complete planning with specs only

#### Step 2.3: Detailed Spec Files

1. Using the spec file count confirmed by the user in Step 2.2, create the spec files
2. Name them with numeric prefixes: `specs/01-<name>.md`, `specs/02-<name>.md`, etc.
3. For EACH spec file, sequentially:
   a. Write the file using natural language descriptions, pseudo-code, and text-based diagrams (mermaid syntax)
   b. **No real code** - only pseudo-code where algorithms need to be clear
   c. Present the full content to the user
   d. Ask for approval or edits
   e. If the user requests changes, apply them and re-present until approved
   f. Only move to the next spec file after the current one is approved

**Spec file content guidelines:**
- Use natural language as the primary medium
- Include pseudo-code blocks for complex logic or algorithms
- Include mermaid diagrams for data flow, state machines, or architecture
- Describe interfaces, data models, and behavior - not implementation details
- Each spec file should be self-contained and focused on one aspect/module

#### Step 2.4: TODO Files (Conditional)

If the user chose to generate TODO files in Step 2.2, execute this step; otherwise skip to Phase 3.

1. Create one TODO file per spec file: `todos/01-<name>.md`, `todos/02-<name>.md`, etc.
2. Each TODO file contains:
   - Reference to its corresponding spec file
   - A checklist of actionable tasks (using `- [ ]` markdown checkboxes)
   - Tasks ordered by implementation sequence
   - Each task described clearly enough for a developer to act on
3. Present ALL TODO files together as a batch for review
4. Ask the user to review and approve (or request changes)
5. Apply any changes and re-present until approved

### Phase 3: Completion

1. Present a summary of everything generated:
   - Master plan file path
   - List of all spec files
   - List of all TODO files (if generated) or note that TODO files were not created
2. If TODO files were generated, ask: "Ready to start implementation, or do you want to revisit any part of the plan?"
3. If TODO files were NOT generated, ask: "The planning phase is complete. Would you like to generate TODO files now, or are you ready to proceed with your own implementation approach?"

## Output Structure

```
docs/plans/<topic-name>/
├── master-plan.md          # Overall project plan and architecture
├── specs/                  # Detailed design documents
│   ├── 01-<name>.md
│   ├── 02-<name>.md
│   ├── 03-<name>.md
│   └── ...
└── todos/                  # [OPTIONAL] Actionable task checklists
    ├── 01-<name>.md
    ├── 02-<name>.md
    ├── 03-<name>.md
    └── ...
```

**Note:** The `todos/` directory is only created if the user chooses to generate TODO files.

## Key Principles

- **10 questions per round** - Always present exactly 10, no more, no less
- **Agent-driven questions** - No rigid categories; ask what matters most right now
- **User controls the pace** - User can trigger spec writing at any time
- **Sequential approval** - Each spec file must be approved before the next is written
- **No real code** - Pseudo-code and diagrams only; this is a planning tool, not a coding tool
- **Language flexibility** - Determine the working language at the start and stay consistent
- **Incremental refinement** - Each Q&A round builds on all previous knowledge
- **User-controlled scope** - User decides spec count and TODO preference after master plan approval
- **Agent recommends, user decides** - Agent analyzes the master plan and proposes a recommended spec count; user makes the final call
- **Optional TODO generation** - Let users decide if they need task checklists or prefer their own implementation approach

## Red Flags

- Starting to write spec files before the user has agreed to begin
- Writing real/concrete code instead of pseudo-code
- Skipping user approval on any spec file
- Asking fewer than 10 questions per round
- Repeating questions already answered in previous rounds
- Starting to write spec files without confirming the count with the user
- Ignoring the user's chosen spec count and creating a different number of files
- Generating TODO files without asking the user first
- Generating TODO tasks that don't trace back to approved specs (when TODOs are generated)
- Changing the working language mid-process without user consent
- Moving to the next spec file before the current one is approved

## Compatibility

This skill uses only standard tools available in both Claude Code CLI and Claude Code X:
- `Read`, `Write`, `Edit` for file operations
- `Glob`, `Grep` for project exploration
- `AskUserQuestion` for structured choices
- `Bash` only for creating directories

No environment-specific features are used.
