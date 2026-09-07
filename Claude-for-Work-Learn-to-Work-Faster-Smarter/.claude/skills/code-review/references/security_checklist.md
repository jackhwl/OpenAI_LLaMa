# Security Checklist Reference

Review code for each of the following common security issues:

1. **Input Validation**
   - [ ] All user-input is validated and sanitized.
   - [ ] No untrusted data is used in commands or queries without cleaning.

2. **Authentication**
   - [ ] Sensitive actions are always protected by authentication.
   - [ ] No hard-coded credentials, API keys, or secrets in code or configs.

3. **Authorization**
   - [ ] Proper permission checks for sensitive resources and actions.
   - [ ] No privilege escalation possible.

4. **Sensitive Data Handling**
   - [ ] Secrets, passwords, and tokens are never logged or printed.
   - [ ] Data is encrypted in transit (TLS/HTTPS) and at rest when appropriate.

5. **Dependency Security**
   - [ ] Third-party dependencies are up to date and free of known vulnerabilities.

6. **Error Handling**
   - [ ] Error messages do not leak sensitive information or stack traces.
   - [ ] Exception handling is robust and doesn’t crash the application.

7. **Injection Prevention**
   - [ ] Database, shell, and OS command calls are safe from injection (use parameterized APIs).
   - [ ] No eval, exec, or similar calls with user-controllable input.

8. **File Operations**
   - [ ] File uploads are type-checked and storage paths are securely managed.
   - [ ] No unsafe file reads/writes from untrusted sources.

9. **Logging**
   - [ ] Logging does not expose PII or sensitive credentials.

10. **Other Best Practices**
    - [ ] Use secure defaults.
    - [ ] Remove or protect debugging code and endpoints before deploying.

Use this checklist as a reference for code review. Investigate any unchecked boxes.