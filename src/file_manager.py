
from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
APPROVED_DIR = PROCESSED_DIR / "approved"
PENDING_DIR = PROCESSED_DIR / "pending"
REJECTED_DIR = PROCESSED_DIR / "rejected"
OUTPUT_DIR = BASE_DIR / "data" / "output"

NAVY = "17365D"
BLUE = "2F75B5"
WHITE = "FFFFFF"
LIGHT_GRAY = "F3F6F9"
DARK_GRAY = "44546A"
GREEN = "E2F0D9"
YELLOW = "FFF2CC"
RED = "FCE4D6"

CURRENCY_FORMAT = '"R$" #,##0.00'
DATE_FORMAT = "dd/mm/yyyy"


def style_excel_file(path: Path) -> None:
    """Aplica formatação profissional a uma planilha gerada."""

    from openpyxl import load_workbook

    workbook = load_workbook(path)

    header_fill = PatternFill("solid", fgColor=NAVY)
    alternate_fill = PatternFill("solid", fgColor=LIGHT_GRAY)
    thin_gray = Side(style="thin", color="D9E2F3")

    status_colors = {
        "Aprovada automaticamente": GREEN,
        "Pendente de aprovação": YELLOW,
        "Rejeitada": RED,
    }

    for ws in workbook.worksheets:
        ws.sheet_view.showGridLines = False
        ws.sheet_view.zoomScale = 95
        ws.freeze_panes = "A2"

        if ws.max_row >= 1 and ws.max_column >= 1:
            ws.auto_filter.ref = ws.dimensions

        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        ws.page_setup.orientation = "landscape"

        # Cabeçalho
        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = Font(
                name="Aptos",
                size=10,
                bold=True,
                color=WHITE,
            )
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True,
            )
            cell.border = Border(
                bottom=Side(style="medium", color=BLUE)
            )

        ws.row_dimensions[1].height = 30

        # Linhas e conteúdo
        for row_index in range(2, ws.max_row + 1):
            ws.row_dimensions[row_index].height = 23

            for cell in ws[row_index]:
                cell.font = Font(
                    name="Aptos",
                    size=10,
                    color=DARK_GRAY,
                )
                cell.alignment = Alignment(vertical="center")
                cell.border = Border(bottom=thin_gray)

                if row_index % 2 == 0:
                    cell.fill = alternate_fill

        # Larguras e formatos por coluna
        for column_index in range(1, ws.max_column + 1):
            letter = get_column_letter(column_index)
            header = str(
                ws.cell(1, column_index).value or ""
            ).lower()

            lengths = [
                len(str(ws.cell(r, column_index).value or ""))
                for r in range(1, min(ws.max_row, 100) + 1)
            ]

            ws.column_dimensions[letter].width = min(
                max(max(lengths, default=10) + 3, 13),
                35,
            )

            if "employee" in header or "funcionário" in header:
                ws.column_dimensions[letter].width = 25
            elif "error" in header or "erro" in header:
                ws.column_dimensions[letter].width = 38
            elif "status" in header:
                ws.column_dimensions[letter].width = 30
            elif "date" in header or "data" in header:
                ws.column_dimensions[letter].width = 15
            elif "amount" in header or "valor" in header:
                ws.column_dimensions[letter].width = 18
            elif "request_type" in header or "solicitação" in header:
                ws.column_dimensions[letter].width = 22

            for row_index in range(2, ws.max_row + 1):
                cell = ws.cell(row_index, column_index)

                if "amount" in header or "valor" in header:
                    cell.number_format = CURRENCY_FORMAT
                    cell.alignment = Alignment(
                        horizontal="right",
                        vertical="center",
                    )
                elif "date" in header or "data" in header:
                    cell.number_format = DATE_FORMAT

        # Destaque visual do status
        for column_index in range(1, ws.max_column + 1):
            header = str(
                ws.cell(1, column_index).value or ""
            ).lower()

            if "status" not in header:
                continue

            for row_index in range(2, ws.max_row + 1):
                cell = ws.cell(row_index, column_index)
                value = str(cell.value or "")

                for status, color in status_colors.items():
                    if status in value:
                        cell.fill = PatternFill(
                            "solid",
                            fgColor=color,
                        )
                        cell.font = Font(
                            name="Aptos",
                            size=10,
                            bold=True,
                            color=DARK_GRAY,
                        )
                        break

    workbook.save(path)


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
        style_excel_file(output_file)
        output_paths[name] = output_file

    full_report = OUTPUT_DIR / f"{prefix}all_results.xlsx"
    df.to_excel(full_report, index=False)
    style_excel_file(full_report)
    output_paths["all_results"] = full_report

    return output_paths