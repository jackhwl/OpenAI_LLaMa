# Tasks

## 1. Application and Database Foundation

- [ ] 1.1 Scaffold a TypeScript Next.js App Router application with linting and a test runner, and verify the default application builds and the test command exits successfully
- [ ] 1.2 Add Prisma, PostgreSQL configuration, Argon2id support, and server-side validation dependencies, and verify dependency installation and environment validation succeed with documented required variables
- [ ] 1.3 Define the `User`, `Session`, and `AuthThrottle` models with the required unique constraints, indexes, relations, and timestamps, and verify Prisma schema validation and migration generation succeed
- [ ] 1.4 Apply the initial database migration to a test database and verify the generated tables, unique normalized-email constraint, and session-token index are present

## 2. Authentication Domain

- [ ] 2.1 Implement shared credential validation and email normalization with minimum and maximum password limits, and verify unit tests cover valid input, malformed email, short password, oversized password, and case normalization
- [ ] 2.2 Implement Argon2id password hashing and verification with production-safe parameters plus a fixed dummy hash for unknown users, and verify tests accept the correct password and reject incorrect or malformed hashes
- [ ] 2.3 Implement 256-bit opaque session creation, SHA-256 token storage, 30-day expiry, secure cookie options, lookup, and invalidation, and verify unit tests cover valid, expired, revoked, and tampered sessions without persisting raw tokens
- [ ] 2.4 Implement database-backed account and IP throttling with five failures per 15-minute window, generic blocked responses, and success reset behavior, and verify deterministic tests cover threshold, expiry, both key types, and reset

## 3. Authentication Operations

- [ ] 3.1 Implement the registration Server Action with validation, normalized-email uniqueness handling, password hashing, atomic account/session creation, and safe redirect selection, and verify integration tests cover success, invalid fields, case-insensitive duplicates, and concurrent duplicate submissions
- [ ] 3.2 Implement the sign-in Server Action with throttling, generic credential errors, dummy-hash verification for unknown emails, session creation, and safe return paths, and verify integration tests cover success, wrong password, unknown email, blocked attempts, and external redirect rejection
- [ ] 3.3 Implement the sign-out Server Action to invalidate the current database session and clear its cookie, and verify an integration test proves the old token cannot access protected content afterward
- [ ] 3.4 Enforce same-origin POST handling for all authentication mutations and verify request tests reject mismatched Origin or Host values without changing account or session state

## 4. Pages and Access Control

- [ ] 4.1 Build progressively enhanced registration and sign-in pages with accessible labels, pending states, field-level registration errors, and generic sign-in errors, and verify component or browser tests cover keyboard submission and error rendering
- [ ] 4.2 Add a protected route group with a server-side session guard and a placeholder authenticated application page, and verify request tests redirect anonymous or invalid sessions while rendering the page for a valid session
- [ ] 4.3 Add reusable authentication enforcement for protected Server Actions and route handlers, and verify direct requests cannot bypass the page layout guard
- [ ] 4.4 Add the authenticated sign-out control and safe post-authentication navigation, and verify browser tests cover registration-to-app, sign-in return path, reload persistence, and sign-out-to-sign-in flows

## 5. Security and Delivery Verification

- [ ] 5.1 Add tests that inspect session cookie flags in development and production modes, and verify `HttpOnly`, `SameSite=Lax`, `Path=/`, expiry, and production `Secure` behavior
- [ ] 5.2 Add sanitization assertions for authentication logs and error responses, and verify tests demonstrate that passwords, raw session tokens, and account-existence details are not exposed
- [ ] 5.3 Run formatting, linting, type checking, unit tests, integration tests, production build, and database migration checks, and verify every command completes successfully in a clean environment
- [ ] 5.4 Document local database setup, authentication environment variables, migration commands, and the excluded email-verification, recovery, and OAuth features, and verify a fresh setup can follow the documentation to reach the registration page
