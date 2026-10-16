# MW Data — Components V2 & Emoji Edition

A Discord item-lookup bot backed by Google Sheets. This edition adds Discord Components V2 result layouts and a central custom-emoji registry while retaining the existing single-guild workflow.

> **Compatibility note:** This README describes the supplied `MW Data_Scaled_V2_Emoji_Replacement` source. It does not claim multi-guild support, a distributed queue, Redis, or a database-backed cache.

## Features

- `/check` — find an item by name.
- `/type` — find an item by type and name.
- `/item` — check up to ten item names in one command.
- `/add`, `/edit`, `/delete`, `/reload` — owner-restricted Google Sheets administration.
- `/botowner` — owner-only status panel.
- `/reportperms` — check permissions for the configured report channel.
- `/ping` — display Discord websocket latency and response timing.
- Report Item button and modal for items missing from the dataset.
- Components V2 layouts for item-result messages.
- Central emoji registry in `emojis.py`, with Unicode fallbacks.
- Bounded text-normalization caching and normalized-column reuse.
- Google Sheets blocking operations moved off the Discord event loop in the administrative workflows.

## Project layout

```text
MW Data_Scaled/
├── bot.py
├── emojis.py
├── requirements.txt
├── .env.example
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   └── operations/
│       ├── DEPLOYMENT.md
│       ├── TROUBLESHOOTING.md
│       ├── SECURITY.md
│       └── RUNBOOK.md
└── tests/
    └── test_source_contract.py
```

## Requirements

- Python 3.10 or newer (the source uses modern type-union syntax).
- `discord.py` 2.6 or newer for Components V2 APIs.
- A Discord application and bot token.
- Google Sheets API enabled in a Google Cloud project.
- A service-account credential with access to the target spreadsheet.

## Quick start

1. Download and extract the replacement package.
2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate it:

   **Windows PowerShell**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux/macOS**

   ```bash
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env` and fill in the required settings.
6. Invite the bot with the `bot` and `applications.commands` scopes and the required channel permissions.
7. Start the bot:

   ```bash
   python bot.py
   ```

See [`docs/operations/DEPLOYMENT.md`](docs/operations/DEPLOYMENT.md) for the full procedure.

## Environment configuration

Required values:

| Variable                      | Purpose                                                     |
| ----------------------------- | ----------------------------------------------------------- |
| `TOKEN`                       | Discord bot token.                                          |
| `OWNER_ID`                    | Numeric Discord user ID authorized for owner-only commands. |
| `GOOGLE_SHEETS_ID`            | Spreadsheet ID from the spreadsheet URL.                    |
| `GOOGLE_SHEETS_TAB`           | Tab name; defaults to `Sheet1`.                             |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Service-account JSON encoded as a single-line JSON value.   |

Optional values include `EDITOR_ROLE_NAMES`, `LOG_LEVEL`, and emoji name/ID/animation variables. `GUILD_ID`, `REPORT_CHANNEL_NAME`, and `LOG_CHANNEL_NAME` are currently configured in `bot.py`, not `.env`.

**Never commit `.env`, bot tokens, or service-account private keys.** Keep the service account shared only with the spreadsheet it needs.

## Google Sheet format

The bot reads the configured tab range `A:G`. The expected columns are:

1. `No`
2. `name`
3. `country`
4. `tier`
5. `type`
6. `how_to_obtain`
7. Optional full-release source column (the implementation recognizes several header spellings and falls back to column G)

Keep the column order stable unless you also update and test the code. The Google Sheet is persistent storage; the bot's DataFrame is an in-memory snapshot. External sheet edits are not automatically detected and require `/reload`.

## Components V2 and emojis

Item lookup results use Components V2 layout primitives. Discord Components V2 messages must be sent using the V2 view/layout API and cannot combine the V2 payload with legacy `content` or `embed` parameters in the same message. Operational messages and logs may still use regular embeds.

Custom emoji configuration is centralized in `emojis.py`. For a custom emoji key, configure the matching environment variables. Example:

```env
EMOJI_SUCCESS_NAME=custom_check
EMOJI_SUCCESS_ID=123456789012345678
EMOJI_SUCCESS_ANIMATED=false
```

Use the exact emoji name and numeric ID. For animated emojis, set `ANIMATED=true`. If a custom emoji is not configured, the registry returns its Unicode fallback. See [`docs/operations/DEPLOYMENT.md`](docs/operations/DEPLOYMENT.md#configure-custom-emojis).

## Validation

Run these checks from the project root:

```bash
python -m py_compile bot.py emojis.py
python -m unittest discover -s tests -v
```

These checks do not replace live integration testing. Before production deployment, test commands, autocomplete, report modal submission, channel permissions, and actual Google Sheets writes in a private test guild.

## Architecture and operations

- [Architecture and design notes](docs/ARCHITECTURE.md)
- [Deployment guide](docs/operations/DEPLOYMENT.md)
- [Troubleshooting](docs/operations/TROUBLESHOOTING.md)
- [Security checklist](docs/operations/SECURITY.md)
- [Operations runbook](docs/operations/RUNBOOK.md)

## Current limitations

- **Single guild:** slash commands are registered to the `GUILD_ID` constant in `bot.py`.
- **Fixed channel names:** report and log channels are resolved by `REPORT_CHANNEL_NAME` and `LOG_CHANNEL_NAME`.
- **Single-process coordination:** the write lock coordinates tasks inside one running process only; it is not a distributed lock.
- **Report duplicate detection:** report history is scanned (up to 1,000 messages) when checking duplicates; this can become expensive in a high-volume channel.
- **External sheet changes:** external edits require `/reload` before they appear in the bot's local snapshot.
- **Integration verification:** static tests cannot prove Discord API, application-emoji, or Google Sheets runtime behavior.

## Safe upgrade / rollback

Back up the current project and `.env` before replacing files. Keep the previous version available until the new version has been tested in Discord. If the new version fails, stop it and restore the previous source and dependency set; do not delete or overwrite the Google Sheet as part of rollback.

## Complete replacement package

This archive includes the complete bot entry point (`bot.py`), emoji registry, dependency list, environment template, regression checks, architecture notes, and operations guides. Configure `.env` from `.env.example` before running. Do not commit `.env` or service-account credentials.

## Validation

Run `python -m py_compile bot.py emojis.py` and `python -m unittest discover -s tests -v`. Static tests do not replace a live test in a private Discord server connected to a test spreadsheet.
