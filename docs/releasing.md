# Release process

## One-time repository setup

1. Create an empty GitHub repository and push this project to its `main` branch.
2. Verify the `Lumitorus/freecad-mcp-next` URLs in `pyproject.toml` and `package.xml`.
3. Protect `main` and require the `CI / test` and `CI / package` checks.
4. Add the repository to the FreeCAD addon index after the first stable release.
5. If publishing to PyPI, create the project and configure GitHub trusted publishing for
   the `pypi` environment; then enable the commented publish step in `release.yml`.

## Create a release

1. Update the version in `pyproject.toml` and `package.xml`.
2. Update `CHANGELOG.md` and the package date.
3. Run the local checks from `CONTRIBUTING.md`.
4. Merge through a pull request.
5. Create and push a matching tag, for example `v0.2.0`.

The release workflow checks that the tag and both metadata versions match. It builds the
Python wheel/sdist and the FreeCAD addon ZIP, writes SHA-256 files, and creates a GitHub
Release. No release is published from an untagged branch build.
