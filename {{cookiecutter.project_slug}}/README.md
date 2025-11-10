# {{ cookiecutter.project_name }}

{{ cookiecutter.project_short_description }}

## 📋 Visão Geral

Este projeto fornece uma estrutura completa para orquestração de workflows de dados usando [Luigi](https://github.com/spotify/luigi), desenvolvido pela Spotify. Luigi permite construir pipelines de dados complexos com gerenciamento automático de dependências, visualização e monitoramento.

**Autor:** {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>

## 🚀 Começando

### Pré-requisitos

- Python {{ cookiecutter.python_version }} ou superior
- uv (gerenciador de pacotes Python) ou pip

### Instalação

1. **Crie e ative um ambiente virtual**

```bash
# Usando uv
uv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Ou usando venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

2. **Instale as dependências**

```bash
# Usando uv
uv sync

# Ou usando pip
pip install -e .
```

3. **Configure variáveis de ambiente**

```bash
cp .env.example .env
# Edite o .env com suas configurações
```

4. **Configure o Luigi**

```bash
cp luigi.cfg.example luigi.cfg
# Edite luigi.cfg conforme necessário
```
{% if cookiecutter.include_scrapy == "y" %}
5. **Configure o Scrapy** (se estiver usando web scraping)

```bash
cp scrapy.cfg.example scrapy.cfg
```
{% endif %}

## 📁 Estrutura do Projeto

```
{{ cookiecutter.project_slug }}/
├── src/{{ cookiecutter.project_slug }}/
│   ├── tasks/              # Luigi tasks
│   │   ├── core/           # Core task base classes
│   │   └── ...
{% if cookiecutter.include_scrapy == "y" %}│   ├── spiders/            # Scrapy spiders
│   ├── scrapers/           # Custom scrapers
{% endif %}{% if cookiecutter.include_scheduler == "y" %}│   ├── scheduler/          # Task scheduling
{% endif %}{% if cookiecutter.include_fastapi == "y" %}│   ├── api/                # FastAPI endpoints
{% endif %}│   ├── utils/              # Utility functions
│   └── settings.py         # Configuration
├── data/
│   ├── raw/                # Raw data
│   ├── processed/          # Processed data
│   └── outputs/            # Final outputs
├── tests/                  # Unit tests
├── logs/                   # Application logs
├── pyproject.toml          # Project configuration
{% if cookiecutter.include_scrapy == "y" %}├── scrapy.cfg              # Scrapy configuration
{% endif %}└── README.md               # This file
```

## 🏃 Executando o Projeto

### Rodar uma task Luigi

```bash
# Com scheduler local
luigi --module {{ cookiecutter.project_slug }}.tasks ExampleTask --local-scheduler

# Com scheduler central
luigid --port 8082  # Em um terminal
luigi --module {{ cookiecutter.project_slug }}.tasks ExampleTask  # Em outro terminal
```
{% if cookiecutter.include_scheduler == "y" %}
### Iniciar o Scheduler Customizado

```bash
python -m {{ cookiecutter.project_slug }}.scheduler
```
{% endif %}{% if cookiecutter.include_scrapy == "y" %}
### Rodar Scrapy Spiders

```bash
scrapy crawl spider_name
```
{% endif %}{% if cookiecutter.include_fastapi == "y" %}
### Iniciar o Servidor API

```bash
uvicorn {{ cookiecutter.project_slug }}.api.serve:app --reload
```

API disponível em: http://localhost:8000
Documentação: http://localhost:8000/docs
{% endif %}

## 🧪 Testes

Execute os testes com pytest:

```bash
pytest tests/ -v
```

Com cobertura:

```bash
pytest tests/ --cov={{ cookiecutter.project_slug }} --cov-report=html
```

## 📝 Desenvolvimento

### Criar Nova Task

Crie um arquivo em `src/{{ cookiecutter.project_slug }}/tasks/` seguindo o padrão:

```python
import luigi
from datetime import datetime
from {{ cookiecutter.project_slug }}.settings import PROCESSED_DATA_PATH

class MyTask(luigi.Task):
    date = luigi.DateParameter(default=datetime.now().date())
    
    def output(self):
        return luigi.LocalTarget(PROCESSED_DATA_PATH / f"my_task_{self.date}.csv")
    
    def run(self):
        # Sua lógica aqui
        pass
```
{% if cookiecutter.include_scrapy == "y" %}
### Criar Novo Spider

```bash
scrapy genspider spider_name domain.com
```

Ou crie manualmente em `src/{{ cookiecutter.project_slug }}/spiders/`.
{% endif %}

## 🔧 Configuração

### Luigi Configuration (luigi.cfg)

Configure workers, retries, logging e outros parâmetros do Luigi.

### Environment Variables (.env)

Defina API keys, database URLs e outras configurações sensíveis.

### Settings (src/{{ cookiecutter.project_slug }}/settings.py)

Configure paths de dados, configurações do Scrapy e outras constantes do projeto.

## 📚 Recursos

- [Luigi Documentation](https://luigi.readthedocs.io/)
{% if cookiecutter.include_scrapy == "y" %}- [Scrapy Documentation](https://docs.scrapy.org/)
{% endif %}{% if cookiecutter.include_fastapi == "y" %}- [FastAPI Documentation](https://fastapi.tiangolo.com/)
{% endif %}- [Python Best Practices](https://docs.python-guide.org/)

## 📄 Licença

Este projeto está licenciado sob a licença {{ cookiecutter.open_source_license }} - veja o arquivo LICENSE para detalhes.

## ✨ Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📧 Contato

{{ cookiecutter.author_name }} - {{ cookiecutter.author_email }}

---

Gerado com ❤️ usando [Cookiecutter](https://github.com/cookiecutter/cookiecutter)
