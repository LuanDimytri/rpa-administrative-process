
from pathlib import Path
import shutil


def discover_input_files(inbox_dir: Path) -> list[Path]:
    """Localiza arquivos Excel na pasta de entrada."""

    return sorted(
        path
        for path in inbox_dir.glob("*.xlsx")
        if path.is_file() and not path.name.startswith("~$")
    )


def archive_input_file(
    input_file: Path,
    archive_dir: Path,
) -> Path:
    """Move um arquivo processado para o arquivo histórico."""

    archive_dir.mkdir(parents=True, exist_ok=True)

    destination = archive_dir / input_file.name

    # Evita sobrescrever um arquivo arquivado anteriormente.
    if destination.exists():
        timestamp = input_file.stat().st_mtime_ns
        destination = archive_dir / (
            f"{input_file.stem}_{timestamp}{input_file.suffix}"
        )

    return Path(shutil.move(str(input_file), str(destination)))