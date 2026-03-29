#!/usr/bin/env python3
"""Symlink ai-resources as Agent Skills for Claude Code and/or Copilot CLI."""

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_DIRS = ["commands", "prompts"]


def link(src: Path, skills_dir: Path) -> None:
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


def unlink(src: Path, skills_dir: Path) -> None:
    slug = src.stem
    skill_dir = skills_dir / slug
    dest = skill_dir / "SKILL.md"

    if dest.is_symlink():
        dest.unlink()
        print(f"  removed {dest}")
    if skill_dir.is_dir() and not any(skill_dir.iterdir()):
        skill_dir.rmdir()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Link ai-resources as skills for Claude Code and Copilot CLI"
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--global", dest="global_", action="store_true",
                        help="Install globally")
    target.add_argument("--project", type=str, metavar="PATH",
                        help="Install into a specific project")

    parser.add_argument("--copilot", action="store_true",
                        help="Use .copilot/skills/ instead of .claude/skills/")
    parser.add_argument("--unlink", action="store_true", help="Remove linked skills")
    args = parser.parse_args()

    home = Path.home()
    tool_dir = ".copilot" if args.copilot else ".claude"

    if args.global_:
        skills_dir = home / tool_dir / "skills"
    else:
        project = Path(args.project).resolve()
        if not project.is_dir():
            print(f"Project path '{args.project}' does not exist", file=sys.stderr)
            sys.exit(1)
        skills_dir = project / tool_dir / "skills"

    action = "Unlinking" if args.unlink else "Linking"
    mode = "global" if args.global_ else args.project
    print(f"{action} ai-resources ({mode}) -> {skills_dir}")

    for dir_name in SOURCE_DIRS:
        source_dir = SCRIPT_DIR / dir_name
        if not source_dir.is_dir():
            continue
        for src in sorted(source_dir.glob("*.md")):
            print(f"[{dir_name}/{src.name}]")
            if args.unlink:
                unlink(src, skills_dir)
            else:
                link(src, skills_dir)

    print("Done.")


if __name__ == "__main__":
    main()
