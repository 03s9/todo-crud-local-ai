# Todo CRUD Local AI

![CI Status](https://github.com/03s9/todo-crud-local-ai/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.x-green.svg)
![Ruff](https://img.shields.io/badge/Ruff-0.13.0+-blueviolet.svg)

## Visão Geral e Arquitetura

O projeto `todo-crud-local-ai` é uma implementação de um sistema CRUD (Create, Read, Update, Delete) para gerenciamento de tarefas (To-Do) utilizando Python 3.11+ e SQLite. A arquitetura é modular, com o módulo `todo_crud.py` contendo a lógica de negócios e persistência de dados. O sistema utiliza uma abordagem com a dataclass `TodoItem` e o repositório `TodoRepository` para manipulação dos dados em memória (`:memory:`) ou persistidos em arquivo.

## Funcionalidades Principais

- **CRUD Completo**: Operações de criação, leitura, atualização e exclusão de tarefas.
- **Validação de Dados**: Verificação de integridade garantindo que `title` não seja vazio nem apenas espaços em branco.
- **Persistência Parametrizada**: Queries SQL com `?` prevenindo SQL injection no SQLite.
- **Testes Automatizados**: Suíte de testes com `pytest` e auto-teste determinístico no `__main__`.
- **Integração CI/CD Sanitizada**: Workflow do GitHub Actions com auto-abertura de Issues e mascaramento de segredos para diagnóstico conjunto com IAs locais (`gemma4:31b` + `chatgpt-codex`).

## Pré-requisitos e Instalação

1. **Clonar o Repositório**:
   ```bash
   git clone https://github.com/03s9/todo-crud-local-ai.git
   cd todo-crud-local-ai
   ```

2. **Criar e Ativar Ambiente Virtual**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scriptsctivate
   ```

3. **Instalar Dependências de Teste/Lint**:
   ```bash
   pip install ruff pytest
   ```

## Guia Rápido de Uso

```python
from todo_crud import TodoRepository

# Inicializar repositório em memória (ou passar caminho do banco SQLite: "todos.db")
repo = TodoRepository()

# 1. Criar tarefas (com validação anti-vazio)
task1 = repo.create(title="Estudar Python", description="Revisar padrões de dados e tipagem")
task2 = repo.create(title="Testar CI", description="Validar GitHub Actions com auto-issue")
print(f"Criada: {task1.id} - {task1.title}")

# 2. Listar tarefas
tasks = repo.list_all()
print(f"Total de tarefas: {len(tasks)}")

# 3. Atualizar tarefa
updated = repo.update(task1.id, completed=True)
print(f"Status atualizado: {updated.completed}")

# 4. Deletar tarefa
repo.delete(task2.id)
print(f"Restantes: {len(repo.list_all())}")
```

## Execução de Testes

```bash
# Executar suíte de testes com pytest
pytest -q

# Ou executar o auto-teste direto do módulo
python3 todo_crud.py
```

## Pipeline de CI/CD & Auto-Triagem

O pipeline em `.github/workflows/ci.yml` executa as seguintes etapas:

- **Lint & Compilação**: Executa `ruff` e `py_compile` para validação estática imediata.
- **Testes**: Roda `pytest -q --tb=line --show-capture=no` para evitar vazamento de memória ou stdout/stderr nos logs.
- **Sanitização Prévia de Logs**: Filtra expressões sensíveis (tokens `ghp_`/`sk-`, CPFs, e-mails, senhas) via regex `sed -E`.
- **Auto-Abertura de Issue**: Se o teste falhar no push, abre automaticamente uma Issue com o log sanitizado para o pipeline local `resolve_ci_issue_gemma4_codex` (`gemma4:31b` para diagnóstico + `chatgpt-codex` para resolução).

## Governança e Boas Práticas

- **Human-in-the-Loop**: Automações atuam no diagnóstico e testes; `git commit` e `git push` ocorrem exclusivamente sob ordem explícita do usuário.
- **Zero Vazamentos**: Repositório livre de tokens, segredos, senhas e caminhos locais da máquina host.

