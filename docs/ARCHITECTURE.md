
# Musicstudio architecture

## Why this architecture

Commercial AI music products increasingly combine generation with editing and production. Suno describes Studio as a generative audio workstation and its current Studio workflow includes chat-driven creation, audio clips, MIDI, arrangement and effects. Udio exposes audio upload, extension, inpainting, remix, style transformation and a waveform-centered session. ACE-Step 1.5 provides a strong local engine/API surface including generation, reference audio, repaint/edit operations, stems, multi-track generation and metadata controls.

Musicstudio therefore treats generation as an engine, not as the application.

## Layers

MUSICSTUDIO
    Creative UI
    Projects / versions
    Prompt & intent
    Job orchestration
    History
    Timeline / future arrangement

        Provider contract

PROVIDERS
    Mock
    ACE-Step
    Future local engines
    Future cloud/API engines

        generated audio

## Provider contract

The Studio knows four concepts:

- submit generation
- inspect job status
- obtain resulting audio
- identify provider capabilities

Everything model-specific stays inside the provider.

## Why ACE-Step first

ACE-Step 1.5 currently documents:

- local operation
- 10-second to 10-minute generation
- REST API
- BPM, key and time-signature control
- reference audio
- cover and edit operations
- track separation and multi-track generation
- batch generation

Its API is asynchronous:

release_task -> task id -> query_result -> audio path

That maps naturally onto Musicstudio's own job model.

## Engine independence

The internal request uses a small stable schema:

prompt
lyrics
duration
bpm
key_scale
vocal_language
batch_size
seed

Provider adapters may enrich this request, but the UI does not need to know whether the target is diffusion, autoregressive generation, a remote HTTP service or a local command.

## UX principles

1. Describe first, tune second.
2. Controls reveal complexity gradually.
3. Results are versions, not disposable outputs.
4. Audio is the centre of the workspace.
5. Editing is a first-class operation.
6. Local-first where practical.

## Research references

Suno Studio:
https://help.suno.com/en/articles/13670529

Suno:
https://suno.com/

Udio audio workflows:
https://help.udio.com/en/articles/10754328-create-music-with-your-own-audio

ACE-Step 1.5:
https://github.com/ace-step/ACE-Step-1.5

ACE-Step REST API:
https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/API.md

Meta MusicGen:
https://github.com/facebookresearch/audiocraft
