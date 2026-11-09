# skillport proof

Captured 2026-11-09 13:40 PST (America/Los_Angeles).

Fresh-venv install: `pip install .` succeeded and `skillport --version` printed `skillport 0.1.2`.

Tests: 25 passed in 0.08s

## version
```
skillport 0.1.2
```

## agents
```
agent	project path	user path
claude	.claude/skills	~/.claude/skills
fable	.claude/skills	~/.claude/skills
agents	.agents/skills	~/.agents/skills
copilot	.github/skills	(none)
cursor	.cursor/skills	~/.cursor/skills
codex	.codex/skills	~/.codex/skills
grok	.grok/skills	~/.grok/skills
```

## install + status (`--agents claude,fable,grok,cursor`)
```
installed my-skill -> /tmp/ai-tools-proof/skillport-012/.claude/skills/my-skill (copy; agents: claude, fable)
installed my-skill -> /tmp/ai-tools-proof/skillport-012/.grok/skills/my-skill (copy)
installed my-skill -> /tmp/ai-tools-proof/skillport-012/.cursor/skills/my-skill (copy)
agent	name	kind	hash	path
claude	my-skill	copy	47df1b91ec8f	/tmp/ai-tools-proof/skillport-012/.claude/skills/my-skill
fable	my-skill	copy	47df1b91ec8f	/tmp/ai-tools-proof/skillport-012/.claude/skills/my-skill
grok	my-skill	copy	47df1b91ec8f	/tmp/ai-tools-proof/skillport-012/.grok/skills/my-skill
cursor	my-skill	copy	47df1b91ec8f	/tmp/ai-tools-proof/skillport-012/.cursor/skills/my-skill
no drift
```
