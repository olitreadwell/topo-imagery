# linz/topo-imagery context
> refreshed 2026-09-09 | upstream default: master @ d9ae752d1623dec9a9e8946ed90b8235cf190e5c

## Identity & policies
- upstream: linz/topo-imagery, default branch `master`, primary language Python, English-first (yes — README/CONTRIBUTING in English)
- CLA/DCO: none (no CLA bot, no DCO; vetted policy cla_required=false, dco_required=false)
- AI-assisted PR policy: unstated (bans_ai=false, ai_disclosure_required=false)
- signed commits required: no (vetted policy signed_commits_required=false)
- PR template: `.github/pull_request_template.md` (Motivation / Modifications / Verification)
- external tracker: GitHub issues; tickets referenced as `TDE-####` in branch names/commits
- org: LINZ (Land Information New Zealand) — govtech, NZ

## Conventions (verified from merged PRs)
- branch naming: `type/kebab-description-tde-####` (e.g. `fix/no-valid-pixels-tde-1990`, `feat/Title-generation-...-TDE-2010`, `ci/...-tde-2021`, `refactor/...-tde-1920`); release-please uses `release-please--branches--master`
- commit style: Conventional Commits (`fix:`, `feat:`, `refactor:`, `build:`, `ci:`, `chore:`); `.gitlint` enforces it
- test command: `pytest` (per-package `test/` dirs); lint: black, isort, mypy, pylint, prettier (pre-commit)
- CI: GitHub Actions (`Build` workflow) — substantive checks run on the fork
- outside PRs merge: responsive; recent external merges 60d = 14; maintainers review small PRs

## Maintainer picture
- active maintainers: LINZ team; recent merged PRs by maintainers (feat/refactor/ci) and dependabot
- areas actively worked: bigtiff support, STAC package refactor, PDAL package, release-please token automation

## Issue-area health
- open issues are mostly dependabot bumps + feature/refactor issues (TDE-####); no trivial typo/link issues open
- no open good-first-issue/help-wanted issues

## Gap ledger (dedupe — READ FIRST, never re-pick)
- `2026-08-05` PR #1 (test-coverage, str_to_positive_int) — pr-opened; superseded by PR #2
- `2026-08-05` PR #2 (bug-fix-combined-story, harden CLI arg parsers) — pr-opened-green; promote #2, close #1
- `2026-08-26` PR #6 (bug-fix) — pr-opened; body updated in audit sweep
- `2026-09-09` self-found trivial pass (typos + stale command/link in README/CONTRIBUTING + docstring typos) — pr-opened
- `2026-09-09` self-found bug-fix (duplicate `generate_hillshade_start` log line in scripts/generate_hillshade.py main()) — pr-opened

## Mined gaps (discovered, not yet attempted)
- `2026-09-09` README/CONTRIBUTING typos + stale command/link + docstring typos (7 fixes, 5 files) — pr-opened (PR #11)
- `2026-09-09` clean-code duplicate `generate_hillshade_start` log line emitted twice in scripts/generate_hillshade.py main() (introduced 6ce42f15, TDE-1441 #1301); repro: grep -c generate_hillshade_start == 2; expected 1 — status: attempted
