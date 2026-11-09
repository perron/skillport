from __future__ import annotations

import json
from pathlib import Path

import pytest

import skillport.cli as sp


def write_skill(root: Path, name: str, body: str = "Do the thing.\n", filename: str = "SKILL.md", frontmatter_name: str | None = None) -> Path:
    folder = root / name
    folder.mkdir(parents=True, exist_ok=True)
    fm_name = name if frontmatter_name is None else frontmatter_name
    (folder / filename).write_text(
        f"---\nname: {fm_name}\ndescription: Demo skill used when testing {name}.\n---\n\n{body}",
        encoding="utf-8",
    )
    return folder


def test_help_and_version():
    with pytest.raises(SystemExit) as exc:
        sp.main(["--help"])
    assert exc.value.code == 0
    with pytest.raises(SystemExit) as exc:
        sp.main(["--version"])
    assert exc.value.code == 0


def test_install_copy_and_link(tmp_path, capsys):
    skill = write_skill(tmp_path, "tidy-notes")
    project = tmp_path / "proj"
    project.mkdir()
    assert sp.main(["install", str(skill), "--root", str(project), "--agents", "claude,agents"]) == 0
    copied = project / ".claude" / "skills" / "tidy-notes" / "SKILL.md"
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


def test_status_json_and_agents(tmp_path, capsys):
    assert sp.main(["agents"]) == 0
    out = capsys.readouterr().out
    assert ".claude/skills" in out
    assert ".github/skills" in out
    skill = write_skill(tmp_path, "tidy-notes")
    project = tmp_path / "proj"
    project.mkdir()
    sp.main(["install", str(skill), "--root", str(project), "--agents", "claude"])
    capsys.readouterr()
    assert sp.main(["status", "--root", str(project), "--agents", "claude", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["skills"][0]["name"] == "tidy-notes"
    assert data["drift"] == []


def test_missing_skill_md(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    assert sp.main(["install", str(empty), "--root", str(tmp_path)]) == 1


def test_missing_skill_dir(tmp_path, capsys):
    missing = tmp_path / "no-such-skill"
    assert sp.main(["install", str(missing), "--root", str(tmp_path)]) == 1
    assert "error:" in capsys.readouterr().err


def test_unknown_agent(tmp_path):
    skill = write_skill(tmp_path, "tidy-notes")
    with pytest.raises(SystemExit):
        sp.main(["install", str(skill), "--root", str(tmp_path), "--agents", "not-an-agent"])


def test_tree_hash_stable(tmp_path):
    a = write_skill(tmp_path, "tidy-notes")
    b = tmp_path / "copy"
    b.mkdir()
    (b / "SKILL.md").write_text((a / "SKILL.md").read_text())
    assert sp.tree_hash(a) == sp.tree_hash(b)
    (b / "SKILL.md").write_text((b / "SKILL.md").read_text() + "x")
    assert sp.tree_hash(a) != sp.tree_hash(b)


def test_status_empty(tmp_path, capsys):
    project = tmp_path / "proj"
    project.mkdir()
    assert sp.main(["status", "--root", str(project)]) == 0
    assert "no skills installed" in capsys.readouterr().out


def test_target_install(tmp_path, capsys):
    skill = write_skill(tmp_path, "tidy-notes")
    target = tmp_path / "elsewhere"
    assert sp.main(["install", str(skill), "--target", str(target)]) == 0
    assert (target / "tidy-notes" / "SKILL.md").is_file()


def test_path_traversal_name_rejected(tmp_path, capsys):
    skill = write_skill(tmp_path, "tidy-notes", frontmatter_name="../../evil")
    project = tmp_path / "proj"
    project.mkdir()
    assert sp.main(["install", str(skill), "--root", str(project), "--agents", "claude"]) == 1
    assert "invalid skill name" in capsys.readouterr().err
    assert not (tmp_path / "evil").exists()
    assert not list(project.rglob("SKILL.md"))


def test_skill_md_case_fallback(tmp_path):
    skill = write_skill(tmp_path, "tidy-notes", filename="skill.md")
    project = tmp_path / "proj"
    project.mkdir()
    assert sp.main(["install", str(skill), "--root", str(project), "--agents", "claude"]) == 0
    dest = project / ".claude" / "skills" / "tidy-notes"
    assert (dest / "skill.md").is_file()


def test_unicode_skill(tmp_path, capsys):
    skill = write_skill(tmp_path, "notes-ja", body="メモを整理する。\n")
    # override name in folder while keeping a valid single-segment name
    (skill / "SKILL.md").write_text(
        "---\nname: notes-ja\ndescription: 日本語のメモを整理するスキルです。\n---\n\n漢字と絵文字 ✅\n",
        encoding="utf-8",
    )
    project = tmp_path / "proj"
    project.mkdir()
    assert sp.main(["install", str(skill), "--root", str(project), "--agents", "claude"]) == 0
    text = (project / ".claude" / "skills" / "notes-ja" / "SKILL.md").read_text(encoding="utf-8")
    assert "漢字" in text
    assert "✅" in text


def test_overwrite_existing_copy(tmp_path):
    skill = write_skill(tmp_path, "tidy-notes", body="first\n")
    project = tmp_path / "proj"
    project.mkdir()
    assert sp.main(["install", str(skill), "--root", str(project), "--agents", "claude"]) == 0
    (skill / "SKILL.md").write_text(
        "---\nname: tidy-notes\ndescription: Demo skill used when testing tidy-notes.\n---\n\nsecond\n",
        encoding="utf-8",
    )
    assert sp.main(["install", str(skill), "--root", str(project), "--agents", "claude"]) == 0
    assert "second" in (project / ".claude" / "skills" / "tidy-notes" / "SKILL.md").read_text()


def test_copilot_global_requires_target(tmp_path, capsys):
    skill = write_skill(tmp_path, "tidy-notes")
    assert sp.main(["install", str(skill), "--agents", "copilot", "--global"]) == 1
    assert "no default user-level path" in capsys.readouterr().err


def test_estimate_tokens():
    assert sp.estimate_tokens("") == 0
    assert sp.estimate_tokens("abcd") == 1
    assert sp.estimate_tokens("あ") >= 1
