# Design

## Context

See `proposal.md` for motivation and `specs/user-auth/spec.md` for the behavior contract. The repository currently contains OpenSpec planning files but no application source, package configuration, database schema, or tests. This design therefore treats the implementation as a greenfield Next.js full-stack application and makes the minimum authentication architecture decisions needed to produce an actionable plan.

Authentication crosses the page layer, server request handling, persistent storage, and deployment configuration. The design must keep password material and session authority on the server while supporting browser-based forms and protected server-rendered pages.

## Goals / Non-Goals

**Goals:**

- Use server-side authentication checks as the authority for protected pages and actions.
- Make sessions revocable, expiring, and safe from direct access by browser scripts.
- Keep the first implementation deployable as one Next.js application backed by one relational database.
- Centralize validation and session operations so future todo APIs can reuse the authenticated user identity.

**Non-Goals:**

- Designing todo ownership or authorization beyond authenticated-versus-unauthenticated access.
- Supporting multiple devices management, global sign-out, email verification, account recovery, OAuth, or multi-factor authentication.
- Creating a separate identity service or public authentication API.

## Decisions

### Use a Next.js App Router application with server-side auth operations

Registration, sign-in, and sign-out will be implemented as Server Actions invoked by progressively enhanced forms. Protected pages will live in a route group whose server layout resolves the current session before rendering. Any protected server action or route handler must call the same session resolver rather than relying only on the layout.

This keeps credentials out of client-side state and uses Next.js same-origin protections for Server Actions. A client-only route guard was rejected because protected content or mutations could still be reached directly. Middleware-based database validation was rejected because it complicates runtime and database compatibility; middleware may perform only an optional cookie-presence redirect, never the authoritative check.

### Store users and opaque sessions in PostgreSQL through Prisma

Use PostgreSQL as the relational store and Prisma for schema migrations and typed data access. The data model will contain:

- `User`: generated ID, normalized unique email, password hash, and timestamps.
- `Session`: hashed token identifier, user ID, expiration timestamp, and creation timestamp.
- `AuthThrottle`: hashed throttle key, failure count, window start, and blocked-until timestamp.

A database-backed opaque session was chosen over a self-contained JWT because sign-out must revoke the current session immediately and server-side expiry must remain authoritative. Auth.js was considered, but custom credential validation and explicit database session semantics would still require most of this domain logic; the small local module keeps the behavior visible and testable.

### Normalize email and hash passwords with Argon2id

Trim email input, validate its syntax, and store a lowercase normalized value protected by a database unique constraint. Hash passwords with Argon2id using parameters selected from current OWASP guidance and verify them only on the server. Enforce the specified minimum length before hashing and place a conservative maximum byte length on input to prevent resource abuse.

Argon2id was selected over general-purpose hashes because it is memory-hard and intended for password storage. Bcrypt was considered as a mature alternative, but its input handling and lower resistance to specialized hardware make Argon2id preferable for a greenfield implementation.

### Use hashed random session tokens in secure cookies

Generate session tokens from at least 256 bits of cryptographically secure randomness. Store only a SHA-256 digest of each token in the database and place the raw token in a cookie configured with `HttpOnly`, `SameSite=Lax`, `Path=/`, and `Secure` outside local development. Sessions will expire after 30 days; every authenticated request checks the database expiry. Creating a session and setting its cookie occurs only after registration or credential verification succeeds.

Hashing tokens reduces the impact of a session-table disclosure. Database lookup on protected requests is an accepted trade-off for revocation. A 30-day lifetime gives the requested persistence while bounding exposure; rolling extension is excluded from the first version to keep expiry deterministic.

### Validate redirects and authentication form requests on the server

An optional return destination will be accepted only when it is a relative application path beginning with a single `/`; protocol-relative and absolute URLs will be discarded. Authentication mutations will remain POST-only Server Actions and retain Next.js Origin-versus-Host validation. Cookie `SameSite=Lax` adds defense in depth, but it is not the sole CSRF control.

### Apply persistent fixed-window throttling to failed sign-ins

Before password verification, derive non-reversible throttle keys from the normalized email candidate and request IP using an application secret. Track failures in the database over a 15-minute window and block further attempts for 15 minutes after five failures for either key. Successful sign-in clears the account-key failure state. Responses use the same generic error and broadly similar work regardless of whether an account exists; a fixed dummy password hash will be verified for unknown emails.

Database-backed throttling works across processes without another infrastructure service. A managed rate-limit service would scale better and can replace this module later behind the same interface. In-memory counters were rejected because they fail under horizontal scaling and reset on deployment.

### Separate domain errors from form presentation

Shared schemas will validate credentials on the server and return field errors only for registration format or password policy failures. Sign-in failures and throttle blocks will return a generic form-level authentication error. Logs may record internal categories but must not include passwords, raw session tokens, or full credential payloads.

## Risks / Trade-offs

- [Database lookup on each protected request adds latency] -> Keep session lookup indexed by token digest and centralize it so request-level deduplication can be added if measurement justifies it.
- [Argon2 parameters can overload constrained hosting] -> Benchmark in the deployment environment and keep parameters configurable while maintaining the selected security floor.
- [IP-based throttling can affect users behind shared networks] -> Combine IP and account-derived limits, use a short block window, and retain generic messaging.
- [Email addresses are accepted without verification] -> Clearly treat accounts as unverified and avoid email-dependent trust decisions until a later verification capability is added.
- [Greenfield assumptions may differ from the eventual application scaffold] -> Establish the listed stack and module boundaries before feature implementation; revise this change before applying if an existing application is introduced.

## Migration Plan

1. Scaffold the Next.js application and environment validation without exposing protected routes.
2. Provision PostgreSQL and apply the initial user, session, and throttle schema migration.
3. Deploy authentication server logic and pages together, then enable the protected route group.
4. Verify registration, session persistence, expiry, revocation, CSRF rejection, redirect safety, and throttling in the deployed environment.

Because there is no existing application data, no account backfill is required. Rollback consists of removing the authentication routes and protection before reverting the schema migration; database records should be retained until rollback is confirmed to avoid accidental account loss during a redeploy.
