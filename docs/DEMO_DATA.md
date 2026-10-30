# Public synthetic library data

This repository is an academic group prototype, **not a production library system**.

## What changed

`librarydb.sql` preserves the original seven-table MariaDB schema and its foreign-key relationships, but **all imported data rows have been replaced** with fictional demo books, two fictional members, one fictional librarian, loan history, a fine and a question. Demo emails use the reserved `example.invalid` domain. Phone numbers and addresses are NULL.

**No account in the SQL fixture can log in.** The password columns contain the literal `DISABLED_ACCOUNT_CREATE_LOCALLY`, not usable credentials or password hashes. Do not replace these with public shared passwords. For an authenticated local demonstration, create a disposable account through the app's registration workflow in a private environment; the current prototype restricts signups to institutional email addresses and uses legacy SHA-256 authentication. A proper password-hash migration and stronger authorization/CSRF protections are still needed before any internet-facing deployment.

## Import locally

1. Use an isolated local MariaDB 10.4+ instance and a **new empty** database named `librarydb`. Never import into a real organization's database.
2. From the repository root, run `mariadb -u <local-user> -p librarydb < librarydb.sql` (replace the placeholder with your local DB user). Do not commit database passwords.
3. Check the example records with `SELECT COUNT(*) FROM members;` and `SELECT COUNT(*) FROM transactions;`. Expected counts are 2 and 2.
4. Configure the PHP application with local-only database credentials. **The default-branch PHP prototype has known security and cross-platform table-case issues; this fixture change alone does not make the app deployable.**
5. Validate the fixture without a database: `python -m unittest discover -s tests -v`.

The fixture includes an overdue loan and a current loan for exercising fine and return logic. It is a demonstration of relational structure, **not** a verified end-to-end integration test of the PHP application.

## Public-history exposure warning

Replacing a file on the default branch **does not delete its earlier Git history, forks, caches or clones**. The origin and permission status of the original imported rows remain unverified. If any were real, coordinate privately with the relevant data owners to rotate affected credentials, assess exposure, and perform an approved history cleanup. Do not paste original values into issues, PRs, test logs or reports.

## Testing and limitations

- `tests/test_public_fixture.py` checks that the public SQL fixture contains only the expected synthetic INSERT statements, reserved email addresses, disabled password placeholders and preserved table relationships.
- GitHub Actions additionally imports the SQL into a temporary MariaDB service and checks table counts and referential integrity. PHP files receive syntax checks, but there is no authenticated browser/MySQL application integration test.
- The fixture is intentionally not idempotent: import into a fresh database only.
- This change does not rewrite historical commits or verify whether original rows were synthetic.
