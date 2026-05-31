# Manual Code Review Checklist

| No | Item to Check | Description | Implemented? Yes/No | Evidence | File location | SSDF Practice |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Input Validation | Confirm all input uses Django forms, validators, and server-side `clean()` checks. | Yes | Registration and borrow request invalid input rejected. | `accounts/forms.py`, `equipment/forms.py` | PW.5 |
| 2 | Authentication & Session Management | Confirm Django auth, hashed passwords, strong passwords, timeout, and secure cookie flags. | Yes | Demo login and session settings. | `settings.py`, `accounts/views.py` | PW.6 |
| 3 | Access Control | Confirm admin-only views and ownership checks block URL tampering. | Yes | Normal user receives 403 for admin URL or another user's request. | `accounts/decorators.py`, `equipment/views.py` | PW.7 |
| 4 | Error Handling | Confirm custom error pages and `DEBUG` from environment. | Yes | Custom 403/404/500 pages. | `templates/403.html`, `templates/404.html`, `templates/500.html` | PW.8 |
| 5 | Sensitive Data Protection | Confirm secrets are not committed and logs do not store passwords/tokens. | Yes | `.env.example` only; audit descriptions exclude secrets. | `.gitignore`, `.env.example`, `audit/utils.py` | PW.8 |
| 6 | File Upload Security | Confirm allowed extension, MIME, size limit, and UUID naming. | Yes | Upload accepts PDF/JPG/PNG only, max 2MB. | `accounts/models.py` | PW.8 |
| 7 | Configuration Security | Confirm secure headers, CSP, and local/production cookie comments. | Yes | Header check with browser/ZAP. | `settings.py`, `security_headers.py` | PO.5 |
| 8 | Logging & Monitoring | Confirm important security events are captured in audit logs. | Yes | Failed login and unauthorized access appear in Audit Logs. | `audit/models.py`, `audit/utils.py`, views | RV.1 |
| 9 | Dependency Management | Confirm dependencies are pinned and scanned. | Yes | `pip-audit` output screenshot. | `requirements.txt`, `README.md` | RV.1 |
| 10 | Output Encoding / Escaping | Confirm templates rely on autoescaping and do not use `safe` on user input. | Yes | XSS payload rendered as text, not executed. | `templates/` | PW.5 |
| 11 | Automated Security Tests | Confirm security controls have repeatable Django tests. | Yes | `python manage.py test` passes. | `accounts/tests.py`, `equipment/tests.py` | RV.1 |
| 12 | CI/CD Security Checks | Confirm GitHub Actions runs checks on push and pull request. | Yes | Workflow run screenshot. | `.github/workflows/security-checks.yml` | PO.3 |
