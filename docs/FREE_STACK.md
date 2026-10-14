# Musicstudio — Zero-Cost Resource Strategy

The project is designed to prove how far a serious music-production environment can be pushed without recurring service subscriptions.

## Current assistant options

### Gemini
Google currently offers free input/output for selected Gemini models through the Gemini API free tier. Musicstudio has live-verified Gemini connectivity and uses it as the first free provider when configured.

### Groq
Groq currently publishes free-plan limits for several models, including qwen/qwen3.8-27b at 30 RPM, 1,000 RPD, 8K TPM and 200K TPD. Musicstudio treats it as a second free provider and fallback.

### OpenRouter
OpenRouter currently lists 25+ free models and a Free plan with 50 requests/day. Its openrouter/free router dynamically chooses among currently available free models. Availability and model quality can change, so this is opportunistic rather than foundational.

### OpenAI
OpenAI is optional. ChatGPT and API billing are separate. The current Musicstudio account reached the API but reported no remaining credits, so OpenAI must never be silently selected by automatic free routing.

## Provider policy

Automatic mode:
    FREE LOCAL
      -> FREE REMOTE
        -> optional external free provider
          -> stop

Paid providers:
    explicit selection only

## Deterministic-first rule

Before calling a model:

1. Can the task be measured or transformed deterministically?
2. Can an open-source local tool do it?
3. Can a free remote provider do it?
4. Only then consider paid inference.

Examples:
- BPM -> audio analysis
- loudness -> DSP meter
- file hashing -> code
- lyric syllable estimate -> deterministic heuristic
- lyric interpretation -> language model
- production planning -> language model
- waveform rendering -> browser / audio tools

## Privacy

Each provider should eventually declare data retention, logging, training/use policy, region where known, supported modalities and cost class.

Policies:
    LOCAL_ONLY
    FREE_REMOTE_ALLOWED
    PAID_ALLOWED

The router must enforce the selected policy.

## Ecosystem notes

GitHub Models was retired on July 30, 2026. Do not build a Musicstudio dependency around it.

Cerebras currently offers a time- and credit-bounded Free Trial rather than a perpetually renewable no-cost tier. It can be added later as an opportunistic provider, but it is not part of the strict zero-cost baseline.