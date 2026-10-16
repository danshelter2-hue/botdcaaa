# Operations Guide

## Startup failures

- `TOKEN not found`: configure `TOKEN` in `.env`.
- `GOOGLE_SHEETS_ID not found`: set the spreadsheet ID.
- `GOOGLE_SERVICE_ACCOUNT_JSON not found`: provide the service-account JSON as one-line JSON.
- Empty sheet: check the tab name, range, headers, and service-account sharing permissions.
- Commands missing: confirm the bot is invited with `applications.commands`, check `GUILD_ID`, and inspect startup logs for sync errors.

## Owner access

Set `OWNER_ID` to the numeric Discord user ID. The owner-only commands deny all users when the value is missing or invalid. The bot does not infer ownership from server administrator permissions.

## Updating data

- Bot-side `/add`, `/edit`, and `/delete` refresh the local DataFrame after successful sheet writes.
- External spreadsheet edits require `/reload`.
- `/reload` retains the last known in-memory snapshot if the Google Sheets refresh fails.

## Safe deployment procedure

1. Stop the currently running bot.
2. Back up `bot.py`, `.env`, and the existing deployment configuration. Do not include secrets in the source ZIP or Git.
3. Install requirements in the target Python environment.
4. Run `python -m py_compile bot.py` and `python -m unittest discover -s tests -v`.
5. Start in a private test guild or during a low-traffic window.
6. Test `/check`, `/type`, `/item`, all owner-only commands, `/reportperms`, `/ping`, and the report button/modal.
7. Inspect logs and verify the Google Sheet after add/edit/delete.
8. Keep the previous version available for rollback.

## Logging and secrets

Set `LOG_LEVEL` to `INFO`, `WARNING`, or `DEBUG` as needed. Never log the bot token or service-account JSON. Restrict access to `.env`.

## Components V2 / emoji setup

- Use `discord.py>=2.6.0` for Components V2 support.
- Configure custom emoji names and IDs in `.env` using the `EMOJI_<KEY>_NAME` and `EMOJI_<KEY>_ID` pattern documented in `.env.example`.
- Confirm the emoji is available to the application and the name/ID pair is exact. Blank or invalid configuration falls back to Unicode.
- After replacing the code or changing emoji environment variables, restart the bot.
- If V2 result messages fail, verify the installed `discord.py` version before changing command code.
