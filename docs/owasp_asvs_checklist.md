# OWASP ASVS Checklist

This project is a student demonstration system, so the checklist focuses on practical ASVS-aligned controls that are visible in code and easy to explain.

| ASVS area | Control implemented | Evidence location |
| --- | --- | --- |
| V1 Architecture | Small separated apps for accounts, equipment, and audit responsibilities. | `accounts/`, `equipment/`, `audit/` |
| V2 Authentication | Django built-in authentication and password hashing. | `accounts/views.py`, `settings.py` |
| V2 Authentication | Strong password validators enforce length and common-password checks. | `AUTH_PASSWORD_VALIDATORS` in `settings.py` |
| V3 Session Management | Session timeout is 900 seconds and expires at browser close. | `settings.py` |
| V3 Session Management | Session and CSRF cookies are HttpOnly. Secure flags documented for HTTPS production. | `settings.py` |
| V4 Access Control | Admin-only decorator blocks normal users from admin pages. | `accounts/decorators.py` |
| V4 Access Control | Object ownership checks prevent IDOR on request edit/delete. | `_get_owned_pending_request` in `equipment/views.py` |
| V5 Validation | Django forms validate registration, equipment, request dates, quantity, and purpose. | `accounts/forms.py`, `equipment/forms.py` |
| V5 Output Encoding | Django template autoescaping is used and user input is not marked safe. | `templates/` |
| V7 Error Handling | Custom 403, 404, and 500 pages avoid exposing stack traces. | `templates/403.html`, `templates/404.html`, `templates/500.html` |
| V8 Data Protection | Passwords are stored by Django's default password hashers, never in plaintext. | Django `UserCreationForm`, `User` model |
| V10 Malicious Code | Bandit is used to scan for unsafe Python patterns. | `docs/testing_plan.md`, `.github/workflows/security-checks.yml` |
| V12 File Upload | Profile attachment validation limits type, MIME, size, and file name. | `accounts/models.py` |
| V14 Configuration | Secrets come from `.env`; `.gitignore` excludes sensitive local files. | `.env.example`, `.gitignore`, `settings.py` |
| V14 Configuration | CSP, X-Frame-Options, nosniff, and Referrer-Policy are configured. | `settings.py`, `security_headers.py` |
