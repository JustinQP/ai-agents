# AI Agents Personal Rules

个人使用的 AI 指令与项目治理模板库。本仓库不是可运行的 Agent 框架。

## 内容分层

- 个人全局指令：长期稳定、跨项目通用的偏好
- 项目 `AGENTS.md`：具体项目的开发与治理规则
- 专项规则：测试、工程、文档等按任务类型读取的细则
- 当前对话：一次性任务要求

## 当前推荐版本

- 项目规则完整模板：`agent/v0.8/`
- Codex 全局指令：`codex-global/v0.1.md`
- ChatGPT 指令模板：`chatgpt-rule/v0.1.example.md`
- `agent/v0.1` 至 `agent/v0.7`：历史版本，仅用于回顾演进过程

## 使用项目规则

把 `agent/v0.8/` 目录中的全部内容复制到目标项目根目录。复制后的结构应为：

```text
AGENTS.md
docs/
  30-rules/
    ai-workflow.md
    docs-governance.md
    engineering-baseline.md
    testing-acceptance.md
```

复制后先填写 `AGENTS.md` 中的“项目特定信息”，至少补充：

- 项目类型和技术栈
- 关键目录与模块边界
- 安装、启动和构建命令
- 测试与静态检查命令
- 禁止修改区域
- 项目完成标准

通用模板不能替代具体项目的真实上下文。

## 个人指令

`codex-global/v0.1.md` 只保存跨项目通用偏好，不写入具体项目的技术栈、目录和测试命令。

`chatgpt-rule/v0.1.example.md` 是去隐私化模板。真实个人配置应保存为 `chatgpt-rule/local.md`；该路径已被忽略，不应提交到仓库。

## 大小建议

- 个人全局指令：约 500–1200 中文字
- 项目主 `AGENTS.md`：优先控制在 100–150 个非空行
- 低频专项规则：拆分到 `docs/30-rules/`

核心原则：全局指令保持短小，项目规则提供真实上下文，专项流程按需加载，临时要求留在当前对话。
