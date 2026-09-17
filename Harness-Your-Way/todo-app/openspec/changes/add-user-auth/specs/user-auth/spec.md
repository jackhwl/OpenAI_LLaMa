# Spec Delta

## Purpose

Provide a secure email-and-password identity flow so users can create an account, maintain a session, and access protected areas of the todo application.

## ADDED Requirements

### Requirement: User registration
The system SHALL allow a visitor to create an account with a valid email address and a password of at least eight characters. Email uniqueness SHALL be evaluated case-insensitively, passwords SHALL never be stored in plaintext, and successful registration SHALL establish an authenticated session.

#### Scenario: Successful registration
- **WHEN** a visitor submits a valid email address that is not registered and a password of at least eight characters
- **THEN** the system creates the account, establishes an authenticated session, and grants access to the protected application

#### Scenario: Invalid registration input
- **WHEN** a visitor submits an invalid email address or a password shorter than eight characters
- **THEN** the system rejects the request, identifies the invalid field, and does not create an account or session

#### Scenario: Duplicate email address
- **WHEN** a visitor submits an email address that matches an existing account regardless of letter case
- **THEN** the system rejects the request and does not create another account or authenticated session

### Requirement: User sign-in
The system SHALL authenticate a registered user using their email address and password. Failed authentication SHALL use a generic error that does not reveal whether the email address or password was incorrect.

#### Scenario: Successful sign-in
- **WHEN** a registered user submits the correct email address and password
- **THEN** the system establishes an authenticated session and grants access to the protected application

#### Scenario: Invalid credentials
- **WHEN** a visitor submits an unknown email address or an incorrect password
- **THEN** the system rejects the request with the same generic authentication error and does not establish a session

### Requirement: Persistent server-validated sessions
The system SHALL persist authentication across page reloads and browser navigation using a session that is validated by the server on protected requests. Sessions SHALL have a server-enforced expiration and SHALL not expose reusable credentials to client-side scripts.

#### Scenario: Valid session is reused
- **WHEN** a user with a valid unexpired session reloads the application or returns in the same browser
- **THEN** the system recognizes the user without requiring another sign-in

#### Scenario: Session is expired or invalid
- **WHEN** a protected request contains an expired, revoked, or otherwise invalid session
- **THEN** the system treats the requester as unauthenticated and does not expose protected content

### Requirement: User sign-out
The system SHALL allow an authenticated user to sign out and SHALL invalidate the current session on the server as part of that operation.

#### Scenario: Successful sign-out
- **WHEN** an authenticated user signs out
- **THEN** the system invalidates the current session, clears its browser session credential, and returns the user to the sign-in flow

#### Scenario: Reusing a signed-out session
- **WHEN** a client attempts to access protected content with a session that has been signed out
- **THEN** the system rejects the session and treats the requester as unauthenticated

### Requirement: Protected application access
The system SHALL prevent unauthenticated visitors from viewing protected application pages and SHALL direct them to sign in. After successful authentication, the system SHALL return the user only to a safe local destination when one was recorded.

#### Scenario: Unauthenticated visitor requests a protected page
- **WHEN** an unauthenticated visitor requests a protected application page
- **THEN** the system redirects the visitor to sign in without rendering protected content

#### Scenario: Authenticated user requests a protected page
- **WHEN** a user with a valid session requests a protected application page
- **THEN** the system renders the requested page

#### Scenario: Unsafe return destination is supplied
- **WHEN** authentication completes with a return destination outside the application
- **THEN** the system ignores that destination and redirects to the default protected page

### Requirement: Authentication request protection
The system SHALL protect registration, sign-in, and sign-out requests against cross-site request forgery and SHALL apply throttling to repeated failed sign-in attempts.

#### Scenario: Cross-site authentication request
- **WHEN** an authentication state-changing request fails the system's origin or anti-forgery validation
- **THEN** the system rejects the request without creating, changing, or invalidating a session

#### Scenario: Repeated failed sign-in attempts
- **WHEN** failed sign-in attempts exceed the configured threshold for the same source or account identifier
- **THEN** the system temporarily rejects further attempts without revealing whether the account exists
