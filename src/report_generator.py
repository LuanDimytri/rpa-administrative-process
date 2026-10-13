
from pathlib import Path

import pandas as pd
from openpyxl.chart import PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

BASE_DIR = Path(__file__).resolve().parent.parent
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


def style_worksheet(ws, summary=False):
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 95
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.orientation = "landscape"

    header_fill = PatternFill("solid", fgColor=NAVY)
    alternate_fill = PatternFill("solid", fgColor=LIGHT_GRAY)
    thin_gray = Side(style="thin", color="D9E2F3")

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = Font(name="Aptos", size=10, bold=True, color=WHITE)
        cell.alignment = Alignment(
            horizontal="center", vertical="center", wrap_text=True
        )
        cell.border = Border(bottom=Side(style="medium", color=BLUE))

    ws.row_dimensions[1].height = 30

    for row_index in range(2, ws.max_row + 1):
        ws.row_dimensions[row_index].height = 23
        for cell in ws[row_index]:
            cell.font = Font(name="Aptos", size=10, color=DARK_GRAY)
            cell.alignment = Alignment(vertical="center")
            cell.border = Border(bottom=thin_gray)

            if row_index % 2 == 0:
                cell.fill = alternate_fill

    for column_index in range(1, ws.max_column + 1):
        letter = get_column_letter(column_index)
        header = str(ws.cell(1, column_index).value or "").lower()

        lengths = [
            len(str(ws.cell(r, column_index).value or ""))
            for r in range(1, min(ws.max_row, 100) + 1)
        ]
        ws.column_dimensions[letter].width = min(
            max(max(lengths, default=10) + 3, 13), 35
        )

        if any(word in header for word in ("employee", "funcionário")):
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
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif "date" in header or "data" in header:
                cell.number_format = DATE_FORMAT

    for column_index in range(1, ws.max_column + 1):
        header = str(ws.cell(1, column_index).value or "").lower()
        if "status" not in header:
            continue

        letter = get_column_letter(column_index)
        status_range = f"{letter}2:{letter}{max(ws.max_row, 2)}"

        for status, color in [
            ("Aprovada automaticamente", GREEN),
            ("Pendente de aprovação", YELLOW),
            ("Rejeitada", RED),
        ]:
            ws.conditional_formatting.add(
                status_range,
                FormulaRule(
                    formula=[f'ISNUMBER(SEARCH("{status}",{letter}2))'],
                    fill=PatternFill("solid", fgColor=color),
                ),
            )

    if summary:
        ws.sheet_view.zoomScale = 110
        ws.column_dimensions["A"].width = 42
        ws.column_dimensions["B"].width = 24

        for row_index in range(2, ws.max_row + 1):
            metric = str(ws.cell(row_index, 1).value or "").lower()
            value_cell = ws.cell(row_index, 2)

            if "(r$)" in metric:
                value_cell.number_format = CURRENCY_FORMAT
            elif "(%)" in metric:
                value_cell.number_format = '0.00"%"'

            value_cell.font = Font(
                name="Aptos", size=10, bold=True, color=NAVY
            )
            value_cell.alignment = Alignment(
                horizontal="right", vertical="center"
            )


def style_dashboard(ws):
    """Adiciona indicadores visuais e gráfico à aba Resumo."""

    ws.sheet_view.zoomScale = 85

    # Título
    ws.merge_cells("D1:H1")
    title = ws["D1"]
    title.value = "PAINEL DE SOLICITAÇÕES ADMINISTRATIVAS"
    title.fill = PatternFill("solid", fgColor=NAVY)
    title.font = Font(
        name="Aptos Display",
        size=16,
        bold=True,
        color=WHITE,
    )
    title.alignment = Alignment(
        horizontal="center",
        vertical="center",
    )
    ws.row_dimensions[1].height = 38

    # Indicadores: título, célula inicial, fórmula e cor
    cards = [
        ("TOTAL DE SOLICITAÇÕES", "D3", "=B2", BLUE),
        ("APROVADAS", "F3", "=B3", "548235"),
        ("PENDENTES", "D6", "=B4", "BF9000"),
        ("REJEITADAS", "F6", "=B5", "C00000"),
    ]

    for label, start, formula, color in cards:
        col = ws[start].column
        row = ws[start].row

        from openpyxl.utils import get_column_letter

        first_col = get_column_letter(col)
        second_col = get_column_letter(col + 1)

        label_range = f"{first_col}{row}:{second_col}{row}"
        value_range = (
            f"{first_col}{row + 1}:{second_col}{row + 2}"
        )

        ws.merge_cells(label_range)
        ws.merge_cells(value_range)

        label_cell = ws.cell(row=row, column=col)
        label_cell.value = label
        label_cell.fill = PatternFill("solid", fgColor=color)
        label_cell.font = Font(
            name="Aptos",
            size=10,
            bold=True,
            color=WHITE,
        )
        label_cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True,
        )

        value_cell = ws.cell(row=row + 1, column=col)
        value_cell.value = formula
        value_cell.fill = PatternFill("solid", fgColor="F3F6F9")
        value_cell.font = Font(
            name="Aptos Display",
            size=24,
            bold=True,
            color=color,
        )
        value_cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
        )

        # Aplica fundo a todas as células da área mesclada
        for cells in ws[label_range]:
            for cell in cells:
                cell.fill = PatternFill("solid", fgColor=color)

        for cells in ws[value_range]:
            for cell in cells:
                cell.fill = PatternFill("solid", fgColor="F3F6F9")

    # Espaçamento e largura do painel
    for col in ["D", "F"]:
        ws.column_dimensions[col].width = 23

    for col in ["E", "G"]:
        ws.column_dimensions[col].width = 15

    ws.column_dimensions["H"].width = 15

    for row in [3, 6]:
        ws.row_dimensions[row].height = 25

    for row in [4, 5, 7, 8]:
        ws.row_dimensions[row].height = 24

    # Gráfico de distribuição por status
    chart = PieChart()
    chart.title = "Distribuição das solicitações"
    chart.style = 10
    chart.height = 8
    chart.width = 15
    chart.varyColors = True

    data = Reference(ws, min_col=2, min_row=3, max_row=5)
    categories = Reference(ws, min_col=1, min_row=3, max_row=5)

    chart.add_data(data, titles_from_data=False)
    chart.set_categories(categories)

    chart.dataLabels = DataLabelList()
    chart.dataLabels.showCatName = True
    chart.dataLabels.showVal = True

    ws.add_chart(chart, "D10")

def generate_report(df: pd.DataFrame, output_prefix: str = "") -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    status = df["status"].astype(str)
    approved = df[status == "Aprovada automaticamente"]
    pending = df[status == "Pendente de aprovação"]
    rejected = df[status == "Rejeitada"]

    amounts = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    total_amount = amounts.sum()
    approved_amount = pd.to_numeric(
        approved["amount"], errors="coerce"
    ).fillna(0).sum()
    pending_amount = pd.to_numeric(
        pending["amount"], errors="coerce"
    ).fillna(0).sum()

    total = len(df)
    valid_count = len(approved) + len(pending)
    valid_percentage = valid_count / total * 100 if total else 0

    summary = pd.DataFrame([
        {"Métrica": "Total de solicitações", "Valor": total},
        {"Métrica": "Aprovadas automaticamente", "Valor": len(approved)},
        {"Métrica": "Pendentes de aprovação", "Valor": len(pending)},
        {"Métrica": "Rejeitadas", "Valor": len(rejected)},
        {"Métrica": "Solicitações válidas (%)", "Valor": round(valid_percentage, 2)},
        {"Métrica": "Valor total recebido (R$)", "Valor": round(total_amount, 2)},
        {"Métrica": "Valor aprovado automaticamente (R$)", "Valor": round(approved_amount, 2)},
        {"Métrica": "Valor pendente (R$)", "Valor": round(pending_amount, 2)},
    ])

    rejection_columns = [
        col for col in ["id", "employee", "amount", "errors"]
        if col in rejected.columns
    ]
    rejection_details = rejected[rejection_columns].copy()

    prefix = f"{output_prefix}_" if output_prefix else ""
    report_path = OUTPUT_DIR / f"{prefix}management_report.xlsx"

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Resumo", index=False)
        df.to_excel(writer, sheet_name="Todas as solicitações", index=False)
        rejection_details.to_excel(writer, sheet_name="Rejeições", index=False)

        for ws in writer.book.worksheets:
            style_worksheet(ws, summary=(ws.title == "Resumo"))

        style_dashboard(writer.book["Resumo"])

    return report_path