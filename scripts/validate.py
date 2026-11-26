#!/usr/bin/env python3
"""Validate the ai-workspace control repository without third-party packages."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "registry.yaml",
    "CONTINUE_PROMPT.md",
    "MULTI_MACHINE_RULES.md",
    "thinking/CORE.md",
    "thinking/ACTIVATION.md",
    "thinking/patterns/README.md",
    "jy/README.md",
    "jy/TEMPLATE.md",
    "jy/reviews/README.md",
    "templates/START_HERE.md",
    "templates/AGENTS.md",
    "templates/project.yaml",
    "templates/state.md",
    "templates/PROJECT_ONBOARDING_PROMPT.md",
    "templates/PROJECT_CONTINUE_PROMPT.md",
    "templates/FIRST_PUSH.md",
    "local/projects.example.yaml",
    "local/apps.example.yaml",
    "skills/README.md",
]
FORBIDDEN_REGISTRY_PATHS = ("/Users/", "C:\\", "D:\\", "\\\\")
PROJECT_ID = re.compile(r"^[a-z0-9][a-z0-9-]{2,63}$")


def main():
    errors = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"缺少文件：{relative}")

    # README 必须引用范式规则、思考协议与建议工作区（让标准“接线生效”）
    readme_path = ROOT / "README.md"
    if readme_path.is_file():
        readme_text = readme_path.read_text(encoding="utf-8")
        if "MULTI_MACHINE_RULES" not in readme_text:
            errors.append("README.md 未引用 MULTI_MACHINE_RULES.md")
        for reference in ("thinking/CORE.md", "thinking/ACTIVATION.md", "jy/README.md"):
            if reference not in readme_text:
                errors.append(f"README.md 未引用 {reference}")

    # 通用续作与模板必须加载同一份思考协议
    for relative in ("CONTINUE_PROMPT.md", "templates/PROJECT_CONTINUE_PROMPT.md"):
        path = ROOT / relative
        if path.is_file() and "thinking/CORE.md" not in path.read_text(encoding="utf-8"):
            errors.append(f"{relative} 未引用 thinking/CORE.md")

    template_path = ROOT / "jy/TEMPLATE.md"
    if template_path.is_file() and "base_commit" not in template_path.read_text(encoding="utf-8"):
        errors.append("jy/TEMPLATE.md 未记录 base_commit")

    # 框架自身必须可移植：扫描 .py / .yaml（不含 local/ 与 .git）是否含本机绝对路径
    # 注意：不纳入 UNC 标记 "\\\\"，否则本校验脚本的标记定义行会自我误伤
    portability_markers = ("/Users/", "C:\\", "D:\\")
    for suffix in ("*.py", "*.yaml"):
        for path in ROOT.rglob(suffix):
            parts = path.relative_to(ROOT).parts
            if "local" in parts or ".git" in parts:
                continue
            # 跳过本校验脚本自身：它必然包含要检查的标记定义
            if path.name == "validate.py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in portability_markers:
                if marker in text:
                    errors.append(
                        f"框架文件包含本机绝对路径：{path.relative_to(ROOT)}（违反 R1）"
                    )
                    break

    # 协议与建议必须跨设备可移植，不能记录某台电脑的真实路径
    for directory_name in ("thinking", "jy"):
        directory = ROOT / directory_name
        if directory.is_dir():
            for path in directory.rglob("*.md"):
                text = path.read_text(encoding="utf-8", errors="ignore")
                for marker in portability_markers:
                    if marker in text:
                        errors.append(f"{directory_name} 文档包含本机绝对路径：{path.relative_to(ROOT)}")
                        break

    registry_path = ROOT / "registry.yaml"
    if registry_path.is_file():
        text = registry_path.read_text(encoding="utf-8")
        for marker in FORBIDDEN_REGISTRY_PATHS:
            if marker in text:
                errors.append("registry.yaml 包含本机绝对路径")
                break
        project_lines = [
            line for line in text.splitlines()
            if re.match(r"^  [a-z0-9][a-z0-9-]*:$", line)
        ]
        project_ids = [line.strip()[:-1] for line in project_lines]
        if not project_ids:
            errors.append("registry.yaml 未登记任何项目")
        if len(project_ids) != len(set(project_ids)):
            errors.append("registry.yaml 存在重复项目 ID")
        for project_id in project_ids:
            if not PROJECT_ID.fullmatch(project_id):
                errors.append(f"项目 ID 不符合规范：{project_id}")

    if errors:
        print("校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ai-workspace 校验通过：必要文件、思考协议、建议工作区、项目 ID 和远程登记规范完整。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
