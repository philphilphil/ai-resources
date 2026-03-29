---
name: Maintenance Audit
description: Audit project docs and package inventory for drift against the actual codebase
---

# Project Maintenance Audit

Audit the current state of the project and update documentation that has drifted. Read every source of truth before changing anything — do not guess.

## 1. Update Package Inventory

Find or create a package inventory document (e.g. `docs/packages.md`). Regenerate it by reading the actual dependency manifests:

- **Language-level** — scan for `package.json`, `requirements.txt`, `Pipfile`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `*.csproj`, `Gemfile`, `Package.swift`, `build.gradle`, `pom.xml`, or equivalent
- **Infrastructure** — scan `docker-compose*.yml`, `Dockerfile*`, `.github/workflows/`, CI configs for image versions and tool versions

Group dependencies by subproject or layer. Update the generated date to today.

## 2. Update Project Documentation

Read the actual codebase and compare against the main project docs (CLAUDE.md, README.md, AGENTS.md, or equivalent). Fix anything that has drifted. Common drift areas:

### Tech Stack
- Read dependency manifests for framework and language versions
- Read Docker/CI configs for runtime and database versions

### Architecture
- Verify the documented folder structure still matches reality
- Check for new top-level directories or modules that aren't documented

### API Routes / Endpoints
- Grep for route definitions (framework-specific: `MapGet`/`MapPost`, `app.get`/`app.post`, `@app.route`, `router.get`, etc.)
- Verify every route group is documented; add missing ones, remove stale ones

### Features
- Skim frontend routes/views or CLI commands for new or removed features
- Verify the feature list in docs matches what actually exists

### Build & Run / Ports / Environment Variables
- Verify documented ports, URLs, connection strings, and env vars match the actual config files (`.env.example`, `appsettings.*`, `docker-compose.yml`, etc.)

### Everything Else
- Read through every remaining section and verify it still reflects reality
- Don't add new sections unless something major is undocumented
- Don't remove sections that are still accurate

## Rules

- Only change lines that are actually wrong or missing. Don't rewrite sections that are accurate.
- If you're unsure whether something has changed, read the source file — don't guess.
- Keep docs concise. Match the existing tone and level of detail.
- Commit the changes when done with a descriptive message.
