# Musicstudio — Intelligent Library

The Library is the bridge between creative work and storage management.

## Goals

- keep source material safe;
- make references reusable;
- record provenance;
- separate active work from temporary output;
- make cleanup explainable;
- avoid accumulating generated debris;
- keep project assets discoverable.

## Categories

projects/
references/
samples/
stems/
renders/
masters/
exports/
temp/
trash/

The physical directory layout is a deployment choice. The persistent asset catalog remains the canonical index.

## Provenance

Imported material should record source, license, owner information where supplied, retrieval time and allowed operations where known.

Spotify and other streaming catalog connectors are reference/playback integrations, not raw editable-media extraction mechanisms.

## Cleanup

Cleanup first reports candidates.

Deletion is a separate operation.

A future Storage Manager can apply a retention policy to `temp`, move candidates into `trash`, and purge only after an explicit grace period.

## Agent interaction

Librarian:
- indexes and organizes
- links assets to projects
- detects duplicates and stale references

Cleanup:
- identifies expired temporary work
- reports storage pressure
- proposes safe lifecycle changes

Rights / Provenance:
- checks source metadata
- blocks operations when rights information is required but missing