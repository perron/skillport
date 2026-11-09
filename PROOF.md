# skillport proof

Captured 2026-11-09 13:26 PST.

Fresh-venv install: `pip install .` succeeded and `skillport --version` printed `skillport 0.1.1`.

Tests: 17 passed in 0.04s

## agents
```
agent	project path	user path
claude	.claude/skills	~/.claude/skills
agents	.agents/skills	~/.agents/skills
copilot	.github/skills	(none)
cursor	.cursor/skills	~/.cursor/skills
codex	.codex/skills	~/.codex/skills
```

## install + status
```
installed my-skill -> /tmp/ai-tools-proof/skillport/.claude/skills/my-skill (copy)
installed my-skill -> /tmp/ai-tools-proof/skillport/.agents/skills/my-skill (copy)
installed my-skill -> /tmp/ai-tools-proof/skillport/.github/skills/my-skill (copy)
installed my-skill -> /tmp/ai-tools-proof/skillport/.cursor/skills/my-skill (copy)
agent	name	kind	hash	path
claude	my-skill	copy	47df1b91ec8f	/tmp/ai-tools-proof/skillport/.claude/skills/my-skill
agents	my-skill	copy	47df1b91ec8f	/tmp/ai-tools-proof/skillport/.agents/skills/my-skill
copilot	my-skill	copy	47df1b91ec8f	/tmp/ai-tools-proof/skillport/.github/skills/my-skill
cursor	my-skill	copy	47df1b91ec8f	/tmp/ai-tools-proof/skillport/.cursor/skills/my-skill
no drift
```
