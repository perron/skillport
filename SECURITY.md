# Security Policy

This project is a small local command-line tool. It does not phone home and does not require an API key.

## Reporting a vulnerability

Please open a [GitHub issue](https://github.com/perron/skillport/issues) and mention that it is a security report. Do not include secrets, tokens, or private file contents in the issue.

If the report includes a working exploit against this tool, describe the impact and a minimal reproduction without pasting live credentials.

## Notes for this tool

skillport copies or symlinks a skill folder into agent paths you choose. It will refuse skill names that contain path separators, so an untrusted SKILL.md cannot write outside the destination directory. Review a skill before installing it (see also skillguard).

## Supported versions

The `master` branch and the latest tagged release, when one exists, are supported.
