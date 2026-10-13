
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "output"


def generate_report(
    df: pd.DataFrame,
    output_prefix: str = "",
) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = len(df)

    approved = df[
        df["status"] == "Aprovada automaticamente"
    ]
    pending = df[
        df["status"] == "Pendente de aprovação"
    ]
    rejected = df[
        df["status"] == "Rejeitada"
    ]

    total_amount = (
        pd.to_numeric(df["amount"], errors="coerce")
        .fillna(0)
        .sum()
    )

    approved_amount = approved["amount"].sum()
    pending_amount = pending["amount"].sum()

    valid_count = len(approved) + len(pending)
    valid_percentage = (
        valid_count / total * 100
        if total
        else 0
    )

    summary = pd.DataFrame([
        {
            "Métrica": "Total de solicitações",
            "Valor": total,
        },
        {
            "Métrica": "Aprovadas automaticamente",
            "Valor": len(approved),
        },
        {
            "Métrica": "Pendentes de aprovação",
            "Valor": len(pending),
        },
        {
            "Métrica": "Rejeitadas",
            "Valor": len(rejected),
        },
        {
            "Métrica": "Solicitações válidas (%)",
            "Valor": round(valid_percentage, 2),
        },
        {
            "Métrica": "Valor total recebido (R$)",
            "Valor": round(total_amount, 2),
        },
        {
            "Métrica": "Valor aprovado automaticamente (R$)",
            "Valor": round(approved_amount, 2),
        },
        {
            "Métrica": "Valor pendente (R$)",
            "Valor": round(pending_amount, 2),
        },
    ])

    rejection_details = rejected[
        ["id", "employee", "amount", "errors"]
    ].copy()

    prefix = f"{output_prefix}_" if output_prefix else ""
    report_path = OUTPUT_DIR / f"{prefix}management_report.xlsx"

    with pd.ExcelWriter(
        report_path,
        engine="openpyxl",
    ) as writer:
        summary.to_excel(
            writer,
            sheet_name="Resumo",
            index=False,
        )

        df.to_excel(
            writer,
            sheet_name="Todas as solicitações",
            index=False,
        )

        rejection_details.to_excel(
            writer,
            sheet_name="Rejeições",
            index=False,
        )

        for worksheet in writer.book.worksheets:
            for column_cells in worksheet.columns:
                max_length = max(
                    len(str(cell.value))
                    if cell.value is not None
                    else 0
                    for cell in column_cells
                )

                worksheet.column_dimensions[
                    column_cells[0].column_letter
                ].width = min(max_length + 2, 45)

    return report_path