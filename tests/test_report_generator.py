
import pandas as pd

import src.report_generator as report_generator


def test_report_contains_expected_metrics(tmp_path, monkeypatch):
    monkeypatch.setattr(report_generator, "OUTPUT_DIR", tmp_path)

    df = pd.DataFrame(
        [
            {
                "id": "REQ001",
                "employee": "Joao",
                "amount": 150.00,
                "status": "Aprovada automaticamente",
                "errors": "",
            },
            {
                "id": "REQ002",
                "employee": "Maria",
                "amount": 850.00,
                "status": "Pendente de aprovação",
                "errors": "",
            },
            {
                "id": "REQ003",
                "employee": "Ana",
                "amount": -50.00,
                "status": "Rejeitada",
                "errors": "Valor inválido",
            },
        ]
    )

    report_path = report_generator.generate_report(df)

    assert report_path.exists()

    summary = pd.read_excel(report_path, sheet_name="Resumo")
    metrics = dict(zip(summary["Métrica"], summary["Valor"]))

    assert metrics["Total de solicitações"] == 3
    assert metrics["Aprovadas automaticamente"] == 1
    assert metrics["Pendentes de aprovação"] == 1
    assert metrics["Rejeitadas"] == 1
    assert metrics["Solicitações válidas (%)"] == 66.67
    assert metrics["Valor aprovado automaticamente (R$)"] == 150.00
    assert metrics["Valor pendente (R$)"] == 850.00


def test_empty_report_does_not_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(report_generator, "OUTPUT_DIR", tmp_path)

    df = pd.DataFrame(
        columns=["id", "employee", "amount", "status", "errors"]
    )

    report_path = report_generator.generate_report(df)

    summary = pd.read_excel(report_path, sheet_name="Resumo")
    metrics = dict(zip(summary["Métrica"], summary["Valor"]))

    assert metrics["Total de solicitações"] == 0
    assert metrics["Solicitações válidas (%)"] == 0