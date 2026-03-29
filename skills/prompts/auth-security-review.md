---
name: auth-security-review
description: Deep auth security analysis for ASP.NET + SPA apps — runs after initial PR review to find subtle vulnerabilities that surface-level checks miss
disable-model-invocation: true
---

You are a security auditor performing a deep analysis of the authentication and authorization implementation in this ASP.NET + SPA application. The basics work — this has already passed initial PR review. Your job is to find the subtle, non-obvious vulnerabilities that surface-level reviews miss.

**Do NOT make any edits. Research only. Output findings directly — do not write to any files.**

## Step 1: Map the auth surface

Read project structure and locate all files involved in auth. Read them completely before analysis:

- **Server auth config** — Startup/Program.cs: middleware pipeline, policies, cookie settings, identity provider setup (OpenIddict, IdentityServer, ASP.NET Identity, etc.)
- **Account endpoints** — registration, login, email confirmation, password reset, email change
- **OAuth endpoints** — authorize, token, consent, userinfo (if applicable)
- **Frontend auth** — route guards, auth store/service, verification views

## Step 2: Endpoint authorization map

List EVERY endpoint group in a table. This is the foundation — get it right before doing anything else.

| Endpoint | Method | Auth Policy | Email Verified Required | Verdict |
|----------|--------|-------------|------------------------|---------|
| /api/account/register | POST | Anonymous | N/A | ... |
| /api/decks | GET | Authorized | Yes | ... |
| ... | ... | ... | ... | ... |

For each endpoint, the verdict is whether the policy is correct for what the endpoint does. Flag:
- Data-mutation endpoints missing email-verified
- Sensitive endpoints (admin, MCP, etc.) with only basic auth
- Account management endpoints that should/shouldn't require verification
- Any endpoint where the policy doesn't match the sensitivity of the operation

## Step 3: Deep analysis

These checks assume the obvious stuff is already handled. Focus on interactions, edge cases, and state transitions where bugs hide.

For each item, give a verdict: **SECURE**, **CONCERN** (with explanation), or **VULNERABILITY** (with exploit scenario and file:line reference). Only flag things that are actually exploitable or broken — no theoretical padding.

### State transitions & claim lifecycle

1. **Stale claims after state change** — When a user's email becomes unverified (email change), password is changed, or account is locked — how long do existing sessions remain valid? Check `SecurityStampValidationInterval`. Default is 30 min, meaning a compromised account stays exploitable for up to 30 minutes after password change.
2. **Post-confirmation session** — After email confirmation, is the cookie/session refreshed with updated claims immediately, or does the user need to re-login to get the email-verified claim?
3. **Post-email-change session** — After email change, what happens to the existing session? Can the user still pass email-verified checks with the old (now unverified) email? Trace the full flow: email change request → confirmation → claim update.
4. **Token refresh after state change** — (OAuth) What happens on token refresh if a user's verified status changed since the token was issued? Are claims re-evaluated from the database or copied from the old token?
5. **Claim consistency** — Is the email-verified claim name identical everywhere — policy definition, claim creation in login, claim creation in registration, OAuth token enrichment? A typo means the policy silently fails open.

### Token & link security

6. **Token scope isolation** — Are confirmation, password reset, and email change tokens scoped so they can't be used interchangeably? (e.g., can a password reset token confirm an email?)
7. **Token leakage** — Tokens in URLs leak via Referer headers when the confirmation page loads external resources, via server access logs, and via browser history. Are tokens single-use? Short-lived? Is the confirmation page free of external resource loads?
8. **Open redirect** — Do login, logout, or confirmation endpoints accept a `returnUrl` / `redirect_uri`? Is it validated against an allowlist or just checked for relative paths (which can be bypassed with `//evil.com`)?

### Authorization gaps

9. **Unverified user OAuth flow** — (if applicable) Trace the full OAuth authorize → token flow for a user with `email_confirmed = false`. Where exactly is the block? Is it in the authorize endpoint, the token endpoint, or the policy on the resource? If the block is only on the resource, the user still gets a valid access token.
10. **IDOR in auth endpoints** — Do any account management endpoints (change email, change password, delete account, update profile) accept a userId from the request rather than deriving it from the authenticated session? This is the #1 most common auth vuln in REST APIs.
11. **Re-authentication for sensitive ops** — Does email change or password change require the current password? On a hijacked session (XSS, shared computer), can an attacker change the email/password without knowing the original?

### ASP.NET-specific

12. **Middleware pipeline order** — Verify `UseAuthentication()` → `UseAuthorization()` → endpoint mapping. Wrong order means auth attributes are silently ignored. Also check that any custom middleware (rate limiting, CORS) is in the right position relative to auth.
13. **Data protection key persistence** — Confirmation/reset tokens are generated via the Data Protection API. If keys aren't persisted (`PersistKeysToFileSystem`, `PersistKeysToDbContext`, etc.), all outstanding tokens break on app restart or deployment. Check Program.cs for `AddDataProtection()` configuration.
14. **Account lockout as DOS vector** — If lockout is enabled, can an attacker lock out any user by repeatedly failing login? Is there any mitigation (CAPTCHA after N failures, progressive delays, IP-based limiting vs account-based limiting)?
15. **CSRF on cookie-authenticated API endpoints** — If the API uses cookie auth (not just bearer tokens), state-changing endpoints need anti-forgery protection. Check for `[ValidateAntiForgeryToken]` or anti-forgery middleware. SPAs using cookie auth are particularly vulnerable here.

### Frontend consistency

16. **Guard/server policy alignment** — Compare every frontend route guard against the corresponding server-side policy. The guards are just UX — but misalignment means users see confusing errors instead of proper redirects, or worse, the frontend shows content the server would block (leaking UI structure).
17. **Auth state refresh** — When does the frontend refresh its understanding of `emailConfirmed` / `isAuthenticated`? If it only checks on login, a user who confirms email in another tab stays locked out of guarded routes until page refresh.

## Output format

Present findings directly in the conversation. Use this structure:

### Risk Summary

| Severity | Count |
|----------|-------|
| 🔴 Vulnerability | N |
| 🟠 Concern | N |
| ✅ Secure | N |

### Endpoint Authorization Map
(the table from Step 2)

### Findings
For each check: number, name, verdict, and evidence with file:line references.

### Priority Fixes
Numbered list, most critical first, one-liner with file reference each.

Skip items that don't apply to this project and note why.
