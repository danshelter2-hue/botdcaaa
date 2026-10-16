# Troubleshooting Guide

## Bot fails during startup

### `TOKEN not found in environment variables`

- Confirm `.env` exists in the working directory from which `python bot.py` is launched.
- Confirm `TOKEN` is set and has no surrounding quote or whitespace issue.
- Reset the token in the Developer Portal if it was exposed. Do not paste it into logs or support chats.

### Owner-only commands deny everyone

- Set `OWNER_ID` to the owner's numeric Discord user ID, not a username, display name, role ID, or server ID.
- Restart the process after changing `.env`.
- Missing/invalid values intentionally fail closed.

### Google Sheets configuration errors

Check that:

- `GOOGLE_SHEETS_ID` is the spreadsheet ID, not the whole URL.
- `GOOGLE_SHEETS_TAB` exactly matches the tab name.
- `GOOGLE_SERVICE_ACCOUNT_JSON` is valid one-line JSON.
- The Sheets API is enabled in the correct Google Cloud project.
- The service-account email has access to the spreadsheet.
- The sheet has the expected headers and data columns.

### Google API permission or quota errors

- Verify the service account has the required spreadsheet access.
- Review Google Cloud API quota and error details.
- Avoid repeatedly retrying write commands without checking whether the previous write succeeded.
- Do not grant broad project permissions as a workaround for a spreadsheet-sharing issue.

## Slash commands missing

- Confirm the bot was invited with the `applications.commands` scope.
- Verify the configured `GUILD_ID` is the intended server ID.
- Inspect startup logs for command sync errors.
- Remember this source registers commands to one guild; it does not globally publish commands to every server.

## Components V2 result fails to render

- Confirm the deployed `discord.py` version is 2.6 or newer.
- Update using the supplied `requirements.txt` in the same virtual environment used to run the bot.
- Ensure the V2 message is sent through its V2 layout/view builder, not mixed with legacy `content` or `embed` payload fields.
- Test with the Unicode fallback first, then configure custom emojis.

## Custom emoji appears as text or does not render

- Check the `EMOJI_<KEY>_NAME` and `EMOJI_<KEY>_ID` pair.
- Ensure the ID is numeric and belongs to the intended application emoji.
- Ensure the name exactly matches the emoji's configured name.
- Set `EMOJI_<KEY>_ANIMATED=true` only for animated emojis.
- Restart after editing `.env`.
- If configuration is blank or invalid, the registry intentionally falls back to Unicode.

## Item data looks stale

The in-memory DataFrame does not automatically poll Google Sheets. Run `/reload` after external edits. Bot-side successful add/edit/delete operations refresh the in-memory data as part of the workflow.

## Report button or modal fails

- Confirm the bot can view and send messages in the report channel and can read message history.
- Run `/reportperms` to check the report channel permissions.
- Check whether the report channel name matches `REPORT_CHANNEL_NAME` in `bot.py`.
- Inspect logs for missing permissions or API errors.
- The duplicate check scans up to 1,000 messages; a very busy channel may make this operation slower.

## Bot appears slow

- Run `/ping` to inspect websocket and response timing.
- Check logs and Google API latency.
- Confirm there is only one active process unless distributed coordination has been added.
- Avoid running several copies that write to the same spreadsheet: the lock is process-local.
- The current design does not include distributed queueing or cross-process cache coordination.

## Tests fail

Run from the project root and confirm the correct virtual environment is active:

```bash
python -m py_compile bot.py emojis.py
python -m unittest discover -s tests -v
```

Static tests do not exercise real Discord interactions or real Google Sheets requests. Use a private test guild and a test spreadsheet for integration validation.
