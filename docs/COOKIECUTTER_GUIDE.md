# Cookiecutter Template Guide

Este guia explica como usar os templates Cookiecutter para gerar componentes padronizados no projeto Luigi Pipelines.

## 📚 Índice

- [Introdução](#introdução)
- [Instalação](#instalação)
- [Templates Disponíveis](#templates-disponíveis)
- [Uso Básico](#uso-básico)
- [Exemplos Práticos](#exemplos-práticos)
- [Personalização](#personalização)
- [Boas Práticas](#boas-práticas)

## 🎯 Introdução

Cookiecutter é um utilitário de linha de comando que cria projetos a partir de templates. Neste projeto, usamos Cookiecutter para:

- ✅ Padronizar a estrutura de tasks, spiders e projetos
- ✅ Reduzir erros manuais de digitação
- ✅ Acelerar o desenvolvimento
- ✅ Facilitar onboarding de novos membros
- ✅ Aplicar boas práticas automaticamente

## 🔧 Instalação

O Cookiecutter já está incluído como dependência do projeto. Após instalar as dependências:

```bash
uv sync
# ou
pip install -e .
```

## 📋 Templates Disponíveis

### 1. Luigi Task Template

Gera uma task Luigi completa com:
- Tipos: `basic`, `extract`, `transform`, `load`
- Formatos de saída: `csv`, `json`, `excel`, `parquet`
- Suporte para parâmetros de data
- Gerenciamento de dependências
- Estrutura ETL completa

**Localização:** `templates/luigi-task/`

### 2. Scrapy Spider Template

Gera um spider Scrapy com:
- Tipos: `basic`, `crawl`, `sitemap`, `csv_feed`
- Configuração de URLs e domínios
- Suporte para login
- Extração de múltiplos campos
- Paginação automática

**Localização:** `templates/scrapy-spider/`

### 3. New Pipeline Project Template

Gera um projeto completo com:
- Estrutura de diretórios Luigi
- Componentes opcionais: Scrapy, FastAPI, Scheduler
- Configurações base (luigi.cfg, .env, etc.)
- README personalizado
- Testes básicos

**Localização:** `templates/new-pipeline/`

## 🚀 Uso Básico

### Comando Geral

```bash
python scripts/cli/generate.py <template_type> [-o OUTPUT_DIR]
```

### Listar Templates

```bash
python scripts/cli/generate.py --list
```

### Ajuda

```bash
python scripts/cli/generate.py --help
```

## 💡 Exemplos Práticos

### Exemplo 1: Task de Extração de API

Criar uma task que extrai dados de uma API e salva em CSV:

```bash
python scripts/cli/generate.py task
```

**Respostas sugeridas:**
```
task_name: ExtractAPIDataTask
task_description: Extract data from REST API
task_type: extract
include_requires: n
include_date_parameter: y
output_format: csv
author_name: Seu Nome
author_email: seu.email@exemplo.com
```

**Resultado:** Task criada em `src/pipelines_planejamento/tasks/extractapidatatask/extractapidatatask.py`

### Exemplo 2: Spider para E-commerce

Criar um spider para extrair produtos de um site:

```bash
python scripts/cli/generate.py spider
```

**Respostas sugeridas:**
```
spider_name: ecommerce_products
spider_description: Extract product data from e-commerce site
start_urls: https://exemplo.com.br/produtos
allowed_domains: exemplo.com.br
spider_type: crawl
include_login: n
output_items: title,price,description,image_url
author_name: Seu Nome
author_email: seu.email@exemplo.com
```

**Rodar o spider:**
```bash
scrapy crawl ecommerce_products -o data/outputs/scraped/products.jsonl
```

### Exemplo 3: Novo Projeto de Pipeline

Criar um novo projeto para análise de dados de vendas:

```bash
python scripts/cli/generate.py pipeline -o ~/projects
```

**Respostas sugeridas:**
```
project_name: Sales Analytics Pipeline
project_description: Pipeline for sales data analysis and reporting
author_name: Seu Nome
author_email: seu.email@exemplo.com
python_version: 3.12
include_scrapy: y
include_fastapi: y
include_scheduler: y
license: MIT
```

## 🎨 Personalização

### Modificar Templates

Os templates estão em `templates/`. Para personalizar:

1. Edite os arquivos `.json` para alterar perguntas/opções
2. Edite os arquivos de template (`.py`, `.md`) para alterar código gerado
3. Use variáveis Jinja2: `{{ cookiecutter.variable_name }}`
4. Use condicionais: `{% if cookiecutter.option == "value" %}`

### Criar Novo Template

1. Criar diretório em `templates/my-new-template/`
2. Adicionar `cookiecutter.json` com configurações
3. Criar estrutura de arquivos usando variáveis Jinja2
4. Adicionar ao CLI em `scripts/cli/generate.py`
5. Adicionar testes em `tests/test_cookiecutter.py`

## 📝 Boas Práticas

### 1. Nomenclatura

- **Tasks**: Use sufixo `Task` (ex: `ExtractDataTask`)
- **Spiders**: Use snake_case (ex: `product_spider`)
- **Projetos**: Use snake_case (ex: `sales_analytics`)

### 2. Organização

```
src/pipelines_planejamento/
├── tasks/
│   ├── extract_*.py      # Tasks de extração
│   ├── transform_*.py    # Tasks de transformação
│   └── load_*.py         # Tasks de carregamento
└── spiders/
    └── *_spider.py       # Spiders
```

### 3. Documentação

- Complete os docstrings gerados
- Adicione exemplos de uso
- Documente parâmetros especiais

## 🔍 Troubleshooting

### Erro: "Template not found"

```bash
# Verificar se templates existem
ls templates/

# Usar caminho absoluto se necessário
python scripts/cli/generate.py task -o $(pwd)/src/pipelines_planejamento/tasks
```

### Erro: "Module not found" ao rodar task gerada

```python
# Adicionar import no __init__.py
# src/pipelines_planejamento/tasks/__init__.py
from .extractapidatatask.extractapidatatask import ExtractAPIDataTask
```

## 📚 Recursos Adicionais

- [Documentação Oficial Cookiecutter](https://cookiecutter.readthedocs.io/)
- [Jinja2 Template Designer Documentation](https://jinja.palletsprojects.com/)
- [Luigi Documentation](https://luigi.readthedocs.io/)
- [Scrapy Documentation](https://docs.scrapy.org/)

## ❓ Perguntas Frequentes

**P: Posso usar templates em outros projetos?**  
R: Sim! Os templates são independentes. Copie a pasta `templates/` para qualquer projeto.

**P: Como adicionar novos formatos de saída?**  
R: Edite `templates/luigi-task/cookiecutter.json` e adicione à lista `output_format`.

**P: Os templates funcionam no Windows?**  
R: Sim! Cookiecutter é multiplataforma. Use PowerShell ou CMD.

---

**Precisa de ajuda?** Abra uma issue no GitHub!
