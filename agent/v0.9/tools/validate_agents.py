#!/usr/bin/env python3
"""Validate the active AGENTS.md template without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


TEMPLATE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = TEMPLATE_ROOT / "agents-config.json"
AGENTS_PATH = TEMPLATE_ROOT / "AGENTS.md"
SKILLS_DIR = TEMPLATE_ROOT / "skills"

errors: list[str] = []
checks: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def passed(message: str) -> None:
    checks.append(message)


def read_utf8(path: Path) -> str:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        error(f"无法读取 {path}: {exc}")
        return ""

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        error(f"{path} 不是有效 UTF-8: {exc}")
        return ""

    if b"\r" in raw:
        error(f"{path} 包含 CR 或 CRLF，应使用 LF")
    if raw and not raw.endswith(b"\n"):
        error(f"{path} 末尾缺少换行")
    return text


def load_manifest() -> dict[str, object]:
    text = read_utf8(MANIFEST_PATH)
    if not text:
        return {}
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        error(f"{MANIFEST_PATH} 不是有效 JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        error(f"{MANIFEST_PATH} 顶层必须是对象")
        return {}
    return value


manifest = load_manifest()
required_keys = {
    "version",
    "last_reviewed",
    "review_after_days",
    "max_agents_lines",
}
missing_keys = required_keys - manifest.keys()
if missing_keys:
    error(f"agents-config.json 缺少字段: {', '.join(sorted(missing_keys))}")

version = str(manifest.get("version", ""))
max_lines = manifest.get("max_agents_lines", 0)
review_after_days = manifest.get("review_after_days", 0)

if not isinstance(max_lines, int) or max_lines <= 0:
    error("max_agents_lines 必须是正整数")
if not isinstance(review_after_days, int) or review_after_days <= 0:
    error("review_after_days 必须是正整数")

agents_text = read_utf8(AGENTS_PATH)
agents_lines = agents_text.splitlines()
if isinstance(max_lines, int) and max_lines > 0:
    if len(agents_lines) > max_lines:
        error(f"AGENTS.md 共 {len(agents_lines)} 行，超过限制 {max_lines}")
    else:
        passed(f"AGENTS.md 行数 {len(agents_lines)}/{max_lines}")

route_pattern = re.compile(
    r"^\|\s*(?!-{3})(.*?)\s*\|\s*`(skills/[^`]+\.md)`\s*\|\s*(.*?)\s*\|$"
)
routes: dict[str, tuple[str, str]] = {}

for line in agents_lines:
    match = route_pattern.match(line)
    if not match:
        continue
    trigger, relative_path, purpose = (item.strip() for item in match.groups())
    if not trigger or trigger == "触发条件":
        continue
    if not purpose or purpose == "用途":
        error(f"路由 {relative_path} 缺少用途说明")
    if relative_path in routes:
        error(f"Skill 路由重复: {relative_path}")
    routes[relative_path] = (trigger, purpose)

if not routes:
    error("AGENTS.md 未解析到任何 Skill 路由")
else:
    passed(f"解析到 {len(routes)} 条带触发条件和用途的 Skill 路由")

for relative_path, (trigger, purpose) in routes.items():
    target = TEMPLATE_ROOT / relative_path
    if not target.is_file():
        error(f"Skill 引用不存在: {relative_path}")
    if len(trigger) < 4 or len(purpose) < 4:
        error(f"Skill 路由描述过短: {relative_path}")

skill_files = {
    path.relative_to(TEMPLATE_ROOT).as_posix()
    for path in SKILLS_DIR.glob("*.md")
    if path.is_file()
}
route_files = set(routes)

for missing in sorted(route_files - skill_files):
    error(f"路由指向不存在的 Skill: {missing}")
for orphan in sorted(skill_files - route_files):
    error(f"Skill 未在路由表中声明: {orphan}")

if skill_files == route_files and skill_files:
    passed("所有 Skill 均有且仅有明确路由")

md_references = set(re.findall(r"`([^`]+\.md)`", agents_text))
allowed_non_skill_refs = {"AGENTS.md"}
naked_refs = {
    ref for ref in md_references
    if ref not in allowed_non_skill_refs and ref not in route_files
}
if naked_refs:
    error(f"发现未在路由表说明的 Markdown 引用: {', '.join(sorted(naked_refs))}")
else:
    passed("未发现裸 Markdown 引用")

for skill in sorted(SKILLS_DIR.glob("*.md")):
    text = read_utf8(skill)
    if not text.startswith("# "):
        error(f"{skill} 缺少一级标题")
    if "## 1. 加载条件" not in text:
        error(f"{skill} 缺少统一的加载条件章节")

lint_leakage_patterns = [
    r"(?:必须|应当|统一使用|禁止使用).{0,30}(?:camelCase|PascalCase|snake_case)",
    r"(?:必须|应当|统一使用|禁止使用).{0,30}(?:缩进|行长|导入顺序)",
    r"(?:使用|缩进为)\s*[24]\s*个空格",
]
for pattern in lint_leakage_patterns:
    if re.search(pattern, agents_text, flags=re.IGNORECASE):
        error(f"AGENTS.md 疑似包含应由工具执行的样式规则: {pattern}")

if "确定性规则交由项目现有工具执行" not in agents_text:
    error("AGENTS.md 未明确将确定性样式规则交给项目工具")
else:
    passed("确定性样式规则已委托给项目工具")

try:
    reviewed = date.fromisoformat(str(manifest.get("last_reviewed", "")))
except ValueError:
    error("last_reviewed 必须使用 YYYY-MM-DD")
else:
    age = (date.today() - reviewed).days
    if age < 0:
        error("last_reviewed 不能晚于当前日期")
    elif isinstance(review_after_days, int) and age > review_after_days:
        error(
            f"配置距上次审查已 {age} 天，超过 {review_after_days} 天；"
            "请执行配置异味审查并更新 last_reviewed"
        )
    else:
        passed(f"维护审查日期有效，距今 {age} 天")

# 在模板源码仓库内运行时，额外校验当前版本入口；复制到其他项目后自动跳过。
if TEMPLATE_ROOT.parent.name == "agent" and TEMPLATE_ROOT.name == f"v{version}":
    repo_root = TEMPLATE_ROOT.parents[1]
    expected = f"agent/v{version}/"

    for path in (repo_root / "README.md", repo_root / "AGENTS.md"):
        text = read_utf8(path)
        if expected not in text:
            error(f"{path} 未声明当前模板 {expected}")

    version_text = read_utf8(repo_root / "agent" / "version.md")
    if f"### v{version}" not in version_text:
        error(f"agent/version.md 未记录 v{version}")

    if not (repo_root / ".editorconfig").is_file():
        error("仓库缺少 .editorconfig，确定性文本规则未工具化")
    if not (repo_root / ".github" / "workflows" / "validate-agent-config.yml").is_file():
        error("仓库缺少 AGENTS 配置校验工作流")
    passed("源码仓库入口和自动化文件已检查")

if errors:
    print("AGENTS 配置校验失败：")
    for item in errors:
        print(f"- {item}")
    sys.exit(1)

print("AGENTS 配置校验通过：")
for item in checks:
    print(f"- {item}")
