# Production Readiness 插件设计（中文版）

日期：2026-05-30

## 目标

做一个可以发布到 GitHub 的“生产上线准备度评审”插件包，供 Codex、Claude Code 以及类似的开发 agent 工具使用。

第一版不是做一个 SaaS 扫描平台，而是做一个可复用的 agent skill / plugin：

- 能让 agent 检查一个 demo app 是否真的具备上线条件。
- 支持接口级项目、Web app、全栈项目和通用项目评审。
- 自带检查域参考文档。
- 自带一个轻量脚本，用来快速识别项目类型和明显缺口。
- 同时提供 Codex 和 Claude Code 的安装说明。
- 接入 Jarvis workflow：生产上线准备度评审。

## 不做什么

第一版不做这些事：

- 不做托管服务。
- 不要求联网。
- 不声称能完成 SOC 2、HIPAA、PCI、GDPR 等合规认证。
- 不自动修改被评审项目。
- 不替代真正高风险项目的人工上线审批。

## 仓库形态

本地仓库路径：

```text
/Users/rockyyang/Workspace/production-readiness
```

第一版目录结构：

```text
production-readiness/
  .codex-plugin/
    plugin.json
  skills/
    production-readiness/
      SKILL.md
      references/
        api.md
        data.md
        deployment.md
        full-stack.md
        general.md
        observability.md
        reliability.md
        security.md
        testing.md
        web-app.md
      scripts/
        inspect_project.py
  docs/
    superpowers/
      specs/
        2026-05-30-production-readiness-plugin-design.md
        2026-05-30-production-readiness-plugin-design.zh.md
  README.md
  LICENSE
```

## 插件定位

插件包名：

```text
production-readiness
```

展示名称：

```text
Production Readiness
```

主要触发词：

- production readiness
- launch readiness
- release readiness
- demo app review
- production 上线准备度
- 上线前评审
- 发布前检查

## 主 Skill

主 skill 放在：

```text
skills/production-readiness/SKILL.md
```

当用户让 agent 检查一个项目是否可以上线、发布、部署、交付或从 demo 进入 production 时，就应该触发这个 skill。

主 skill 的工作流程：

1. 先判断项目类型和评审范围。
2. 如果能访问本地文件，就运行或建议运行 `inspect_project.py`。
3. 根据项目类型选择相关检查域。
4. 从源码、文档、配置、测试、日志、截图和命令输出里收集证据。
5. 输出结构化的上线准备度报告。
6. 对没有验证过的内容标记为假设。
7. 给出最小但有用的下一步行动。

核心原则：必须基于证据评审。不能只因为 README 写得漂亮、框架默认看起来安全，或者用户说“这是 demo”，就判断项目已准备好上线。

## 检查域

第一版会拆成多个 reference 文件。主 skill 按需读取，不需要每次全部加载。

### general.md

通用项目检查。关注项目目标是否清晰、是否能复现安装和运行、依赖是否健康、配置是否完整、许可证是否明确、文档是否够用、维护责任是否清楚。

### security.md

安全检查。关注密钥处理、认证、授权、输入校验、依赖漏洞、浏览器安全基础、CORS、限流、安全默认值、敏感日志。

### reliability.md

可靠性检查。关注错误处理、重试、降级、超时、并发假设、后台任务、资源限制、恢复路径。

### observability.md

可观测性检查。关注日志、指标、trace、健康检查、审计线索、可告警的失败模式、排查问题时是否方便。

### deployment.md

部署检查。关注环境变量、构建脚本、启动脚本、部署文档、运行时要求、数据库迁移、回滚计划、冒烟测试、发布门禁。

### data.md

数据检查。关注 schema 归属、迁移、备份恢复、数据校验、保留策略、隐私敏感字段、幂等性、破坏性操作。

### api.md

接口检查。关注接口契约、认证、参数校验、错误返回、分页、幂等性、限流、版本管理、OpenAPI 或同等文档、集成测试。

### web-app.md

Web app 检查。关注核心用户流程、响应式布局、基础可访问性、加载/错误/空状态、浏览器控制台错误、表单校验、前端密钥泄露、缓存、性能预算。

### full-stack.md

全栈项目检查。关注前后端契约、环境一致性、数据库集成、异步边界、认证流程、部署拓扑、集成测试、端到端冒烟测试。

### testing.md

测试检查。关注单元测试、集成测试、e2e、冒烟测试、契约测试、fixture、回归测试、人工验收证据。必须区分“测试存在”和“测试真的运行过”。

## inspect_project.py

脚本位置：

```text
skills/production-readiness/scripts/inspect_project.py
```

使用方式：

```bash
python3 skills/production-readiness/scripts/inspect_project.py /path/to/project
```

第一版能力：

- 识别项目大致类型：API、Web app、全栈、库、文档型项目、未知。
- 识别常见生态和框架线索，比如 `package.json`、`pyproject.toml`、`requirements.txt`、`go.mod`、`Cargo.toml`、`Dockerfile`、`compose.yaml`、`.env.example`、CI 配置、常见前后端目录。
- 输出每个判断背后的文件证据。
- 标记明显缺口，比如缺 README、缺测试、缺环境变量示例、缺 CI、缺部署线索、缺 LICENSE、缺健康检查线索。
- 默认输出 Markdown。
- 支持 `--json` 输出机器可读结果。

第一版不做深度密钥扫描。它可以提示疑似敏感文件名，并建议使用专门的 secret scanner。

## 评审报告格式

主 skill 输出报告时使用这个结构：

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

结论规则：

- `Ready`：没有已知上线阻塞项，关键生产控制有证据，剩余问题风险较低。
- `Conditionally Ready`：可以在明确限制下做内部发布、试点、有限发布或 demo 发布。
- `Not Ready`：缺少关键安全、可靠性、部署、数据或验证证据。

## Codex 接入

Codex 通过这个文件识别插件：

```text
.codex-plugin/plugin.json
```

manifest 第一版包含：

- name: `production-readiness`
- version: `0.1.0`
- license: `MIT`
- skills path: `./skills/`
- 插件展示信息和 starter prompts

第一版不接 MCP server、不接 app manifest、不接 hooks，也不需要外部认证。

## Claude Code 接入

Claude Code 使用文件安装方式：

- 把 `skills/production-readiness` 复制或 symlink 到 Claude Code 的 skills 目录。
- 用户直接要求 production-readiness、launch-readiness 或 release-readiness review 即可触发。

仓库本身不依赖 Claude 专属格式，只保持标准 `SKILL.md` 结构。

## README 要写什么

`README.md` 第一版包含：

- 这个项目是什么。
- 支持哪些评审范围。
- 能保证什么，不能保证什么。
- Codex 快速安装。
- Claude Code 快速安装。
- 如何运行 `inspect_project.py`。
- 示例评审 prompt。
- 预期报告格式。
- 仓库目录说明。
- LICENSE。

## Jarvis Workflow 接入

新增 Jarvis workflow：

```text
/Users/rockyyang/Jarvis/90_System/Workflows/Production Readiness Review.md
```

同时更新：

```text
/Users/rockyyang/Jarvis/90_System/Workflows/Workflows.md
/Users/rockyyang/Jarvis/90_System/Agents/Workflow Registry.md
```

Workflow 中文名：

```text
生产上线准备度评审
```

用途：

当一个项目、demo app、Web app、API 或全栈项目准备被认为“可以上线”或“可以发布”之前，使用这个 workflow。

Workflow 需要说明：

- 输入：项目路径、目标部署环境、可接受风险、发布范围、已有证据。
- 输出：上线准备度结论、阻塞项、风险项、验证证据、下一步。
- agent 边界：评审 agent 只评估准备度，不偷偷部署、不归档、不删除、不重写长期 Jarvis 知识、不对外发通知。
- 人工确认点：写入长期 Jarvis 知识、真实生产部署、公开发布、对外沟通之前都需要确认。

## 第一版完成标准

完成第一版前要满足：

- Codex plugin manifest 能通过本地 validator。
- `inspect_project.py --json` 能跑这个仓库本身。
- `inspect_project.py` 默认 Markdown 输出能跑这个仓库本身。
- 主 skill 有合法 YAML frontmatter。
- README 安装步骤可直接照着执行。
- Jarvis workflow 链接已更新。
- 发布文件里没有未解决的脚手架标记。

## 已定决策

- 仓库形态：中立 GitHub repo，同时提供 Codex 和 Claude Code 安装路径。
- License：MIT。
- 第一版版本号：`0.1.0`。
- 第一版不接外部服务。
- 第一版不创建个人 marketplace entry，除非后面单独要求。
