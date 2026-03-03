# Phase 1: Discovery — Detailed Instructions

## Objective

Systematically scan the target codebase to discover all security vulnerabilities, including potential 0-day vulnerabilities.

## Team Setup

1. Create team: `TeamCreate` with name like `sec-scan-p1`
2. Create tasks — one per scan domain:
   - `TaskCreate`: "Scan authentication & authorization code"
   - `TaskCreate`: "Scan input validation & injection surfaces"
   - `TaskCreate`: "Scan cryptography & secrets management"
   - `TaskCreate`: "Scan container & infrastructure configuration"
   - `TaskCreate`: "Scan API & network security"
   - `TaskCreate`: "Scan logic flaws & race conditions"
3. Spawn 5-6 agents, each assigned to a domain

## Agent Instructions Template

Each agent receives:

```
You are a senior Google security engineer with 10+ years of experience in {domain_expertise}.
You are conducting a security audit of a {project_description} project for academic research
targeting top-tier computer science conferences.

## Your Assignment

Scan domain: {scan_domain}
Target project: {project_path}

## Process

1. Read the project structure — understand the codebase layout, build system, dependencies
2. Identify attack surfaces relevant to your scan domain
3. For each potential vulnerability found:
   a. Trace the code path to confirm reachability
   b. Check for existing mitigations
   c. Assess severity (CVSS v3.1)
   d. Determine if it could be a 0-day (check against known CVEs)
4. Write your report

## Output

Write your report to: {report_dir}/phase1-discovery/detail-reports/{agent-name}-scan-report.md

Use this structure:

# {Scan Domain} 安全扫描报告

## 扫描范围
- 扫描领域: {domain}
- 扫描文件/目录: {list}
- 扫描时间: {date}

## 发现概要
| 编号 | 漏洞名称 | 严重程度 | CVSS评分 | 是否0-day | 文件位置 |
|------|---------|---------|---------|----------|---------|

## 详细发现

### VULN-{domain_prefix}-001: {漏洞名称}
- **严重程度**: Critical/High/Medium/Low
- **CVSS评分**: X.X
- **CWE分类**: CWE-XXX
- **影响范围**: {description}
- **漏洞位置**: `{file}:{line}`
- **漏洞代码**:
  ```{lang}
  {vulnerable code snippet}
  ```
- **漏洞分析**: {detailed analysis of why this is vulnerable}
- **攻击向量**: {how an attacker could exploit this}
- **是否0-day**: Yes/No — {justification}
- **修复建议**: {recommended fix}

(Repeat for each finding)

## 未确认的可疑点
{List items that look suspicious but couldn't be confirmed — for Phase 2 to investigate}
```

## Consolidation

After all agents complete, the team lead:

1. Read all individual reports from `phase1-discovery/detail-reports/`
2. Deduplicate findings (different agents may find the same vuln from different angles)
3. Assign unified vulnerability IDs: `VULN-001`, `VULN-002`, etc.
4. Create severity summary statistics
5. Write consolidated report to `phase1-discovery/security-audit-final-report.md`

Consolidated report structure:

```
# 安全审计报告

## 项目信息
- 项目名称: {name}
- 审计日期: {date}
- 审计团队: {agent count} 名高级安全工程师
- 审计范围: {scope}

## 执行摘要
{1-2 paragraph summary of key findings}

## 发现统计
| 严重程度 | 数量 |
|---------|------|
| Critical | X |
| High | X |
| Medium | X |
| Low | X |
| **总计** | **X** |

其中疑似0-day漏洞: X 个

## 漏洞列表
| ID | 名称 | 严重程度 | CVSS | 0-day | 发现者 |
|----|------|---------|------|-------|--------|

## 详细漏洞报告
(Each vulnerability with full details, merged from individual reports)

## 附录
- 各扫描员详细报告索引
- 扫描方法论说明
```
