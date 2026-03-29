# ai-resources

Reusable prompts and commands for AI coding assistants. Works with both [Claude Code](https://claude.ai/code) and [GitHub Copilot CLI](https://github.com/features/copilot/cli).

## Structure

```
ai-resources/
├── commands/           # Slash commands (short, action-oriented)
│   └── pr.md
├── prompts/            # Longer prompts (multi-step workflows)
│   ├── code-and-security-review.md
│   ├── frontend-test-instructions.md
│   └── maintenance-audit.md
└── link.py             # Symlinks everything into the right places
```

## Usage

### Link globally (available in all projects)

```sh
python3 link.py --global              # both tools
python3 link.py --global --claude     # Claude Code only
python3 link.py --global --copilot    # Copilot CLI only
```

### Link into a specific project

```sh
python3 link.py --project ~/Projects/my-app
python3 link.py --project ~/Projects/my-app --claude
python3 link.py --project ~/Projects/my-app --copilot
```

### Unlink

```sh
python3 link.py --global --unlink
python3 link.py --project ~/Projects/my-app --unlink
```

## How it works

| | Claude Code | Copilot CLI |
|---|---|---|
| Format | Plain markdown | `.agent.md` with YAML frontmatter |
| Project dir | `.claude/commands/` | `.github/agents/` |
| Global dir | `~/.claude/commands/` | `~/.copilot/agents/` |
| Invoke | `/command-name` | `/agent` or `--agent name` |

The script symlinks files directly for Claude Code (it reads plain `.md`). For Copilot CLI, it generates `.agent.md` wrapper files that reference the source markdown, since Copilot expects YAML frontmatter with `name` and `description`.

## Adding new commands/prompts

1. Add a `.md` file to `commands/` or `prompts/`
2. Use a YAML frontmatter block so the link script can extract metadata:
   ```markdown
   ---
   name: My Command
   description: One-line description of what this does
   ---

   The actual prompt content...
   ```
   If no frontmatter is present, the script derives the name from the filename.
3. Re-run `python3 link.py` to pick up new files.

## Sources

- [Claude Code custom commands](https://code.claude.com/docs/en/skills)
- [Copilot CLI custom agents](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli)
- [Copilot CLI custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions)
