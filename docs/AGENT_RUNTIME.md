# Musicstudio — Agent Runtime

## Goal

Turn specialist definitions into bounded, auditable work.

The runtime separates:

1. project context
2. specialist role
3. provider inference
4. candidate output
5. deterministic evaluation
6. acceptance/review
7. version creation

## Bounded execution

The default refinement loop has a maximum of three iterations.

A loop may end with:
- accepted
- human_review
- max_iterations

Every iteration records a candidate fingerprint, decision and reason.

## First executable specialist

The Lyricist is the first executable specialist.

Flow:
    project brief
      -> lyricist prompt
      -> structured lyric draft
      -> deterministic prosody measurements
      -> accept / refine / human review
      -> project version

The current prosody analyzer is deliberately heuristic. It estimates syllables and rhyme endings and explicitly reports remaining limitations around Spanish synalepha, stress and singability.

## Why this order

Lyrics are a useful first proving ground because they combine creative language generation, structure, domain constraints, deterministic checks, iterative refinement and versioning.

The same runtime can later power composer, arranger, mixer, polisher, mastering QA and release continuity.

## Provider independence

The specialist does not know whether the provider is Gemini, Groq, OpenRouter, OpenAI or a future local model.

It sees only the normalized assistant contract.

## No silent destruction

Agent results are candidates until persisted as a version.
The runtime never replaces accepted project state in-place.