# ai-resources

Reusable prompts and commands for AI coding assistants. Works with both [Claude Code](https://claude.ai/code) and [GitHub Copilot CLI](https://github.com/features/copilot/cli) via the shared [Agent Skills](https://agentskills.io) standard.

## Structure

```
ai-resources/
├── skills/                 # Linked into AI tools via link.py
│   ├── commands/           # One-liner shortcuts
│   │   └── pr.md
│   └── prompts/            # Detailed multi-step playbooks
│       ├── security-review.md
│       ├── frontend-tests.md
│       └── maintenance-audit.md
├── agent/                  # Standalone prompt runner (Claude CLI wrapper)
│   ├── agent               # Bash script — parses frontmatter, runs prompts, writes output
│   └── prompts/            # Prompts for the agent runner
│       ├── system.md       # Shared system prompt (formatting rules)
│       ├── daily_news.md   # Daily news briefing
│       └── music_news.md   # Classical music & opera scout
├── prompts/                # Standalone prompts (not linked, just a collection)
└── link.py
```

- **skills/** — everything here gets symlinked as Agent Skills. Both `commands/` and `prompts/` are linked; the split is just organizational (short triggers vs detailed playbooks).
- **agent/** — a standalone prompt runner that calls `claude` CLI, injects context from previous outputs, and writes results to files (e.g. an Obsidian vault). Prompts use YAML frontmatter for config (`output`, `model`, `tools`, `context`, `static`). Run with `./agent run <name>` or `./agent run --all`.
- **prompts/** (root) — reference prompts you copy-paste or feed manually. Not linked into any tool.

## Usage

### Link globally (available in all projects)

```sh
python3 link.py --global
```

### Link into a specific project

```sh
python3 link.py --project ~/Projects/my-app
```

### Copilot-only projects

By default, skills are linked into `.claude/skills/` (which both tools read). For projects that only use Copilot CLI, use `--copilot` to write to `.copilot/skills/` instead:

```sh
python3 link.py --global --copilot
python3 link.py --project ~/Projects/my-app --copilot
```

### Unlink

```sh
python3 link.py --global --unlink
python3 link.py --project ~/Projects/my-app --unlink
```

## How it works

Both Claude Code and Copilot CLI support the [Agent Skills](https://agentskills.io) open standard. Skills live in `.claude/skills/<name>/SKILL.md` — a directory per skill with a `SKILL.md` entrypoint containing YAML frontmatter (`name`, `description`) and markdown instructions.

Both tools look for skills in these locations:

| Scope | Claude Code | Copilot CLI |
|---|---|---|
| **Global** | `~/.claude/skills/<name>/SKILL.md` | `~/.claude/skills/` or `~/.copilot/skills/` |
| **Per-project** | `<project>/.claude/skills/<name>/SKILL.md` | `<project>/.claude/skills/` or `<project>/.copilot/skills/` |

Copilot CLI reads from both `.claude/skills/` and `.copilot/skills/`. The default writes to `.claude/skills/` so both tools pick it up. Use `--copilot` for Copilot-only projects.

The script symlinks each source file as a `SKILL.md` inside the appropriate skill directory. Since it's the same format and path, one symlink works for both tools.

**Invoking skills:**

| Claude Code | Copilot CLI |
|---|---|
| `/skill-name` | `/skills` to browse, or reference by name in prompt |
| Auto-invoked when description matches context | Auto-invoked when description matches prompt |

Docs: [Claude Code skills](https://code.claude.com/docs/en/skills), [Copilot CLI skills](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-skills)

## Adding new skills

1. Add a `.md` file to `skills/commands/` (short triggers) or `skills/prompts/` (detailed playbooks)
2. Include YAML frontmatter so both tools know when to activate it:
   ```markdown
   ---
   name: my-skill
   description: One-line description of what this does
   ---

   The actual prompt content...
   ```
   If no frontmatter is present, skills still work but won't auto-activate.
3. Re-run `python3 link.py` to pick up new files.

For standalone prompts that don't need tool integration, just add them to `prompts/` at the root.
