<!-- markdownlint-disable -->

# Hardening Report: dawidd6--action-send-mail/v16

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **dawidd6--action-send-mail/v16** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Workflow files reference actions/reusable workflows using mutable tag or branch refs instead of pinned 40-character commit SHAs. This exposes the workflow to supply-chain attacks if the referenced ref is updated maliciously.

- `.github/workflows/test.yml`: `uses: actions/checkout@v6` — `@v6` is a mutable tag, not a SHA.
- `.github/workflows/npm-updates.yml`: `uses: dawidd6/reusable-workflows/.github/workflows/npm-updates.yml@master` — `@master` is a mutable branch, not a SHA.

Locations:

- `.github/workflows/test.yml:20`
- `.github/workflows/npm-updates.yml:6`

### missing-permissions (severity: medium)

Neither workflow file defines a `permissions:` block at the top level or at the job level. Without explicit permissions, workflows run with the default (potentially broad) token permissions. Both `test.yml` and `npm-updates.yml` are missing any `permissions:` declaration.

Locations:

- `.github/workflows/test.yml:1`
- `.github/workflows/npm-updates.yml:1`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions

**Notes:**

Fixed both workflow files:
- test.yml: Added `permissions: {}` at the top level; pinned `actions/checkout@v6` to `actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6`.
- npm-updates.yml: Added `permissions: {}` at the top level; pinned `dawidd6/reusable-workflows/.github/workflows/npm-updates.yml@master` to `@eef24d408f08a926601a42fd4051807bcf3d3569 # master`.

