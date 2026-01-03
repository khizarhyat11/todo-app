"""Todo App - Phase I: In-Memory Task Store

This module provides TaskStore, an in-memory storage layer for tasks.
It implements CRUD operations with auto-increment ID generation and timestamp management.
"""

from datetime import datetime
from src.models import Task


class TaskStore:
    """
    In-memory storage for tasks with CRUD operations.

    This class manages a collection of Task objects, handling:
    - Auto-increment ID generation (starting from 1)
    - CRUD operations (create, read, update, delete)
    - Task filtering by completion status
    - Timestamp management for created_at and completed_at

    Attributes:
        _tasks: Internal list holding Task objects
        _next_id: Next ID to assign on task creation
    """

    def __init__(self) -> None:
        """Initialize an empty task store."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add(self, title: str, description: str = "") -> Task:
        """
        Create and store a new task with auto-incremented ID.

        Args:
            title: Task title (must not be empty or whitespace-only)
            description: Optional task description

        Returns:
            The created Task object with assigned ID and created_at timestamp

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            created_at=datetime.now(),
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:
        """
        Retrieve a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def list(self, filter_by: str = "all") -> list[Task]:
        """
        List tasks, optionally filtered by completion status.

        Args:
            filter_by: Filter type - "all", "pending", or "completed"

        Returns:
            List of Task objects matching the filter

        Raises:
            ValueError: If filter_by is not a valid option
        """
        if filter_by not in ("all", "pending", "completed"):
            raise ValueError(
                "Invalid filter. Use 'all', 'pending', or 'completed'."
            )

        if filter_by == "all":
            return self._tasks.copy()
        elif filter_by == "pending":
            return [t for t in self._tasks if not t.completed]
        else:  # completed
            return [t for t in self._tasks if t.completed]

    def update(self, task_id: int, **changes) -> Task:
        """
        Update one or more fields of a task.

        Args:
            task_id: The ID of the task to update
            **changes: Keyword arguments for fields to update
                      (e.g., title="new", completed=True, description="new desc")

        Returns:
            The updated Task object

        Raises:
            KeyError: If task ID not found
        """
        task = self.get(task_id)
        if task is None:
            raise KeyError(f"Task {task_id} not found")

        # Handle completed status change
        if "completed" in changes:
            new_completed = changes["completed"]
            if new_completed and not task.completed:
                # Marking as complete
                task.completed = True
                task.completed_at = datetime.now()
            elif not new_completed and task.completed:
                # Marking as pending
                task.completed = False
                task.completed_at = None
            else:
                # No change in status
                task.completed = new_completed
        else:
            # If completed not in changes, don't modify status
            pass

        # Update other fields
        for key, value in changes.items():
            if key != "completed":
                if hasattr(task, key):
                    setattr(task, key, value)

        return task

    def delete(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task was found and deleted, False otherwise
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                return True
        return False
