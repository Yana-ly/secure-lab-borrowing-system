# Security Testing Evidence Log

Use this file as the report evidence index. Add screenshot filenames after you capture them.

| Evidence ID | Test/control | Command or action | Expected result | Screenshot filename |
| --- | --- | --- | --- | --- |
| E01 | Django system check | `python manage.py check` | No issues found | `01_django_check.png` |
| E02 | Migration consistency | `python manage.py makemigrations --check --dry-run` | No changes detected | `02_migration_check.png` |
| E03 | Automated security tests | `python manage.py test` | All tests pass | `03_django_tests.png` |
| E04 | Static analysis | `bandit -r accounts audit equipment secure_lab_borrowing -x "*/migrations/*,*/tests.py"` | No issues identified | `04_bandit.png` |
| E05 | Dependency scan | `pip-audit` | No known vulnerabilities found | `05_pip_audit.png` |
| E06 | Failed login logging | Enter wrong password on login page | `LOGIN_FAILED` appears in audit log without password | `06_failed_login_log.png` |
| E07 | Successful login/logout logging | Login and logout with demo account | `LOGIN_SUCCESS` and `LOGOUT` appear in audit log | `07_login_logout_log.png` |
| E08 | Access control | Normal user opens `/audit/logs/` | Custom 403 page and audit entry | `08_forbidden_admin_page.png` |
| E09 | IDOR prevention | Normal user changes request ID in edit/delete URL | Custom 403 page | `09_idor_blocked.png` |
| E10 | CSRF protection | Submit POST without CSRF token using ZAP/repeater | Request rejected | `10_csrf_rejected.png` |
| E11 | XSS prevention | Submit `<script>alert(1)</script>` in purpose | Text is escaped, no script runs | `11_xss_escaped.png` |
| E12 | SQL injection prevention | Submit `' OR '1'='1` in forms | No database error or bypass; ORM handles query safely | `12_sql_injection_blocked.png` |
| E13 | Secure headers | Inspect response headers in browser or ZAP | CSP, X-Frame-Options, nosniff, Referrer-Policy present | `13_secure_headers.png` |
| E14 | File upload validation | Upload `.exe` or file larger than 2MB | Upload rejected | `14_file_upload_rejected.png` |
| E15 | GitHub evidence | Repository home page and commit history | README and organized commits visible | `15_github_repo.png` |
