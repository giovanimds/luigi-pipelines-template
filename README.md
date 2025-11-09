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

## 🎨 Gerando Componentes com Cookiecutter

Este projeto inclui suporte ao **Cookiecutter** para gerar automaticamente componentes padronizados. Isso facilita a criação de novas tasks, spiders e projetos completos de pipeline.

### Templates Disponíveis

#### 1. **Luigi Task** - Criar nova task
Gera uma task Luigi com estrutura padronizada (Extract, Transform, Load ou Basic).

```bash
python scripts/cli/generate.py task
```

Você será solicitado a fornecer:
- Nome da task
- Descrição
- Tipo da task (extract, transform, load, basic)
- Formato de saída (csv, json, excel, parquet)
- Incluir dependências
- Incluir parâmetro de data

**Exemplo de uso:**
```bash
python scripts/cli/generate.py task
# Responda as perguntas interativas
# A task será criada em src/pipelines_planejamento/tasks/
```

#### 2. **Scrapy Spider** - Criar novo spider
Gera um spider Scrapy com diferentes tipos (basic, crawl, sitemap, csv_feed).

```bash
python scripts/cli/generate.py spider
```

Você será solicitado a fornecer:
- Nome do spider
- URLs iniciais
- Domínios permitidos
- Tipo de spider
- Campos a extrair
- Incluir login

**Exemplo de uso:**
```bash
python scripts/cli/generate.py spider
# Responda as perguntas interativas
# O spider será criado em src/pipelines_planejamento/spiders/
```

#### 3. **Pipeline Project** - Criar projeto completo
Gera um novo projeto de pipeline completo com estrutura base.

```bash
python scripts/cli/generate.py pipeline
```

Você será solicitado a fornecer:
- Nome do projeto
- Descrição
- Autor
- Incluir Scrapy
- Incluir FastAPI
- Incluir Scheduler
- Tipo de licença

**Exemplo de uso:**
```bash
# Gerar em outro diretório
python scripts/cli/generate.py pipeline -o /path/to/projects
```

### Listar Templates Disponíveis

```bash
python scripts/cli/generate.py --list
```

### Benefícios do Cookiecutter

✅ **Padronização**: Todos os componentes seguem a mesma estrutura e boas práticas  
✅ **Rapidez**: Crie novos componentes em segundos  
✅ **Redução de erros**: Templates testados reduzem erros manuais  
✅ **Onboarding**: Facilita integração de novos desenvolvedores  
✅ **Documentação**: Componentes gerados já incluem comentários e documentação básica

### 📖 Documentação Completa

Para exemplos detalhados, casos de uso avançados e guia completo, consulte:

**[📚 Guia Completo de Cookiecutter](docs/COOKIECUTTER_GUIDE.md)**

Este guia inclui:
- Exemplos práticos passo a passo
- Como personalizar templates
- Boas práticas de organização
- Troubleshooting comum
- FAQ
