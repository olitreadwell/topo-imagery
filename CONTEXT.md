# linz/topo-imagery context
> refreshed 2026-10-01 | upstream default: master @ f0a1794566409c66bcf18a6fa99089e0652321a1

Upstream moved 3 commits since the 2026-09-30 refresh: `0fb3b3a` fix: raise clear error when intermediate files disappear TDE-2099 (#1665), `c546acd` revert: streaming file copies (#1663), `f0a1794` release: 9.0.3 (#1669). None touch the docstring lines below. Upstream still has ZERO open issues (2026-10-01); open upstream PRs are dependabot bumps plus in-flight #1655 (rename), #1654 and #1668 (drafts).

## Identity & policies
- upstream: linz/topo-imagery — renamed on GitHub to `linz/geoprocessor` (same repo; `repos/linz/topo-imagery` redirects). Default branch `master`, primary language Python, English-first (yes — README/CONTRIBUTING in English).
- repo renamed topo-imagery -> geoprocessor (PR #1655 in flight; packages already renamed to `geoprocessor-*` in #1649). Fork `olitreadwell/topo-imagery` tracks it.
- CLA/DCO: none (no CLA bot, no DCO; vetted policy cla_required=false, dco_required=false)
- AI-assisted PR policy: unstated (bans_ai=false, ai_disclosure_required=false)
- signed commits required: no (vetted policy signed_commits_required=false)
- PR template: `.github/pull_request_template.md` (Motivation / Modifications / Verification)
- external tracker: GitHub issues; tickets referenced as `TDE-####` in branch names/commits
- org: LINZ (Land Information New Zealand) — govtech, NZ

Note: prior runs referenced `scripts/*.py` at repo root. Code now lives under `packages/geoprocessor-*/src/…` after #1649, so re-locate paths when re-checking old fixes (e.g. the duplicate hillshade log fix from PR #12 is now in `packages/geoprocessor-raster/src/geoprocessor_raster/generate_hillshade.py`).

## Conventions (verified from merged PRs)
- branch naming: `type/kebab-description-tde-####` (e.g. `fix/no-valid-pixels-tde-1990`, `feat/Title-generation-...-TDE-2010`, `ci/...-tde-2021`, `refactor/...-tde-1920`); release-please uses `release-please--branches--master`
- commit style: Conventional Commits (`fix:`, `feat:`, `refactor:`, `build:`, `ci:`, `chore:`); `.gitlint` enforces it
- test command: `pytest` (per-package `test/` dirs); lint: black, isort, mypy, pylint, prettier (pre-commit)
- CI: GitHub Actions (`Format and Tests` workflow, plus `Pull Request lint` and `Containers`) — substantive checks run on the fork. Note: the old `Build` workflow no longer exists, so badges/links naming `Build` are stale.
- outside PRs merge: responsive; recent external merges 60d = 14; maintainers review small PRs

## Maintainer picture
- active maintainers: LINZ team; recent merged PRs by maintainers (feat/refactor/ci) and dependabot
- areas actively worked: bigtiff support, STAC package refactor, PDAL package, release-please token automation
- in-flight maintainer/contributor PRs to avoid: #1655 rename topo-imagery->geoprocessor (repo-wide), #1654 tunable COG creation options, #1524 temporary gdal info / check-pixel-size, #1493 river DEM nodata, #1461 bulk gdalinfo, #1651 tini entrypoint

## Issue-area health
- confirmed 2026-09-25: upstream has ZERO open issues (dependabot bumps are PRs, not issues); no maintainer-engaged open issue survives -> self-found gap via repo-audit
- no open good-first-issue/help-wanted issues

## Gap ledger (dedupe — READ FIRST, never re-pick)
- `2026-08-05` PR #1 (test-coverage, str_to_positive_int) — pr-opened; superseded by PR #2
- `2026-08-05` PR #2 (bug-fix-combined-story, harden CLI arg parsers) — pr-opened-green; promote #2, close #1
- `2026-08-26` PR #6 (bug-fix) — pr-opened; body updated in audit sweep
- `2026-09-09` self-found trivial pass (typos + stale command/link in README/CONTRIBUTING + docstring typos) — pr-opened
- `2026-09-09` self-found bug-fix (duplicate `generate_hillshade_start` log line in scripts/generate_hillshade.py main()) — pr-opened

- `2026-09-25` PR #17 (bug-fix: charcodeat error message reported `type(int)` instead of actual `index` type) — pr-opened; fork CI green; 1-line fix + regression test
- `2026-09-30` self-found trivial pass (8 genuine fixes, 5 files: dependabot link `network/updates`->`network/dependencies`, README grammar x2, CONTRIBUTING "make researches"->"do research", `wellingon`->`wellington` doctest, `a a` docstring, "unexisting" test comment, "the the" docstring) — pr-opened (PR #19)
- `2026-10-01` self-found trivial pass (9 grammar/article fixes, 5 files, all distinct from PR #19: `as its not`->`as it's not` x2 and `a alpha`->`an alpha` x2 in gdal_commands.py; `a alpha band`->`an alpha band` + `int 512x512px`->`into` in gdal_presets.py; `an stderr`->`a stderr` in gdal_helper.py; `a end date`->`an end date` in stac item.py; `a invalid band count`->`an invalid` in file_tiff_test.py) — pr-opened (PR #20)
## Mined gaps (discovered, not yet attempted)
- `2026-09-09` README/CONTRIBUTING typos + stale command/link + docstring typos (7 fixes, 5 files) — pr-opened (PR #11)
- `2026-09-09` clean-code duplicate `generate_hillshade_start` log line emitted twice in scripts/generate_hillshade.py main() (introduced 6ce42f15, TDE-1441 #1301); repro: grep -c generate_hillshade_start == 2; expected 1 — pr-opened (PR #12)
- `2026-09-25` clean-code `charcodeat()` in packages/geoprocessor-gdal/src/geoprocessor_gdal/tile/util.py raises an error that reports `type(int)` instead of the actual type of `index`. Repro: `charcodeat("A", "0")` -> "…received <class 'str'> and <class 'type'>." (wrong); expected to name the real index type (a str). Verifiable in pure Python, no GDAL. Dedupe: `rg type(int)` unique in repo; no upstream issue/PR touches it — status: attempted (PR #17)
- `2026-09-30` docs: README badge still points at the removed `Build` workflow (`workflows/Build/badge.svg` renders "Build - no status"); current workflow is `Format and Tests` (badge 200 "passing"). Left out of PR #19 as the which-workflow choice is a maintainer call — status: proposed
- `2026-10-01` grammar: `fs_s3.py` has four `a AWS S3`/`a AWS s3` docstring articles that should be `an AWS S3` (lines ~24, 90, 126, 164). NOT fixed in PR #20 to keep zero file overlap with the open PR #19 (which also edits fs_s3.py). Re-check once #19 closes — status: proposed
