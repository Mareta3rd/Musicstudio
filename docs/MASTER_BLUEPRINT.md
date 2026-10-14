
# Musicstudio — Master Blueprint

## North Star

Musicstudio is a local-first intelligent music production environment.

It is not just a song generator and not just a DAW with an AI chatbot attached.

The target is a system in which a human can move from an idea to a finished production while AI specialists understand the project state and can perform or propose concrete work.

## The production lifecycle

Musicstudio treats the release as the highest creative container. A track is an element of a larger work, and the system can therefore produce singles, three-song mini-releases, EPs, LPs, live sets and unplugged reinterpretations.

### 01. IDEA / BRIEF
Creative intent, mood, use case, audience, references, constraints.

### 02. LYRIC / TEXT
Lyrics, poetry, meter, rhyme, syllable targets, phonetics, section structure, singability, language and emotional arc.

### 03. COMPOSITION
Melody, harmony, rhythm, form, tempo, key, chord progression and motif development.

### 04. ARRANGEMENT
Instrumentation, layers, entrances, exits, density, dynamics and section transitions.

### 05. SOUND DESIGN
Instrument choices, timbre, synthesis, samples, textures and effects.

### 06. GENERATION / RECORDING
AI generation, MIDI, recorded instruments, vocals, field recordings and imported audio.

### 07. EDITING
Cut, trim, fade, stretch, pitch, repair, timing, comping, replacement, extension and reconstruction.

### 08. MIX
Gain staging, EQ, dynamics, panning, ambience, buses, automation and translation checks.

### 09. FINISH / POLISH
Noise cleanup, pops/clicks, lyric fixes, micro-edits, transitions, tuning, timing nudges and final artistic details.

This is the role the user described as the specialist that fixes the things that are difficult to notice but make a finished record feel finished.

### 10. MASTERING
Loudness, true peak, dynamics, tonal balance and delivery targets.

### 11. DELIVERY
WAV, FLAC, MP3/AAC where appropriate, stems, instrumentals, acapella, MIDI, project archive and metadata.

### 12. LIBRARY / ORGANIZATION
Projects, versions, assets, references, samples, temporary files, exports, trash and recovery.

## The production team

The team is deliberately broader than "one producer agent".

### Producer / Director
Owns the artistic objective and project state. Decides what should happen next.

### Lyricist
Writes and edits lyrics with explicit knowledge of:
- rhyme scheme
- meter and syllable count
- stress pattern
- internal rhyme
- phonetics
- section architecture
- emotional progression
- singability

### Poetry / Prosody Specialist
Checks whether a lyric works as poetry and as something a human can sing. It may reject a technically rhyming line when the stress pattern is wrong.

### Composer
Works on melody, harmony, motifs, chord movement and form.

### Arranger
Transforms musical ideas into an instrument-by-instrument arrangement.

### Sound Designer
Chooses or designs timbres, samples, textures and effects.

### Recording / Performance Assistant
Handles takes, comping, timing, tuning, markers and recording metadata.

### Editor
Performs deterministic audio operations and non-destructive edits.

### Mixing Engineer
Analyses and improves balance, space, dynamics, masking and translation.

### Finish / Polish Engineer
Finds micro-defects: clicks, harsh edits, lyric inconsistencies, timing anomalies, breaths/noise issues, awkward transitions and tiny detail problems.

### Mastering Engineer
Prepares the final master and delivery variants.

### Reference Analyst
Extracts BPM, key, structure, energy, spectral and other usable descriptors from supplied audio.

### Rights / Provenance Guardian
Tracks where imported audio came from and whether it is known to be own, licensed, public-domain or unknown.

This is a production safeguard, not legal advice.

### Release / A&R Director
Builds the artistic arc of a release and keeps the catalogue coherent without forcing every track to sound identical.

### Visual Director
Owns cover, back cover, booklet, lyrics layout and visual identity.

### Video Director
Builds music-video / visualizer plans and links visual assets to release concepts.

### Continuity / Sequence Specialist
Checks the narrative flow of track order, intros, interludes, transitions and outros.

### Librarian
Organizes projects, versions, assets, stems, exports, references and temporary material.

### Cleanup / Storage Manager
Prevents temporary work and generated debris from silently consuming disk space.

### QA Engineer
Runs tests, validates renders, detects broken assets and compares requested vs delivered properties.

### Researcher
Finds models, algorithms, datasets and open-source tools that can improve the Studio.

## Agent rules

Agents do not own the project.

Musicstudio owns the canonical project state.

An agent produces one of:

- observation
- proposal
- transformation
- validation result

All transformations must be versioned and reversible.

Agents must report confidence and the evidence used for important changes.

Agents may disagree. The Producer/Director decides whether to accept, reject or ask another specialist.

## Shared project state

Every agent operates on the same project graph:

Project
- CreativeIntent
- References
- Sections
- Tracks
- Clips
- MIDI
- Lyrics
- Versions
- Stems
- Mix
- Master
- Deliverables
- Asset provenance
- Task history

The project graph is more important than any single model.

## Human intervention policy

Default:

- AI acts autonomously inside explicitly allowed scopes.
- Deterministic operations may run automatically.
- Destructive operations create a new version first.
- Rights-sensitive imports require explicit user confirmation when provenance is unknown.
- Provider/model installation can require a human because it may involve OS permissions, large downloads, GPU drivers or credentials.

The user should normally be needed only for:
1. creative decisions,
2. credentials/permissions,
3. physical hardware,
4. resolving an environment-specific failure.

## Runtime strategy

The system is designed around a root controller and optional workers.

### Control plane

The Studio application holds:
- project state
- orchestration
- agent registry
- provider registry
- permissions
- task queue
- history
- UI

### Worker nodes

A worker can be:
- the same PC
- a laptop
- a home server
- a GPU workstation
- a cloud VM
- a browser runtime for Web Audio tasks
- an external API adapter

Workers register capabilities and receive jobs.

The control plane should not assume where computation happens.

## Zero-cost strategy

The default path must be composed of free/open-source/local software.

Examples currently under consideration:

- ACE-Step for generation
- MusicGen as a baseline/alternative
- Essentia for music analysis
- source-separation tools such as Demucs where licensing and maintenance fit
- FFmpeg for media conversion
- Web Audio / Tone.js for browser-side audio interaction
- Audacity/LMMS/Ardour interoperability for external editing when useful
- Free/CC/open asset sources with provenance tracking

Cloud APIs are optional accelerators, never hidden requirements.

## Audio architecture

The audio pipeline should be non-destructive.

Original:
  -> imported asset
  -> derived asset
  -> edit graph
  -> preview render
  -> mix render
  -> master render
  -> delivery

Never silently overwrite the source.

## Library architecture

The library has explicit classes:

projects/
references/
samples/
stems/
renders/
masters/
exports/
temp/
trash/

Temp content receives a retention policy.

Trash is reversible before purge.

Automatic cleanup never deletes a source, project, reference or final delivery without explicit policy.

## Desktop, Web and Remote

Musicstudio should expose the same control plane through:

1. Web UI — fastest iteration.
2. Desktop shell — local files, audio devices, MIDI and native integrations.
3. Remote worker mode — heavy generation/analysis elsewhere.
4. CLI — automation, testing and batch work.

The interfaces are clients of the same project API.

## ChatGPT / external intelligence connector

The application should have an OpenAI-compatible provider interface for an optional intelligent assistant.

However, the ChatGPT subscription and API platform are separate billing systems. An installed ChatGPT subscription does not make arbitrary API calls free. Therefore the strict zero-cost default uses local models; an OpenAI API connector is an opt-in accelerator and must never be a hidden dependency.

## Design ambition

The product should feel closer to a creative instrument than to an administration panel.

The interface should surface:
- what is being made
- what changed
- what is playing
- what the AI proposes
- what needs attention

Complexity should be available without being permanently visible.

## Milestone sequence

M0 — Foundation
M1 — Real generation
M2 — Projects and versions
M3 — Audio assets and provenance
M4 — Timeline / multitrack editing
M5 — Analysis and separation
M6 — Agent team
M7 — Mix / finish / mastering
M8 — Desktop + remote workers
M9 — Library intelligence
M10 — Advanced co-production
