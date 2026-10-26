# Note data processing

## Requirements

### Requirement: Field validation is deterministic
The system SHALL validate/normalize note fields without making external network requests as a side effect of Pydantic model construction.

#### Scenario: Construct fields without translation service
- **WHEN** a `CustomFields` instance is built with German meaning or example values and missing Spanish fields
- **THEN** validation succeeds without calling a translation provider
- **AND** the model retains supplied source-language values

### Requirement: Processor fallback retains collected content
The system SHALL pass the latest successful note through fallback processors and determine completion from its fields.

#### Scenario: Earlier processor supplies partial fields
- **WHEN** the first configured lookup produces a note with partial fields
- **AND** a later fallback processor supplies additional fields
- **THEN** existing non-empty values are preserved
- **AND** missing values may be filled by later processors

#### Scenario: Explicit processor name is unknown
- **WHEN** a caller requests an unregistered processor
- **THEN** note generation returns no note without making a dictionary lookup request
