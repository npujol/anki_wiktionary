# Anki local sync

## Requirements

### Requirement: Audio updates preserve scheduling
The system SHALL update the Anki note's audio field without invoking actions that reset card scheduling.

#### Scenario: Add missing audio to a note
- **WHEN** a note has no audio value and audio generation succeeds
- **THEN** AnkiConnect receives an `updateNoteFields` request containing the note ID and audio field
- **AND** no `forgetCards` request is sent

### Requirement: AnkiConnect requests have bounded network waits
The system SHALL set a finite timeout on HTTP requests to AnkiConnect.

#### Scenario: AnkiConnect does not respond
- **WHEN** the local AnkiConnect server does not respond before the configured timeout
- **THEN** the request fails rather than hanging indefinitely
