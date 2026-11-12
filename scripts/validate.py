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
    print("ai-workspace 校验通过：必要文件、项目 ID 和远程登记规范完整。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
