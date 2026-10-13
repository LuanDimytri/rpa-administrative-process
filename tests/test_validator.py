
import pandas as pd

from src.validator import validate_requests


def test_valid_request_is_accepted():
    df = pd.DataFrame(
        [
            {
                "id": "REQ001",
                "employee": "Joao Silva",
                "request_type": "Reembolso",
                "amount": 150.00,
                "date": "2026-10-13",
            }
        ]
    )

    result = validate_requests(df)

    assert result.loc[0, "is_valid"]


def test_negative_amount_is_rejected():
    df = pd.DataFrame(
        [
            {
                "id": "REQ002",
                "employee": "Maria Souza",
                "request_type": "Material",
                "amount": -50.00,
                "date": "2026-10-13",
            }
        ]
    )

    result = validate_requests(df)

    assert not result.loc[0, "is_valid"]
    assert "Valor inválido" in result.loc[0, "errors"]


def test_missing_employee_is_rejected():
    df = pd.DataFrame(
        [
            {
                "id": "REQ003",
                "employee": "",
                "request_type": "Material",
                "amount": 100.00,
                "date": "2026-10-13",
            }
        ]
    )

    result = validate_requests(df)

    assert not result.loc[0, "is_valid"]
    assert "employee não informado" in result.loc[0, "errors"]


def test_duplicate_ids_are_rejected():
    df = pd.DataFrame(
        [
            {
                "id": "REQ004",
                "employee": "Ana Costa",
                "request_type": "Material",
                "amount": 100.00,
                "date": "2026-10-13",
            },
            {
                "id": "REQ004",
                "employee": "Pedro Alves",
                "request_type": "Reembolso",
                "amount": 200.00,
                "date": "2026-10-13",
            },
        ]
    )

    result = validate_requests(df)

    assert result["is_valid"].sum() == 0
    assert result["errors"].str.contains("ID duplicado").all()