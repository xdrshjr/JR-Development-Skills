# Report Templates

Chinese-language templates for all report types.

## Final Summary Template (When All 3 Phases Complete)

```markdown
# {项目名称} 安全审计总报告

## 项目信息
| 项目 | 详情 |
|------|------|
| 项目名称 | {name} |
| 审计日期 | {date} |
| 审计版本 | {commit/version} |
| 审计阶段 | 发现 → 验证 → 编码验证 |
| 参与工程师 | {total agent count} 名 |

## 执行摘要

{2-3段总结，涵盖：发现了多少漏洞、验证确认了多少、PoC验证了多少、关键0-day发现}

## 统计概览

### 漏洞发现与验证统计
| 指标 | 数量 |
|------|------|
| Phase 1 发现漏洞 | X |
| Phase 2 确认漏洞 | X |
| Phase 2 排除误报 | X |
| Phase 3 PoC验证 | X |
| Phase 3 分析文档 | X |

### 严重程度分布（确认漏洞）
| 严重程度 | 数量 | 占比 |
|---------|------|------|
| Critical | X | X% |
| High | X | X% |
| Medium | X | X% |
| Low | X | X% |

### 0-day漏洞
| 漏洞ID | 名称 | 严重程度 | 验证状态 |
|--------|------|---------|---------|

## 关键发现

### 最高风险漏洞 Top 5
{Brief description of top 5 most critical findings}

### 0-day漏洞详情
{Summary of each 0-day with key evidence}

## 报告索引

### Phase 1: 发现阶段
- 综合报告: `phase1-discovery/security-audit-final-report.md`
- 详细报告: `phase1-discovery/detail-reports/`

### Phase 2: 验证阶段
- 综合报告: `phase2-verification/verification-final-report.md`
- 第一轮: `phase2-verification/detail-reports/round1/`
- 第二轮: `phase2-verification/detail-reports/round2/`

### Phase 3: 编码验证阶段
- 综合报告: `phase3-validation/validation-final-report.md`
- PoC代码: `phase3-validation/poc/`
- 分析文档: `phase3-validation/analysis/`

## 审计方法论

### Phase 1: 漏洞发现
{agent count} 名安全工程师分别负责不同安全领域，对项目代码进行系统性扫描。

### Phase 2: 两轮交叉验证
第一轮：各工程师独立验证分配的漏洞。
第二轮：工程师交叉审查他人的验证结果。

### Phase 3: 编码验证
对确认漏洞编写PoC代码验证，无法本地验证的编写专业验证指导文档。

## 免责声明
本报告仅用于学术研究目的。所有漏洞发现均在授权范围内进行。
```

## Vulnerability Severity Definitions

| Level | CVSS | Description |
|-------|------|-------------|
| Critical | 9.0-10.0 | 可远程利用，无需认证，可完全控制系统 |
| High | 7.0-8.9 | 可远程利用，可能导致数据泄露或权限提升 |
| Medium | 4.0-6.9 | 需要特定条件，影响范围有限 |
| Low | 0.1-3.9 | 难以利用，影响极小 |
