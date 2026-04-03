---
applyTo: '**/Dockerfile,**/Dockerfile.*,**/*.dockerfile,**/docker-compose*.yml,**/docker-compose*.yaml,**/compose*.yml,**/compose*.yaml'
description: 'Best practices for optimized, secure Docker images and container configuration.'
---

# Containerization & Docker Best Practices

## Dockerfile

- **Multi-stage builds** — use builder stages for compilation; copy only final artifacts into a minimal runtime image
- **Pin base images** — use specific versioned tags (e.g. `node:20-alpine`), never `latest`
- **Minimal base image** — prefer `alpine`, `slim`, or distroless variants for the final stage
- **Layer optimization** — combine `RUN` commands with `&&`; delete temp files in the same layer they are created
- **`.dockerignore`** — exclude `node_modules`, `.git`, build artifacts, secrets, and anything not needed in the image
- **Non-root user** — create and switch to a dedicated low-privilege user (`USER app`); never run as root in production
- **`COPY` specificity** — copy only what is needed; avoid `COPY . .` in final stages
- **`HEALTHCHECK`** — define a health check for all production images
- **`CMD` vs `ENTRYPOINT`** — use `ENTRYPOINT` for the executable, `CMD` for default arguments; prefer exec form (`["cmd", "arg"]`)
- **Secrets** — inject via environment variables or `--secret` mounts at build time; never bake into image layers
- **`EXPOSE`** — document the port the container listens on; this is metadata, not a firewall rule

## Security

- Run containers as non-root; verify with `docker inspect` that `User` is set
- Use read-only filesystems where possible (`--read-only`); mount writable tmpfs only for dirs that need it
- Drop unnecessary Linux capabilities (`--cap-drop ALL`, add back only what is needed)
- Scan images for vulnerabilities with Trivy or Grype in CI; fail on critical findings
- Lint Dockerfiles with Hadolint in CI
- Never store secrets, tokens, or credentials in image layers; they persist in history even after `RUN rm`

## docker-compose

- Pin image versions for all services — never use `latest`
- Set resource limits (`cpus`, `mem_limit`) to prevent a single service from starving others
- Use `depends_on` with `condition: service_healthy` for correct startup ordering
- Prefer named volumes over bind mounts for portable, cross-platform data persistence
- Use `.env` files for environment-specific configuration; never commit secrets to the repo

## Troubleshooting

- **Large image** — run `docker history <image>` to find fat layers; check for missing `.dockerignore` and uncleaned temp files
- **Slow build** — order instructions from least to most frequently changed so the cache is reused; verify cache hits with `--progress=plain`
- **Crash on start** — check `CMD`/`ENTRYPOINT` syntax, review `docker logs <container>`, verify all runtime deps are present in the final stage
- **Permission error inside container** — ensure the non-root user has read/write access to required paths and mounted volumes
