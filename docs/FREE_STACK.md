
# Musicstudio — Zero-Cost Resource Strategy

The project is designed to prove how far a serious music-production environment can be pushed without paid subscriptions or metered APIs.

"Zero cost" here means no recurring service requirement. Hardware electricity, internet access and optional paid services are outside the software constraint.

## Development

GitHub personal accounts currently include 120 Codespaces core-hours and 15 GB-month storage under the GitHub Free allowance. GitHub also documents a 30-minute default inactivity timeout. We should use Codespaces for short development/test sessions, not leave them running continuously.

Important: usage beyond the included allowance can become billable when a payment method/budget permits it. Keep spending controls configured to stop before paid usage.

## Heavy AI

Do not put large model inference into the Codespace by default.

Use a worker strategy:

- local consumer GPU when available
- local CPU for lightweight models and deterministic tasks
- remote free execution only when a service is actually available and permitted
- optional cloud/API adapters later

The Studio should work without any single remote service.

## Generation

ACE-Step 1.5 is a strong first provider candidate because its current documentation describes local generation, 10-second to 10-minute audio, reference audio, repainting, stems, multi-track generation and audio understanding.

MusicGen remains useful as a simpler alternative/baseline.

## Analysis

Essentia provides a large open-source music/audio analysis toolkit with Python bindings.

Analysis should be used heavily because many jobs are better solved by measurement than by an LLM.

Examples:
- BPM
- loudness
- spectral information
- tonal information
- onset/tempo information
- descriptors

## Separation

Demucs is a mature source-separation reference, but its original Meta repository is archived and says development has moved to a fork. We should treat it as an interchangeable capability, not a permanent architectural dependency.

## Audio utilities

FFmpeg should be the general-purpose media conversion layer.

Browser audio:
- Web Audio API
- Tone.js where scheduling/synthesis primitives are useful

Time stretching and pitch:
- investigate Rubber Band
- review its GPL licensing before embedding it in a distributed product

## DAW interoperability

LMMS is free and open source and can be useful as an external fallback for composition/editing.

Ardour is an open-source DAW and a useful interoperability/reference target.

We do not need to reinvent every mature DAW primitive immediately.

## Sounds and samples

Freesound provides an API for interacting with its database, but its API terms state that API use is free for non-commercial purposes and requires compliance with individual sound licenses and attribution.

Therefore Musicstudio must store provenance and license metadata for every imported public asset.

## Spotify

Spotify is useful as a catalog/playback companion, not as an extraction source.

The Spotify Web API can retrieve metadata, manage playlists and control playback. Streaming through the Web Playback SDK requires Spotify Premium, and Spotify's policies prohibit altering Spotify content and prohibit synchronization with visual media.

Therefore:

Allowed architecture:
Musicstudio
  -> Spotify metadata / playlist integration
  -> Spotify playback controlled in Spotify

Not the architecture:
Spotify stream
  -> Musicstudio downloads/edits/remixes raw copyrighted audio

For covers/remixes, the user supplies an asset they have rights to use, or the Studio uses a licensed/public-domain source.

## Free/public-domain asset layer

Build connectors for:
- Freesound
- public-domain libraries
- Creative Commons libraries
- user-owned local files

Every asset keeps:
source
license
author
retrieved_at
allowed_operations

## OpenAI / ChatGPT connector

ChatGPT and the OpenAI API are separately billed. A ChatGPT subscription does not automatically provide free API usage.

Therefore the connector is optional.

Architecture:

Musicstudio
   -> AssistantProvider
       -> Local LLM (default)
       -> OpenAI API (optional)
       -> other provider (optional)

No feature outside the connector may require the OpenAI API.

## Economic rule

Before adding a service ask:

1. Can this be deterministic?
2. Can it run locally?
3. Can an open-source project provide it?
4. Can we use a free provider without locking the architecture?
5. Does the feature truly require paid inference?

If the answer to 1-4 is yes, do not pay for it.
