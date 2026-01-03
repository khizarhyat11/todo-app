"""Todo App - Phase I: Domain Data Models

This module defines the core domain data structures for the Todo application.
No business logic or I/O operations are performed here.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single task/todo item in the application.

    Attributes:
        id: Unique identifier (auto-assigned by TaskStore, None before assignment)
        title: Non-empty task title/description
        description: Optional detailed explanation of the task
        completed: Current completion status (default: False)
        created_at: Timestamp when task was created (auto-set)
        completed_at: Timestamp when task was marked complete (None if not completed)
    """

    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    id: int | None = None
