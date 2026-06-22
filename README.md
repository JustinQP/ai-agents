# AI Agents Personal Rules

个人使用的 AI 指令与项目治理模板库。本仓库不是可运行的 Agent 框架。

## 内容分层

- Codex Global：行为层（思考方式控制）
- AGENTS.md：决策层（任务分解与 Skill 路由）
- Skills：执行层（领域化实现规则）
- Validator：结构约束层（机器校验）

## 当前推荐版本

- 项目模板：`agent/v0.9/`
- Codex 全局指令：`codex-global/v0.1.md`
- 架构说明：`docs/codex-global-architecture.md`
- ChatGPT 指令模板：`chatgpt-rule/v0.1.example.md`
- 历史版本：`agent/v0.1` 至 `agent/v0.8`

新项目默认使用 v0.9。

## v0.9 结构

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

## 三层系统说明

本仓库的设计已经从“规则集合”升级为“分层行为系统”：

- Codex Global：定义思考方式（behavior layer）
- AGENTS.md：定义任务调度与风险控制（decision layer）
- Skills：定义具体领域执行逻辑（execution layer）
- Validator：提供机器级约束（constraint layer）

详细设计见：`docs/codex-global-architecture.md`

## 设计原则（简化版）

- 不通过增加规则提升稳定性，而是通过分层降低复杂度
- 不把工程细节写进 Global
- 不把执行逻辑写进 AGENTS
- 不把判断逻辑写进 Skills
- 所有结构问题交给 Validator
