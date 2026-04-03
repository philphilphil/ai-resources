---
applyTo: '.github/workflows/*.yml,.github/workflows/*.yaml'
description: 'Best practices for secure, efficient GitHub Actions CI/CD workflows.'
---

# GitHub Actions Best Practices

## Structure

- Give workflows and jobs clear, descriptive `name` fields
- Use granular `on` triggers with branch/path filters; use `workflow_dispatch` for manual runs
- Set `concurrency` groups to cancel in-progress runs when new commits are pushed
- Set `permissions` at the workflow level to least privilege (`contents: read`) and override per job as needed
- Set `timeout-minutes` on long-running jobs to prevent hung workflows
- Extract common patterns into reusable workflows (`workflow_call`) to reduce duplication

## Security

- **Pin actions to full commit SHA** — `uses: actions/checkout@<sha> # v4.x.x`; tags and branches are mutable and can be silently redirected
- **Secrets only via `secrets` context** — `${{ secrets.MY_SECRET }}`; never hardcode or log secrets
- **Least-privilege `GITHUB_TOKEN`** — explicitly define `permissions`; default to `read-only` and add write scopes only where required
- **OIDC for cloud auth** — use OIDC federation instead of long-lived service account credentials stored as secrets
- Integrate `actions/dependency-review-action` on pull requests to catch vulnerable dependencies
- Integrate SAST (CodeQL or equivalent) with critical findings blocking merge
- Restrict self-hosted runners to private repos; harden runner environments; isolate from production

## Caching and Performance

- Cache package manager dependencies with `actions/cache` keyed on `hashFiles('<lockfile>')`
- Use `fetch-depth: 1` on `actions/checkout` unless full Git history is required
- Parallelize across environments/versions with `strategy.matrix`
- Transfer data between jobs via `outputs` or `actions/upload-artifact` / `actions/download-artifact`

## Testing and Deployment

- Structure jobs as distinct phases: `lint → build → test → deploy`
- Use `needs` to enforce execution order; use `if` conditions for environment-specific steps
- Deploy to a staging environment before production; protect production with `environment` rules and required reviewers
- Run post-deploy health checks or smoke tests to validate each deployment
- Define and test a rollback strategy (e.g. re-run previous workflow, `kubectl rollout undo`, image tag revert)
- Publish test results as artifacts and integrate with GitHub Checks for visibility

## Common Issues

- **Workflow not triggering** — verify the `on` trigger and branch/path filter exactly matches the ref
- **Permission denied** — check the `permissions` block; ensure the job has the needed scope (e.g. `pull-requests: write`)
- **Cache miss** — verify the cache `key` is deterministic and a `restore-keys` fallback is set
- **Flaky tests** — pin runner OS versions; set `timeout-minutes`; isolate services with `services:` containers
