"""Documentation contract for Python CLI and wrapper-only flags."""

from __future__ import annotations

from pathlib import Path

import last30days as cli

ROOT = Path(__file__).resolve().parents[1]
CONFIGURATION = ROOT / "CONFIGURATION.md"
SKILL_MD = ROOT / "skills" / "last30days" / "SKILL.md"
HTML_REFERENCE = ROOT / "skills" / "last30days" / "references" / "save-html-brief.md"


def _parser_flags() -> set[str]:
    parser = cli.build_parser()
    flags: set[str] = set()
    for action in parser._actions:
        flags.update(action.option_strings)
    return flags


def test_configuration_documents_new_safety_flags():
    text = CONFIGURATION.read_text(encoding="utf-8")
    flags = _parser_flags()
    assert "--no-browser-cookies" in flags
    assert "--no-browser-cookies" in text
    assert "--save-dir" in text
    assert "--output" in text


def test_save_is_not_documented_as_python_cli_flag():
    text = CONFIGURATION.read_text(encoding="utf-8")
    assert "--save-dir <path>" in text
    assert "--save " not in text
    assert "`--save`" not in text


def test_agent_is_documented_as_skill_argument_not_python_flag():
    text = SKILL_MD.read_text(encoding="utf-8")
    start = text.index("## Agent Mode (--agent flag)")
    agent_section = text[start:start + 2000]
    assert "If `--agent` appears in ARGUMENTS" in agent_section
    assert "Skill tool" in text


def test_html_reference_documents_structured_cache_reuse():
    text = HTML_REFERENCE.read_text(encoding="utf-8")
    assert "~/.config/last30days/last-report.json" in text
    assert "without re-running source fetchers" in text
    assert "No matching cached report data" in text
