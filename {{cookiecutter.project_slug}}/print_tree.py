import sys
from pathlib import Path

# Arquivos/Pastas que devem ser ignoradas na visualização da estrutura
EXCLUDES = [
    ".git",
    ".vscode",
    "__pycache__",
    "*.pyc",
    "*.log",
    "*.pickle",
    "logs",
    "state",
    "data/outputs",  # Excluindo pastas de artefatos
]


def generate_tree(dir_path: Path, prefix: str = ""):
    """Gera a estrutura de árvore recursivamente."""

    # Lista o conteúdo do diretório, ordenado, ignorando os arquivos e pastas excluídos
    contents = sorted(
        [p for p in dir_path.iterdir() if not any(p.match(e) for e in EXCLUDES)]
    )

    # Calcula o total de arquivos no diretório atual
    pointers = [
        ("└── ", "    ") if i == len(contents) - 1 else ("├── ", "│   ")
        for i, _ in enumerate(contents)
    ]

    for i, path in enumerate(contents):
        pointer, new_prefix = pointers[i]

        # Imprime a linha do arquivo/diretório
        print(
            f"{prefix}{pointer}{path.name}/"
            if path.is_dir()
            else f"{prefix}{pointer}{path.name}"
        )

        # Se for um diretório, chama a função recursivamente
        if path.is_dir():
            generate_tree(path, prefix + new_prefix)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_dir = Path(sys.argv[1])
    else:
        start_dir = Path(".")  # Começa do diretório atual

    print(f"{start_dir.resolve().name}/")
    generate_tree(start_dir)
