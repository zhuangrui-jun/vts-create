## ADDED Requirements

### Requirement: Emotion-to-expression mapping configuration

The backend SHALL maintain a JSON configuration file that maps emotion categories to Live2D model expression names.

#### Scenario: Load mapping on startup

- **WHEN** the backend starts
- **THEN** the emotion-to-expression mapping is loaded from the configuration file

#### Scenario: Default mapping

- **WHEN** no custom mapping file is provided
- **THEN** the system SHALL use the built-in default mapping:
  - `happy` → `笑眯眯`
  - `very_happy` → `眯眯眼`
  - `embarrassed` → `泪珠`
  - `sad` → `眼泪`
  - `neutral` → `normal`

### Requirement: Emotion normalization

The system SHALL normalize emotion labels from the LLM to the predefined set, case-insensitively matching where possible, and falling back to `neutral` for unrecognized labels.

#### Scenario: Exact match

- **WHEN** the LLM outputs emotion label `happy`
- **THEN** it maps directly to the expression configured for `happy`

#### Scenario: Case-insensitive match

- **WHEN** the LLM outputs emotion label `HAPPY` or `Happy`
- **THEN** it SHALL be normalized to `happy` and map to the corresponding expression

#### Scenario: Unrecognized emotion fallback

- **WHEN** the LLM outputs an emotion label not in the predefined set (e.g., `angry` or `excited`)
- **THEN** the system SHALL fall back to `neutral` and map to the `normal` expression

### Requirement: Expression validation against model

The system SHALL log a warning at startup if any configured expression name does not exist in the Live2D model's available expression list, but SHALL NOT block operation.

#### Scenario: Mismatch warning

- **WHEN** the config maps `happy` to `big_smile` but the model only has `笑眯眯` and `normal`
- **THEN** a warning is logged: "Expression 'big_smile' not found in model's available expressions"

#### Scenario: All expressions valid

- **WHEN** all configured expression names exist in the model's expression list
- **THEN** no warnings are emitted
