# 项目规则版本记录

## 当前版本

### v0.9

目标：按照 AGENTS.md 配置异味研究，降低常驻上下文、明确按需加载，并增加可执行维护检查。

主要变化：

- Context Bloat：主 `AGENTS.md` 从 v0.8 的 162 行压缩到 75 行，自动上限为 150 行
- Skill Leakage：将复杂流程、测试、文档、数据库、外部服务、前端、部署、安全和 AI 规则拆为独立 Skill
- Lint Leakage：将 UTF-8、LF 和末尾换行交给 `.editorconfig` 与校验脚本
- Blind Reference：增加带触发条件、路径和用途的 Skill 路由表，并自动检查引用
- Init Fossilization：增加审查日期、180 天周期和配置维护 Skill
- Conflicting Instructions：明确规则优先级、同层冲突处理和不可逆操作边界
- 新增无第三方依赖的 `tools/validate_agents.py`
- 新增 GitHub Actions 自动校验

目录：

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

## 历史版本

- v0.1：限制 AI 无关修改和跳步
- v0.2：增加执行步骤和文件约束
- v0.3：按开发阶段推进
- v0.4：增加文档治理
- v0.5：增加工程化底线
- v0.6：增加测试与验收
- v0.7：主规则瘦身并拆分专项文件
- v0.8：形成可直接复制的完整模板包，补充项目事实和高风险边界
