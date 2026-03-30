#!/usr/bin/env python3
"""Link ai-resources skills and instructions for Claude Code and/or Copilot CLI / VS Code."""

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_SOURCE_DIRS = ["skills/commands", "skills/prompts"]
INSTRUCTIONS_DIR = SCRIPT_DIR / "instructions"

CLAUDE_MD_MARKER_START = "<!-- ai-resources instructions -->"
CLAUDE_MD_MARKER_END = "<!-- /ai-resources instructions -->"


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

def link_skill(src: Path, skills_dir: Path) -> None:
    slug = src.stem
    skill_dir = skills_dir / slug
    dest = skill_dir / "SKILL.md"

    skill_dir.mkdir(parents=True, exist_ok=True)

    if dest.exists() and not dest.is_symlink():
        print(f"  skip {dest} (exists, not a symlink)")
        return

    if dest.is_symlink():
        dest.unlink()

    dest.symlink_to(src)
    print(f"  /{slug} -> {dest}")


def unlink_skill(src: Path, skills_dir: Path) -> None:
    slug = src.stem
    skill_dir = skills_dir / slug
    dest = skill_dir / "SKILL.md"

    if dest.is_symlink():
        dest.unlink()
        print(f"  removed {dest}")
    if skill_dir.is_dir() and not any(skill_dir.iterdir()):
        skill_dir.rmdir()


# ---------------------------------------------------------------------------
# Instructions — .github/instructions/ symlinks (Copilot / VS Code)
# ---------------------------------------------------------------------------

def link_instruction_vscode(src: Path, gh_instructions_dir: Path) -> None:
    dest = gh_instructions_dir / src.name

    gh_instructions_dir.mkdir(parents=True, exist_ok=True)

    if dest.exists() and not dest.is_symlink():
        print(f"  skip {dest} (exists, not a symlink)")
        return

    if dest.is_symlink():
        dest.unlink()

    dest.symlink_to(src)
    print(f"  {src.name} -> {dest}")


def unlink_instruction_vscode(src: Path, gh_instructions_dir: Path) -> None:
    dest = gh_instructions_dir / src.name

    if dest.is_symlink():
        dest.unlink()
        print(f"  removed {dest}")


# ---------------------------------------------------------------------------
# Instructions — CLAUDE.md imports (Claude Code)
# ---------------------------------------------------------------------------

def _build_import_block(instruction_files: list[Path]) -> str:
    lines = [CLAUDE_MD_MARKER_START]
    for f in sorted(instruction_files):
        lines.append(f"@{f}")
    lines.append(CLAUDE_MD_MARKER_END)
    return "\n".join(lines) + "\n"


def link_instruction_claude_md(claude_md: Path, instruction_files: list[Path]) -> None:
    block = _build_import_block(instruction_files)

    if not claude_md.exists():
        claude_md.parent.mkdir(parents=True, exist_ok=True)
        claude_md.write_text(block)
        print(f"  created {claude_md} with instruction imports")
        return

    content = claude_md.read_text()
    pattern = re.compile(
        rf"{re.escape(CLAUDE_MD_MARKER_START)}.*?{re.escape(CLAUDE_MD_MARKER_END)}\n?",
        re.DOTALL,
    )

    if pattern.search(content):
        new_content = pattern.sub(block, content)
        claude_md.write_text(new_content)
        print(f"  updated instruction imports in {claude_md}")
    else:
        separator = "\n" if content and not content.endswith("\n") else ""
        claude_md.write_text(content + separator + block)
        print(f"  appended instruction imports to {claude_md}")


def unlink_instruction_claude_md(claude_md: Path) -> None:
    if not claude_md.exists():
        return

    content = claude_md.read_text()
    pattern = re.compile(
        rf"\n?{re.escape(CLAUDE_MD_MARKER_START)}.*?{re.escape(CLAUDE_MD_MARKER_END)}\n?",
        re.DOTALL,
    )

    new_content = pattern.sub("", content)
    if new_content != content:
        claude_md.write_text(new_content)
        print(f"  removed instruction imports from {claude_md}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Link ai-resources skills and instructions for Claude Code and Copilot CLI / VS Code"
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--global", dest="global_", action="store_true",
                        help="Install globally (~/.claude/)")
    target.add_argument("--project", type=str, metavar="PATH",
                        help="Install into a specific project directory")

    parser.add_argument("--copilot", action="store_true",
                        help="Use .copilot/skills/ instead of .claude/skills/ for skills")
    parser.add_argument("--unlink", action="store_true",
                        help="Remove linked skills and instructions")
    args = parser.parse_args()

    home = Path.home()
    tool_dir = ".copilot" if args.copilot else ".claude"
    action = "Unlinking" if args.unlink else "Linking"

    if args.global_:
        skills_dir = home / tool_dir / "skills"
        claude_md = home / ".claude" / "CLAUDE.md"
        gh_instructions_dir = None  # no global .github/instructions for Copilot
        mode = "global"
    else:
        project = Path(args.project).resolve()
        if not project.is_dir():
            print(f"Project path '{args.project}' does not exist", file=sys.stderr)
            sys.exit(1)
        skills_dir = project / tool_dir / "skills"
        claude_md = project / "CLAUDE.md"
        gh_instructions_dir = project / ".github" / "instructions"
        mode = args.project

    print(f"{action} ai-resources ({mode})")

    # --- Skills ---
    print(f"\n[skills] -> {skills_dir}")
    for dir_name in SKILL_SOURCE_DIRS:
        source_dir = SCRIPT_DIR / dir_name
        if not source_dir.is_dir():
            continue
        for src in sorted(source_dir.glob("*.md")):
            if args.unlink:
                unlink_skill(src, skills_dir)
            else:
                link_skill(src, skills_dir)

    # --- Instructions ---
    instruction_files = sorted(INSTRUCTIONS_DIR.glob("*.md")) if INSTRUCTIONS_DIR.is_dir() else []

    if instruction_files:
        print(f"\n[instructions]")

        if args.unlink:
            if gh_instructions_dir is not None:
                for src in instruction_files:
                    unlink_instruction_vscode(src, gh_instructions_dir)
            unlink_instruction_claude_md(claude_md)
        else:
            if gh_instructions_dir is not None:
                print(f"  VS Code/Copilot -> {gh_instructions_dir}")
                for src in instruction_files:
                    link_instruction_vscode(src, gh_instructions_dir)
            print(f"  Claude Code -> {claude_md}")
            link_instruction_claude_md(claude_md, instruction_files)
    else:
        print("\n[instructions] no files found, skipping")

    print("\nDone.")


if __name__ == "__main__":
    main()
