"""Todo App - Phase I: In-Memory Console Application

An AI-native, spec-driven Todo application built with Python 3.13+.
All functionality is derived from specifications in specs/core/.
"""

from src.models import Task
from src.store import TaskStore

__all__ = ["Task", "TaskStore"]
