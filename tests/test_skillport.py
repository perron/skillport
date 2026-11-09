from __future__ import annotations

import json
from pathlib import Path

import skillport.cli as sp


def write_skill(root: Path, name: str, body: str = "Do the thing.\n", filename: str = "SKILL.md") -> Path:
    folder = root / name
    folder.mkdir(parents=True)
    (folder / filename).write_text(
        f"---\nname: {name}\ndescription: Demo skill used when testing {name}.\n---\n\n{body}",
        encoding="utf-8",
    )
    return folder


def test_install_copy_and_link(tmp_path, capsys):
    skill = write_skill(tmp_path, "tidy-notes")
    project = tmp_path / "proj"
    project.mkdir()
    assert sp.main(["install", str(skill), "--root", str(project), "--agents", "claude,agents"]) == 0
    copied = project / ".claude" / "skills" / "tidy-notes" / "SKILL.md"
    linked_parent = project / ".agents" / "skills"
    assert copied.is_file()
    assert sp.main(["install", str(skill), "--root", str(project), "--agents", "cursor", "--link"]) == 0
    dest = project / ".cursor" / "skills" / "tidy-notes"
    assert dest.is_symlink()
    assert dest.resolve() == skill.resolve()


def test_status_detects_drift(tmp_path, capsys):
    skill = write_skill(tmp_path, "tidy-notes", body="version one\n")
    project = tmp_path / "proj"
    project.mkdir()
    sp.main(["install", str(skill), "--root", str(project), "--agents", "claude,copilot"])
    drifted = project / ".github" / "skills" / "tidy-notes" / "SKILL.md"
    drifted.write_text(drifted.read_text() + "\nextra line\n", encoding="utf-8")
    code = sp.main(["status", "--root", str(project), "--agents", "claude,copilot"])
    assert code == 2
    out = capsys.readouterr().out
    assert "drift detected" in out
    assert "tidy-notes" in out


def test_sync_repairs_drift(tmp_path, capsys):
    skill = write_skill(tmp_path, "tidy-notes", body="canonical\n")
    project = tmp_path / "proj"
    project.mkdir()
    sp.main(["install", str(skill), "--root", str(project), "--agents", "claude,copilot"])
    (project / ".github" / "skills" / "tidy-notes" / "SKILL.md").write_text("stale\n")
    assert sp.main(["sync", str(skill), "--root", str(project), "--agents", "claude,copilot"]) == 0
    assert sp.main(["status", "--root", str(project), "--agents", "claude,copilot"]) == 0
    out = capsys.readouterr().out
    assert "no drift" in out


def test_status_json_and_agents(capsys):
    assert sp.main(["agents"]) == 0
    out = capsys.readouterr().out
    assert ".claude/skills" in out
    assert ".github/skills" in out


def test_missing_skill_md(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    assert sp.main(["install", str(empty), "--root", str(tmp_path)]) == 1


def test_tree_hash_stable(tmp_path):
    a = write_skill(tmp_path, "tidy-notes")
    b = tmp_path / "copy"
    b.mkdir()
    (b / "SKILL.md").write_text((a / "SKILL.md").read_text())
    assert sp.tree_hash(a) == sp.tree_hash(b)
    (b / "SKILL.md").write_text((b / "SKILL.md").read_text() + "x")
    assert sp.tree_hash(a) != sp.tree_hash(b)
