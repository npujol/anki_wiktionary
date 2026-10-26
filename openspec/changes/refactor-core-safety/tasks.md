# Tasks

- [x] Remove translation network calls from `CustomFields` validation.
- [x] Merge each processor's successful note into the fallback pipeline and check completeness against the final fields.
- [x] Parameterize Verben lookup and set an HTTP timeout.
- [x] Harden AnkiConnect requests and avoid mutable default params.
- [x] Update only the audio field; do not reset card scheduling after audio updates.
- [x] Replace mutable list defaults in serializer models.
- [ ] Add focused unit tests for processor fallback, AnkiConnect audio update payload, and validation without network calls.
- [ ] Run the complete test suite in the project's Poetry environment.
