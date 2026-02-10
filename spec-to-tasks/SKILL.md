---
name: spec-to-tasks
description: Converts project specification documents into structured TODO task plans with traceability. Use when users want to generate development tasks from specification documents, create project task breakdowns, or need structured TODO files based on requirements documentation. Triggers on requests like "create tasks from specs", "generate TODO from documents", "break down project into tasks", or when starting a new project that needs task planning from existing documentation.
---

# Spec to Tasks

Generates structured TODO task files from project specification and development documents with full traceability to source requirements.

## Workflow

Follow these steps in order when this skill is invoked:

### Step 1: Language Selection

Use AskUserQuestion to ask the user to select their preferred language:

```
Question: "Which language would you like to use for the TODO files?"
Header: "Language"
Options:
  - English (Recommended)
  - 中文 (Chinese)
```

Store the language choice for all subsequent interactions and file generation.

### Step 2: Document Path Collection

Ask the user to provide the path to their specification documents:

"Please provide the path to your project specification and development documents folder. I'll read all .md, .doc, and .docx files in that directory."

Wait for the user to respond with the path before proceeding.

### Step 3: Read Documentation

Once the path is provided:

1. Use Glob to find all documentation files:
   - Pattern: `**/*.md` for Markdown files
   - Pattern: `**/*.doc` and `**/*.docx` for Word documents

2. Read all found documents using the Read tool

3. Analyze and understand:
   - Project requirements
   - Feature specifications
   - Technical architecture
   - Development phases

### Step 4: Requirements Clarification (Optional)

Use AskUserQuestion to ask if requirements need further clarification:

```
Question: "Would you like to clarify or refine the requirements before generating TODO tasks?"
Header: "Clarification"
Options:
  - No, proceed with current requirements (Recommended)
  - Yes, I want to clarify requirements
```

If user selects "Yes":
- Review the documentation with the user
- Ask clarifying questions about ambiguous requirements
- Document any additional context or decisions
- Update understanding before proceeding

If user selects "No":
- Proceed directly to Step 5

### Step 5: Task Count Selection

Use AskUserQuestion to determine the number of TODO files to create:

```
Question: "How many TODO task files should be created?"
Header: "Task Count"
Options:
  - 3 tasks (Quick breakdown)
  - 5 tasks (Balanced approach, Recommended)
  - 10 tasks (Detailed breakdown)
```

### Step 6: Generate TODO Task Files

Based on the selected task count and language, generate the corresponding number of TODO task files:

#### File Organization

1. Create a `todo/` folder in the same directory as the specification documents
2. Name files sequentially based on count:
   - For 3-9 tasks: `task-1.md`, `task-2.md`, etc.
   - For 10+ tasks: `task-01.md`, `task-02.md`, etc.
3. Generate files in the user's selected language (English or Chinese)

#### Task File Content Requirements

Each TODO task file must include:

1. **Task Position and Phase**
   - Current task number (e.g., "Task 1 of 5")
   - Development phase (e.g., "Foundation", "Core Features", "Integration", "Polish")

2. **Task Overview**
   - Clear, concise description of what this task accomplishes
   - High-level goals and deliverables

3. **Specification Traceability** (CRITICAL)
   - List specific specification documents this task relates to
   - Reference exact sections/chapters from those documents
   - Describe the relationship in 1-2 sentences
   - Example: "This task implements the user authentication flow described in `specs/security.md`, Section 3.2 'Login Flow'. It covers the requirements for password-based authentication and session management."

4. **TODO Checklist**
   - 3-10 actionable TODO items
   - Each item should have:
     - Clear description
     - Pseudocode if implementation is involved (NOT real code)
   - Order items logically (dependencies first)

5. **Dependencies**
   - Prerequisites: Which tasks must be completed first
   - Following tasks: Which tasks depend on this one

6. **Acceptance Criteria**
   - 3-5 clear, testable criteria

#### Task Distribution Strategy

Distribute tasks logically across development phases:
- **Early tasks**: Foundation, setup, core data models
- **Middle tasks**: Feature implementation, business logic
- **Later tasks**: Integration, testing, polish, deployment

Ensure tasks are:
- Roughly equal in scope and effort
- Sequentially logical (natural dependencies)
- Comprehensive (cover all requirements)

#### Pseudocode Guidelines

When including pseudocode:
- Use clear, language-agnostic syntax
- Focus on logic, not implementation details
- Include key algorithms and data flows
- Example:
  ```
  function authenticateUser(username, password):
    user = database.findUser(username)
    if user is null:
      return error("User not found")

    if not verifyPassword(password, user.hashedPassword):
      return error("Invalid password")

    session = createSession(user)
    return success(session)
  ```

### Step 7: Confirmation

After generating all TODO files:
1. Summarize what was created
2. Show the file paths
3. Provide a brief overview of the task breakdown
4. Remind the user about the traceability links to specification documents

## Important Guidelines

### Language Consistency
- All generated files must match the user's language selection
- Follow the appropriate structure (English or Chinese) from the "TODO File Structure" section
- Maintain consistent terminology throughout all files

### Traceability (CRITICAL)
Every TODO item must have clear traceability to source documentation. This enables:
- Easy reference back to original requirements
- Verification that implementation matches specifications
- Quick navigation when clarification is needed

Format: "This task implements [feature] from [document], [section]. It addresses [specific requirement]."

### Task Granularity
- Each task should be completable in a reasonable timeframe
- Break down large features into logical sub-tasks
- Avoid tasks that are too small (combine related items)
- Avoid tasks that are too large (split into phases)

### File Naming

Use sequential numbering based on task count:
- **For 3-9 tasks**: `task-1.md`, `task-2.md`, `task-3.md`, etc.
- **For 10+ tasks**: `task-01.md`, `task-02.md`, ..., `task-10.md`, etc.

### Pseudocode Only
Never include real implementation code in TODO files. Use pseudocode to:
- Express algorithms and logic
- Show data structures and flows
- Maintain language/framework independence
- Keep focus on "what" not "how"

## TODO File Structure

Each generated TODO file should follow this structure:

### English Structure
```markdown
# TODO Task N: [Task Title]

## Task Position
- **Phase**: [Development phase name]
- **Order**: Task N of [total]

## Task Overview
[2-3 sentences describing what this task accomplishes]

## Specification Traceability
- **Related Documents**: [document names]
- **Related Sections**: [section references]
- **Relationship**: [1-2 sentences describing how this task maps to specs]

## TODO Checklist

### 1. [First TODO item]
[Description of what needs to be done]

**Pseudocode** (if applicable):
```
[language-agnostic pseudocode]
```

### 2. [Second TODO item]
[Description]

**Pseudocode** (if applicable):
```
[pseudocode]
```

[Continue for 3-10 items total]

## Dependencies
- **Prerequisites**: [Tasks that must be completed first, or "None"]
- **Following Tasks**: [Tasks that depend on this one, or "None"]

## Acceptance Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]
```

### Chinese Structure
```markdown
# TODO任务 N: [任务标题]

## 任务位置
- **阶段**: [开发阶段]
- **顺序**: 第N个任务，共[总数]个任务

## 任务概述
[2-3句话描述任务目标]

## 规格文档追溯
- **相关文档**: [文档名称]
- **对应章节**: [章节引用]
- **关联关系**: [1-2句话描述任务与规格的对应关系]

## TODO清单

### 1. [第一个TODO项]
[需要完成的内容描述]

**伪代码**（如适用）:
```
[语言无关的伪代码]
```

### 2. [第二个TODO项]
[描述]

**伪代码**（如适用）:
```
[伪代码]
```

[继续添加，共3-10项]

## 依赖关系
- **前置任务**: [必须先完成的任务，或"无"]
- **后续任务**: [依赖本任务的任务，或"无"]

## 验收标准
- [ ] [可测试的标准1]
- [ ] [可测试的标准2]
- [ ] [可测试的标准3]
```

## Example Usage

**User**: "Create development tasks from my project specs"

**Workflow**:
1. Ask language preference → User selects "English"
2. Ask for document path → User provides `./docs/specs`
3. Read all .md and .docx files in `./docs/specs`
4. Ask about clarification → User selects "No, proceed"
5. Ask task count → User selects "5 tasks"
6. Generate 5 TODO files in `./docs/specs/todo/`:
   - `task-1.md` - Project Setup & Foundation
   - `task-2.md` - Core Data Models
   - `task-3.md` - Business Logic Implementation
   - `task-4.md` - API Integration
   - `task-5.md` - Testing & Deployment

Each file contains detailed TODO items with traceability back to specific sections in the specification documents.
