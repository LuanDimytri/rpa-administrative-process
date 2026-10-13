
import pandas as pd
import pytest

from src.processor import process_requests


def test_low_value_request_is_automatically_approved():
    df = pd.DataFrame(
        [{"is_valid": True, "amount": 150.00}]
    )

    result = process_requests(df)

    assert result.loc[0, "status"] == "Aprovada automaticamente"


def test_high_value_request_requires_human_approval():
    df = pd.DataFrame(
        [{"is_valid": True, "amount": 850.00}]
    )

    result = process_requests(df)

    assert result.loc[0, "status"] == "Pendente de aprovação"


def test_invalid_request_is_rejected():
    df = pd.DataFrame(
        [{"is_valid": False, "amount": 100.00}]
    )

    result = process_requests(df)

    assert result.loc[0, "status"] == "Rejeitada"


def test_processing_requires_validation():
    df = pd.DataFrame(
        [{"amount": 100.00}]
    )

    with pytest.raises(ValueError, match="passar pela validação"):
        process_requests(df)


def test_exactly_500_is_automatically_approved():
    df = pd.DataFrame(
        [{"is_valid": True, "amount": 500.00}]
    )

    result = process_requests(df)

    assert result.loc[0, "status"] == "Aprovada automaticamente"