
from pathlib import Path

from src.batch_processor import (
    archive_input_file,
    discover_input_files,
)


def test_discover_only_excel_files(tmp_path):
    (tmp_path / "solicitacoes.xlsx").touch()
    (tmp_path / "outra_planilha.xlsx").touch()
    (tmp_path / "notas.txt").touch()
    (tmp_path / "~$planilha.xlsx").touch()

    files = discover_input_files(tmp_path)

    assert [path.name for path in files] == [
        "outra_planilha.xlsx",
        "solicitacoes.xlsx",
    ]


def test_archive_moves_file(tmp_path):
    inbox = tmp_path / "inbox"
    archive = tmp_path / "archive"

    inbox.mkdir()
    source = inbox / "solicitacoes.xlsx"
    source.write_text("arquivo de teste", encoding="utf-8")

    destination = archive_input_file(source, archive)

    assert not source.exists()
    assert destination.exists()
    assert destination.parent == archive
    assert destination.read_text(encoding="utf-8") == "arquivo de teste"


def test_archive_does_not_overwrite_existing_file(tmp_path):
    inbox = tmp_path / "inbox"
    archive = tmp_path / "archive"

    inbox.mkdir()
    archive.mkdir()

    source = inbox / "solicitacoes.xlsx"
    existing = archive / "solicitacoes.xlsx"

    source.write_text("novo conteúdo", encoding="utf-8")
    existing.write_text("conteúdo antigo", encoding="utf-8")

    destination = archive_input_file(source, archive)

    assert destination != existing
    assert existing.read_text(encoding="utf-8") == "conteúdo antigo"
    assert destination.read_text(encoding="utf-8") == "novo conteúdo"
    assert not source.exists()