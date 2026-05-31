# Secure Lab Equipment Borrowing System

A secure Django web application for a university Secure Software Development project. The system manages laboratory equipment borrowing with authentication, role-based access control, audit logging, secure validation, and repeatable security testing evidence.

## Project Goals

- Build a small but complete Django web application.
- Demonstrate OWASP Top 10 and OWASP ASVS security controls.
- Use secure coding practices that are easy to explain in a report and video.
- Provide evidence files, testing commands, and GitHub-ready documentation.

## Features

- User registration, login, logout, and profile page
- Admin and Normal User roles
- Admin equipment CRUD
- Normal-user borrowing request CRUD
- Admin approve, reject, and delete request actions
- Admin-only audit log page
- Optional secure profile attachment upload
- Clean Bootstrap dark SOC-style interface with custom CSS theme
- Final route prefix: `/SSDProject/`

## Security Features

- Django built-in authentication and password hashing
- Strong password validation
- Server-side input validation using Django forms
- Django ORM only; no raw SQL
- CSRF middleware enabled and CSRF tokens in all POST forms
- POST-only logout
- Admin-only decorators for restricted views
- Object ownership checks to prevent IDOR
- Custom 403, 404, and 500 pages
- Audit logs for login, logout, CRUD, approvals, rejections, failed logins, and unauthorized access
- No passwords, tokens, or secrets written to audit logs
- Content Security Policy and secure response headers
- Session timeout after 15 minutes
- `.env` configuration for `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS`
- `.gitignore` excludes `.env`, database, virtual environment, cache files, and media uploads
- Secure file upload validation for PDF/JPG/PNG, MIME type, size, and UUID filename

## Tech Stack

- Python 3.11+
- Django 5.2 LTS line
- SQLite
- Django Templates
- Bootstrap 5
- Bootstrap Icons
- Custom dashboard CSS in `static/css/app.css`
- python-decouple
- Bandit
- pip-audit
- OWASP ZAP for dynamic testing

## Quick Start

```bash
cd secure_lab_borrowing
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
copy .env.example .env
python manage.py migrate
python manage.py create_demo_data
python manage.py runserver
```

Open: http://127.0.0.1:8000/SSDProject/

## Default Local Demo Accounts

These accounts are for local demo only.

| Role | Username | Password |
| --- | --- | --- |
| Admin | `admin` | `Admin@12345` |
| Normal User | `user1` | `User@12345` |

## Security Test Commands

Run these before recording evidence screenshots:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
bandit -r accounts audit equipment secure_lab_borrowing -x "*/migrations/*,*/tests.py"
pip-audit
```

## OWASP ZAP Suggested Steps

1. Start the app locally with `python manage.py runserver`.
2. Open OWASP ZAP.
3. Browse login, registration, dashboard, equipment, requests, profile, and audit pages.
4. Run a passive scan first.
5. Run an active scan only against the local demo app.
6. Test XSS, SQL injection, IDOR, missing headers, weak cookies, and CSRF.
7. Export the ZAP report and capture before/after mitigation screenshots.

## OWASP Mapping Summary

| Control | OWASP Top 10 area | Implementation |
| --- | --- | --- |
| Access control | A01 Broken Access Control | `@login_required`, `admin_required`, ownership checks, 403 page |
| Sensitive data protection | A02 Cryptographic Failures | Django password hashing, `.env`, no sensitive audit logging |
| Injection prevention | A03 Injection | Django forms, validators, ORM only, no raw SQL |
| Secure design | A04 Insecure Design | Role separation, request status workflow, approval stock checks |
| Secure configuration | A05 Security Misconfiguration | Secure headers, CSP, DEBUG from `.env`, custom error pages |
| Dependency management | A06 Vulnerable Components | `requirements.txt`, `requirements-dev.txt`, pip-audit |
| Authentication | A07 Identification and Authentication Failures | Django auth, password validators, session timeout |
| Integrity and testing | A08 Software and Data Integrity Failures | GitHub Actions workflow and repeatable tests |
| Logging and monitoring | A09 Security Logging and Monitoring Failures | `AuditLog` model and admin-only audit log page |
| SSRF | A10 Server-Side Request Forgery | No user-controlled outbound server requests are implemented |

## Report Support Files

- `docs/security_mapping.md`: OWASP Top 10 and ASVS security mapping.
- `docs/owasp_asvs_checklist.md`: ASVS-focused checklist for the report.
- `docs/manual_code_review_checklist.md`: SSDF/manual review checklist.
- `docs/testing_plan.md`: Bandit, pip-audit, OWASP ZAP, and mitigation comparison plan.
- `docs/evidence_log.md`: Screenshot evidence index.
- `docs/screenshots_needed.md`: Required report screenshots.
- `docs/video_script.md`: Four-member presentation script.
- `docs/github_submission_checklist.md`: GitHub and CI/CD submission checklist.
- `docs/secure_coding_notes.md`: Plain-English explanation of secure coding choices.

## CI/CD

The project includes `.github/workflows/security-checks.yml`. On GitHub, it runs:

- Django system check
- Migration consistency check
- Django automated tests
- Bandit static analysis of production code
- pip-audit dependency scan

## Folder Structure

```text
secure_lab_borrowing/
|-- .github/workflows/security-checks.yml
|-- accounts/
|-- audit/
|-- docs/
|-- equipment/
|-- secure_lab_borrowing/
|-- static/
|   |-- css/app.css
|   `-- js/app.js
|-- templates/
|-- manage.py
|-- requirements.txt
|-- requirements-dev.txt
|-- README.md
|-- .env.example
`-- .gitignore
```
## Final UI Design

The final website uses a dark cybersecurity / IT laboratory dashboard style:

- Dark navy SOC-style background
- Sidebar navigation with Bootstrap Icons
- Top bar with breadcrumb and protected-session indicator
- Dashboard statistic cards
- Clean light glass-style tables for readability
- Bootstrap components with custom CSS in `static/css/app.css`
- Responsive layout for laptop and desktop demonstration

## Project Prepared By

Lyana Yasmin
> UniKL MIIT
