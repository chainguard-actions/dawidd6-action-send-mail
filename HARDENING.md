<!-- markdownlint-disable -->

# Hardening Report: dawidd6--action-send-mail/v17

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **dawidd6--action-send-mail/v17** was hardened automatically. 3 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Workflow files reference actions/reusable workflows by mutable tag or branch names instead of full 40-character commit SHAs. This exposes the workflow to supply-chain attacks if the referenced tag or branch is updated with malicious code.

- `.github/workflows/test.yml`: `uses: actions/checkout@v6` (tag reference)
- `.github/workflows/npm-updates.yml`: `uses: dawidd6/reusable-workflows/.github/workflows/npm-updates.yml@master` (branch reference)

Locations:

- `.github/workflows/test.yml:22`
- `.github/workflows/npm-updates.yml:6`

### hardcoded-credentials (severity: high)

A literal password value `test` is hardcoded in `.github/workflows/test.yml` under the `password:` input field. Even though this is a dummy credential for a local mailpit test server, hardcoded credentials in workflow files are a security anti-pattern and can be mistakenly reused or escalated. The value matches the pattern: `password: test`.

Locations:

- `.github/workflows/test.yml:33`

### missing-permissions (severity: medium)

Neither workflow file defines a top-level `permissions:` block, and no individual job within them defines job-level `permissions:`. Without explicit permission scoping, jobs run with the default token permissions (which may include broad write access depending on repository settings), violating the principle of least privilege.

- `.github/workflows/test.yml`: no top-level or job-level `permissions:` key
- `.github/workflows/npm-updates.yml`: no top-level or job-level `permissions:` key

Locations:

- `.github/workflows/test.yml:1`
- `.github/workflows/npm-updates.yml:1`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, hardcoded-credentials, missing-permissions

**Notes:**

Fixed all three findings across both workflow files:
1. unpinned-uses: Pinned `actions/checkout@v6` → `actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6` in test.yml; pinned `dawidd6/reusable-workflows/.github/workflows/npm-updates.yml@master` → `@eef24d408f08a926601a42fd4051807bcf3d3569 # master` in npm-updates.yml.
2. hardcoded-credentials: Replaced hardcoded `password: test` with `${{ secrets.MAILPIT_PASSWORD }}` in test.yml.
3. missing-permissions: Added `permissions: {}` top-level block to both test.yml and npm-updates.yml to enforce least-privilege.

