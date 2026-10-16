# Security Checklist

## Secrets

- [ ] Keep `.env` out of source control.
- [ ] Never commit or share the Discord token.
- [ ] Never commit or share service-account private keys or full credential JSON.
- [ ] Restrict access to the host, environment file, logs, and backups.
- [ ] Rotate credentials immediately if exposed.
- [ ] Use a secret manager when the hosting platform supports one.

## Google Sheets

- [ ] Enable only the APIs needed by the deployment.
- [ ] Share the spreadsheet with the service-account email instead of making it public.
- [ ] Grant the service account access only to the required spreadsheet.
- [ ] Check the spreadsheet after uncertain write failures before retrying.
- [ ] Keep a separate test spreadsheet for acceptance tests.

## Discord

- [ ] Configure `OWNER_ID` with a numeric user ID.
- [ ] Verify owner-only commands are denied when `OWNER_ID` is missing or invalid.
- [ ] Give the bot only required channel permissions.
- [ ] Do not assume Discord server Administrator permission grants owner-only access; the code checks the configured user ID.
- [ ] Review the report channel because user-submitted names may appear in report embeds.

## Runtime and operations

- [ ] Keep dependencies updated deliberately and test version changes before production.
- [ ] Keep one active bot instance for this spreadsheet unless distributed write coordination is implemented.
- [ ] Avoid logging tokens, credential JSON, or other secrets.
- [ ] Restrict access to operational logs.
- [ ] Test the replacement in a private server before deployment.

## Known security boundaries

The owner ID is a configuration gate, not a replacement for host security or secret management. This version does not implement distributed locking, a dedicated secret manager, or multi-guild permission configuration. Do not describe those features as present unless separately implemented and tested.
