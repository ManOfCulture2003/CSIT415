# University Library Management System (Academic Group Project)

PHP + MySQL web application prototype with book searches, account registration, member borrowing history, librarian pages, and an experimental fine-management workflow.

**Status:** Educational prototype, **not production-ready**. This was a university group project, not a professional deployed library service. Credit contributions accurately if discussing it in interviews.

## Local setup
1. Install PHP 8.2+ with MySQLi, MySQL/MariaDB, and the cURL extension (for Google Books).
2. Create a *local development-only* database named `libraryDB` and import `librarydb.sql` using phpMyAdmin or your database client.
3. Configure these environment variables as needed: `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`. Defaults target a typical local development database; do not expose it on a public host.
4. Start the PHP development server with `php -S localhost:8000` and open `http://localhost:8000`.
5. Create a new member account with a test Montclair-format email. Internet access is required for the Google Books search.

## Security limitations and required follow-up
- **Do not deploy this publicly.** This branch includes targeted role/session fixes and output escaping, but is not a complete security overhaul.
- Password handling still uses unsalted SHA-256 hashes for compatibility with the historical database. Migrate to `password_hash`/`password_verify` before public hosting.
- The checked-in SQL dump contains **sample member and librarian records and credential hashes**. Treat all samples as potentially sensitive; replace them with fictional data, rotate any real passwords that might have been used, and regenerate a sanitized seed file before making public demonstrations.
- Add CSRF protection for every state-changing action, consistent server-side validation, tighter fine/borrow transaction rules and inventory checks, appropriate authorization checks throughout, and rate limiting.
- Do not assume the old `TESTS.md` entries represent independently repeatable tests. A full integration test requires a MySQL database and application runtime.

## Features to discuss in interviews
Web forms, session-based authentication, MySQL prepared statements in several workflows, normalized tables with foreign keys, third-party API usage, and role-based feature design. Explain the limitations candidly.

## Suggested next milestone
Create a Docker Compose local demo with sanitized fixture data and integration tests for authorization, borrowing, returns, and fines. Verify all database migrations first.
