# ai-resources

Reusable prompts and commands for AI coding assistants. Works with both [Claude Code](https://claude.ai/code) and [GitHub Copilot CLI](https://github.com/features/copilot/cli) via the shared [Agent Skills](https://agentskills.io) standard.

## Structure

```
ai-resources/
├── skills/                 # Linked into AI tools via link.py
│   ├── commands/           # One-liner shortcuts
│   │   └── pr.md
│   └── prompts/            # Detailed multi-step playbooks
│       ├── architecture-blueprint-generator.md
│       ├── code-review.md
│       ├── frontend-tests.md
│       ├── maintenance-audit.md
│       ├── multi-stage-dockerfile.md
│       ├── review-skill.md
│       ├── secret-scanning.md
│       ├── security-review.md
│       └── web-coder.md
├── instructions/           # Technology-specific coding instructions (.instructions.md)
│   ├── containerization-docker-best-practices.instructions.md
│   ├── github-actions-ci-cd-best-practices.instructions.md
│   ├── go.instructions.md
│   ├── markdown.instructions.md
│   ├── nextjs.instructions.md
│   ├── performance-optimization.instructions.md
│   ├── react-typescript.instructions.md
│   └── security-and-owasp.instructions.md
├── agent/                  # Standalone prompt runner (Claude CLI wrapper)
│   ├── agent               # Bash script — parses frontmatter, runs prompts, writes output
│   └── prompts/            # Prompts for the agent runner
│       ├── system.md       # Shared system prompt (formatting rules)
│       ├── daily_news.md   # Daily news briefing
│       └── music_news.md   # Classical music & opera scout
└── link.py
```

- **skills/** — everything here gets symlinked as Agent Skills. Both `commands/` and `prompts/` are linked; the split is just organizational (short triggers vs detailed playbooks).
- **instructions/** — technology-specific `.instructions.md` files. Each file targets a specific stack via an `applyTo` glob in its frontmatter. When linked into a project, they land in `.github/instructions/` where VS Code and Copilot auto-inject them based on which files you're editing. Claude Code gets them as `@path` imports in `CLAUDE.md`.
- **agent/** — a standalone prompt runner that calls `claude` CLI, injects context from previous outputs, and writes results to files (e.g. an Obsidian vault). Prompts use YAML frontmatter for config (`output`, `model`, `tools`, `context`, `static`). Run with `./agent run <name>` or `./agent run --all`.

## Usage

`link.py` handles two things: **skills** (Agent Skills for Claude Code / Copilot CLI) and **instructions** (coding guidelines auto-injected per file type).

### Link globally (available in all projects)

```sh
python3 link.py --global
```

Skills are symlinked into `~/.claude/skills/`. Instructions are injected as `@path` imports into `~/.claude/CLAUDE.md` so Claude Code picks them up globally. (No global `.github/instructions/` — that's per-project for Copilot/VS Code.)

### Link into a specific project

```sh
python3 link.py --project ~/Projects/my-app
```

Skills are symlinked into `<project>/.claude/skills/`. Instructions are symlinked into `<project>/.github/instructions/` (for Copilot/VS Code auto-injection) **and** injected as `@path` imports into `<project>/CLAUDE.md` (for Claude Code).

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

Removes skill symlinks and strips the instruction import block from `CLAUDE.md`. The `.github/instructions/` symlinks are also removed for project-scoped unlinks.

## How it works

### Skills

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

### Instructions

Each `.instructions.md` file has an `applyTo` glob in its YAML frontmatter. When linked into a project:

- **VS Code / Copilot** — the file is symlinked into `.github/instructions/`. VS Code and Copilot read this directory and automatically inject matching instruction files based on the `applyTo` glob for the file you're editing.
- **Claude Code** — an `@absolute/path` import is written into `CLAUDE.md` (project root for `--project`, `~/.claude/CLAUDE.md` for `--global`). Claude Code reads all imports at startup and includes them in its context.

The import block is wrapped in HTML comment markers so re-running `link.py` can update it in place without duplicating entries.

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

## Adding new instructions

1. Add a `.instructions.md` file to `instructions/`
2. Include YAML frontmatter with an `applyTo` glob targeting the relevant file types:
   ```markdown
   ---
   applyTo: "**/*.ts,**/*.tsx"
   ---

   The instruction content...
   ```
3. Re-run `python3 link.py` to pick up new files — the symlink and `CLAUDE.md` import block are updated automatically.
