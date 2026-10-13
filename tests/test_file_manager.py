
import pandas as pd

from src.file_manager import save_results


def test_save_results_creates_all_spreadsheets(tmp_path, monkeypatch):
    import src.file_manager as file_manager

    monkeypatch.setattr(file_manager, "BASE_DIR", tmp_path)
    monkeypatch.setattr(
        file_manager,
        "PROCESSED_DIR",
        tmp_path / "data" / "processed",
    )
    monkeypatch.setattr(
        file_manager,
        "APPROVED_DIR",
        tmp_path / "data" / "processed" / "approved",
    )
    monkeypatch.setattr(
        file_manager,
        "PENDING_DIR",
        tmp_path / "data" / "processed" / "pending",
    )
    monkeypatch.setattr(
        file_manager,
        "REJECTED_DIR",
        tmp_path / "data" / "processed" / "rejected",
    )
    monkeypatch.setattr(
        file_manager,
        "OUTPUT_DIR",
        tmp_path / "data" / "output",
    )

    df = pd.DataFrame(
        [
            {
                "id": "REQ001",
                "amount": 150.00,
                "status": "Aprovada automaticamente",
            },
            {
                "id": "REQ002",
                "amount": 850.00,
                "status": "Pendente de aprovação",
            },
            {
                "id": "REQ003",
                "amount": -50.00,
                "status": "Rejeitada",
            },
        ]
    )

    paths = save_results(df)

    assert len(paths) == 4

    for path in paths.values():
        assert path.exists()

    approved = pd.read_excel(paths["approved"])
    pending = pd.read_excel(paths["pending"])
    rejected = pd.read_excel(paths["rejected"])
    all_results = pd.read_excel(paths["all_results"])

    assert approved["id"].tolist() == ["REQ001"]
    assert pending["id"].tolist() == ["REQ002"]
    assert rejected["id"].tolist() == ["REQ003"]
    assert len(all_results) == 3