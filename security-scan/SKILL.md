---
name: security-scan
description: "Multi-agent security vulnerability scanning, verification, and PoC validation for codebases. Deploys teams of senior security engineers to systematically discover vulnerabilities (including 0-day), verify findings through multi-round cross-checking, and produce coding proofs or analysis documentation. Use when the user asks to: (1) scan a project for security vulnerabilities, (2) perform security audit with multiple agents, (3) verify or validate known vulnerabilities, (4) write PoC exploits for discovered vulnerabilities, (5) conduct multi-agent security research, or mentions 'security scan', 'vulnerability scan', 'security audit', '安全扫描', '漏洞扫描', '漏洞挖掘', '安全审计', '0-day', 'zero-day'."
---

# Security Scan - Multi-Agent Vulnerability Audit

Three-phase security audit pipeline using agent teams. Each phase builds on the previous phase's output.

## Phase Overview

1. **Discovery** — Scan codebase, find vulnerabilities (including 0-day)
2. **Verification** — Two-round cross-verification of discovered vulnerabilities
3. **Validation** — PoC coding or analysis documentation for confirmed vulnerabilities

## Pre-flight: Project Index Check

Before collecting configuration, check whether the target project has proper context files:

1. Use `Glob` to check if `{project_path}/CLAUDE.md` exists
2. Use `Glob` to check if `{project_path}/.claude-index/` directory exists

**If both exist** → Proceed to Quick Start. These files provide critical project context that agents will use during scanning.

**If either is missing** → Use `AskUserQuestion`:
```
question: "项目缺少索引文件，是否先生成？ / Project is missing index files. Generate them first?"
header: "Index"
options:
  - label: "Yes, generate with project-indexer (Recommended)"
    description: "使用 project-indexer skill 生成 CLAUDE.md 和 .claude-index，帮助扫描Agent更好地理解项目结构"
  - label: "Skip, scan without index"
    description: "跳过索引生成，直接开始扫描（Agent对项目理解可能不够全面）"
```

If user chooses to generate:
1. Invoke the `project-indexer` skill on the target project to create `CLAUDE.md` and `.claude-index/`
2. Wait for completion, then proceed to Quick Start

## Quick Start

Before any scanning, use `AskUserQuestion` to collect configuration. Ask these in **one call** (up to 4 questions):

**Question 1 — Report Language:**
```
question: "报告使用什么语言？ / What language for reports?"
header: "Language"
options:
  - label: "中文 (Recommended)"
    description: "所有报告、分析文档使用中文撰写"
  - label: "English"
    description: "All reports and documentation in English"
```

**Question 2 — Team Identity:**
```
question: "选择安全团队背景 / Which security team to deploy?"
header: "Team"
options:
  - label: "Google Security (Recommended)"
    description: "Google Project Zero / Cloud Security 风格，擅长云原生、容器、基础设施安全"
  - label: "Microsoft MSRC"
    description: "Microsoft Security Response Center 风格，擅长系统级漏洞、内核安全、供应链安全"
  - label: "Meta Red Team"
    description: "Meta(Facebook) Red Team 风格，擅长Web安全、API安全、社交平台安全"
  - label: "Apple Security Engineering"
    description: "Apple SEAR 风格，擅长隐私安全、加密实现、移动端安全"
```

**Question 3 — Phase Selection:**
```
question: "执行哪些阶段？ / Which phases to run?"
header: "Phases"
options:
  - label: "Full Pipeline (1→2→3) (Recommended)"
    description: "完整流水线：发现 → 验证 → 编码验证"
  - label: "Phase 1 Only"
    description: "仅执行漏洞发现扫描"
  - label: "Phase 2+3 (have scan report)"
    description: "已有扫描报告，从验证阶段开始"
  - label: "Phase 3 Only (have verified report)"
    description: "已有验证报告，仅执行编码验证"
```

**Question 4 — Domain Expertise:**
```
question: "项目的技术领域？ / Project's technical domain?"
header: "Domain"
multiSelect: false
options:
  - label: "全领域自动扫描 (Recommended)"
    description: "自动识别项目技术栈，覆盖所有相关安全领域，适合大多数项目"
  - label: "Cloud Native / Container"
    description: "Kubernetes, Docker, 微服务, Service Mesh, Helm, Istio, 容器编排, 镜像安全"
  - label: "Web / API / Mobile"
    description: "Web前后端, REST API, GraphQL, WebSocket, SPA, Android/iOS, 小程序"
  - label: "System / Infra / Crypto"
    description: "操作系统, 内核模块, 驱动开发, 加密实现, 区块链, 智能合约, PKI, 密钥管理"
```

> Note: User can also select "Other" to specify custom domains like IoT/嵌入式, 数据库/中间件, AI/ML pipeline, 游戏安全, etc.

After collecting answers, also ask for:
- Target project path (if not already provided)
- Report output directory (default: `{project}/security-report/`)

### Applying Configuration

Store user choices and propagate to all phases:

- **Language** → Set `{report_language}` for all agent prompts and report templates. If Chinese: "所有报告使用中文撰写". If English: "All reports in English."
- **Team Identity** → Set `{team_identity}` for agent persona prompts:
  - Google: "You are a senior Google Project Zero / Cloud Security engineer..."
  - Microsoft: "You are a senior Microsoft MSRC security researcher..."
  - Meta: "You are a senior Meta Red Team security engineer..."
  - Apple: "You are a senior Apple Security Engineering (SEAR) researcher..."
- **Phases** → Determine which phases to execute
- **Domain** → Set `{domain_focus}` for agent prompts:
  - 全领域自动扫描: First explore the project structure (build files, dependencies, code patterns) to auto-detect the tech stack, then set domain focus accordingly. Cover all 6 vulnerability categories.
  - Cloud Native / Container: Prioritize INFRA category, emphasize K8s RBAC, container escape, image security, network policies
  - Web / API / Mobile: Prioritize INJ and API categories, emphasize XSS, SSRF, IDOR, auth flows, mobile-specific risks
  - System / Infra / Crypto: Prioritize CRYPTO and LOGIC categories, emphasize memory safety, kernel exploits, crypto misuse, side-channels
  - Other (user-specified): Adapt scan focus to the user's custom domain description

## Output Directory Structure

All phases write to a unified directory structure:

```
{report_dir}/
├── phase1-discovery/
│   ├── detail-reports/
│   │   ├── {agent-name}-scan-report.md    # Individual agent reports
│   │   └── ...
│   └── security-audit-final-report.md     # Consolidated discovery report
├── phase2-verification/
│   ├── detail-reports/
│   │   ├── round1/
│   │   │   ├── {agent-name}-verify-r1.md
│   │   │   └── ...
│   │   └── round2/
│   │       ├── {agent-name}-verify-r2.md
│   │       └── ...
│   └── verification-final-report.md       # Consolidated verification report
├── phase3-validation/
│   ├── poc/
│   │   ├── {vuln-id}/
│   │   │   ├── poc_exploit.{ext}          # PoC code
│   │   │   ├── run_result.md              # Execution results
│   │   │   └── validation-report.md       # Validation summary
│   │   └── ...
│   ├── analysis/
│   │   ├── {vuln-id}/
│   │   │   └── verification-guide.md      # Analysis for non-local-verifiable
│   │   └── ...
│   └── validation-final-report.md         # Final index & summary
└── final-summary.md                       # Overall project summary (if all 3 phases)
```

## Phase 1: Discovery

See [references/phase1-discovery.md](references/phase1-discovery.md) for detailed instructions.

**Summary:**
1. Create team with 5-6 `general-purpose` agents in isolated worktrees
2. Assign each agent a scan domain (see vulnerability categories in references)
3. Each agent scans code and writes individual report to `phase1-discovery/detail-reports/`
4. Team lead consolidates into `security-audit-final-report.md`

**Agent roles** — Distribute these scan domains across agents:
- Authentication & Authorization (authn/authz bypass, privilege escalation)
- Input Validation & Injection (command injection, SQL injection, XSS, path traversal)
- Cryptography & Secrets (weak crypto, hardcoded credentials, key management)
- Container & Infrastructure (container escape, misconfig, insecure defaults)
- API & Network (SSRF, CORS, rate limiting, protocol vulnerabilities)
- Logic & Race Conditions (TOCTOU, business logic flaws, resource exhaustion)

## Phase 2: Verification

See [references/phase2-verification.md](references/phase2-verification.md) for detailed instructions.

**Summary:**
1. Create team with 5-6 agents, each reads the Phase 1 final report
2. **Round 1**: Each agent independently verifies assigned vulnerabilities against source code
3. **Round 2**: Agents cross-review Round 1 results — each agent verifies another agent's findings
4. Team lead consolidates into `verification-final-report.md`

**Verification criteria per vulnerability:**
- Can the vulnerable code path be reached?
- Are there existing mitigations that prevent exploitation?
- Is the severity rating accurate?
- For 0-day: Is it truly novel (not a known CVE)?

## Phase 3: Validation

See [references/phase3-validation.md](references/phase3-validation.md) for detailed instructions.

**Summary:**
1. Create team with ~10 agents (can spawn multiple rounds until all vulns covered)
2. Each agent reads Phase 1 + Phase 2 reports, claims specific vulnerabilities
3. For each confirmed vulnerability, determine if local PoC is feasible:
   - **Yes** → Write PoC code, execute, document results in `phase3-validation/poc/{vuln-id}/`
   - **No** → Write analysis + verification guide in `phase3-validation/analysis/{vuln-id}/`
4. Team lead produces `validation-final-report.md` as index of all results

## Team Orchestration Pattern

Each phase follows this pattern:

```
1. TeamCreate with descriptive name (e.g., "security-scan-phase1")
2. TaskCreate for each work item
3. Spawn agents via Agent tool:
   - subagent_type: "general-purpose"
   - team_name: the team name
   - Each agent gets a unique name (e.g., "scanner-authn", "scanner-injection")
   - mode: "bypassPermissions" (agents need to read/write files freely)
4. Assign tasks to agents via TaskUpdate
5. Monitor progress, resolve blockers
6. Consolidate results when all agents complete
7. Shutdown agents via SendMessage type: "shutdown_request"
8. TeamDelete to clean up
```

**Agent spawn template:**

```
Agent tool call:
  subagent_type: "general-purpose"
  name: "{role-name}"
  team_name: "{team-name}"
  isolation: "worktree"
  prompt: |
    You are a senior {team_identity} with deep expertise in {domain}.
    Your task: {specific task description}
    Target project: {project_path}
    Output your report to: {output_path}
    Report language: {report_language}

    ## IMPORTANT: Project Context Files
    Before starting your scan, read these files to understand the project:
    1. Read `{project_path}/CLAUDE.md` — project overview, architecture, conventions
    2. Browse `{project_path}/.claude-index/` — code index with module structure, symbols, dependencies
    These files give you a map of the codebase. Use them to quickly locate relevant
    code areas for your scan domain instead of blindly searching.

    {phase-specific instructions from references}
```

## Report Quality Standards

All reports target academic conference publication quality:

- **Language**: Use `{report_language}` as selected by the user
- **Evidence**: Every finding must cite specific file paths, line numbers, and code snippets
- **Severity**: Use CVSS v3.1 scoring with clear justification
- **Reproducibility**: Clear steps to reproduce each vulnerability
- **Novelty**: 0-day findings must explain why they are not known CVEs
- **References**: Link to relevant CWE, CVE, and academic literature where applicable

See [references/report-templates.md](references/report-templates.md) for report format templates.
See [references/vulnerability-categories.md](references/vulnerability-categories.md) for classification taxonomy.
