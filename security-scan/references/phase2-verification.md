# Phase 2: Verification — Detailed Instructions

## Objective

Verify each vulnerability from Phase 1 through two independent rounds of cross-checking. Eliminate false positives, confirm true vulnerabilities, and validate 0-day claims.

## Prerequisites

- Phase 1 final report: `{report_dir}/phase1-discovery/security-audit-final-report.md`
- Phase 1 detail reports: `{report_dir}/phase1-discovery/detail-reports/` (agents read as needed)

## Team Setup

1. Create team: `TeamCreate` with name like `sec-scan-p2`
2. Distribute vulnerabilities across agents — each agent gets a subset
3. Spawn 5-6 agents

## Round 1: Independent Verification

Each agent independently verifies their assigned vulnerabilities against source code.

Agent instructions template:

```
You are a senior Google security engineer conducting an independent verification of
previously discovered vulnerabilities. This verification targets top-tier academic
conference publication — rigor and accuracy are paramount.

## Your Assignment

Read the audit report: {report_dir}/phase1-discovery/security-audit-final-report.md
You may also read detail reports in phase1-discovery/detail-reports/ as needed.

Verify these specific vulnerabilities: {vuln_id_list}
Target project: {project_path}

## Project Context

Before starting verification, read project context files to understand the codebase:
- `{project_path}/CLAUDE.md` — project overview, architecture, key conventions
- Browse `{project_path}/.claude-index/` — code index with module structure, symbols, dependencies
Use these to quickly navigate to relevant code areas when verifying each vulnerability.

## Verification Process

For EACH assigned vulnerability:

1. **Locate the code**: Find the exact file and line cited in the report
2. **Trace the execution path**: Can the vulnerable code actually be reached?
   - Follow call chains from entry points
   - Check if the code path is gated by conditions
3. **Check mitigations**: Are there existing protections?
   - Input sanitization, validation layers, WAF rules
   - Access control checks upstream
   - Framework-level protections
4. **Validate severity**: Is the CVSS score justified?
   - Re-score using CVSS v3.1 calculator logic
5. **For 0-day claims**: Search for similar known CVEs
   - Check if the pattern matches known vulnerability classes
   - Assess novelty — is this truly undisclosed?
6. **Verdict**: CONFIRMED / DISPUTED / NEEDS-MORE-INFO

## Output

Write to: {report_dir}/phase2-verification/detail-reports/round1/{agent-name}-verify-r1.md

Structure:

# 第一轮验证报告 — {Agent Name}

## 验证概要
| 漏洞ID | 原始严重程度 | 验证结果 | 调整后严重程度 | 说明 |
|--------|------------|---------|--------------|------|

## 详细验证

### VULN-XXX: {漏洞名称}
- **验证结果**: CONFIRMED / DISPUTED / NEEDS-MORE-INFO
- **代码路径可达性**: Yes/No — {analysis}
- **现有缓解措施**: {list any mitigations found}
- **严重程度调整**: {original} → {adjusted} — {reason}
- **0-day验证** (if applicable): {novelty assessment}
- **验证依据**:
  ```{lang}
  {relevant code showing reachability or mitigation}
  ```
- **结论**: {final assessment}
```

## Round 2: Cross-Verification

After Round 1 completes, redistribute — each agent verifies ANOTHER agent's Round 1 results.

```
You are conducting Round 2 cross-verification. Review another verifier's findings
for accuracy and completeness.

Read Round 1 report: {report_dir}/phase2-verification/detail-reports/round1/{other-agent}-verify-r1.md
Also reference: {report_dir}/phase1-discovery/security-audit-final-report.md

For each vulnerability in the Round 1 report:
1. Do you agree with the verification result?
2. Did the verifier miss any code paths or mitigations?
3. Is the severity adjustment justified?
4. For DISPUTED items: is the dispute valid, or was the original finding correct?
5. For 0-day: do you agree with the novelty assessment?

Write to: {report_dir}/phase2-verification/detail-reports/round2/{agent-name}-verify-r2.md
```

Round 2 report structure:

```
# 第二轮交叉验证报告 — {Agent Name}

## 交叉验证对象: {Round 1 agent name}

## 验证概要
| 漏洞ID | R1结果 | R2结果 | 是否一致 | 备注 |
|--------|--------|--------|---------|------|

## 详细交叉验证
### VULN-XXX
- **R1判定**: {R1 result}
- **R2判定**: AGREE / DISAGREE
- **分歧说明** (if disagree): {reasoning}
- **补充发现**: {any additional findings}
```

## Consolidation

After both rounds complete, the team lead:

1. Read all Round 1 and Round 2 reports
2. For each vulnerability, determine final status:
   - Both rounds CONFIRMED → **CONFIRMED**
   - Disagreement → team lead makes final call based on evidence
   - Both rounds DISPUTED → **FALSE POSITIVE**
3. Write `verification-final-report.md`

```
# 漏洞验证报告

## 验证方法论
- 两轮独立验证 + 交叉审查
- 验证团队: {agent count} 名高级安全工程师

## 验证结果统计
| 类别 | 数量 |
|------|------|
| 确认漏洞 | X |
| 误报排除 | X |
| 需进一步调查 | X |

## 确认漏洞列表
| ID | 名称 | 最终严重程度 | CVSS | 0-day | R1结果 | R2结果 |
|----|------|------------|------|-------|--------|--------|

## 误报列表
| ID | 名称 | 误报原因 |
|----|------|---------|

## 各漏洞详细验证结论
(Merged verification details for each vulnerability)
```
