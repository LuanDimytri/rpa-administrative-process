# RPA de Processos Administrativos

Automação de processamento de solicitações administrativas utilizando Python e Excel. O projeto simula um fluxo de trabalho que recebe planilhas, valida os dados, classifica solicitações, gera relatórios e registra as operações realizadas.

## Objetivo

Demonstrar como automatizar tarefas administrativas repetitivas, reduzindo trabalho manual, padronizando validações e facilitando o acompanhamento das solicitações.

## Funcionalidades

* Leitura de múltiplas planilhas Excel em uma pasta de entrada.
* Validação de campos obrigatórios, IDs duplicados, tipos de solicitação, valores e datas.
* Classificação das solicitações em aprovadas automaticamente, pendentes de aprovação ou rejeitadas.
* Separação dos resultados em arquivos Excel.
* Geração de relatório gerencial com métricas e detalhes das rejeições.
* Registro de eventos e erros em logs.
* Arquivamento das planilhas processadas com sucesso.
* Continuação do lote quando um arquivo apresenta erro.
* Testes automatizados com pytest.

## Tecnologias

* Python
* Pandas
* OpenPyXL
* Pytest
* Git e GitHub

## Como funciona

1. As planilhas são colocadas em `data/inbox/`.
2. O sistema identifica os arquivos Excel disponíveis.
3. Os dados são validados e classificados.
4. Os resultados e relatórios são salvos com nomes associados à planilha de origem.
5. Os arquivos de entrada processados com sucesso são movidos para `data/archive/`.
6. As operações e eventuais erros são registrados em `logs/rpa.log`.

## Regras de classificação

* **Aprovada automaticamente:** solicitação válida de até R$ 500,00.
* **Pendente de aprovação:** solicitação válida acima de R$ 500,00.
* **Rejeitada:** solicitação que não atende às regras de validação.

O limite de R$ 500,00 é uma regra demonstrativa definida para este projeto, não uma política real de aprovação financeira.

## Estrutura do projeto

```text
rpa-administrative-process/
├── src/
│   ├── batch_processor.py
│   ├── file_manager.py
│   ├── generate_data.py
│   ├── main.py
│   ├── processor.py
│   ├── report_generator.py
│   └── validator.py
├── tests/
├── data/
│   ├── inbox/
│   ├── archive/
│   ├── processed/
│   └── output/
├── logs/
├── .gitignore
└── requirements.txt
```

As pastas `data/` e os logs são gerados localmente e não precisam ser enviados ao repositório.

## Requisitos

* Python 3.10 ou superior.
* pip.

## Instalação

Clone o repositório e acesse a pasta do projeto:

```bash
git clone <URL_DO_REPOSITORIO>
cd rpa-administrative-process
```

Crie e ative um ambiente virtual no Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

## Execução

Para gerar uma planilha de exemplo:

```powershell
python -m src.generate_data
```

Para processar as planilhas disponíveis na caixa de entrada:

```powershell
python -m src.main
```

Para executar os testes automatizados:

```powershell
python -m pytest -v
```

## Resultados gerados

O sistema gera arquivos separados para solicitações aprovadas, pendentes e rejeitadas, além de uma planilha consolidada e um relatório gerencial com resumo, solicitações e detalhes das rejeições.

## Testes

Os testes automatizados verificam as regras de validação, a classificação das solicitações, o gerenciamento de arquivos e a geração dos relatórios.

## Limitações e melhorias futuras

Este projeto é uma simulação educacional de um processo administrativo. A aprovação automática não substitui uma autorização humana ou regras de negócio reais.

Possíveis evoluções incluem monitoramento contínuo da pasta de entrada, notificações por e-mail, integração com APIs, banco de dados, painel de acompanhamento e tratamento mais avançado de falhas.

## Autor

Projeto desenvolvido como parte de um portfólio de Ciência da Computação, com foco em Python, automação de processos e qualidade de software.
