# GitHub Submission Checklist

| Item | Required evidence | Status |
| --- | --- | --- |
| Repository has clear project name | Repository title or README heading | Ready |
| README explains setup and demo accounts | `README.md` installation and accounts sections | Ready |
| Secrets are not committed | `.env` is ignored; only `.env.example` is committed | Ready |
| Database is not committed | `db.sqlite3` is ignored | Ready |
| Virtual environment is not committed | `venv/` and `.venv/` are ignored | Ready |
| Source code is organized | `accounts`, `equipment`, `audit`, `templates`, `docs` folders | Ready |
| Migrations are committed | App `migrations/0001_initial.py` files | Ready |
| Security documentation is included | `docs/security_mapping.md`, `docs/testing_plan.md`, `docs/evidence_log.md` | Ready |
| Manual review checklist is included | `docs/manual_code_review_checklist.md` | Ready |
| Video script is included | `docs/video_script.md` | Ready |
| CI/CD workflow is included | `.github/workflows/security-checks.yml` | Ready |
| Commit history is meaningful | Use small commits such as `Initial Django project`, `Add RBAC and audit logs`, `Add security tests and docs` | To do in GitHub |

## Recommended Commit Order

1. `Initial Django secure borrowing project`
2. `Add role based access control and audit logging`
3. `Add secure forms and upload validation`
4. `Add security documentation and testing plan`
5. `Add CI security checks`

## Before Uploading

Run these commands and capture screenshots:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
bandit -r accounts audit equipment secure_lab_borrowing -x "*/migrations/*,*/tests.py"
pip-audit
```
