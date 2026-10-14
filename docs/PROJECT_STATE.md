# Musicstudio — Project State

The project is the durable source of truth for a musical work.

## Current persisted layers

### Project index
- id
- title
- artist
- release kind
- concept
- creative brief
- timestamps

### Version history
Every significant generated or transformed state can be saved as a numbered version with a label and JSON payload.

Examples:
- Creative brief
- Producer plan
- Project state
- generated track
- arrangement
- mix
- master

### Generic project state
The project state is a JSON document intentionally independent from the SQL schema.

Target shape:

project
  release
  tracks
  clips
  lyrics
  references
  assets
  stems
  mix
  master
  artwork
  video
  provenance

This lets Musicstudio add new production capabilities without repeatedly redesigning the database schema.

## Asset library

Assets are stored separately from project state so a single source can be referenced by multiple projects.

Each asset tracks:
- provenance
- license
- kind
- physical/logical path
- project association
- lifecycle state
- optional checksum
- optional retention date

Lifecycle states currently include:
- active
- reference
- temp
- trash

Temporary assets can be identified as expired without deleting them. Actual file deletion is a later, explicit storage-manager capability.

## Version principle

Never silently overwrite an accepted creative artifact.

Prefer:

source -> proposal -> new version -> evaluation -> accepted version

The project graph and version history will later become the common state read by all specialists.