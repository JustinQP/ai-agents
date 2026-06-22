# 系统降噪重构图（v1 视角）

## 1. 目标

将 v0.9 规则体系从“规则堆叠系统”收敛为“分层决策系统”，降低重复约束与认知负担。

---

## 2. 降噪前 vs 降噪后

### Before（v0.9 规则堆叠）

```text
Codex Global
 + 工程细节
 + 部分行为规则

AGENTS.md
 + 决策 + 工程约束 + 路由

Skills
 + 执行逻辑 + 部分策略 + 部分校验

Validator
 + 结构校验 + smell detection
```

问题：
- 规则重复（Global / AGENTS / Skills）
- 判断逻辑分散
- 工程细节污染上层
- 认知负担随规模增长
```

---

### After（v1 降噪结构）

```text
Codex Global
 → 只保留“思维方式”

AGENTS.md
 → 只保留“任务路由 + 风险控制”

Skills
 → 只保留“领域执行逻辑”

Validator
 → 只保留“机器约束 + smell detection”
```

---

## 3. 信息流（关键）

```text
User Input
    ↓
Codex Global（思维策略）
    ↓
AGENTS（任务解析 + Skill 路由）
    ↓
Skills（执行）
    ↓
Validator（结构校验）
    ↓
Output
```

---

## 4. 降噪核心原则

### 1）单一职责收敛

- Global：不碰工程细节
- AGENTS：不写执行细节
- Skills：不写跨领域规则
- Validator：不参与语义决策

---

### 2）规则去重策略

| 冗余来源 | 处理方式 |
|----------|----------|
| Global vs AGENTS | 删除 Global 中工程规则 |
| AGENTS vs Skills | 下沉到 Skill |
| Skills vs Validator | 可验证逻辑上移 Validator |

---

### 3）控制点唯一化

```text
行为控制：Codex Global
决策控制：AGENTS
执行控制：Skills
结构控制：Validator
```

---

## 5. 当前系统状态评估

### 已完成降噪

- Skill 拆分完成（领域化）
- Validator 引入（结构约束）
- AGENTS 路由化

### 剩余风险

- Global 仍可能回流工程语义（需持续收缩）
- Skills 可能产生跨域重复（需去重）

---

## 6. 结论

> 系统降噪的本质不是减少规则，而是“减少规则的重叠区域”。
