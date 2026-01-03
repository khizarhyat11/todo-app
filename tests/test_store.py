"""Unit Tests for TaskStore

Comprehensive test coverage for the TaskStore class including:
- CRUD operations (add, get, list, update, delete)
- Filtering functionality
- Error handling and edge cases
- ID auto-increment behavior
- Timestamp management
"""

import pytest
from datetime import datetime
from src.store import TaskStore
from src.models import Task


@pytest.fixture
def store() -> TaskStore:
    """Fixture providing a fresh TaskStore instance for each test."""
    return TaskStore()


class TestTaskStoreAdd:
    """Test TaskStore.add() method"""

    def test_add_single_task(self, store: TaskStore) -> None:
        """Test adding a single task with title only"""
        task = store.add("Buy milk")
        assert task.id == 1
        assert task.title == "Buy milk"
        assert task.description == ""
        assert task.completed is False
        assert task.created_at is not None
        assert task.completed_at is None

    def test_add_with_description(self, store: TaskStore) -> None:
        """Test adding a task with both title and description"""
        task = store.add("Buy milk", "whole milk")
        assert task.title == "Buy milk"
        assert task.description == "whole milk"

    def test_add_multiple_tasks_auto_increment(self, store: TaskStore) -> None:
        """Test that multiple adds auto-increment IDs"""
        t1 = store.add("Task 1")
        t2 = store.add("Task 2")
        t3 = store.add("Task 3")
        assert t1.id == 1
        assert t2.id == 2
        assert t3.id == 3

    def test_add_empty_title_raises_error(self, store: TaskStore) -> None:
        """Test that adding task with empty title raises ValueError"""
        with pytest.raises(ValueError):
            store.add("")

    def test_add_whitespace_title_raises_error(self, store: TaskStore) -> None:
        """Test that adding task with whitespace-only title raises ValueError"""
        with pytest.raises(ValueError):
            store.add("   ")

    def test_add_sets_created_at(self, store: TaskStore) -> None:
        """Test that created_at is automatically set"""
        before = datetime.now()
        task = store.add("Test")
        after = datetime.now()
        assert before <= task.created_at <= after

    def test_add_returns_task_object(self, store: TaskStore) -> None:
        """Test that add() returns a Task instance"""
        task = store.add("Test")
        assert isinstance(task, Task)


class TestTaskStoreGet:
    """Test TaskStore.get() method"""

    def test_get_existing_task(self, store: TaskStore) -> None:
        """Test retrieving an existing task"""
        added = store.add("Test")
        retrieved = store.get(1)
        assert retrieved is not None
        assert retrieved.id == added.id
        assert retrieved.title == added.title

    def test_get_non_existent_task(self, store: TaskStore) -> None:
        """Test that get() returns None for non-existent ID"""
        assert store.get(999) is None

    def test_get_empty_store(self, store: TaskStore) -> None:
        """Test that get() on empty store returns None"""
        assert store.get(1) is None


class TestTaskStoreList:
    """Test TaskStore.list() method"""

    def test_list_all_tasks(self, store: TaskStore) -> None:
        """Test listing all tasks"""
        store.add("Task 1")
        store.add("Task 2")
        tasks = store.list()
        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"

    def test_list_empty_store(self, store: TaskStore) -> None:
        """Test listing tasks from empty store"""
        tasks = store.list()
        assert tasks == []

    def test_list_filter_pending(self, store: TaskStore) -> None:
        """Test listing only pending tasks"""
        t1 = store.add("Task 1")
        t2 = store.add("Task 2")
        store.update(1, completed=True)
        pending = store.list(filter_by="pending")
        assert len(pending) == 1
        assert pending[0].id == 2

    def test_list_filter_completed(self, store: TaskStore) -> None:
        """Test listing only completed tasks"""
        t1 = store.add("Task 1")
        t2 = store.add("Task 2")
        store.update(1, completed=True)
        completed = store.list(filter_by="completed")
        assert len(completed) == 1
        assert completed[0].id == 1

    def test_list_filter_all(self, store: TaskStore) -> None:
        """Test listing all tasks with explicit 'all' filter"""
        store.add("Task 1")
        store.add("Task 2")
        store.update(1, completed=True)
        all_tasks = store.list(filter_by="all")
        assert len(all_tasks) == 2

    def test_list_invalid_filter(self, store: TaskStore) -> None:
        """Test that invalid filter raises ValueError"""
        with pytest.raises(ValueError):
            store.list(filter_by="invalid")

    def test_list_returns_copy(self, store: TaskStore) -> None:
        """Test that list() returns a copy, not reference"""
        store.add("Task 1")
        tasks = store.list()
        tasks.pop()  # Modify returned list
        assert len(store.list()) == 1  # Original unchanged


class TestTaskStoreUpdate:
    """Test TaskStore.update() method"""

    def test_update_title(self, store: TaskStore) -> None:
        """Test updating task title"""
        store.add("Old title")
        updated = store.update(1, title="New title")
        assert updated.title == "New title"
        assert updated.id == 1

    def test_update_description(self, store: TaskStore) -> None:
        """Test updating task description"""
        store.add("Task", "Old desc")
        updated = store.update(1, description="New desc")
        assert updated.description == "New desc"

    def test_update_completed_true(self, store: TaskStore) -> None:
        """Test marking task as completed"""
        store.add("Task")
        before = datetime.now()
        updated = store.update(1, completed=True)
        after = datetime.now()
        assert updated.completed is True
        assert updated.completed_at is not None
        assert before <= updated.completed_at <= after

    def test_update_completed_false(self, store: TaskStore) -> None:
        """Test marking completed task as pending"""
        store.add("Task")
        store.update(1, completed=True)
        assert store.get(1).completed_at is not None
        updated = store.update(1, completed=False)
        assert updated.completed is False
        assert updated.completed_at is None

    def test_update_non_existent_raises_error(self, store: TaskStore) -> None:
        """Test that updating non-existent task raises KeyError"""
        with pytest.raises(KeyError):
            store.update(999, title="New")

    def test_update_multiple_fields(self, store: TaskStore) -> None:
        """Test updating multiple fields at once"""
        store.add("Old", "Old desc")
        updated = store.update(1, title="New", description="New desc")
        assert updated.title == "New"
        assert updated.description == "New desc"

    def test_update_persists_unchanged_fields(self, store: TaskStore) -> None:
        """Test that updating one field preserves others"""
        store.add("Title", "Desc")
        store.update(1, completed=True)
        task = store.get(1)
        assert task.title == "Title"
        assert task.description == "Desc"


class TestTaskStoreDelete:
    """Test TaskStore.delete() method"""

    def test_delete_existing_task(self, store: TaskStore) -> None:
        """Test deleting an existing task"""
        store.add("Task")
        result = store.delete(1)
        assert result is True
        assert store.get(1) is None

    def test_delete_non_existent_task(self, store: TaskStore) -> None:
        """Test that deleting non-existent task returns False"""
        result = store.delete(999)
        assert result is False

    def test_delete_removes_from_list(self, store: TaskStore) -> None:
        """Test that delete removes task from list"""
        store.add("Task 1")
        store.add("Task 2")
        store.delete(1)
        tasks = store.list()
        assert len(tasks) == 1
        assert tasks[0].id == 2


class TestTaskStoreIntegration:
    """Integration tests combining multiple operations"""

    def test_full_crud_workflow(self, store: TaskStore) -> None:
        """Test complete CRUD workflow"""
        # Create
        t1 = store.add("Buy milk", "whole milk")
        assert t1.id == 1

        # Read
        retrieved = store.get(1)
        assert retrieved.title == "Buy milk"

        # Update
        store.update(1, completed=True)
        assert store.get(1).completed is True

        # Delete
        assert store.delete(1) is True
        assert store.get(1) is None

    def test_mixed_task_states(self, store: TaskStore) -> None:
        """Test store with tasks in different states"""
        store.add("Task 1")
        store.add("Task 2")
        store.add("Task 3")
        store.update(1, completed=True)
        store.update(2, completed=True)

        all_tasks = store.list()
        pending = store.list(filter_by="pending")
        completed = store.list(filter_by="completed")

        assert len(all_tasks) == 3
        assert len(pending) == 1
        assert len(completed) == 2

    def test_id_persistence_after_delete(self, store: TaskStore) -> None:
        """Test that next ID continues after deletion"""
        t1 = store.add("Task 1")
        t2 = store.add("Task 2")
        store.delete(1)
        t3 = store.add("Task 3")
        assert t3.id == 3  # ID continues, not reset
