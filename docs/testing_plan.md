# Testing Plan

## Static Analysis With Bandit

Run:

```bash
bandit -r accounts audit equipment secure_lab_borrowing -x "*/migrations/*,*/tests.py"
```

Record findings before and after mitigation. The final expected result should have no high-risk issues in production project code. Test files are excluded because they contain dummy fixture passwords used only by Django's temporary test database.

## Automated Django Security Tests

Run:

```bash
python manage.py test
```

The automated tests cover failed-login audit logging, password validation, default user role, borrowing request validation, admin-only access control, IDOR prevention, and double-approval prevention.

## Dependency Scanning With pip-audit

Run:

```bash
pip install pip-audit
pip-audit
```

If vulnerable dependencies are found, update the affected packages and scan again.

## Dynamic Testing With OWASP ZAP

1. Start the Django app locally.
2. Browse the app through ZAP.
3. Use passive scan for general issues.
4. Use active scan only on the local demo application.
5. Save reports before and after fixes.
6. Export the ZAP HTML report and capture key screenshots for `docs/evidence_log.md`.

## Security Header Checks

Use browser developer tools, curl, or ZAP to verify:

- `Content-Security-Policy`
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: same-origin`

## Before and After Mitigation Comparison

| Test Area | Before mitigation evidence | After mitigation evidence |
| --- | --- | --- |
| XSS | Payload executes or reflected unsafely | Payload is escaped and CSP is present |
| SQL injection | Error or unexpected data returned | Input rejected or safely parameterized by ORM |
| IDOR | User accesses another user's request | HTTP 403 and audit log entry |
| Weak session cookies | Missing HttpOnly/timeout | HttpOnly and 15-minute timeout configured |
| Missing security headers | ZAP flags missing headers | CSP, X-Frame-Options, nosniff, Referrer-Policy present |
| CSRF | POST works without token | POST rejected without valid CSRF token |

## Example Vulnerabilities to Test

- XSS: enter `<script>alert(1)</script>` in purpose or equipment description.
- SQL injection: enter `' OR '1'='1` in username, purpose, or equipment fields.
- IDOR: login as `user1`, create a request, then try editing another request ID.
- Weak cookies: inspect cookies for HttpOnly and session timeout settings.
- Missing headers: check response headers in browser developer tools or ZAP.
- CSRF: submit POST request without CSRF token using ZAP repeater.
