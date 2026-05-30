# Production Readiness

语言：[English](README.md) | 简体中文

Production Readiness 是一个证据优先的上线准备度评审 skill，也可以作为 Codex 兼容插件使用。它用于检查一个项目是否真的准备好进入 production、上线、发布、部署或公开使用。

它适合让开发 agent 评审 demo app、API、Web app、全栈项目和通用软件项目。它不会假装自己是合规扫描器，也不会替代人的上线决策。

## 支持的评审范围

- demo app 从展示进入真实使用前的评审
- API 发布准备度评审
- 浏览器 Web app 上线准备度评审
- 全栈项目发布评审
- 通用项目健康度和可维护性评审
- 部署、可观测性、可靠性、安全、数据、测试证据评审

## 这个插件提供什么

- 主 skill：`skills/production-readiness/SKILL.md`
- 分域检查参考：`skills/production-readiness/references/`
- 无第三方依赖的 Python 检查脚本：`skills/production-readiness/scripts/inspect_project.py`
- Codex 插件元数据：`.codex-plugin/plugin.json`
- Codex、Claude Code 和其他文件型 agent 工具的安装说明
- inspector 的单元测试和 GitHub Actions 工作流

## 这个插件不提供什么

这个项目不提供合规认证、渗透测试、法律审查，也不保证一个系统一定可以安全上线。

它不会自动部署、修改或修复目标项目。评审应该区分“已验证证据”和“未验证假设”，最终发布决策仍然由人负责。

## 快速开始

你可以这样让 agent 使用它：

```text
Use the production-readiness skill to review this project.
Project path: /path/to/project
Scope: full-stack web app
Target deployment: public web deployment
Risk tolerance: low for auth and data
Return blockers, high-risk gaps, evidence, unverified assumptions, and a release checklist.
```

只评审 API 层时可以这样说：

```text
Use the production-readiness skill to review the API layer only.
Focus on auth, validation, error responses, pagination, rate limits, idempotency, docs, and integration tests.
```

## 安装

### Codex

克隆仓库：

```bash
git clone https://github.com/RockyYang1225/production-readiness.git
```

把本地 checkout 作为插件安装或指向 Codex。Codex 会读取：

```text
.codex-plugin/plugin.json
```

插件暴露的 skill 位于：

```text
skills/production-readiness/SKILL.md
```

### Claude Code

把 skill 软链接到 Claude Code 的 skills 目录：

```bash
mkdir -p ~/.claude/skills
ln -s /path/to/production-readiness/skills/production-readiness ~/.claude/skills/production-readiness
```

也可以直接复制：

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/production-readiness/skills/production-readiness ~/.claude/skills/
```

### 其他 Agent 工具

任何支持文件型 skill 的工具都可以指向：

```text
skills/production-readiness/SKILL.md
```

## 项目检查脚本

对目标项目运行 inspector：

```bash
python3 skills/production-readiness/scripts/inspect_project.py /path/to/project
```

输出 JSON：

```bash
python3 skills/production-readiness/scripts/inspect_project.py /path/to/project --json
```

inspector 会识别项目类型、常见生态、框架线索、基础发布信号、缺失的准备度信号和可供 agent 继续查看的证据路径。它是轻量辅助工具，不替代人工或 agent 的完整评审。

## 评审输出格式

skill 要求 agent 输出类似下面的报告：

```text
Production Readiness Review

Conclusion: Ready | Conditionally Ready | Not Ready
Scope:
Project Type:
Evidence Reviewed:

Must Fix Before Production:

High-Risk Gaps:

Recommended Improvements:

Domain Findings:

Commands / Checks Run:

Unverified Assumptions:

Release Checklist:
```

结论含义：

- `Ready`：没有已知上线阻塞项，关键生产控制有证据，剩余缺口风险较低。
- `Conditionally Ready`：可以在明确限制下做有限发布、试点、内部部署或 demo 发布。
- `Not Ready`：缺少关键安全、可靠性、部署、数据或验证证据。

## 本仓库的准备度证据

这个仓库已经用自己的 production-readiness workflow 检查过。

当前已有证据：

- README：`README.md`、`README.zh.md`
- 安装说明：`INSTALL.md`
- License：`LICENSE`
- Codex 插件 manifest：`.codex-plugin/plugin.json`
- 主 skill：`skills/production-readiness/SKILL.md`
- 检查域 reference：`skills/production-readiness/references/`
- inspector 脚本：`skills/production-readiness/scripts/inspect_project.py`
- 单元测试：`tests/test_inspect_project.py`
- CI workflow：`.github/workflows/test.yml`

这个仓库不需要运行时密钥或环境变量，因此有意不提供 `.env.example`。

## 开发检查

运行测试：

```bash
python3 -m unittest tests/test_inspect_project.py
```

用 inspector 检查本仓库：

```bash
python3 skills/production-readiness/scripts/inspect_project.py .
python3 skills/production-readiness/scripts/inspect_project.py . --json
```

如果有 Codex plugin validator，可以验证插件 manifest：

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
```

## 仓库结构

```text
production-readiness/
  .codex-plugin/
    plugin.json
  .github/
    workflows/
      test.yml
  INSTALL.md
  LICENSE
  README.md
  README.zh.md
  skills/
    production-readiness/
      SKILL.md
      references/
      scripts/
        inspect_project.py
  tests/
    test_inspect_project.py
```

## 状态

初始发布目标：`0.1.0`。

## License

MIT
