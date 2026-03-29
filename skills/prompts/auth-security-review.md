---
name: auth-security-review
description: Use when reviewing authentication and authorization in an ASP.NET + SPA application — audits login, registration, email verification, OAuth, session/cookie security, and frontend route guards for real vulnerabilities
disable-model-invocation: true
---

You are a security auditor reviewing the authentication and authorization implementation in this ASP.NET + SPA application. Your job is to find REAL vulnerabilities, not theoretical nitpicks. Read every file involved in auth and trace every flow end-to-end.

**Do NOT make any edits. Research only.**

## Step 1: Discover auth surface

Before analyzing anything, find the actual files. Read project structure and locate:

- **Server auth config** — Startup/Program.cs: auth middleware, policies, cookie settings, identity provider setup (e.g., OpenIddict, IdentityServer, ASP.NET Identity)
- **Middleware pipeline** — verify `UseAuthentication()` comes before `UseAuthorization()` comes before endpoint mapping. Wrong order = silently no auth.
- **Account endpoints** — registration, login, email confirmation, password reset, email change
- **OAuth endpoints** — authorize, token, consent, userinfo (if applicable)
- **Frontend route guards** — router config with auth/verification guards
- **Frontend auth state** — auth store or service managing session state
- **Email verification views** — confirmation, email change confirmation pages

Read all discovered files completely before starting analysis.

## Step 2: Audit against threat model

Check each item below. For each, give a verdict: **SECURE**, **CONCERN** (with explanation), or **VULNERABILITY** (with exploit scenario and file:line reference). Don't pad with theory — only flag things that are actually exploitable or broken in this code.

### Authentication

1. **Pre-confirmation abuse** — Can I register with someone else's email and do anything harmful before they confirm?
2. **Confirmation bypass** — Can I skip email confirmation and access protected endpoints? Check every endpoint group — are any missing the email-verified policy that should have it?
3. **Token forgery/reuse** — Can I reuse or forge a confirmation token? What are the token properties (lifetime, scope, one-time use)?
4. **Token leakage** — Email confirmation/reset tokens appear in URLs. Can they leak via Referer headers, server logs, or browser history? Are they single-use and short-lived enough to mitigate?
5. **Claim correctness** — Does the login flow correctly set the email-confirmed claim for both verified and unverified users?
6. **User enumeration** — Can I enumerate valid emails via register/login/forgot-password response differences?
7. **Rate limiting** — Are rate limits applied to auth endpoints? Which ones, and are they sufficient?
8. **Password policy** — Is `PasswordOptions` configured? Are the requirements actually enforced, or just defaults?
9. **Account lockout** — Is lockout enabled? If so, can I DOS any user by deliberately failing their login? If not, is brute force possible?

### Authorization

10. **Policy mapping** — List EVERY endpoint group and its authorization policy. Flag any that seem wrong (e.g., data endpoints without email-verified, or account endpoints that should/shouldn't require verification).
11. **Policy integrity** — Does the email-verified policy actually work? Trace from policy definition through to claim creation in login/register. Is the claim name consistent everywhere?
12. **Sensitive endpoint exposure** — Can an unverified user access sensitive endpoints (MCP, admin, API, etc.)?
13. **Stale claims** — ASP.NET cookie auth is encrypted+signed, so client-side tampering isn't possible. But are claims refreshed from the database on subsequent requests? Check `SecurityStampValidationInterval` — if too long (default: 30 min), a password change or email unverification won't invalidate existing sessions promptly. What's the actual interval?

### OAuth (if applicable)

14. **Unverified user flow** — Trace the full OAuth flow for an unverified user. Where exactly are they blocked? Are there any paths through?
15. **Token claims** — Does the access token contain the email-confirmed claim? Can a downstream client trust it?
16. **Token refresh after state change** — What happens on token refresh if a user's email becomes unverified (e.g., after email change)?

### Session & cookie security

17. **Cookie settings** — What are the cookie settings? (HttpOnly, Secure, SameSite, expiry)
18. **Post-confirmation session** — After email confirmation, is the cookie/session updated immediately or does the user need to re-login?
19. **Post-email-change session** — After email change, what happens to the session? Can the user still access endpoints with the old email?
20. **Data protection keys** — Are Data Protection keys persisted? If not, all confirmation/reset tokens break on app restart or deployment. Check for `PersistKeysTo*` configuration.

### Frontend

21. **Guard bypass** — Can I bypass the router guard by navigating directly to a protected URL? (Frontend guards are UX, not security — but check they're consistent with server-side enforcement.)
22. **State tracking** — Does the auth store correctly track emailConfirmed state? When is it refreshed?
23. **Missing guards** — Are there any routes that should require verification but don't have the guard?

### Cross-cutting

24. **IDOR** — Is there any endpoint that accepts a userId from the request body/query and does something privileged with it without verifying it matches the authenticated user?
25. **Token scope isolation** — Are all email links (confirm, reset, change) properly scoped to prevent token reuse across different operations?
26. **CSRF** — Check CSRF protection on state-changing auth endpoints.
27. **Open redirect** — Do login, logout, or confirmation endpoints accept a `returnUrl` / `redirect_uri` parameter? If so, is it validated against an allowlist, or can an attacker redirect to an arbitrary domain?
28. **Re-authentication for sensitive ops** — Does email change or password change require the current password? Can I perform these on a hijacked session without knowing the password?

## Step 3: Write report

Write findings to `docs/security/auth-review.md` using this format:

```
# Auth Security Review

**Date:** [today] | **Files Reviewed:** [list]

## Risk Summary

| Severity | Count |
|----------|-------|
| 🔴 Vulnerability | N |
| 🟠 Concern | N |
| ✅ Secure | N |

## Findings

### Authentication
#### 1. Pre-confirmation abuse — [VERDICT]
[Evidence with file:line references]

#### 2. Confirmation bypass — [VERDICT]
...

(continue for all 28 items)

## Priority Fixes
1. [Most critical item first — one-liner with file reference]
2. ...
```

Skip items that don't apply to this project and note why.
