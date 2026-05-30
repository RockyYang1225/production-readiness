# Production Readiness

[![test](https://github.com/RockyYang1225/production-readiness/actions/workflows/test.yml/badge.svg)](https://github.com/RockyYang1225/production-readiness/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)

语言：[English](../README.md) | 简体中文

面向 Codex、Claude Code 和其他 agent 开发工具的证据优先上线准备度评审插件。

Production Readiness 帮助开发 agent 判断一个 demo app、API、Web app、全栈项目或通用软件项目是否真的准备好上线。它由主 skill、分域 reference 和轻量 inspector 组成，让评审基于文件、命令和证据，而不是感觉。

[快速开始](#快速开始) · [安装](#安装) · [Inspector](#项目-inspector) · [报告格式](#评审报告格式) · [验证](#验证这个仓库)

## 目录

- [为什么需要它](#为什么需要它)
- [包含什么](#包含什么)
- [当前准备度](#当前准备度)
- [支持的评审范围](#支持的评审范围)
- [快速开始](#快速开始)
- [安装](#安装)
- [项目 Inspector](#项目-inspector)
- [评审报告格式](#评审报告格式)
- [验证这个仓库](#验证这个仓库)
- [仓库结构](#仓库结构)
- [状态](#状态)
- [License](#license)

## 为什么需要它

demo app 经常看起来已经很完整，但这不等于可以上线。生产准备度更关心证据：安装是否可复现，测试是否真的运行过，密钥是否安全，部署是否说得清楚，哪些内容还只是未验证假设。

这个插件给 agent 一条可重复的评审路径，并明确边界。它不提供合规认证、不做渗透测试，也不会替人做最终发布决定。

## 包含什么

| 模块 | 路径 | 作用 |
|---|---|---|
| 主 skill | `skills/production-readiness/SKILL.md` | 指导 agent 完成证据优先的准备度评审 |
| 检查域 reference | `skills/production-readiness/references/` | 安全、可靠性、可观测性、部署、数据、API、Web、全栈、测试、通用检查 |
| Inspector | `skills/production-readiness/scripts/inspect_project.py` | 识别项目类型、发布信号、缺失项和证据路径 |
| Codex 插件 manifest | `.codex-plugin/plugin.json` | 让 Codex 识别这个仓库 |
| 安装脚本 | `install.sh` | 为 Codex、Claude Code 和文件型 skill 工具提供一行安装、更新和卸载 |
| 安装说明 | `INSTALL.md` | 安装细节和手动安装备用方案 |
| 测试与 CI | `tests/test_inspect_project.py`、`tests/test_install_script.py`、`.github/workflows/test.yml` | 为 inspector 和安装脚本提供可重复验证 |

## 当前准备度

这个仓库已经用自己的 `production-readiness` skill 做过评审。

```text
Production Readiness Review

Conclusion: Ready
Scope: Initial public 0.1.0 plugin release
Project Type: documentation-heavy agent skill/plugin repository
Evidence Reviewed: README files, INSTALL.md, LICENSE, Codex manifest, skill files, references, inspector script, tests, CI config, inspector output

Must Fix Before Production:
- None currently known for the initial public plugin release.

High-Risk Gaps:
- None currently known for the initial public plugin release.

Recommended Improvements:
- Add example review reports as the project matures.
- Add release tags once the first version is cut.

Commands / Checks Run:
- python3 -m unittest tests/test_inspect_project.py
- python3 -m unittest tests/test_install_script.py
- python3 skills/production-readiness/scripts/inspect_project.py .
- python3 skills/production-readiness/scripts/inspect_project.py . --json
- python3 /path/to/plugin-creator/scripts/validate_plugin.py .

Unverified Assumptions:
- Marketplace installation behavior depends on the user's host tool configuration.

Release Checklist:
- README present
- License present
- Plugin manifest present and validated
- Skill and references present
- Inspector script present and tested
- Installer script present and tested
- CI workflow present
```

inspector 会提示缺少 `.env.example`，但这个仓库没有运行时配置或密钥，所以这是有意缺省，不是发布阻塞项。

## 支持的评审范围

- demo app 从展示进入真实使用前的评审
- API 发布准备度评审
- 浏览器 Web app 上线准备度评审
- 全栈项目发布评审
- 通用项目健康度和可维护性评审
- 部署、可观测性、可靠性、安全、数据、测试证据评审

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

### 一行安装

macOS / Linux：

```bash
curl -fsSL https://raw.githubusercontent.com/RockyYang1225/production-readiness/main/install.sh | bash
```

只安装某个平台：

```bash
curl -fsSL https://raw.githubusercontent.com/RockyYang1225/production-readiness/main/install.sh | bash -s codex
curl -fsSL https://raw.githubusercontent.com/RockyYang1225/production-readiness/main/install.sh | bash -s claude
curl -fsSL https://raw.githubusercontent.com/RockyYang1225/production-readiness/main/install.sh | bash -s agents
```

安装脚本会 clone 或更新仓库到：

```text
~/.production-readiness/repo
```

然后按所选平台创建 symlink：

| 工具 | 安装位置 |
|---|---|
| Codex | `~/plugins/production-readiness` 和 `~/.agents/plugins/marketplace.json` |
| Claude Code | `~/.claude/skills/production-readiness` |
| 文件型 skill 工具 | `~/.agents/skills/production-readiness` |

更新：

```bash
~/.production-readiness/repo/install.sh --update
```

卸载：

```bash
~/.production-readiness/repo/install.sh --uninstall all
~/.production-readiness/repo/install.sh --uninstall codex
~/.production-readiness/repo/install.sh --uninstall claude
~/.production-readiness/repo/install.sh --uninstall agents
```

### 手动安装

自己克隆仓库：

```bash
git clone https://github.com/RockyYang1225/production-readiness.git
cd production-readiness
```

| 工具 | 设置方式 |
|---|---|
| Codex | 把本地 checkout 作为插件安装或指向 Codex。Codex 会读取 `.codex-plugin/plugin.json`。 |
| Claude Code | 把 `skills/production-readiness` 软链接或复制到 `~/.claude/skills/production-readiness`。 |
| 其他文件型 skill 工具 | 指向 `skills/production-readiness/SKILL.md`。 |

Claude Code 软链接示例：

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/production-readiness" ~/.claude/skills/production-readiness
```

也可以复制：

```bash
mkdir -p ~/.claude/skills
cp -R skills/production-readiness ~/.claude/skills/
```

## 项目 Inspector

对目标项目运行 inspector：

```bash
python3 skills/production-readiness/scripts/inspect_project.py /path/to/project
```

输出 JSON：

```bash
python3 skills/production-readiness/scripts/inspect_project.py /path/to/project --json
```

inspector 是轻量工具。它会识别项目类型、常见生态、框架线索、基础发布信号、缺失的准备度信号、可疑文件名和可供 agent 深入查看的证据路径。

## 评审报告格式

使用这个 skill 的 agent 应输出：

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
python3 -m unittest tests/test_install_script.py
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
  READMEs/
    README.zh-CN.md
  install.sh
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

MIT。见 [LICENSE](../LICENSE)。
