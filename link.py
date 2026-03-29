#!/usr/bin/env python3
"""Symlink ai-resources commands/prompts into Claude Code and GitHub Copilot CLI."""

import argparse
import os
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SOURCE_DIRS = ["commands", "prompts"]


def parse_frontmatter(path: Path) -> tuple[str, str, str]:
    """Return (name, description, body) from a markdown file with optional YAML frontmatter."""
    text = path.read_text(encoding="utf-8")

    # Try to extract frontmatter
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", text, re.DOTALL)
    if m:
        fm, body = m.group(1), m.group(2).lstrip("\n")
        name = ""
        desc = ""
        for line in fm.splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("\"'")
            elif line.startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip("\"'")
    else:
        body = text
        name = ""
        desc = ""

    # Fallbacks
    if not name:
        name = path.stem.replace("-", " ").title()
    if not desc:
        for line in body.splitlines():
            if line.startswith("#"):
                desc = re.sub(r"^#+\s*", "", line)
                break
        else:
            desc = "Custom agent"

    return name, desc, body


def link_claude(src: Path, dest_dir: Path, unlink: bool) -> None:
    slug = src.stem
    skill_dir = dest_dir / slug
    dest = skill_dir / "SKILL.md"

    if unlink:
        if dest.is_symlink():
            dest.unlink()
            print(f"  removed {dest}")
        # Clean up empty skill directory
        if skill_dir.is_dir() and not any(skill_dir.iterdir()):
            skill_dir.rmdir()
        return

    skill_dir.mkdir(parents=True, exist_ok=True)

    if dest.exists() and not dest.is_symlink():
        print(f"  skip {dest} (exists, not a symlink)")
        return

    # Remove stale symlink
    if dest.is_symlink():
        dest.unlink()

    dest.symlink_to(src)
    print(f"  claude: /{slug} -> {dest}")


def link_copilot(src: Path, dest_dir: Path, unlink: bool) -> None:
    slug = src.stem
    dest = dest_dir / f"{slug}.agent.md"

    if unlink:
        if dest.exists():
            dest.unlink()
            print(f"  removed {dest}")
        return

    dest_dir.mkdir(parents=True, exist_ok=True)

    name, desc, body = parse_frontmatter(src)
    dest.write_text(
        f'---\nname: "{name}"\ndescription: "{desc}"\n---\n\n{body}',
        encoding="utf-8",
    )
    print(f"  copilot: /agent {slug} -> {dest}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Link ai-resources into Claude Code and/or Copilot CLI"
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--global", dest="global_", action="store_true",
                        help="Install globally (~/.claude, ~/.copilot)")
    target.add_argument("--project", type=str, metavar="PATH",
                        help="Install into a specific project directory")

    tool = parser.add_mutually_exclusive_group()
    tool.add_argument("--claude", action="store_true", help="Claude Code only")
    tool.add_argument("--copilot", action="store_true", help="Copilot CLI only")

    parser.add_argument("--unlink", action="store_true", help="Remove linked files")
    args = parser.parse_args()

    # Resolve target directories
    home = Path.home()
    if args.global_:
        claude_dir = home / ".claude" / "skills"
        copilot_dir = home / ".copilot" / "agents"
    else:
        project = Path(args.project).resolve()
        if not project.is_dir():
            print(f"Project path '{args.project}' does not exist", file=sys.stderr)
            sys.exit(1)
        claude_dir = project / ".claude" / "skills"
        copilot_dir = project / ".github" / "agents"

    do_claude = args.claude or (not args.claude and not args.copilot)
    do_copilot = args.copilot or (not args.claude and not args.copilot)

    action = "Unlinking" if args.unlink else "Linking"
    mode = "global" if args.global_ else args.project
    print(f"{action} ai-resources ({mode})...")

    for dir_name in SOURCE_DIRS:
        source_dir = SCRIPT_DIR / dir_name
        if not source_dir.is_dir():
            continue
        for src in sorted(source_dir.glob("*.md")):
            print(f"[{dir_name}/{src.name}]")
            if do_claude:
                link_claude(src, claude_dir, args.unlink)
            if do_copilot:
                link_copilot(src, copilot_dir, args.unlink)

    print("Done.")


if __name__ == "__main__":
    main()
