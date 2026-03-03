# Phase 3: Validation — Detailed Instructions

## Objective

For each confirmed vulnerability, produce either:
1. **PoC code** with execution results (if locally verifiable), OR
2. **Verification guide** documentation (if not locally verifiable)

## Prerequisites

- Phase 1 report: `{report_dir}/phase1-discovery/security-audit-final-report.md`
- Phase 2 report: `{report_dir}/phase2-verification/verification-final-report.md`
- Detail reports in both phase directories (agents read as needed)

## Team Setup

1. Create team: `TeamCreate` with name like `sec-scan-p3`
2. Read the verification report to get the confirmed vulnerability list
3. Create one task per confirmed vulnerability
4. Spawn ~10 agents, assign vulnerabilities. If more than 10 confirmed vulns, spawn additional rounds of agents after the first batch completes.

## Triage: PoC vs Analysis

For each vulnerability, determine the validation approach:

**Can be locally verified (PoC)** when:
- The vulnerability can be triggered by crafting specific input
- A unit test or script can demonstrate the flaw
- The exploit doesn't require a full production environment
- Examples: injection flaws, logic errors, crypto weaknesses, auth bypass with test setup

**Cannot be locally verified (Analysis)** when:
- Requires specific cloud infrastructure or network topology
- Requires multi-node cluster setup
- Requires specific hardware or OS kernel version
- Timing/race condition too environment-dependent
- Examples: distributed system race conditions, kernel exploits, cloud-specific misconfigs

## PoC Validation Path

Agent instructions for PoC-eligible vulnerabilities:

```
You are a senior Google security engineer writing a proof-of-concept exploit for
a confirmed vulnerability. Your work will be used in academic research.

## Your Assignment

Vulnerability: {vuln_id} — {vuln_name}
Details in: {report_dir}/phase2-verification/verification-final-report.md
Target project: {project_path}

## Process

1. Understand the vulnerability deeply — read the code, trace the path
2. Design a minimal PoC that demonstrates the vulnerability
3. Write the PoC code
4. Execute the PoC and capture results
5. Document everything

## Output Directory

{report_dir}/phase3-validation/poc/{vuln-id}/

Write these files:
- poc_exploit.{ext} — The PoC code (Python/Go/Shell/etc.)
- run_result.md — Execution output and analysis
- validation-report.md — Complete validation summary

## validation-report.md Structure

# PoC验证报告: {VULN-ID}

## 漏洞信息
- **漏洞编号**: {ID}
- **漏洞名称**: {name}
- **严重程度**: {severity}
- **CVSS评分**: {score}

## PoC概述
{Brief description of what the PoC demonstrates}

## 环境要求
- 运行环境: {OS, runtime, dependencies}
- 前置条件: {setup steps}

## PoC代码说明
{Explain the PoC logic, what each part does}

## 执行方法
```bash
{exact commands to run the PoC}
```

## 执行结果
{Paste actual output}

## 结果分析
- **是否成功触发漏洞**: Yes/No
- **实际影响**: {what an attacker could achieve}
- **与报告一致性**: {does the PoC confirm the reported severity?}

## 修复建议
{Concrete code changes to fix the vulnerability}
```

## Analysis Documentation Path

Agent instructions for non-locally-verifiable vulnerabilities:

```
You are a senior Google security engineer writing a verification guide for a
confirmed vulnerability that cannot be verified locally. The guide must be
professional yet accessible.

## Your Assignment

Vulnerability: {vuln_id} — {vuln_name}
Target project: {project_path}

## Output Directory

{report_dir}/phase3-validation/analysis/{vuln-id}/

Write: verification-guide.md

## verification-guide.md Structure

# 漏洞验证指导: {VULN-ID}

## 漏洞信息
- **漏洞编号**: {ID}
- **漏洞名称**: {name}
- **严重程度**: {severity}
- **CVSS评分**: {score}

## 为什么无法本地验证
{Clear explanation of why local PoC is not feasible}

## 漏洞原理分析
{Deep technical analysis with code references}

### 关键代码路径
```{lang}
{annotated code showing the vulnerable path}
```

### 数据流分析
{How tainted data flows from source to sink}

## 验证环境要求
{Exact infrastructure/environment needed}

## 验证步骤
{Step-by-step instructions for someone with the right environment}

1. **环境搭建**: {setup instructions}
2. **触发条件**: {how to trigger the vulnerability}
3. **预期结果**: {what successful exploitation looks like}
4. **验证确认**: {how to confirm the vulnerability was triggered}

## 理论影响分析
{What damage could be done if exploited}

## 相关CVE/CWE参考
{Links to similar known vulnerabilities for context}

## 修复建议
{Concrete remediation steps}
```

## Consolidation

After all agents complete, the team lead:

1. Read all PoC reports and analysis guides
2. Verify directory structure consistency — all files in correct folders
3. Write `validation-final-report.md` as the master index

```
# 漏洞验证总报告

## 验证概况
- 确认漏洞总数: X
- 已编码验证(PoC): X
- 分析文档(指导): X
- 验证团队: {agent count} 名高级安全工程师

## PoC验证结果汇总
| 漏洞ID | 名称 | 严重程度 | PoC结果 | 报告路径 |
|--------|------|---------|---------|---------|

## 分析文档汇总
| 漏洞ID | 名称 | 严重程度 | 无法本地验证原因 | 报告路径 |
|--------|------|---------|----------------|---------|

## 关键发现
{Highlight the most significant validated vulnerabilities}

## 0-day漏洞专项
{Dedicated section for validated 0-day vulnerabilities}

## 目录索引
{Complete file listing of all validation artifacts}
```

## Multi-Round Spawning

If there are more confirmed vulnerabilities than a single batch of agents can handle:

1. First batch: Spawn ~10 agents, assign first set of vulnerabilities
2. Wait for completion
3. Second batch: Spawn another ~10 agents for remaining vulnerabilities
4. Repeat until all vulnerabilities are covered
5. Consolidate all results at the end
