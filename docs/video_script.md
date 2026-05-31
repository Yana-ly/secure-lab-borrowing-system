# Video Script

## Member 1: Application Demo and CRUD Functionality

Hello, I will demonstrate the Secure Lab Equipment Borrowing System. The website is opened at `/SSDProject/`. The interface uses a dark cybersecurity dashboard style with a sidebar, top bar, status cards, and readable tables. First, I log in as the normal user. I can see available equipment, create a borrowing request, and view only my own requests. I can edit or delete a request only while it is still pending. Next, I log in as the admin. The admin can manage equipment, view all borrowing requests, and approve or reject requests.

## Member 2: Security Testing Using OWASP ZAP, Bandit, and pip-audit

I will explain the security testing. We used Bandit to scan Python code for insecure patterns. We used pip-audit to check whether dependencies have known vulnerabilities. We also used OWASP ZAP to test the running web application for issues such as missing headers, XSS, SQL injection, CSRF, and weak session cookies. We captured before and after screenshots for the report.

## Member 3: Mitigation and Secure Coding Explanation

I will explain the security controls. Input validation is implemented using Django forms and clean methods. SQL injection is prevented because the project uses Django ORM only and no raw SQL. XSS is reduced by Django template autoescaping and Content Security Policy. CSRF protection is enabled using Django middleware and CSRF tokens in all POST forms. Access control uses login decorators, admin decorators, and ownership checks to prevent IDOR.

## Member 4: GitHub Repository, Commits, README, and CI/CD Explanation

I will present the repository. The project has a clear folder structure with apps for accounts, equipment, and audit logs. The templates folder contains the Django pages, and the static folder contains the final UI files `static/css/app.css` and `static/js/app.js`. The README explains setup, demo accounts, security features, testing commands, and the `/SSDProject/` route. The `.gitignore` prevents secrets, database files, virtual environments, and media uploads from being committed. For CI/CD, the GitHub Actions workflow can run Django checks, tests, Bandit, and pip-audit.
