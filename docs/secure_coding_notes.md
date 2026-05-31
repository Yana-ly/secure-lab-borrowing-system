# Secure Coding Notes

## No Raw SQL

The application uses Django ORM calls such as `Equipment.objects.filter(...)`, `BorrowRequest.objects.create(...)`, and `get_object_or_404(...)`. It does not use `raw()`, database cursors, or string-built SQL queries. This helps prevent SQL injection because Django parameterizes database queries.

## Server-Side Validation

All user input is validated on the server:

- Registration uses `RegistrationForm`.
- Login uses Django's `AuthenticationForm`.
- Equipment CRUD uses `EquipmentForm`.
- Borrowing requests use `BorrowRequestForm`.
- File upload validation is implemented in `validate_profile_file`.

Client-side controls such as date inputs are treated only as user experience helpers, not security boundaries.

## Access Control

Access control is enforced in views, not only in templates:

- `@login_required` blocks anonymous users.
- `admin_required` blocks non-admin users.
- `_get_owned_pending_request` verifies object ownership before edit/delete.
- Unauthorized attempts are written to `AuditLog`.

## XSS Protection

Django templates escape variables by default. The project does not use the `safe` filter on user-controlled data. A Content Security Policy is added in `security_headers.py` to reduce the impact of injected scripts.

## CSRF Protection

CSRF middleware remains enabled in `settings.py`. Every POST form includes `{% csrf_token %}`, including logout, approve, reject, delete, create, and update actions.

## Audit Logging

Audit logs record important security events without sensitive data:

- Successful login
- Failed login
- Logout
- Registration
- Create, update, and delete borrowing requests
- Approve and reject borrowing requests
- Unauthorized access attempts
- Equipment create, update, and delete

Passwords, tokens, and uploaded file contents are not logged.
