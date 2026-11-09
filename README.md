# skillport

Write one agent skill folder, install it into Claude Code, Cursor, Codex, and
GitHub Copilot paths, and catch copies that have drifted apart.

Same-skill-in-three-tools copy drift is a complaint that showed up on X in
early November 2026. skillport is an original, clean-room tool for that job.
It is not a fork of the Vercel Skills CLI or of any skill manager.

## Install

Python 3.10 or later.

From a checkout:

```bash
python3 -m pip install .
python3 -m pip install -e ".[dev]"  # optional, for tests
skillport --help
```

Or without installing:

```bash
PYTHONPATH=. python3 -m skillport --help
```

## 30-second example

```bash
mkdir -p my-skill
cat > my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: Demo skill used when you want a single portable SKILL.md.
---

Remind the user to keep one canonical copy of this skill.
EOF

skillport install ./my-skill --root . --agents claude,agents,copilot,cursor
skillport status --root .
```

`install --link` puts a symlink at each path so one edit updates every agent.
`status` exits `2` if two copies of the same skill name have different content.
`sync` overwrites those copies from a canonical folder.

Default project paths:

| Agent | Path |
|---|---|
| claude | `.claude/skills` |
| agents | `.agents/skills` |
| copilot | `.github/skills` |
| cursor | `.cursor/skills` |
| codex | `.codex/skills` |

`--global` uses the matching folder under your home directory (Copilot has no
default user path). `--target DIR` writes to a single folder instead.

## Credit

Inspired by public reports of cross-agent skill drift and by GitHub's documented
Copilot skill paths (`.claude/skills`, `.github/skills`, `.agents/skills`). No
source was copied from those tools or posts.

## Limits

- Default paths follow public docs and common conventions; they may lag a vendor change. Use `--target` to override.
- `status` detects drift by hashing file contents. It does not watch for live edits.
- Skill names with path separators (`/` or `\\`) are refused so an untrusted frontmatter `name` cannot write outside the destination directory.
- `--global` uses folders under your home directory. Copilot has no default user-level path.

From GitHub you can also install with:

```bash
python3 -m pip install git+https://github.com/perron/skillport.git
```

This package is not published to PyPI.

## License

MIT. See `LICENSE`. Please read `SECURITY.md` before filing a vulnerability report.
