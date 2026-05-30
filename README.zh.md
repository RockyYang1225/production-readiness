# Production Readiness

[![test](https://github.com/RockyYang1225/production-readiness/actions/workflows/test.yml/badge.svg)](https://github.com/RockyYang1225/production-readiness/actions/workflows/test.yml)

语言：[English](README.md) | 简体中文

Production Readiness 是一个证据优先的上线准备度评审 skill，也可以作为 Codex 兼容插件使用。它帮助开发 agent 判断一个项目是否真的准备好进入 production、上线、发布、部署或公开使用。

它面向 demo app、API、Web app、全栈项目和通用软件项目。它不是合规扫描器，也不会替代人的上线决策；它的重点是把“已验证证据”和“未验证假设”分清楚。

## 快速了解

| 模块 | 路径 | 作用 |
|---|---|---|
| 主 skill | `skills/production-readiness/SKILL.md` | 指导 agent 完成评审 |
| 检查域 | `skills/production-readiness/references/` | 安全、部署、API、Web、数据、测试等分域参考 |
| Inspector | `skills/production-readiness/scripts/inspect_project.py` | 识别项目类型和基础发布信号 |
| Codex 插件 | `.codex-plugin/plugin.json` | 让 Codex 识别这个仓库 |
| 安装说明 | `INSTALL.md` | 提供安装和验证步骤 |

## 当前准备度

这个仓库已经用自己的 `production-readiness` skill 做过评审。

结论：适合作为初始 `0.1.0` 公共插件版本发布。

证据：

- Codex plugin validator 可以通过插件 manifest。
- `python3 -m unittest tests/test_inspect_project.py` 可以通过 inspector 测试。
- inspector 可以用 Markdown 和 JSON 两种模式检查本仓库。
- CI 已配置在 `.github/workflows/test.yml`。
- 这个仓库没有运行时密钥或环境变量，所以有意不提供 `.env.example`。

## 什么时候用

当你想让 agent 回答这些问题时，适合使用它：

- 这个 demo app 真的可以上线了吗？
- 这个 API 发布前还有哪些阻塞项？
- 这个 Web app 部署前最高风险的缺口是什么？
- 哪些检查已经验证，哪些只是推测？
- 这个项目是否只能在有限范围内发布？

## 它会检查什么

- 通用项目健康度和可复现性
- 安全基础：密钥、认证、授权、输入校验、CORS、依赖风险、敏感日志
- 可靠性：错误处理、超时、重试、资源限制、恢复路径
- 可观测性：日志、健康检查、指标、trace、可告警失败
- 部署准备度：构建/启动/测试命令、CI、运行时要求、冒烟测试、回滚
- 数据准备度：迁移、备份、校验、保留策略、破坏性操作
- API 准备度：契约、错误返回、分页、幂等性、限流、集成测试
- Web app 准备度：核心流程、响应式、基础可访问性、浏览器错误
- 测试证据：区分“有测试”和“测试已经运行通过”

## 边界

这个项目不提供合规认证、渗透测试、法律审查，也不保证一个系统一定可以安全上线。

它不会自动部署、修改或修复目标项目。它只帮助 agent 做结构化评审，最终发布决策仍然由人负责。

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

克隆仓库：

```bash
git clone https://github.com/RockyYang1225/production-readiness.git
cd production-readiness
```

### Codex

把本地 checkout 作为插件安装或指向 Codex。Codex 会读取：

```text
.codex-plugin/plugin.json
```

### Claude Code

把 skill 软链接到 Claude Code 的 skills 目录：

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/production-readiness" ~/.claude/skills/production-readiness
```

也可以直接复制：

```bash
mkdir -p ~/.claude/skills
cp -R skills/production-readiness ~/.claude/skills/
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

inspector 会识别项目类型、常见生态、框架线索、基础发布信号、缺失的准备度信号和可供 agent 继续查看的证据路径。它是轻量辅助工具，不替代完整评审。

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

## 验证这个仓库

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

这个仓库的预期 inspector 状态：

- 项目类型：`documentation-heavy`
- 已具备的基础发布信号：README、license、tests、CI
- 已知非阻塞项：没有 `.env.example`，因为仓库没有运行时配置

发布证据：

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
