# linz/topo-imagery context
> refreshed 2026-10-10 | upstream default: master @ 4a82c365add948abfbd754d0bcc9032e11b335c3

Upstream moved on since the 2026-10-06 refresh: the repo/project rename landed and was released as 10.0.0 — `42e5ad3` refactor!: rename topo-imagery repo, project and container TDE-2073 TDE-2008 (#1655), `d52628e` pass through geoprocessor package version from scripts TDE-2073 (#1672), `c573ccb` split processing package TDE-2073 (#1678), `4a82c36` release: 10.0.0 (#1682). Upstream still has ZERO open issues (re-confirmed 2026-10-10). Open upstream PRs are dependabot bumps plus in-flight maintainer work #1685 (pointcloud standardising poc, draft), #1684 (argparse empty capture area fix), #1683 (16-bit RGB rescale), #1654 (tunable COG creation options, draft), #1524, #1493, #1461.

## Identity & policies
- upstream: linz/geoprocessor — renamed on GitHub from `linz/topo-imagery` (same repo; `repos/linz/topo-imagery` still redirects, and Oli's fork is still named `olitreadwell/topo-imagery`). Default branch `master`, primary language Python, English-first (yes — README/CONTRIBUTING in English).
- the rename has now LANDED (PR #1655 merged, released in 10.0.0): code lives under `packages/geoprocessor-*/src/geoprocessor_*/…`, there is no `scripts/` directory any more, and the container/project name is `geoprocessor`.
- CLA/DCO: none (no CLA bot, no DCO; vetted policy cla_required=false, dco_required=false)
- AI-assisted PR policy: unstated (bans_ai=false, ai_disclosure_required=false)
- signed commits required: no (vetted policy signed_commits_required=false)
- PR template: `.github/pull_request_template.md` (Motivation / Modifications / Verification)
- external tracker: GitHub issues; tickets referenced as `TDE-####` in branch names/commits
- org: LINZ (Land Information New Zealand) — govtech, NZ

Note: prior runs referenced `scripts/*.py` at repo root. That directory is gone after #1655/#1678, so re-locate paths when re-checking old fixes (e.g. the duplicate hillshade log fix from PR #12 now sits in `packages/geoprocessor-raster/src/geoprocessor_raster/generate_hillshade.py`, and the new `packages/geoprocessor-processing/` package holds the split-out processing code).

## Conventions (verified from merged PRs)
- branch naming: `type/kebab-description-tde-####` (e.g. `fix/no-valid-pixels-tde-1990`, `feat/Title-generation-...-TDE-2010`, `ci/...-tde-2021`, `refactor/...-tde-1920`); release-please uses `release-please--branches--master`
- commit style: Conventional Commits (`fix:`, `feat:`, `refactor:`, `build:`, `ci:`, `chore:`); `.gitlint` enforces it
- test command: `pytest` (per-package `test/` dirs); lint: black, isort, mypy, pylint, prettier (pre-commit)
- CI: GitHub Actions (`Format and Tests` workflow, plus `Pull Request lint` and `Containers`) — substantive checks run on the fork. Note: the old `Build` workflow no longer exists, so badges/links naming `Build` are stale.
- CI pins Python `3.12.3` (`.github/workflows/format-tests.yml`); local `uv` may pick a newer 3.12.x, where the unrelated `test_should_pass_with_empty_supplied_capture_area_and_capture_dates` (raster) fails on clean master — pin `--python 3.12.3` locally to reproduce CI.
- outside PRs merge: responsive; recent external merges 60d = 14; maintainers review small PRs

## Maintainer picture
- active maintainers: LINZ team; recent merged PRs by maintainers (feat/refactor/ci) and dependabot
- areas actively worked: bigtiff support, STAC/processing package refactor, PDAL package, release-please token automation, 16-bit RGB rescale
- in-flight maintainer/contributor PRs to avoid: #1685 pointcloud standardising poc (draft), #1684 argparse empty capture area, #1683 16-bit RGB rescale, #1654 tunable COG creation options (draft), #1524 temporary gdal info / check-pixel-size, #1493 river DEM nodata, #1461 bulk gdalinfo

## Issue-area health
- confirmed 2026-10-10: upstream has ZERO open issues (dependabot bumps are PRs, not issues); no maintainer-engaged open issue survives -> self-found gap via repo-audit
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
- `2026-10-03` self-found trivial pass (8 docstring fixes, 5 files, distinct from PR #20: `fix_laz_header.run_pdal_fix_laz_header` Returns text restored from hillshade wording to "the list of fixed LAZ file paths"; `whereas`->`whether` in `collection.update_extent`; `tiffs files`->`tiff files` in `standardising.create_vrt`; `is simplify`->`is simplified` in `capture_area.merge_polygons`; `a AWS S3/s3`->`an AWS S3/s3` x4 in `fs_s3.py`) — pr-opened (PR #21)
- `2026-10-04` self-found trivial pass (6 meaning-preserving fixes, 4 files, all distinct lines from open PR #20: README GitHub Actions badge points at the removed `Build` workflow (rendered "Build - no status") -> current `Format and Tests` workflow; `generate_hillshade.get_args_parser` `--from-file` help example used JSON key `inputs` but `get_tile_files` reads `input` (runtime-verified KeyError); `aws_credential_source.CredentialSource` unbalanced quote on `type` docstring + `default 1 hours`->`default 1 hour`; `file_tiff_test` `a invalid`->`an invalid` x2 on the invalid_4/invalid_5 descriptions) — pr-opened (PR #22)
- `2026-10-06` self-found trivial pass (6 meaning-preserving fixes, 5 files, ALL distinct lines from open PR #22/#17/#12/#6 — each re-fetched live and re-checked: `.gitlint` configuration + rules comment links both HTTP 404 -> current gitlint docs site (`jorisroovers.com/gitlint/latest/configuration/` and `.../rules/`, both HTTP 200) x2; `aws_helper.parse_path` docstring `A S3 path` -> `An S3 path` (PR #22 only edits line ~100); `fs_s3.list_files_in_uri` docstring `from a s3 path` -> `from an s3 path` (PR #22 edits line ~267 two lines below; simulated merge locally, no conflict); `collection_from_items` error message `uri is not a s3 path` -> `uri is not an s3 path` + matching assert in `collection_from_items_test.py`) — pr-opened (PR #23); PR #23 later CLOSED as superseded by #22 (same doc-cleanup theme folded into one PR)
- `2026-10-10` self-found bug-fix (repo-audit, s3/files): `fs_s3.exists()` returned `True` for ANY s3 prefix path ending in `/` with no matching objects — the guard was `if len(list(objects)) > 0`, and a `list_objects_v2` response is always a non-empty dict (it carries `ResponseMetadata`/`KeyCount` even when no key matches), so the branch always returned `True`; an empty bucket or a non-existent prefix looked like it existed. Fixed to `return "Contents" in objects` (boto3 omits `Contents` when nothing matches; real AWS and moto agree). Repro (moto): bucket + `exists("s3://testbucket/does-not-exist/")` -> `True` before, `False` after; also empty bucket -> `True` before, `False` after. 2 regression tests added in `packages/geoprocessor-common/test/files/fs_s3_test.py`, both verified FAILING on the unpatched file. Local verification on CI's Python 3.12.3: per-package `pytest --doctest-modules` all green (common 98, gdal 80, pdal 6, pointcloud 12, raster 7, stac 108) + `pre-commit run --all-files` black/isort/mypy/pylint/prettier/actionlint all Passed — pr-opened (PR #24)

## Mined gaps (discovered, not yet attempted)
- `2026-09-09` README/CONTRIBUTING typos + stale command/link + docstring typos (7 fixes, 5 files) — pr-opened (PR #11)
- `2026-09-09` clean-code duplicate `generate_hillshade_start` log line emitted twice in scripts/generate_hillshade.py main() (introduced 6ce42f15, TDE-1441 #1301); repro: grep -c generate_hillshade_start == 2; expected 1 — pr-opened (PR #12)
- `2026-09-25` clean-code `charcodeat()` in packages/geoprocessor-gdal/src/geoprocessor_gdal/tile/util.py raises an error that reports `type(int)` instead of the actual type of `index`. Repro: `charcodeat("A", "0")` -> "…received <class 'str'> and <class 'type'>." (wrong); expected to name the real index type (a str). Verifiable in pure Python, no GDAL. Dedupe: `rg type(int)` unique in repo; no upstream issue/PR touches it — status: attempted (PR #17)
- `2026-09-30` docs: README badge still points at the removed `Build` workflow (`workflows/Build/badge.svg` renders "Build - no status"); current workflow is `Format and Tests` (badge 200 "passing"). Left out of PR #19 as the which-workflow choice is a maintainer call — status: attempted (PR #22)
- `2026-10-01` grammar: `fs_s3.py` has four `a AWS S3`/`a AWS s3` docstring articles that should be `an AWS S3` (lines ~24, 90, 126, 164). Fixed in PR #21 (distinct lines from PR #20's `acces`->`access`) — status: attempted (PR #21)
- `2026-10-10` bug (same file/defect class as PR #24, deliberately NOT bundled — different function and symptom, one logical change per PR): `fs_s3.list_files_in_uri` iterates `for contents_data in response["Contents"]` on every `list_objects_v2` page; a page whose prefix matches nothing has no `Contents` key, so the call raises `KeyError` instead of returning `[]`. Repro (moto): `list_files_in_uri("s3://bucket/only-file.tiff", [".tif"], None)` or any prefix with zero matches -> KeyError. Fix shape: iterate `response.get("Contents", [])`. Verifiable with the existing moto-based `test_list_files_in_uri` pattern — status: proposed
