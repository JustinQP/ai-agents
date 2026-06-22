# AGENTS.md

## 1. 仓库定位

本仓库是个人使用的 AI 指令与项目治理模板库，不是可运行的 Agent 框架。

维护目标：

- 保持个人全局指令短小、稳定
- 维护可完整复制的项目级 `AGENTS.md` 模板
- 将低频规则拆分为按需 Skill
- 用自动化检查替代确定性文本约束

## 2. 当前入口

- 当前项目模板：`agent/v0.9/`
- Codex 全局指令：`codex-global/v0.1.md`
- ChatGPT 指令模板：`chatgpt-rule/v0.1.example.md`
- 校验命令：`python agent/v0.9/tools/validate_agents.py`

`agent/v0.1` 至 `agent/v0.8` 是历史快照。除非任务明确要求，不修改历史版本。

## 3. 指令冲突

在不违反平台与安全规则的前提下，当前任务的明确要求优先于本文件；本文件优先于普通项目文档。

同一层级出现冲突时，更具体、作用域更小的规则优先。无法消除的冲突必须说明；高风险或不可逆操作不得任意选择规则继续执行。

## 4. 修改规则

- 只修改与当前目标直接相关的文件。
- 新版本必须是完整快照，不能只保存增量文件。
- 修改当前模板、Skill、版本入口或校验工具时，读取 `agent/v0.9/skills/config-maintenance.md`；该文件用于执行六类配置异味审查和维护流程。
- 主 `AGENTS.md` 只保留常驻规则和 Skill 路由，专项细节放入明确触发的 Skill。
- 每个文件引用必须说明何时读取及其用途，引用路径必须真实存在。
- 格式、编码、换行和可机械检查的结构由 `.editorconfig` 与校验脚本执行，不在指令中重复展开。
- 更新模板时同步更新 `agents-config.json` 的审查日期和 `agent/version.md`。
- 不提交个人资料、账号、Token、密钥或公司敏感信息。
- 私人 ChatGPT 配置只写入已忽略的 `chatgpt-rule/local.md`。

## 5. 验证

完成修改后运行：

```bash
python agent/v0.9/tools/validate_agents.py
```

必须如实报告命令结果、失败、警告和未验证项。不得把未执行的检查写成通过。
