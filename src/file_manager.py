
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
APPROVED_DIR = PROCESSED_DIR / "approved"
PENDING_DIR = PROCESSED_DIR / "pending"
REJECTED_DIR = PROCESSED_DIR / "rejected"
OUTPUT_DIR = BASE_DIR / "data" / "output"


def save_results(
    df: pd.DataFrame,
    output_prefix: str = "",
) -> dict[str, Path]:
    directories = [
        APPROVED_DIR,
        PENDING_DIR,
        REJECTED_DIR,
        OUTPUT_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    prefix = f"{output_prefix}_" if output_prefix else ""

    groups = {
        "approved": df[
            df["status"] == "Aprovada automaticamente"
        ],
        "pending": df[
            df["status"] == "Pendente de aprovação"
        ],
        "rejected": df[
            df["status"] == "Rejeitada"
        ],
    }

    output_paths = {}

    destinations = {
        "approved": APPROVED_DIR / f"{prefix}approved.xlsx",
        "pending": PENDING_DIR / f"{prefix}pending.xlsx",
        "rejected": REJECTED_DIR / f"{prefix}rejected.xlsx",
    }

    for name, group in groups.items():
        output_file = destinations[name]
        group.to_excel(output_file, index=False)
        output_paths[name] = output_file

    full_report = OUTPUT_DIR / f"{prefix}all_results.xlsx"
    df.to_excel(full_report, index=False)
    output_paths["all_results"] = full_report

    return output_paths