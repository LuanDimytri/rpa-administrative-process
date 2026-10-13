
import pandas as pd


AUTO_APPROVAL_LIMIT = 500.00


def process_requests(df: pd.DataFrame) -> pd.DataFrame:
    """Classifica solicitações conforme validação e regras de negócio."""

    result = df.copy()

    if "is_valid" not in result.columns:
        raise ValueError(
            "As solicitações precisam passar pela validação primeiro."
        )

    result["status"] = "Rejeitada"

    valid_requests = result["is_valid"]

    automatic_approval = (
        valid_requests
        & (result["amount"] <= AUTO_APPROVAL_LIMIT)
    )

    human_approval = (
        valid_requests
        & (result["amount"] > AUTO_APPROVAL_LIMIT)
    )

    result.loc[automatic_approval, "status"] = "Aprovada automaticamente"
    result.loc[human_approval, "status"] = "Pendente de aprovação"

    return result