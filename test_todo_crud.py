from __future__ import annotations

import pytest
from todo_crud import TodoRepository


def test_crud_lifecycle() -> None:
    repo = TodoRepository(":memory:")
    item = repo.create("Study Polars", "Vectorized ETL pipelines")
    assert item.id == 1
    assert item.title == "Study Polars"
    assert item.completed is False

    all_items = repo.list_all()
    assert len(all_items) == 1

    updated = repo.update(item.id, completed=True)
    assert updated is not None
    assert updated.completed is True

    assert repo.delete(item.id) is True
    assert repo.get_by_id(item.id) is None


def test_rejects_empty_or_whitespace_title() -> None:
    repo = TodoRepository(":memory:")
    with pytest.raises(ValueError):
        repo.create("   ")

    item = repo.create("Valid task")
    with pytest.raises(ValueError):
        repo.update(item.id, title="")
