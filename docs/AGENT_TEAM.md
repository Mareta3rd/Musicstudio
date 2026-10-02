
# Musicstudio — Agent Team

## Principle

Agents are specialists, not autonomous owners.

Musicstudio remains the orchestrator.

## Agent registry

Each agent declares:

- id
- role
- capabilities
- preferred models
- local/cloud availability
- input types
- output types
- destructive operations allowed
- confidence requirements
- cost policy

## Initial registry

| ID | Role | Core responsibility | Zero-cost default |
| --- | --- | --- | --- |
| producer | Producer/Director | Goal, priorities, acceptance | Local LLM |
| lyricist | Lyricist | Lyrics, sections, rhyme | Local LLM + deterministic validators |
| prosody | Poetry/Prosody | Meter, syllables, stress, rhyme | Python analyzers + local LLM |
| composer | Composer | Melody, harmony, form | Local model / rule engine |
| arranger | Arranger | Instrumentation and structure | Local model + project rules |
| sound | Sound Designer | Timbre, samples, effects | Local model + asset library |
| editor | Audio Editor | Deterministic edits | FFmpeg / Web Audio |
| reference | Reference Analyst | BPM/key/structure/audio descriptors | ACE-Step / Essentia |
| separation | Stem Specialist | Stem extraction | local separation model |
| mixer | Mixing Engineer | Balance, dynamics, masking | deterministic DSP + optional AI |
| polisher | Finish/Polish | Micro-defects and final details | analysis + deterministic DSP |
| mastering | Mastering Engineer | Final delivery mastering | deterministic mastering pipeline |
| rights | Provenance Guardian | Asset origin tracking | metadata/rules |
| librarian | Librarian | Project/assets/version organization | deterministic |
| cleanup | Storage Manager | temp/trash lifecycle | deterministic |
| qa | QA Engineer | Tests/render checks | deterministic |
| researcher | Researcher | New models/tools/workflows | web/local knowledge |

## Delegation model

The Producer creates a task:

    TASK
      objective
      constraints
      inputs
      allowed operations
      expected outputs
      acceptance criteria

A specialist returns:

    RESULT
      observations
      changes proposed
      artifacts
      confidence
      validation
      follow-up tasks

## Specialist composition

Examples:

### Lyric workflow
brief
 -> lyricist
 -> prosody validator
 -> singability checker
 -> producer approval
 -> locked lyric version

### Track workflow
brief
 -> composer
 -> arranger
 -> generation provider
 -> reference analyst
 -> editor
 -> mixer
 -> polisher
 -> mastering
 -> QA

### Repair workflow
problem report
 -> reference analyst
 -> specialist
 -> non-destructive patch
 -> A/B comparison
 -> QA
 -> new version

## Important distinction

The model that writes lyrics does not need to be the model that analyses meter.

The model that generates audio does not need to mix it.

The model that proposes a mix change does not need to render it.

This separation allows cheap deterministic tools to do the work that AI does not need to do.

## Future model selection

Provider selection should be task-specific.

A generation job may use ACE-Step.

A lyric task may use a lightweight local language model.

A mixing diagnosis may use an audio-analysis model.

A deterministic task such as gain staging should use code, not an LLM.

The Producer chooses the cheapest capable worker unless the project explicitly prefers another provider.

## Safety and provenance

Rights-sensitive operations are opt-in.

The system records source URI/path, owner information where supplied, license metadata where available, retrieval date and transformation history.

The Studio must not make a copyrighted stream editable merely because the user can play it in another application.

## Cost policy

Every task has a cost class:

FREE_LOCAL
FREE_REMOTE
PAID_OPTIONAL
HUMAN_REQUIRED

The default policy is:

FREE_LOCAL first -> FREE_REMOTE when genuinely free and permitted -> PAID_OPTIONAL only by explicit configuration.
