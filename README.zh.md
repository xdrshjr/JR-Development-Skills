# JR Development Skills

<div align="center">
  <img src="logo.png" alt="JR Development Skills Logo" width="200"/>
  <p><strong>专为软件开发工作流程设计的 Claude Code 技能集合</strong></p>
  <p>
    <a href="README.md">English Documentation</a>
  </p>
</div>

## 概述

JR Development Skills 是一个专门的 Claude Code 技能集合，旨在增强软件开发工作流程。这些技能为常见的开发任务提供结构化的方法，从项目探索到需求规划。

## 技能集合

### 🗂️ 项目索引器 (Project Indexer)

为新的 Claude Code 会话快速理解代码库生成结构化索引。

**核心功能：**
- 自动项目结构分析
- 代码符号提取（函数、类、导出）
- 功能地图生成
- 支持 10+ 种编程语言
- CLAUDE.md 集成以实现持久化上下文

**使用场景：**
- 开始处理新的/不熟悉的项目
- 团队成员入职
- 维护项目文档
- 快速代码库导航

[📖 了解更多](./project-indexer/README.md)

**触发短语：**
```
"explore the project"
"understand the codebase"
"了解项目"
"生成索引"
/project-indexer
```

---

### 📋 发现式规划 (Planning with Discovery)

在实现之前进行结构化的需求澄清和规范规划。

**核心功能：**
- 通过 10 个问题轮次进行迭代式需求发现
- 带用户审批的顺序规范编写
- 主计划生成
- 可执行的 TODO 清单创建
- 多语言支持（英文/中文）

**使用场景：**
- 启动需求模糊的新功能
- 团队对项目范围达成一致
- 减少实现返工
- 创建技术规范

[📖 了解更多](./planning-with-discovery/SKILL.md)

**触发短语：**
```
"plan this feature"
"规划功能"
"写一个规范"
"澄清需求"
/planning-with-discovery
```

---

### 🐛 Bug 诊断 (Bug Diagnosis)

通过结构化问题分析和验证修复进行系统化的 Bug 诊断和修复。

**核心功能：**
- 双模式操作（半自动/全自动）
- 结构化问题收集与诊断问题
- 基于索引的代码分析，采用浅层优先策略
- 假设驱动的诊断，提供备选方案
- 立即修复，可选测试验证
- 通过诊断摘要进行轻量级跟踪

**使用场景：**
- 系统化地诊断和修复 Bug
- 在修复前理解根本原因
- 使用自动化测试验证修复
- 跟踪 Bug 解决方案以供将来参考

[📖 了解更多](./bug-diagnosis/README.md)

**触发短语：**
```
"diagnose this bug"
"查找bug"
"诊断问题"
"调试这个问题"
"排查故障"
/bug-diagnosis
```

## 安装

### 手动安装

1. 克隆此仓库：
```bash
git clone https://github.com/yourusername/JR-Development-Skills.git
```

2. 将所需的技能复制到您的 Claude Code 技能目录：
```bash
# 复制单个技能
cp -r JR-Development-Skills/project-indexer ~/.claude/skills/
cp -r JR-Development-Skills/planning-with-discovery ~/.claude/skills/
cp -r JR-Development-Skills/bug-diagnosis ~/.claude/skills/
```

3. 重启 Claude Code 或重新加载技能（如果适用）

### 验证安装

在 Claude Code 中输入：
```
/project-indexer
```
或
```
/planning-with-discovery
```
或
```
/bug-diagnosis
```

如果技能被激活，则安装成功。

## 使用方法

每个技能都可以通过以下方式触发：
1. **斜杠命令**：`/skill-name`
2. **自然语言**：每个技能文档中列出的短语
3. **直接调用**：提及技能处理的任务

示例：
```
用户："我想理解这个代码库"
Claude：[激活 project-indexer 技能]
```

## 贡献

欢迎贡献！以下是您可以提供帮助的方式：

### 添加新技能

1. Fork 此仓库
2. 为您的技能创建新目录：`skill-name/`
3. 包含所需文件：
   - `SKILL.md` - 技能定义和文档
   - `README.md` - 面向用户的文档
   - `_meta.json` - 元数据（可选）
4. 遵循现有的技能结构和约定
5. 提交 pull request

### 改进现有技能

1. 打开一个描述改进的 issue
2. Fork 并进行更改
3. 使用 Claude Code 进行彻底测试
4. 提交带有清晰描述的 pull request

### 技能质量指南

- **清晰的触发条件** - 定义技能何时应该激活
- **全面的文档** - 包括技术文档（SKILL.md）和用户文档（README.md）
- **示例工作流程** - 展示真实使用场景
- **错误处理** - 优雅地处理边缘情况
- **多语言支持** - 在适当的情况下考虑国际用户

## 项目结构

```
JR-Development-Skills/
├── README.md                          # 英文文档
├── README.zh.md                       # 中文文档（本文件）
├── logo.png                           # 项目 logo
├── project-indexer/                   # 项目索引技能
│   ├── SKILL.md                       # 技能实现指南
│   ├── README.md                      # 用户文档
│   ├── _meta.json                     # 技能元数据
│   └── templates/                     # 索引模板
│       ├── index-template.md
│       └── config-template.md
├── planning-with-discovery/           # 需求规划技能
│   └── SKILL.md                       # 技能实现指南
└── bug-diagnosis/                     # Bug 诊断技能
    ├── SKILL.md                       # 技能实现指南
    ├── README.md                      # 用户文档
    └── _meta.json                     # 技能元数据
```

## 系统要求

- Claude Code CLI 或 Claude Code X
- Git（用于安装）
- 支持的操作系统：macOS、Linux、Windows

## 兼容性

此集合中的所有技能都设计为与以下环境兼容：
- **Claude Code CLI** - 基于终端的界面
- **Claude Code X** - 增强的 IDE 集成

技能仅使用标准的 Claude Code 工具（Read、Write、Edit、Glob、Grep、Bash、AskUserQuestion）以确保最大兼容性。

## 路线图

未来考虑的技能：

- [x] **Bug 诊断** - 系统化的 Bug 查找和修复 ✓ 已添加
- [ ] **代码审查助手** - 自动代码质量检查
- [ ] **测试生成器** - 从规范自动生成测试用例
- [ ] **文档生成器** - 从代码创建 API 文档
- [ ] **重构顾问** - 建议重构机会
- [ ] **依赖分析器** - 可视化和优化依赖关系

有想法？[打开一个 issue](https://github.com/yourusername/JR-Development-Skills/issues) 来讨论！

## 许可证

MIT 许可证 - 有关特定许可信息，请参阅各个技能目录。

## 支持

- **问题反馈**：[GitHub Issues](https://github.com/yourusername/JR-Development-Skills/issues)
- **讨论区**：[GitHub Discussions](https://github.com/yourusername/JR-Development-Skills/discussions)

## 致谢

为 Claude Code 社区构建。特别感谢：
- Anthropic 提供 Claude Code
- 此技能集合的所有贡献者

---

<div align="center">
  <p>用 ❤️ 为使用 Claude Code 的开发者制作</p>
  <p>
    <a href="#jr-development-skills">返回顶部</a>
  </p>
</div>
