from __future__ import annotations

import sqlite3
from dataclasses import dataclass


@dataclass(slots=True)
class TodoItem:
    id: int
    title: str
    description: str
    completed: bool

    @classmethod
    def from_row(cls, row: tuple[int, str, str, int]) -> TodoItem:
        return cls(id=row[0], title=row[1], description=row[2], completed=bool(row[3]))


class TodoRepository:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.connection = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self) -> None:
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    completed BOOLEAN NOT NULL DEFAULT 0
                )
                """
            )

    def create(self, title: str, description: str = "") -> TodoItem:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or consist only of whitespace")
        with self.connection:
            cursor = self.connection.execute(
                "INSERT INTO todos (title, description) VALUES (?, ?)",
                (title, description),
            )
            todo_id = int(cursor.lastrowid or 0)
        created = self.get_by_id(todo_id)
        if created is None:
            raise RuntimeError("Falha ao recuperar TodoItem recém-criado.")
        return created

    def list_all(self, completed: bool | None = None) -> list[TodoItem]:
        if completed is None:
            cursor = self.connection.execute(
                "SELECT id, title, description, completed FROM todos ORDER BY id"
            )
        else:
            cursor = self.connection.execute(
                "SELECT id, title, description, completed FROM todos WHERE completed = ? ORDER BY id",
                (int(completed),),
            )
        return [TodoItem.from_row(row) for row in cursor.fetchall()]

    def get_by_id(self, todo_id: int) -> TodoItem | None:
        cursor = self.connection.execute(
            "SELECT id, title, description, completed FROM todos WHERE id = ?",
            (todo_id,),
        )
        row = cursor.fetchone()
        return TodoItem.from_row(row) if row else None

    def update(
        self,
        todo_id: int,
        title: str | None = None,
        description: str | None = None,
        completed: bool | None = None,
    ) -> TodoItem | None:
        todo = self.get_by_id(todo_id)
        if not todo:
            return None
        if title is not None and not title.strip():
            raise ValueError("Title cannot be empty or consist only of whitespace")
        new_title = title if title is not None else todo.title
        new_desc = description if description is not None else todo.description
        new_completed = int(completed if completed is not None else todo.completed)
        with self.connection:
            self.connection.execute(
                "UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?",
                (new_title, new_desc, new_completed, todo_id),
            )
        return self.get_by_id(todo_id)

    def delete(self, todo_id: int) -> bool:
        with self.connection:
            cursor = self.connection.execute(
                "DELETE FROM todos WHERE id = ?",
                (todo_id,),
            )
        return cursor.rowcount > 0


if __name__ == "__main__":
    repo = TodoRepository()

    todo1 = repo.create("Buy milk", "Buy whole milk from the grocery store")
    assert todo1.title == "Buy milk"
    assert todo1.description == "Buy whole milk from the grocery store"
    assert todo1.completed is False

    try:
        repo.create("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("create() deve rejeitar título vazio ou só com espaços")

    todos = repo.list_all()
    assert len(todos) == 1
    assert todos[0].id == todo1.id

    fetched = repo.get_by_id(todo1.id)
    assert fetched is not None and fetched.title == "Buy milk"

    updated_todo = repo.update(todo1.id, completed=True)
    assert updated_todo is not None and updated_todo.completed is True

    try:
        repo.update(todo1.id, title="")
    except ValueError:
        pass
    else:
        raise AssertionError("update() deve rejeitar título vazio")

    assert repo.delete(todo1.id) is True
    assert repo.get_by_id(todo1.id) is None

    print("[PASS] CRUD To-Do List validado com sucesso!")
