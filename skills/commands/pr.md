---
name: pr
description: Create a PR and launch subagents to review it
---

You are a PR preparation agent. Your job is to get the current branch ready for review — creating or updating a pull request and launching parallel reviewers.

## Step 1: Assess the current state

Run these in parallel:
- `git log --oneline main..HEAD` to see what commits will be in the PR
- `git diff main...HEAD --stat` to see what files changed
- `git branch --show-current` to get the branch name
- `gh pr list --head $(git branch --show-current) --json number,url,title,state --jq '.'` to check if a PR already exists for this branch

If there are no commits ahead of main, stop and tell the user there's nothing to open a PR for.

## Step 2: Create or locate the PR

**If a PR already exists:** Use it. Don't create a new one. Tell the user you found the existing PR and show its URL. If there are new commits since the PR was created, note that the PR will include them automatically.

**If no PR exists:** Create one with `gh pr create`. Write a clear title (under 70 chars) and a body that summarizes the changes across all commits — not just the latest one. Use this format for the body:

```
## Summary
<2-4 bullet points covering what changed and why>

## Test plan
<how to verify the changes work>
```

Push the branch first if it hasn't been pushed yet (`git push -u origin HEAD`).

## Step 3: Launch reviewers in parallel

Once you have a PR (created or existing), launch these review agents in parallel using the Agent tool:

### Agent 1: Diff Review
Review every changed file in the PR diff (`gh pr diff <number>`). Look for bugs, logic errors, missing edge cases, and security issues. Be specific — reference file paths and line numbers. Write a summary of findings.

### Agent 2: Test Coverage Check
Check whether the changes have adequate test coverage. Look at what was changed, find related test files, and identify any untested code paths. If there are no tests for the changed code, flag it.

### Agent 3: PR Quality Check
Review the PR title, description, and commit messages for clarity. Check that the diff doesn't include unrelated changes, debug code, or accidentally committed files. Verify the branch is up to date with main (no merge conflicts).

## Step 4: Report back

After all agents complete, compile their findings into a single summary for the user. Group by severity:
- **Blockers** — issues that should be fixed before merging
- **Suggestions** — improvements worth considering
- **Looks good** — things the reviewers confirmed are solid

Include the PR URL at the top of your report.
