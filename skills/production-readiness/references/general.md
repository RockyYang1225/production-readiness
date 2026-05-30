# General Readiness

Check whether the project can be understood, installed, run, maintained, and handed off.

## Evidence To Look For

- Clear README with purpose, setup, run, test, and deployment notes.
- License file for public release.
- Reproducible dependency files such as lockfiles, `pyproject.toml`, `requirements.txt`, `go.mod`, or `Cargo.lock`.
- Environment variable documentation and a safe example file.
- Maintainer ownership, release notes, roadmap, or issue tracker.
- Clear boundaries between source, generated files, tests, docs, and build output.

## Findings To Flag

- Missing setup instructions or commands that cannot be reproduced.
- Undocumented environment variables.
- Missing license for a public repository.
- Stale dependencies or ambiguous package manager usage.
- Generated artifacts committed without explanation.
- No stated owner for production operation.

## Ready Evidence

The project is generally ready only when a fresh user can identify what it does, install it, run it, test it, and understand how releases are managed.
