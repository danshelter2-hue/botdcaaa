# Deployment Guide

## 1. Prerequisites

- Python 3.10 or newer.
- `discord.py` 2.6 or newer (the supplied requirements file pins it to `>=2.6.0,<3.0.0`).
- Discord bot token and application command access.
- Google Sheets API enabled in Google Cloud.
- A service account whose email is shared on the target spreadsheet.

## 2. Back up the existing installation

Before updating, copy the current project folder and `.env` to a secure backup location. Do not put the backup containing secrets in a public repository or share it in chat.

## 3. Prepare Python environment

From the project root:

```bash
python -m venv .venv
```

Activate it.

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Configure environment variables

Copy `.env.example` to `.env`. Fill these required variables:

- `TOKEN`: Discord bot token.
- `OWNER_ID`: numeric Discord user ID for owner-only commands.
- `GOOGLE_SHEETS_ID`: spreadsheet ID.
- `GOOGLE_SHEETS_TAB`: worksheet/tab name.
- `GOOGLE_SERVICE_ACCOUNT_JSON`: valid one-line service-account JSON.

Optional:

- `EDITOR_ROLE_NAMES`: comma-separated role names retained from the current configuration.
- `LOG_LEVEL`: standard logging level such as `INFO` or `WARNING`.
- `EMOJI_<KEY>_NAME`, `EMOJI_<KEY>_ID`, and `EMOJI_<KEY>_ANIMATED`: optional custom emoji settings.

`GUILD_ID`, `REPORT_CHANNEL_NAME`, and `LOG_CHANNEL_NAME` are currently constants in `bot.py`; changing them requires editing the source and testing the result.

### Configure custom emojis

1. Open the Discord Developer Portal and select the application that owns the bot.
2. Open the application's emoji management area and create or select the emoji.
3. Copy the exact emoji name and numeric ID.
4. Add the matching environment variables. Example:

   ```env
   EMOJI_SUCCESS_NAME=custom_check
   EMOJI_SUCCESS_ID=123456789012345678
   EMOJI_SUCCESS_ANIMATED=false
   ```

5. For an animated emoji, set `EMOJI_SUCCESS_ANIMATED=true`.
6. Repeat for other keys as needed. If no valid name/ID pair is configured, the registry uses a Unicode fallback.
7. Restart the bot after changing environment values.

Use actual values from your application; the example ID is not a real configuration value.

## 5. Google Sheet setup

The current source reads `A:G`. The expected column sequence is `No`, `name`, `country`, `tier`, `type`, `how_to_obtain`, and an optional full-release source in column G. The service-account email must have access to the spreadsheet. Do not make the spreadsheet publicly editable just to enable the bot.

## 6. Invite and permissions

Invite the bot with the `bot` and `applications.commands` scopes. Give it only the permissions required for its use, including viewing the report/log channels, reading report-channel history, sending messages, and embedding links where needed. The `/reportperms` command checks the report channel's required permissions.

## 7. Preflight validation

Run:

```bash
python -m py_compile bot.py emojis.py
python -m unittest discover -s tests -v
```

Then launch:

```bash
python bot.py
```

Confirm startup logs show a successful connection and guild command sync. Do not paste logs containing tokens or private keys into support channels.

## 8. Acceptance test checklist

- [ ] `/check` returns a known item.
- [ ] `/type` returns a known item by type and name.
- [ ] `/item` handles one and multiple item names and duplicate inputs.
- [ ] Autocomplete returns choices.
- [ ] Components V2 result layout renders correctly.
- [ ] Report Item opens the modal and sends a report to the configured report channel.
- [ ] A repeated report is rejected as a duplicate.
- [ ] `/add`, `/edit`, `/delete`, and `/reload` are denied to a non-owner.
- [ ] Owner-only commands work with the configured owner ID.
- [ ] `/reportperms` reflects actual channel permissions.
- [ ] `/ping` responds.
- [ ] `/botowner` is restricted to the configured owner.
- [ ] A sheet mutation is reflected in subsequent lookups.
- [ ] Custom emojis render, and Unicode fallback works when a custom emoji is unset.

## 9. Rollback

Stop the new process, restore the previous source and dependency files from backup, and restart the old version. Preserve `.env` and the Google Sheet. If a sheet mutation succeeded before a failure, inspect the sheet manually before retrying the operation to avoid duplicate data.
