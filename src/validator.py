
import pandas as pd


VALID_REQUEST_TYPES = {"Reembolso", "Material"}

REQUIRED_COLUMNS = {
    "id",
    "employee",
    "request_type",
    "amount",
    "date",
}


def validate_requests(df: pd.DataFrame) -> pd.DataFrame:
    """Valida solicitações administrativas e registra os motivos de rejeição."""

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        columns = ", ".join(sorted(missing_columns))
        raise ValueError(f"Colunas obrigatórias ausentes: {columns}")

    result = df.copy()
    result["errors"] = ""

    # Campos obrigatórios
    for column in ["id", "employee", "request_type", "date"]:
        result[column] = result[column].fillna("").astype(str).str.strip()

        invalid = result[column].eq("")
        result.loc[invalid, "errors"] += f"{column} não informado; "

    # IDs duplicados
    valid_ids = result["id"].ne("")
    duplicated = result["id"].duplicated(keep=False) & valid_ids
    result.loc[duplicated, "errors"] += "ID duplicado; "

    # Tipo de solicitação
    invalid_type = (
        result["request_type"].ne("")
        & ~result["request_type"].isin(VALID_REQUEST_TYPES)
    )
    result.loc[invalid_type, "errors"] += "Tipo de solicitação inválido; "

    # Valor numérico e positivo
    result["amount"] = pd.to_numeric(result["amount"], errors="coerce")

    invalid_amount = result["amount"].isna() | (result["amount"] <= 0)
    result.loc[invalid_amount, "errors"] += "Valor inválido; "

    # Data válida
    parsed_dates = pd.to_datetime(result["date"], errors="coerce")
    invalid_date = parsed_dates.isna()

    result.loc[invalid_date, "errors"] += "Data inválida; "
    result["date"] = parsed_dates

    # Resultado da validação
    result["errors"] = result["errors"].str.rstrip("; ")
    result["is_valid"] = result["errors"].eq("")

    return result