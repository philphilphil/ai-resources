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

Claude Code loads skills from `.claude/skills/<name>/SKILL.md`. Each skill is a directory with a `SKILL.md` entrypoint. Skills support YAML frontmatter (`name`, `description`) which Claude uses to decide when to auto-invoke them, and you can always invoke manually with `/skill-name`. ([docs](https://code.claude.com/docs/en/skills))

The script symlinks each source file as a `SKILL.md` inside a skill directory:

- **Global** (`--global`): symlinks into `~/.claude/skills/<name>/SKILL.md` — available in every project
- **Per-project** (`--project`): symlinks into `<project>/.claude/skills/<name>/SKILL.md` — available only in that project

A file like `prompts/code-and-security-review.md` becomes `/code-and-security-review`.

### Copilot CLI

Copilot CLI loads custom agents from `.agent.md` files with YAML frontmatter (`name`, `description`). Since the source files are plain markdown, the script **generates** `.agent.md` wrappers with the frontmatter extracted from each file.

- **Global** (`--global`): writes to `~/.copilot/agents/` — available in every project
- **Per-project** (`--project`): writes to `<project>/.github/agents/` — available only in that project

A file like `prompts/code-and-security-review.md` becomes the agent `code-and-security-review`, invocable via `/agent` in interactive mode or `--agent code-and-security-review` on the command line. ([docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli))

### Summary

| | Claude Code | Copilot CLI |
|---|---|---|
| Source format | Plain `.md` (as `SKILL.md`) | Plain `.md` (converted to `.agent.md`) |
| Link method | Symlink | Generated file |
| Project dir | `.claude/skills/<name>/SKILL.md` | `.github/agents/` |
| Global dir | `~/.claude/skills/<name>/SKILL.md` | `~/.copilot/agents/` |
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
