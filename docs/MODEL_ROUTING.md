# Musicstudio — Assistant Routing Policy

## Purpose

Choose an assistant provider without coupling the Studio to one model or silently spending money.

## Automatic order

1. FREE_LOCAL when a capable local model/worker is available.
2. Gemini free tier when configured.
3. Groq free plan when configured.
4. OpenRouter free routing when configured.
5. Stop rather than activate a paid provider.

OpenAI may be explicitly selected by the user or a future cost policy, but automatic mode never selects it.

## Task routing

### Creative Guide
Deterministic. No model required.

### Producer planning
Needs structured text and planning. Prefer Gemini/Groq/OpenRouter with a structured-output-capable model.

### Lyricist
Needs creative language plus structure. Prefer a stronger text model within the free policy, then validate deterministically.

### Prosody
Use deterministic analysis first; model judgement is supplemental.

### Audio analysis
Prefer deterministic DSP / specialist audio models. Do not spend text-model calls on measurable properties.

### Mix / Mastering
Measure first. Use an LLM only to interpret measurements or produce a proposed operation.

## Fallback behavior

Provider failure may include:
- authentication failure
- quota exhaustion
- rate limiting
- network failure
- malformed provider output

An automatic free fallback may move to the next provider for transient/provider-specific failures.

Once a candidate has been returned, semantic validation belongs to Musicstudio, not to the provider.

## Cost guard

Every provider profile exposes a cost class.

Allowed automatic classes:
FREE_LOCAL
FREE_REMOTE

PAID_OPTIONAL requires explicit configuration.

HUMAN_REQUIRED is used when credentials, permissions, rights decisions or physical actions are needed.

## Current external free options

Gemini: free input/output for selected models in the Gemini API free tier.

Groq: free-plan limits currently include qwen/qwen3.8-27b at 30 RPM, 1,000 RPD, 8K TPM and 200K TPD.

OpenRouter: Free plan currently lists 25+ free models and 50 requests/day; openrouter/free dynamically routes among available free models.

These are changing service policies, so the repository treats them as configuration data rather than permanent guarantees.