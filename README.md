# Luigi Pipelines Template

🎨 Template Cookiecutter para criar projetos de pipelines de dados usando Luigi

## 📋 Sobre

Este é um template Cookiecutter para bootstrapping rápido de projetos de pipeline de dados usando Luigi. Ele fornece uma estrutura completa e configurável com:

- ✅ Luigi para orquestração de workflows
- ✅ Scrapy (opcional) para web scraping
- ✅ FastAPI (opcional) para REST APIs
- ✅ Scheduler customizado (opcional) para tarefas agendadas
- ✅ Estrutura de projeto padronizada
- ✅ Configuração de testes
- ✅ Exemplos de tasks e spiders

## 🚀 Uso Rápido

### Pré-requisitos

```bash
pip install cookiecutter
```

### Criar Novo Projeto

```bash
cookiecutter gh:giovanimds/luigi-pipelines-template
```

Ou diretamente do diretório local:

```bash
cookiecutter /path/to/luigi-pipelines-template
```

### Responda as Perguntas

O Cookiecutter irá fazer algumas perguntas para personalizar seu projeto:

```
project_name [My Data Pipeline]: Sales Analytics Pipeline
project_slug [sales_analytics_pipeline]: 
project_short_description [Luigi-based data pipeline for ETL operations]: Pipeline for sales data analysis
author_name [Your Name]: John Doe
author_email [your.email@example.com]: john@example.com
python_version [3.12]: 
version [0.1.0]: 
Select open_source_license:
1 - MIT
2 - Apache-2.0
3 - BSD-3-Clause
4 - GPL-3.0
5 - Proprietary
Choose from 1, 2, 3, 4, 5 [1]: 1
include_scrapy [y]: y
include_fastapi [y]: y
include_scheduler [y]: y
```

### Configure o Projeto

```bash
cd sales_analytics_pipeline
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
cp .env.example .env
cp luigi.cfg.example luigi.cfg
```

## 🎯 Estrutura Gerada

```
your-project-name/
├── src/
│   └── your_project_slug/
│       ├── tasks/          # Luigi tasks
│       ├── spiders/        # Scrapy spiders (se incluído)
│       ├── api/            # FastAPI (se incluído)
│       ├── scheduler/      # Scheduler (se incluído)
│       └── settings.py
├── tests/                  # Testes unitários
├── data/                   # Diretórios de dados
├── logs/                   # Logs da aplicação
├── pyproject.toml          # Configuração do projeto
└── README.md               # Documentação do projeto
```

## ⚙️ Opções de Configuração

### Variáveis do Template

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `project_name` | Nome legível do projeto | My Data Pipeline |
| `project_slug` | Nome do pacote Python | (gerado automaticamente) |
| `project_short_description` | Descrição breve | Luigi-based data pipeline... |
| `author_name` | Nome do autor | Your Name |
| `author_email` | Email do autor | your.email@example.com |
| `python_version` | Versão Python mínima | 3.12 |
| `version` | Versão inicial | 0.1.0 |
| `open_source_license` | Licença do projeto | MIT |
| `include_scrapy` | Incluir Scrapy? | y |
| `include_fastapi` | Incluir FastAPI? | y |
| `include_scheduler` | Incluir Scheduler? | y |

### Componentes Opcionais

#### Scrapy (Web Scraping)
Quando `include_scrapy = "y"`:
- Configuração do Scrapy
- Exemplos de spiders
- Dependências relacionadas

#### FastAPI (REST API)
Quando `include_fastapi = "y"`:
- Servidor API
- Endpoints de exemplo
- Documentação automática

#### Scheduler Customizado
Quando `include_scheduler = "y"`:
- APScheduler configurado
- File watchers
- Scheduling baseado em YAML

## 📚 Recursos Incluídos

### Tasks Luigi

O template inclui tasks de exemplo:
- Task básica com parâmetros
- Task com dependências
- Tasks de extração, transformação e carga

### Configuração

- `luigi.cfg.example` - Configuração do Luigi
- `.env.example` - Variáveis de ambiente
- `scrapy.cfg.example` - Configuração do Scrapy (se incluído)

### Testes

- Estrutura de testes com pytest
- Exemplos de testes para tasks

### Documentação

- README completo e personalizado
- Exemplos de uso
- Guias de desenvolvimento

## 🔧 Desenvolvimento do Template

### Estrutura do Template

```
luigi-pipelines-template/
├── cookiecutter.json                    # Configuração do template
├── {{cookiecutter.project_slug}}/       # Diretório do projeto gerado
│   ├── src/
│   │   └── {{cookiecutter.project_slug}}/
│   ├── tests/
│   ├── pyproject.toml                   # Com variáveis Jinja2
│   └── README.md                        # Com variáveis Jinja2
└── README.md                            # Este arquivo
```

### Modificar o Template

1. Clone o repositório
2. Edite arquivos em `{{cookiecutter.project_slug}}/`
3. Use variáveis Jinja2: `{{ cookiecutter.variable_name }}`
4. Use condicionais: `{% if cookiecutter.option == "y" %}...{% endif %}`
5. Teste localmente: `cookiecutter .`

### Variáveis Jinja2

Exemplos de uso:

```python
# pyproject.toml
name = "{{ cookiecutter.project_slug }}"
version = "{{ cookiecutter.version }}"

# README.md
# {{ cookiecutter.project_name }}

# Condicional
{% if cookiecutter.include_scrapy == "y" %}
# Código para Scrapy
{% endif %}
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

### Áreas para Contribuição

- Novos componentes opcionais
- Melhorias nas tasks de exemplo
- Mais opções de configuração
- Documentação adicional
- Suporte a mais databases/APIs

## 📖 Exemplos de Uso

### Projeto Simples (apenas Luigi)

```bash
cookiecutter gh:giovanimds/luigi-pipelines-template
# include_scrapy: n
# include_fastapi: n
# include_scheduler: n
```

### Projeto Completo (todos componentes)

```bash
cookiecutter gh:giovanimds/luigi-pipelines-template
# include_scrapy: y
# include_fastapi: y
# include_scheduler: y
```

### Projeto com Web Scraping

```bash
cookiecutter gh:giovanimds/luigi-pipelines-template
# include_scrapy: y
# include_fastapi: n
# include_scheduler: y
```

## 🐛 Troubleshooting

### Erro: "cookiecutter not found"

```bash
pip install cookiecutter
```

### Erro: "Template not found"

Use o URL completo:
```bash
cookiecutter https://github.com/giovanimds/luigi-pipelines-template
```

### Problemas com Dependências

Certifique-se de estar usando Python >= 3.12:
```bash
python --version
```

## 📝 Licença

Este template é disponibilizado sob a licença MIT. Projetos gerados podem usar qualquer licença escolhida durante a criação.

## 📧 Suporte

- GitHub Issues: [luigi-pipelines-template/issues](https://github.com/giovanimds/luigi-pipelines-template/issues)
- Email: giovanimoresco@gmail.com

## 🙏 Agradecimentos

- [Cookiecutter](https://github.com/cookiecutter/cookiecutter) - Framework de templates
- [Luigi](https://github.com/spotify/luigi) - Workflow orchestration
- [Spotify](https://spotify.com) - Por criar o Luigi

---

Criado com ❤️ por [Giovani S.](https://github.com/giovanimds)
