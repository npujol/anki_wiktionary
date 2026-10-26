# Capability: LLM backend selection

## ADDED Requirements

### Requirement: Select backend per account
The system SHALL allow each bot account to select one supported LLM backend independently of other accounts.

#### Scenario: Configure different providers
- **WHEN** one account is configured for Gemini and another for Ollama
- **THEN** each account's requests use only its configured backend and credentials

### Requirement: Validate backend configuration
The system SHALL validate that each configured backend has the settings it needs before starting that account's bot application.

#### Scenario: Missing backend credentials
- **WHEN** a configured provider requires a credential or endpoint that is missing or invalid
- **THEN** startup reports which account has invalid configuration and does not silently use another account's credentials

### Requirement: Avoid shared configured processor instances
The system SHALL create processors from account-scoped configuration rather than sharing configured module-level processor instances across accounts.

#### Scenario: Concurrent requests for different accounts
- **WHEN** different accounts process requests concurrently
- **THEN** each processor uses its owning account's provider, endpoint, model, and credentials
