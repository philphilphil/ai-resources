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

### Claude Code

Claude Code supports two equivalent paths for custom slash commands: `.claude/commands/*.md` (legacy) and `.claude/skills/<name>/SKILL.md` (newer, supports extra features like supporting files and invocation control). Both create `/slash-commands` from plain markdown. This script uses the `commands/` path since the prompts are standalone `.md` files. ([docs](https://code.claude.com/docs/en/skills))

The script creates symlinks pointing back to this repo:

- **Global** (`--global`): symlinks into `~/.claude/commands/` — available in every project
- **Per-project** (`--project`): symlinks into `<project>/.claude/commands/` — available only in that project

A file like `prompts/code-and-security-review.md` becomes the command `/code-and-security-review`.

### Copilot CLI

Copilot CLI loads custom agents from `.agent.md` files with YAML frontmatter (`name`, `description`). Since the source files are plain markdown, the script **generates** `.agent.md` wrappers with the frontmatter extracted from each file.

- **Global** (`--global`): writes to `~/.copilot/agents/` — available in every project
- **Per-project** (`--project`): writes to `<project>/.github/agents/` — available only in that project

A file like `prompts/code-and-security-review.md` becomes the agent `code-and-security-review`, invocable via `/agent` in interactive mode or `--agent code-and-security-review` on the command line. ([docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli))

### Summary

| | Claude Code | Copilot CLI |
|---|---|---|
| Source format | Plain `.md` | Plain `.md` (converted to `.agent.md`) |
| Link method | Symlink | Generated file |
| Project dir | `.claude/commands/` | `.github/agents/` |
| Global dir | `~/.claude/commands/` | `~/.copilot/agents/` |
| Invoke | `/command-name` | `/agent` or `--agent name` |

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
