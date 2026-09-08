<!-- markdownlint-disable -->

# Hardening Report: dawidd6--action-send-mail/v20

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **dawidd6--action-send-mail/v20** was hardened automatically. 2 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Workflow files reference actions/reusable workflows using mutable tags or branch names instead of pinned full-length commit SHAs. This exposes the workflow to supply-chain attacks if the referenced ref is updated maliciously.

Failing references:
- `.github/workflows/test.yml`: `uses: actions/checkout@v7` (tag ref, not a SHA)
- `.github/workflows/npm-updates.yml`: `uses: dawidd6/reusable-workflows/.github/workflows/npm-updates.yml@master` (branch ref, not a SHA)

Locations:

- `.github/workflows/test.yml:21`
- `.github/workflows/npm-updates.yml:6`

### missing-permissions (severity: medium)

Neither workflow file defines a `permissions:` block at the top level or at the job level. Without explicit permissions, workflows run with the default (potentially broad) GITHUB_TOKEN permissions. Each workflow should declare minimal required permissions.

- `.github/workflows/test.yml`: no top-level or job-level `permissions:` key
- `.github/workflows/npm-updates.yml`: no top-level or job-level `permissions:` key

Locations:

- `.github/workflows/test.yml:1`
- `.github/workflows/npm-updates.yml:1`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, missing-permissions

**Notes:**

Fixed both workflow files: (1) Pinned actions/checkout@v7 to SHA 3d3c42e5aac5ba805825da76410c181273ba90b1 in test.yml; (2) Pinned dawidd6/reusable-workflows@master to SHA eef24d408f08a926601a42fd4051807bcf3d3569 in npm-updates.yml; (3) Added `permissions: {}` top-level block to both test.yml and npm-updates.yml to enforce least-privilege GITHUB_TOKEN permissions.

