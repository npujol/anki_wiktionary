# Tasks

- [ ] Define an account configuration model with validation for Telegram token, LLM provider, provider credentials, and account-scoped output paths.
- [ ] Load multiple account configurations securely from environment variables or a documented config file; retain legacy single-account environment variables as fallback.
- [ ] Refactor `app/private_config.py` consumers to receive account configuration rather than relying on mutable/global account-specific settings.
- [ ] Make Gemini and Ollama processors accept credentials, endpoint, and model settings via constructor arguments.
- [ ] Replace the module-level `PROCESSORS_MAP` instances with an account-aware processor factory.
- [ ] Refactor `BotHandler` and `AnkiHandler` construction so each account gets isolated dependencies and output paths.
- [ ] Extract Telegram handler registration and create one `Application` per configured bot token.
- [ ] Implement coordinated async startup, polling, error handling, and shutdown for multiple Telegram applications in one process.
- [ ] Ensure account-specific note files, media files, and temporary audio paths cannot collide.
- [ ] Add unit tests for account config parsing/validation, backend selection, and account isolation.
- [ ] Add tests for multi-application startup/shutdown and preserve the existing single-bot behavior.
- [ ] Document multi-account setup, secrets management, channel permissions, and deployment options in `README.md`.
- [ ] Run formatting, lint, and the complete test suite.
