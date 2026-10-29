# To-Do List CRUD (SQLite + Python 3.11+)

Módulo enxuto de CRUD de To-Do List em Python 3.11+ com persistência SQLite parametrizada, tipagem estrita e CI automatizado via GitHub Actions.

## Estrutura
- `todo_crud.py`: Implementação de `TodoItem` e `TodoRepository` (SQLite `:memory:` ou arquivo).
- `test_todo_crud.py`: Testes determinísticos (`pytest`) cobrindo ciclo CRUD e validação de títulos vazios.
- `.github/workflows/ci.yml`: Pipeline GitHub Actions com `ruff`, `pytest`, sanitização de logs e abertura automática de Issue para triagem conjunta (`gemma4:31b` + `chatgpt-codex`).

## Execução Local
```bash
python3 todo_crud.py
pytest -q
```
