# AI Agents Personal Rules

个人使用的 AI 指令与项目治理模板库。本仓库不是可运行的 Agent 框架。

## 内容分层

- 个人全局指令：长期稳定、跨项目通用的偏好
- 项目 `AGENTS.md`：项目事实、常驻约束和 Skill 路由
- Skill：只在特定任务触发时读取的专项流程
- 当前对话：一次性任务要求

## 当前推荐版本

- 项目模板：`agent/v0.9/`
- Codex 全局指令：`codex-global/v0.1.md`
- ChatGPT 指令模板：`chatgpt-rule/v0.1.example.md`
- `agent/v0.1` 至 `agent/v0.8`：历史快照

新项目默认使用 v0.9。

## v0.9 目录

```text
agent/v0.9/
  AGENTS.md
  agents-config.json
  skills/
    complex-workflow.md
    testing.md
    documentation.md
    database.md
    external-services.md
    frontend.md
    deployment.md
    security.md
    ai-features.md
    config-maintenance.md
  tools/
    validate_agents.py
```

将 `agent/v0.9/` 中的全部内容复制到目标项目根目录后，先填写 `AGENTS.md` 的“项目事实”部分。

至少需要填写：

- 项目目标和技术栈
- 核心目录与模块边界
- 安装、启动、构建命令
- 测试与静态检查命令
- 禁止修改区域
- 项目完成标准

通用模板不能替代真实项目上下文。

## 六类配置异味治理

v0.9 按以下方式调整：

| 配置异味 | 调整方式 |
|---|---|
| Context Bloat | 主 `AGENTS.md` 压缩为 75 行，并设置 150 行自动上限 |
| Skill Leakage | 测试、数据库、部署、安全、AI 等内容拆成按需 Skill |
| Lint Leakage | 编码和换行交由 `.editorconfig`，结构与路径交由校验脚本 |
| Blind Reference | 主文件使用“触发条件—文件—用途”路由表，脚本校验引用 |
| Init Fossilization | `agents-config.json` 记录审查日期和周期，过期后校验失败 |
| Conflicting Instructions | 主文件定义优先级与冲突处理，维护 Skill 要求清理重复规则 |

## 使用 Skill

不要默认读取全部 Skill。根据 `AGENTS.md` 路由表，只加载与当前任务匹配的文件。

例如：

- 数据迁移读取 `skills/database.md`
- 外部 API 或后台任务读取 `skills/external-services.md`
- 大模型或 RAG 功能读取 `skills/ai-features.md`
- 修改规则本身读取 `skills/config-maintenance.md`

每个 Skill 都包含独立的“加载条件”。

## 自动校验

在本仓库中运行：

```bash
python agent/v0.9/tools/validate_agents.py
```

校验内容包括：

- 主 `AGENTS.md` 行数上限
- Skill 路由是否包含触发条件和用途
- 引用文件是否存在
- 是否存在未路由的 Skill 或裸引用
- Skill 是否声明加载条件
- 主文件是否疑似泄漏确定性样式规则
- 审查日期是否过期
- README、根 `AGENTS.md` 和版本记录是否指向当前版本
- UTF-8、LF 和文件末尾换行

GitHub Actions 会在相关文件变化时运行同一校验。

## 维护时机

以下情况应审查规则，而不是简单追加新指令：

- Agent 第二次犯同类错误
- 项目命令、目录、架构或关键流程变化
- 同一纠正需要在多个会话重复说明
- 新增、合并或删除 Skill
- 发布新的模板版本
- 审查周期到期

真实个人配置继续保存于 `chatgpt-rule/local.md`，该文件不会提交到仓库。
