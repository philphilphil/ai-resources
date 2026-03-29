---
name: review-skill
description: Review a skill file for quality, completeness, and adherence to the Agent Skills standard
---

Review the skill at the path provided in $ARGUMENTS. If no path is given, ask which skill to review.

Read the skill file, then evaluate it against every criterion below. For each criterion, report pass/fail with a brief explanation. End with a summary of what to fix, ordered by importance.

## Frontmatter

- **name** — present, lowercase with hyphens, max 64 characters, matches directory name
- **description** — present, front-loads the key use case, under 250 characters, specific enough for auto-invocation to work correctly
- **invocation control** — if the skill has side effects (writes files, creates PRs, deploys, sends messages), it should set `disable-model-invocation: true`. If it's background knowledge not useful as a command, it should set `user-invocable: false`. If neither applies, default is fine.
- **allowed-tools** — if the skill only needs read access, it should restrict tools. If it runs arbitrary commands, consider whether restrictions make sense.
- **No unnecessary fields** — don't set fields to their defaults (e.g. `user-invocable: true` is redundant)

## Description quality

- Does the description explain **what** the skill does and **when** to use it?
- Would Claude correctly auto-invoke this skill based on the description alone?
- Would Claude correctly avoid invoking it when irrelevant?
- Is it free of vague terms like "helps with" or "assists in"?

## Instructions

- **Clarity** — could someone unfamiliar with the skill understand what it does from reading the instructions?
- **Imperative form** — uses verb-first instructions ("Read the file", "Run the tests"), not second person ("You should read the file")
- **Actionable** — every instruction is concrete and executable, not vague guidance
- **Scope** — the skill does one thing well rather than trying to cover too much
- **No ambiguity** — would two different AI models interpret the instructions the same way?

## Structure

- **Length** — SKILL.md should be under 500 lines. If longer, detailed reference material should be moved to separate files.
- **Organization** — logical flow, sections where helpful, not a wall of text
- **Examples** — includes examples or templates where the expected output format matters
- **Edge cases** — handles "what if this doesn't apply" gracefully (skip and note why, rather than fail)

## Portability

- **Tool-agnostic** — avoids Claude Code-specific features (like TeamCreate, specific tool names) unless the skill is intentionally Claude Code-only. Skills following the Agent Skills standard should work across tools.
- **Project-agnostic** — doesn't hardcode paths, credentials, project-specific details (unless the skill is intentionally project-specific)
- **No assumptions** — reads project docs/structure first rather than assuming a specific tech stack or layout

## Output

Start with a one-line verdict: **Good**, **Needs work**, or **Major issues**.

Then list each criterion as:
- pass/fail with brief reasoning

End with **Recommended fixes** ordered by impact — what would improve this skill the most.
