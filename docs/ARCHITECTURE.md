# Architecture and Design Notes

## Scope

This document describes the current Components V2 + emoji edition. It is a lightweight single-process Discord bot, not a distributed multi-guild platform. Its persistent item data remains in Google Sheets.

## Runtime components

- `bot.py`: command registration, item lookup, sheet administration, report modal/button, channel checks, and startup behavior.
- `emojis.py`: maps semantic emoji keys to configured custom emoji markup, or to Unicode fallbacks.
- `requirements.txt`: Python runtime dependencies.
- `tests/test_source_contract.py`: static/source-contract tests; not a live integration suite.

## Request flow

1. Discord sends a slash-command interaction.
2. The registered command validates inputs and, for administrative actions, checks the configured owner ID.
3. Lookup commands query the current in-memory pandas DataFrame.
4. The lookup helpers reuse bounded normalized-text and normalized-column caches where applicable.
5. Administrative commands execute blocking Google API work off the Discord event loop and serialize write/refresh workflows within this process.
6. Successful refreshes invalidate derived lookup caches and replace the in-memory snapshot.
7. The response is rendered as a Components V2 layout for item results or a conventional embed for legacy operational/log responses.

## Data consistency

Google Sheets is the persistent source of truth. The DataFrame is an in-memory snapshot loaded at startup and refreshed after bot-side sheet mutations or `/reload`. An edit made directly in Google Sheets will not be visible until a reload or another operation refreshes the snapshot.

The write lock is process-local. It does not coordinate two separate bot processes. For this version, run one active instance against the spreadsheet unless distributed coordination and duplicate-write handling are designed and tested.

## Caching and memory

- Text normalization uses a bounded LRU cache with a maximum of 8,192 entries.
- Normalized-column cache is capped at eight entries and checks the referenced DataFrame before reuse.
- Cache invalidation is expected when the DataFrame is refreshed.
- These are local performance caches, not a persistent cache and not a cross-process cache.

## Google Sheets access

Google API client operations are synchronous library calls. The administrative workflow moves these calls into a worker thread to avoid blocking Discord's event loop. Client objects are stored per worker thread instead of being shared indiscriminately between threads. This reduces event-loop blocking, but the underlying API calls remain synchronous and subject to Google API quotas and network latency.

## Components V2

Item result views use `discord.ui.LayoutView` and V2 layout components. The Report Item action is registered with a stable custom ID and opens the existing modal. V2 messages should not be sent with legacy `content` or `embed` payload fields in the same message. Conventional embeds remain in use for other messages where not migrated.

## Emoji registry

`emojis.py` is the central source for semantic keys such as `success`, `error`, `warning`, `box`, `type`, `tier`, `country`, `source`, `report`, `owner`, `loading`, `database`, and `ping`. Each can use a configured custom emoji name/ID, with an animated flag, or fall back to Unicode. Emoji IDs and names must belong to an application and be available to the bot's context.

## Security boundaries

- Owner-only commands rely on exact numeric `OWNER_ID` matching.
- Missing or invalid owner configuration fails closed.
- The `.env` file and service-account private key must be protected outside source control.
- The service account should have access only to the required spreadsheet.
- Discord permissions should be restricted to the channels and actions needed by the bot.

## Known constraints

- Single configured guild (`GUILD_ID`).
- Fixed report and log channel names.
- Report duplicate checks scan up to 1,000 messages.
- No distributed queue, Redis cache, database, or distributed lock.
- No native async Google Sheets client.
- No claim of live API integration testing from static tests alone.

## Scaling roadmap

Only introduce the next level of infrastructure when measurement shows a need:

1. Add structured metrics for command duration, Sheets latency, cache hits, and report-history scan time.
2. Add retry/backoff for safe read operations; handle write retries carefully to avoid duplicate appends.
3. Replace history scans with a durable report index if the report channel becomes large or busy.
4. Add per-guild settings only when multi-guild support is a requirement.
5. Consider a persistent datastore or distributed queue only if the workload exceeds what a single process and Google Sheets can reliably support.
