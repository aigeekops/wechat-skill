#!/usr/bin/env python3
"""Validate skill packaging offline; never connects to a device."""

import ast
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    required = (
        "SKILL.md", "README.md", "LICENSE", "CONTRIBUTING.md", "SECURITY.md",
        "THIRD_PARTY.md", "agents/openai.yaml", "docs/verification.md",
    )
    for name in required:
        if not (root / name).is_file():
            errors.append(f"Missing required file: {name}")
    if errors:
        return errors

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", skill, re.S)
    metadata = yaml.safe_load(match.group(1)) if match else None
    if not isinstance(metadata, dict):
        errors.append("SKILL.md requires YAML frontmatter")
    else:
        if metadata.get("name") != "wechat-skill":
            errors.append("Skill name must be wechat-skill")
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append("Skill description must be nonempty text")
        if metadata.get("license") != "MIT":
            errors.append("Skill license must match LICENSE (MIT)")

    ui = yaml.safe_load((root / "agents/openai.yaml").read_text(encoding="utf-8"))
    interface = ui.get("interface", {}) if isinstance(ui, dict) else {}
    if not isinstance(interface, dict):
        interface = {}
    if interface.get("display_name") != "WeChat Skill":
        errors.append("Display name must be WeChat Skill")
    summary = interface.get("short_description", "")
    if not isinstance(summary, str) or not 25 <= len(summary) <= 64:
        errors.append("UI short_description must contain 25-64 characters")
    prompt = interface.get("default_prompt", "")
    if not isinstance(prompt, str) or "$wechat-skill" not in prompt:
        errors.append("Default prompt must reference $wechat-skill")

    docs = [root / name for name in required if name.endswith(".md")]
    for directory in ("references", "workflows", ".github"):
        docs.extend((root / directory).rglob("*.md"))
    for path in sorted(set(docs)):
        content = path.read_text(encoding="utf-8")
        label = path.relative_to(root)
        for target in re.findall(r"\]\(([^\s)]+)\)", content):
            parts = urlsplit(target)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            destination = (path.parent / unquote(parts.path)).resolve()
            if not destination.is_relative_to(root):
                errors.append(f"{label}: link escapes repository: {target}")
            elif not destination.is_file():
                errors.append(f"{label}: broken file link: {target}")
        for code in re.findall(r"```python\n(.*?)```", content, re.S):
            try:
                ast.parse(code)
            except SyntaxError as exc:
                errors.append(f"{label}: invalid Python example: {exc.msg}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        errors = validate(root)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Skill metadata, packaging, relative file links and examples: OK")
    print("Static checks only; no phone actions performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
