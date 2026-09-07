<!-- markdownlint-disable -->

# Hardening Report: dawidd6--action-send-mail/v19

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **dawidd6--action-send-mail/v19** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Workflow files reference actions/reusable workflows using mutable tags or branch names instead of pinned full-length commit SHAs. This exposes the workflow to supply-chain attacks if the referenced ref is updated maliciously.

- `.github/workflows/test.yml` line 23: `uses: actions/checkout@v7` (tag `v7` is mutable)
- `.github/workflows/npm-updates.yml` line 8: `uses: dawidd6/reusable-workflows/.github/workflows/npm-updates.yml@master` (branch `master` is mutable)

Replace each with a full 40-character commit SHA, e.g. `uses: actions/checkout@<40-char-sha> # v7`.

Locations:

- `.github/workflows/test.yml:23`
- `.github/workflows/npm-updates.yml:8`

### missing-permissions (severity: medium)

Neither `.github/workflows/test.yml` nor `.github/workflows/npm-updates.yml` declares a top-level `permissions:` block, and no job in either file has a job-level `permissions:` block. Without explicit permissions, the default GITHUB_TOKEN permissions apply (which may be overly broad depending on repository settings). Add a top-level `permissions: {}` or the minimal required scopes to each workflow.

Locations:

- `.github/workflows/test.yml:1`
- `.github/workflows/npm-updates.yml:1`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions

**Notes:**

Fixed both workflow files:

1. `.github/workflows/test.yml`:
   - Added `permissions: {}` top-level block
   - Pinned `actions/checkout@v7` → `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7`
   - Pinned `docker.io/axllent/mailpit:latest` container image to digest `sha256:98b916bd3c8d61f7633a52d3ea2f58d00620cb01ca57ab59edde68c347a95365`

2. `.github/workflows/npm-updates.yml`:
   - Added `permissions: {}` top-level block
   - Pinned `dawidd6/reusable-workflows/.github/workflows/npm-updates.yml@master` → `@eef24d408f08a926601a42fd4051807bcf3d3569 # master`

