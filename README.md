# Luigi Workflow Orchestrator

🚀 Orquestrador de workflows de dados usando Luigi - Uma solução completa para pipelines ETL robustos e escaláveis.

## 📋 Visão Geral

Este projeto fornece uma estrutura completa para orquestração de workflows de dados usando [Luigi](https://github.com/spotify/luigi), desenvolvido pela Spotify. Luigi permite construir pipelines de dados complexos com gerenciamento automático de dependências, visualização e monitoramento.

## 🚀 Começando

### Pré-requisitos

- Python 3.12 ou superior
- uv (gerenciador de pacotes Python)

1.**Crie e ative um ambiente virtual (recomendado)**

```bash
# Windows
uv venv
venv\Scripts\activate
```

2.**Instale as dependências**

```bash
uv sync
# OU
uv pip install -e .
```

3.**Configure variáveis de ambiente (opcional)**

```bash
copy .env.example .env
# Edite o .env com suas configurações
```
