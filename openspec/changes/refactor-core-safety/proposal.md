# Change: Refactor core data flow and Anki update safety

## Why

The current implementation performs network requests during Pydantic validation, has processor selection embedded in class-name checks, and resets card scheduling after updating audio. These behaviors make data generation unpredictable and risk user review progress.

## What changes

- Make `CustomFields` validation deterministic and free of translation network calls.
- Make the data processor fallback pipeline carry the latest successful note forward and determine completeness from the resulting fields.
- Make the Verben request parameterized and add a request timeout.
- Avoid resetting scheduling when filling missing audio; update only the Anki note's audio field.
- Harden AnkiConnect HTTP requests and remove mutable default request parameters.
- Add explicit default factories for mutable serializer fields.

## Capabilities

### Modified
- `note-data-processing`: processor fallback and field validation behavior.
- `anki-local-sync`: safe media field updates without resetting scheduling.

## Out of scope

- Moving all connector workflows into a service layer.
- Introducing new configuration files, CLI commands, or prompt-management framework.
- Migrating to a new translation provider. Translation can be explicitly added in a separate service change.
