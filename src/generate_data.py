
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
INBOX_DIR = BASE_DIR / "data" / "inbox"


def generate_requests():
    INBOX_DIR.mkdir(parents=True, exist_ok=True)

    requests = [
        {
            "id": "REQ001",
            "employee": "Joao Silva",
            "request_type": "Reembolso",
            "amount": 150.00,
            "date": "2026-10-13",
        },
        {
            "id": "REQ002",
            "employee": "Maria Souza",
            "request_type": "Material",
            "amount": 850.00,
            "date": "2026-10-13",
        },
        {
            "id": "REQ003",
            "employee": "Carlos Lima",
            "request_type": "Reembolso",
            "amount": 230.00,
            "date": "2026-10-12",
        },
        {
            "id": "REQ004",
            "employee": "",
            "request_type": "Material",
            "amount": 120.00,
            "date": "2026-10-13",
        },
        {
            "id": "REQ005",
            "employee": "Ana Costa",
            "request_type": "Reembolso",
            "amount": -50.00,
            "date": "2026-10-13",
        },
        {
            "id": "REQ006",
            "employee": "Pedro Alves",
            "request_type": "TipoInvalido",
            "amount": 100.00,
            "date": "2026-10-13",
        },
        {
            "id": "REQ007",
            "employee": "Julia Santos",
            "request_type": "Material",
            "amount": 600.00,
            "date": "2026-10-11",
        },
    ]

    df = pd.DataFrame(requests)

    output_file = INBOX_DIR / "solicitacoes.xlsx"
    df.to_excel(output_file, index=False)

    print(f"Planilha criada: {output_file}")
    print(f"Total de solicitações: {len(df)}")


if __name__ == "__main__":
    generate_requests()