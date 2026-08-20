# Automated release process

## How it works

1. Normal changes are merged into `main` using Conventional Commit messages.
2. `.github/workflows/release-please.yml` creates or updates one Release Please PR.
3. That PR contains the next version and generated `CHANGELOG.md` changes.
4. A maintainer reviews and merges the release PR.
5. Release Please creates the version tag and a draft GitHub Release.
6. The same workflow checks the tagged source on Windows, macOS, and Linux.
7. If every check succeeds, it builds the wheel, sdist, FreeCAD ZIP, and checksums.
8. The artifacts are attached and the draft is published. A failure leaves the release as a draft.

The separate `Release build dry run` workflow can be started manually at any time. It performs
the full matrix and uploads workflow artifacts but never creates a tag or public release.

## One-time repository setup

1. Create `https://github.com/Lumitorus/freecad-mcp-next` with `main` as its default branch.
2. Open **Settings → Actions → General → Workflow permissions**.
3. Enable **Read and write permissions** and allow GitHub Actions to create pull requests.
4. Recommended: create a fine-grained token for this repository with read/write access to
   Contents, Issues, and Pull requests. Save it as the Actions secret
   `RELEASE_PLEASE_TOKEN`.
5. Protect `main` and require the CI checks after confirming that Release Please PRs trigger CI.
6. If publishing to PyPI, configure Trusted Publishing for the protected `pypi` environment,
   then enable the commented publish step in `release-please.yml`.

The workflow falls back to the built-in `GITHUB_TOKEN` if `RELEASE_PLEASE_TOKEN` is absent.
That fallback can create the release PR and complete releases, but GitHub suppresses new workflow
runs caused by resources created with `GITHUB_TOKEN`. The dedicated token is therefore recommended
when CI checks are required directly on the generated release PR.

## Commit format

Release Please derives semantic versions from commits on `main`:

```text
fix: correct FreeCAD 1.1 profile detection       -> patch
feat: add a new MCP tool                         -> minor
feat!: change the tool request schema            -> major
docs: document another supported MCP client      -> changelog entry
deps: update MCP SDK                              -> dependency entry
```

Prefer squash merging and give the pull request a Conventional Commit title. For example:

```text
feat: add Continue and Ollama integration
```

The manifest is bootstrapped at `0.1.0`, while the project sources are prepared for `0.2.0`.
Therefore the first releasable `feat:` commit is intended to produce the initial `v0.2.0`
release PR. After that merge, Release Please updates the manifest automatically.

## Normal release

Do not edit versions or create tags by hand. Review the automatically maintained Release Please
PR and merge it when the proposed version and changelog are correct. The release pipeline handles
the rest.

To force a specific version in an exceptional commit, use a commit body footer:

```text
Release-As: 0.3.0
```

This should be exceptional; the normal `fix:`/`feat:` rules are preferred.
