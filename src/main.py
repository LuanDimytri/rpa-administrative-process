
import logging
from pathlib import Path

import pandas as pd

from src.batch_processor import (
    archive_input_file,
    discover_input_files,
)
from src.file_manager import save_results
from src.processor import process_requests
from src.report_generator import generate_report
from src.validator import validate_requests


BASE_DIR = Path(__file__).resolve().parent.parent
INBOX_DIR = BASE_DIR / "data" / "inbox"
ARCHIVE_DIR = BASE_DIR / "data" / "archive"
LOG_DIR = BASE_DIR / "logs"


def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(
                LOG_DIR / "rpa.log",
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
        force=True,
    )


def process_file(input_file: Path) -> bool:
    """Processa uma planilha e arquiva a entrada se tudo der certo."""

    logging.info("Iniciando arquivo: %s", input_file.name)

    try:
        df = pd.read_excel(input_file)

        logging.info(
            "%s: solicitações recebidas: %s",
            input_file.name,
            len(df),
        )

        validated_df = validate_requests(df)
        processed_df = process_requests(validated_df)

        prefix = input_file.stem

        paths = save_results(
            processed_df,
            output_prefix=prefix,
        )

        report_path = generate_report(
            processed_df,
            output_prefix=prefix,
        )

        approved = int(
            (processed_df["status"] == "Aprovada automaticamente").sum()
        )
        pending = int(
            (processed_df["status"] == "Pendente de aprovação").sum()
        )
        rejected = int(
            (processed_df["status"] == "Rejeitada").sum()
        )

        logging.info(
            "%s: solicitações válidas: %s",
            input_file.name,
            int(validated_df["is_valid"].sum()),
        )
        logging.info(
            "%s: aprovadas automaticamente: %s",
            input_file.name,
            approved,
        )
        logging.info(
            "%s: pendentes de aprovação: %s",
            input_file.name,
            pending,
        )
        logging.info(
            "%s: rejeitadas: %s",
            input_file.name,
            rejected,
        )

        for name, path in paths.items():
            logging.info(
                "%s: arquivo %s: %s",
                input_file.name,
                name,
                path,
            )

        logging.info(
            "%s: relatório gerencial: %s",
            input_file.name,
            report_path,
        )

        archived_path = archive_input_file(
            input_file,
            ARCHIVE_DIR,
        )

        logging.info(
            "%s: entrada arquivada em: %s",
            input_file.name,
            archived_path,
        )

        return True

    except Exception:
        logging.exception(
            "Falha ao processar %s. "
            "O arquivo permanecerá na caixa de entrada.",
            input_file.name,
        )
        return False


def main():
    setup_logging()

    logging.info(
        "Iniciando o processamento administrativo em lote."
    )

    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    input_files = discover_input_files(INBOX_DIR)

    if not input_files:
        logging.info(
            "Nenhum arquivo Excel encontrado na caixa de entrada."
        )
        return

    successful = 0
    failed = 0

    for input_file in input_files:
        if process_file(input_file):
            successful += 1
        else:
            failed += 1

    logging.info("Lote concluído.")
    logging.info(
        "Arquivos processados com sucesso: %s",
        successful,
    )
    logging.info(
        "Arquivos com falha: %s",
        failed,
    )


if __name__ == "__main__":
    main()