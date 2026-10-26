# Change: Multi-account Telegram bots with selectable LLM backends

## Why

The application currently reads one Telegram token and global backend credentials from environment-based configuration. `main.py` creates one Telegram `Application`, and processor instances are held in a module-level map. This prevents running multiple independently configured bot accounts in one service and makes backend selection difficult to scope safely.

## What changes

- Add typed account configuration loaded from environment variables or a configuration file, with secrets kept outside version control.
- Make Telegram application construction and handler registration account-scoped; each configured account gets its own token, handler, and polling lifecycle.
- Pass account configuration into data processors instead of reading global backend credentials, and select Gemini or Ollama through a per-account backend factory.
- Isolate each account's generated files and note output paths; do not share mutable processor or handler instances between accounts.
- Preserve the existing single-account environment variables as a backward-compatible default during migration.
- Document configuration, deployment, Telegram bot/channel permissions, and validation/testing steps.

## Capabilities

### New
- `multi-account-bot-runtime`: Run multiple Telegram bot identities in one service with isolated configuration and lifecycle.
- `llm-backend-selection`: Configure Gemini or Ollama independently for each bot account.

### Modified
- `telegram-bot`: Construct handlers and applications from account-specific configuration.
- `note-data-processing`: Instantiate backend processors from account configuration rather than a global processor singleton map.

## Out of scope

- Managing Telegram end-user identities or billing/subscriptions.
- Sharing one Telegram bot token across multiple independent accounts.
- Adding new LLM providers beyond the existing Gemini and Ollama integrations.
- Providing a public web administration interface or storing secrets in the repository.
- Guaranteeing that a Telegram bot can post to a channel without being explicitly added and granted the required permissions.

## Design notes

Telegram bot tokens represent distinct bot identities. Each configured account therefore needs its own token and Telegram `Application`. The runtime may host these applications in one process, but must start and stop their polling tasks within a single coordinated async lifecycle; sequential calls to `run_polling()` are not sufficient. A separate process/container per account remains a valid deployment option and should remain possible.

Account configuration should be explicit and injected into handlers, `AnkiHandler`, and LLM processors. Avoid module-level configured processor instances because they can leak settings across accounts. The account identifier should also scope filesystem outputs to prevent collisions.
