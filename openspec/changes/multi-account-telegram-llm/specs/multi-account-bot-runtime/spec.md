# Capability: Multi-account bot runtime

## ADDED Requirements

### Requirement: Run independent Telegram bot accounts
The system SHALL support starting multiple configured Telegram bot identities from one service deployment. Each account SHALL use its own Telegram token, handler instance, account configuration, and polling lifecycle.

#### Scenario: Start two configured bot accounts
- **WHEN** two valid bot accounts are configured with distinct Telegram tokens
- **THEN** the runtime starts one Telegram application for each account
- **AND** updates received by one bot are processed only by that account's handler and configuration

### Requirement: Preserve single-account compatibility
The system SHALL continue to support the existing single-account environment-variable configuration when no multi-account configuration is provided.

#### Scenario: Start using legacy configuration
- **WHEN** only the legacy `TELEGRAM_TOKEN` and related environment variables are configured
- **THEN** the runtime starts one bot with the legacy behavior

### Requirement: Isolate account outputs
The system SHALL isolate files and other mutable resources that can be written during a request by account.

#### Scenario: Two accounts create output concurrently
- **WHEN** two accounts generate notes or audio for the same input
- **THEN** their account-specific output paths do not overwrite or delete each other's files

### Requirement: Coordinate lifecycle
The system SHALL start, monitor, and stop all configured Telegram applications through one coordinated runtime lifecycle.

#### Scenario: Stop service with multiple bots
- **WHEN** the runtime receives a shutdown signal
- **THEN** it stops polling and cleanly shuts down every started application
