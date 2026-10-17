# Public Repository and Data-Lake Publication Review

Date: 2026-10-18  
Scope: focused remote repository review; local PowerShell results pending  
Branch for this review: `audit/publication-boundary-audit-2026-10-18`

## Evidence boundary

Repository metadata reports that `guruPrasath4707/Neer-Nilam` is public, with `main` as the default branch and repository size reported as 340 KB at the time checked. This was a focused review of selected files and search results, not a complete Git object, binary, LFS, local filesystem, or secret scan.

Compared branch heads:
- `main`: `bd57f0713546d1cb386a754c7c74fbb237b2a695`
- `feat/scene-pack-builder-v0`: `26d509a5cdfe33c5f456f18ad631d5ff4632dcf4`
- Common base: `bb2f49ac3b8c0db5aee933f00ac844e92cb8cd6d`

GitHub's compare result reported the feature branch as 68 commits ahead and 2 behind main. The branch histories have diverged; do not merge, rebase or force-push without reviewing the two main-only commits and the local working tree.

## Publication decision

**Do not upload the entire raw data lake to this public Git repository.**

This agrees with the checked-in repository policy:
- The root README says raw datasets should remain on the external data drive unless redistribution rights are explicitly cleared.
- `data/README.md` says large raw source dumps do not belong in Git by default.
- `data/assets/README.md` says the asset directory is for metadata and that large source media/model files should not be committed there by default.

The repository should publish code, schemas, manifests, source links, checksums, test fixtures, attribution/licence metadata, validation scripts and reproducible download instructions. Large raw datasets should remain at authoritative upstream locations or a suitable external data repository. Publish only reviewed derivatives whose specific source terms permit the intended redistribution.

Important holds:
- DHARMA Tamil Nadu and SII remain rights-gated pending authoritative clarification of the README/XML licence conflict and records without detected licence targets.
- The CGWB 2024–2025 yearbook is not recorded as acquired and validated; catalogue discovery is not a valid PDF.
- The Season and Crop Report and Statistical Handbook PDF terms must be reviewed before rehosting.
- OSM, HydroRIVERS, WorldCover and CHIRPS still require their source-specific attribution and intended-use requirements to be recorded.

GitHub's official guidance checked on 2026-10-18:
- [Large files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github): a file above 50 MiB triggers a warning and files above 100 MiB are blocked in ordinary Git.
- [Repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits): large repository histories increase clone and Git-operation costs.
- [Git LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage): LFS stores pointers in Git and payloads separately; it does not resolve licensing or publication permission.

## Remote review findings

1. **No evidence of bulk raw data in the reviewed repository records.** The size reported by GitHub and the inspected manifest/script-oriented content suggest the full external data lake has not been mirrored into ordinary Git. This is not a categorical conclusion: an exhaustive tree/LFS audit was not performed.
2. **Ignore rules are narrow.** The feature-branch `.gitignore` covers Python cache files and generated flat-viewer HTML, not general accidental dataset additions. Propose carefully scoped guards or a size/provenance pre-commit check after reviewing local status; do not blanket-ignore `data/`, which contains versioned schemas and evidence records.
3. **No root `LICENSE` was found at the queried path** on main or the feature branch. Decide an explicit licence for project-authored code/documentation before inviting reuse. Dataset licenses must remain separate. [GitHub explains repository licensing](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).
4. **Current project status wording needs clarification.** The root README says application implementation has not started, while `data/README.md` documents an executable scene-pack resolver/builder and flat viewer. Clarify whether “application” means the full application or whether the status statement is outdated.
5. **Privacy review remains warranted.** Some public logs/instructions contain local machine path details. These are not credentials but may unnecessarily expose environment information. Use portable placeholders in future docs; preserve historical records and correct additively rather than rewriting history.
6. A few targeted code-search probes found no matches for selected common secret-like strings. This is not a complete secret scan.

## Integrity evidence

The checked-in historical audit `docs/audits/storage-integrity-audit-20261010-095110.csv` records 581/581 initial-manifest checks, 120/120 CHIRPS files and 7/7 critical assets passing in the October 10 audit.

Separately, the operator reported a fresh read-only check on October 18: 581/581, 120/120 and 7/7 PASS. This remote review did not reproduce the local checks. These results show agreement with recorded size/hash values, not publisher authenticity, scientific fit or reuse permission. Do not sum the sets as a unique-file total without comparing their actual paths.

The PowerShell session underway was not visible to this remote review. Incorporate its output only after it is supplied and reconciled against local Git status; no local changes are assumed here.

## Safe next steps

1. Capture and inspect local `git status --short --branch`, latest commit and all modified/untracked paths.
2. Compare the local branch with its actual remote head before any push. Preserve the two `012138` CHIRPS metadata files until their disposition is decided.
3. Review the branch divergence and run the applicable tests before integration. Do not merge the 68-commit feature line blindly.
4. Add appropriate raw-data guardrails and an explicit project-code licence only after review.
5. Keep data publishing source-specific: use upstream links and reproducible manifests by default; publish binaries only with clear, item-specific redistribution permission and appropriate size/hosting decisions.

No dataset payloads were uploaded, no licence hold was changed, and this review did not inspect the operator's local filesystem.
