# Operations Runbook

This runbook covers routine actions for the current single-guild deployment.

## Start

1. Activate the project's virtual environment.
2. Confirm `.env` is present and protected.
3. Start with `python bot.py`.
4. Check logs for successful login and command synchronization.

## Verify service health

1. Run `/ping` and confirm the command responds.
2. Run `/check` for a known item.
3. Run `/reportperms` to verify the report channel permissions.
4. Check the bot log output for repeated API errors.

## Refresh external sheet edits

1. Confirm the spreadsheet edit is complete.
2. Run `/reload` as the configured owner.
3. Verify `/check` or `/type` returns the updated value.
4. If refresh fails, consult the logs and troubleshooting guide; do not assume the in-memory snapshot changed.

## Perform an item mutation

1. Confirm the intended item and values.
2. Use `/add`, `/edit`, or `/delete` as the configured owner.
3. Verify the response.
4. Check the Google Sheet directly if the result is ambiguous.
5. Verify the item lookup after the refresh.
6. Before retrying a failed command, check whether the original sheet write actually succeeded.

## Report channel maintenance

1. Keep the channel name aligned with `REPORT_CHANNEL_NAME` in `bot.py`.
2. Keep the bot's View Channel, Read Message History, Send Messages, and Embed Links permissions.
3. Use `/reportperms` after changing channel permissions.
4. Monitor report volume: duplicate detection scans up to 1,000 recent messages.

## Update custom emojis

1. Create/select the application emoji in the Developer Portal.
2. Update its name, ID, and animation environment values.
3. Restart the bot.
4. Test a result message and confirm Unicode fallback still works for unconfigured keys.

## Restart or deploy an update

1. Back up the current code and `.env` securely.
2. Run the syntax and unit checks.
3. Stop the existing process before starting the replacement.
4. Start the bot and perform the health checks.
5. Keep the previous version available until the acceptance tests pass.

## Incident: bot token exposure

1. Reset/revoke the token in the Developer Portal immediately.
2. Update the deployment secret or `.env`.
3. Restart the bot.
4. Review logs and repository history for accidental exposure.
5. Remove exposed secrets from public locations and rotate any other credentials that may have been exposed.

## Incident: Google service-account credential exposure

1. Disable or rotate the exposed key in Google Cloud.
2. Create a replacement credential and update the deployment secret.
3. Recheck spreadsheet sharing and least-privilege access.
4. Restart and test read/write behavior using a controlled test operation.

## Incident: failed or ambiguous write

1. Do not blindly retry.
2. Inspect the Google Sheet for the intended change.
3. If the write succeeded but refresh failed, use `/reload` after connectivity is restored.
4. If the write did not occur, retry once the root cause is understood.
5. Record the error without including secret values.

## Rollback

Stop the current process, restore the last known-good source and dependency files, restore configuration from the secure backup if needed, and restart. Preserve the Google Sheet; rollback code does not reverse spreadsheet mutations.
