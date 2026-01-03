# Phase-I In-Memory Todo Console Application – Implementation Tasks

**Feature:** core  
**Phase:** I  
**Version:** 1.0  
**Status:** Active  
**Date:** 2026-01-03  
**Baseline Specification:** `specs/spec.md`  
**Architecture Plan:** `specs/plan.md`  

---

## Overview

Testable, granular implementation tasks derived from baseline specification and architecture plan. Each task has explicit acceptance criteria and test cases. Tasks must be completed in order (dependencies tracked).

**Execution Rule:** No manual code edits. All code generated from these tasks by Claude Code.

---

## Task 1: Define Task Data Model

**Feature:** core  
**Layer:** Models  
**File:** `src/models.py`  
**Status:** Not Started  
**Dependencies:** None

### Description
Create `Task` dataclass with all required fields, type hints, and docstrings.

### Acceptance Criteria
- [ ] `Task` dataclass defined with exact fields: `id`, `title`, `description`, `completed`, `created_at`, `completed_at`
- [ ] All fields have correct type hints: `id: int | None`, `title: str`, `description: str`, `completed: bool`, `created_at: datetime`, `completed_at: datetime | None`
- [ ] Default values: `description=""`, `completed=False`, `created_at=datetime.now()`, `completed_at=None`, `id=None`
- [ ] Dataclass is properly decorated with `@dataclass`
- [ ] Module has docstring
- [ ] Dataclass has docstring explaining purpose
- [ ] Module is importable: `from src.models import Task`
- [ ] Task instances are creatable with title only: `Task(title="Buy milk")`

### Test Cases

**Test 1.1: Create task with title only**
```python
task = Task(title="Buy milk")
assert task.title == "Buy milk"
assert task.description == ""
assert task.completed == False
assert task.id is None
assert task.created_at is not None
assert task.completed_at is None
```

**Test 1.2: Create task with description**
```python
task = Task(title="Buy milk", description="whole milk")
assert task.title == "Buy milk"
assert task.description == "whole milk"
```

**Test 1.3: Field types are correct**
```python
task = Task(title="Test")
assert isinstance(task.title, str)
assert isinstance(task.completed, bool)
assert isinstance(task.created_at, datetime)
assert task.id is None
assert isinstance(task.description, str)
```

**Test 1.4: Dataclass is importable**
```python
from src.models import Task
assert Task is not None
```

### Code References
- **File:** `src/models.py` (new)
- **Import:** `from datetime import datetime`
- **Import:** `from dataclasses import dataclass, field`

---

## Task 2: Implement TaskStore Class

**Feature:** core  
**Layer:** Store  
**File:** `src/store.py`  
**Status:** Not Started  
**Dependencies:** Task 1

### Description
Implement in-memory `TaskStore` class with CRUD operations, auto-increment ID generation, and timestamp management.

### Acceptance Criteria
- [ ] `TaskStore` class instantiable with no arguments: `store = TaskStore()`
- [ ] Initial state is empty: `store.list() == []`
- [ ] `add(title, description="")` creates task with auto-incremented ID starting from 1
- [ ] `add()` returns `Task` object with assigned ID
- [ ] `add()` auto-sets `created_at` timestamp
- [ ] `add()` raises `ValueError` if title is empty or whitespace-only
- [ ] `get(id)` returns `Task` if found, else `None`
- [ ] `list()` returns all tasks in insertion order
- [ ] `list(filter="all")` returns all tasks
- [ ] `list(filter="pending")` returns only tasks where `completed=False`
- [ ] `list(filter="completed")` returns only tasks where `completed=True`
- [ ] `list(filter="invalid")` raises `ValueError`
- [ ] `update(id, **changes)` modifies task and returns it
- [ ] `update()` raises `KeyError` if task ID not found
- [ ] `update(id, completed=True)` sets `completed_at` timestamp
- [ ] `update(id, completed=False)` clears `completed_at` (sets to None)
- [ ] `delete(id)` removes task and returns `True`
- [ ] `delete(id)` returns `False` if task ID not found
- [ ] Multiple adds generate sequential IDs: 1, 2, 3...
- [ ] Type hints on all methods
- [ ] Docstrings on all public methods
- [ ] Module is importable: `from src.store import TaskStore`

### Test Cases

**Test 2.1: Add single task**
```python
store = TaskStore()
task = store.add("Buy milk")
assert task.id == 1
assert task.title == "Buy milk"
assert task.completed == False
assert task.created_at is not None
```

**Test 2.2: Add with description**
```python
store = TaskStore()
task = store.add("Buy milk", "whole milk")
assert task.title == "Buy milk"
assert task.description == "whole milk"
```

**Test 2.3: Multiple adds auto-increment**
```python
store = TaskStore()
t1 = store.add("Task 1")
t2 = store.add("Task 2")
t3 = store.add("Task 3")
assert t1.id == 1
assert t2.id == 2
assert t3.id == 3
```

**Test 2.4: Add with empty title raises error**
```python
store = TaskStore()
with pytest.raises(ValueError):
    store.add("")
with pytest.raises(ValueError):
    store.add("   ")  # whitespace
```

**Test 2.5: Get existing task**
```python
store = TaskStore()
added = store.add("Test")
retrieved = store.get(1)
assert retrieved == added
```

**Test 2.6: Get non-existent task**
```python
store = TaskStore()
assert store.get(999) is None
```

**Test 2.7: List all tasks**
```python
store = TaskStore()
store.add("Task 1")
store.add("Task 2")
tasks = store.list()
assert len(tasks) == 2
assert tasks[0].title == "Task 1"
assert tasks[1].title == "Task 2"
```

**Test 2.8: List filter completed**
```python
store = TaskStore()
t1 = store.add("Task 1")
t2 = store.add("Task 2")
store.update(1, completed=True)
completed = store.list(filter="completed")
assert len(completed) == 1
assert completed[0].id == 1
```

**Test 2.9: List filter pending**
```python
store = TaskStore()
t1 = store.add("Task 1")
t2 = store.add("Task 2")
store.update(1, completed=True)
pending = store.list(filter="pending")
assert len(pending) == 1
assert pending[0].id == 2
```

**Test 2.10: List invalid filter**
```python
store = TaskStore()
with pytest.raises(ValueError):
    store.list(filter="invalid")
```

**Test 2.11: Update task title**
```python
store = TaskStore()
store.add("Old title")
updated = store.update(1, title="New title")
assert updated.title == "New title"
assert updated.id == 1
```

**Test 2.12: Update sets completed_at timestamp**
```python
store = TaskStore()
store.add("Task")
before = datetime.now()
store.update(1, completed=True)
task = store.get(1)
assert task.completed == True
assert task.completed_at is not None
assert task.completed_at >= before
```

**Test 2.13: Update clears completed_at**
```python
store = TaskStore()
store.add("Task")
store.update(1, completed=True)
assert store.get(1).completed_at is not None
store.update(1, completed=False)
assert store.get(1).completed_at is None
```

**Test 2.14: Update non-existent raises error**
```python
store = TaskStore()
with pytest.raises(KeyError):
    store.update(999, title="New")
```

**Test 2.15: Delete existing task**
```python
store = TaskStore()
store.add("Task")
result = store.delete(1)
assert result == True
assert store.get(1) is None
```

**Test 2.16: Delete non-existent task**
```python
store = TaskStore()
result = store.delete(999)
assert result == False
```

### Code References
- **File:** `src/store.py` (new)
- **Import:** `from datetime import datetime`
- **Import:** `from src.models import Task`

---

## Task 3: Implement Command Handlers

**Feature:** core  
**Layer:** Commands  
**File:** `src/commands.py`  
**Status:** Not Started  
**Dependencies:** Task 1, Task 2

### Description
Implement command parsing and handler functions for all user commands: add, list, show, update, delete, help.

### Acceptance Criteria
- [ ] `cmd_add(args: list[str], store: TaskStore) -> str` implemented
- [ ] `cmd_list(args: list[str], store: TaskStore) -> str` implemented
- [ ] `cmd_show(args: list[str], store: TaskStore) -> str` implemented
- [ ] `cmd_update(args: list[str], store: TaskStore) -> str` implemented
- [ ] `cmd_delete(args: list[str], store: TaskStore) -> str` implemented
- [ ] `cmd_help(args: list[str], store: TaskStore) -> str` implemented
- [ ] `dispatch(command: str, args: list[str], store: TaskStore) -> str` implemented
- [ ] Command registry (dict) maps command names to handlers
- [ ] All handlers return message string with ✓, ✗, or ℹ prefix
- [ ] Argument parsing extracts command and options correctly
- [ ] All handlers have type hints
- [ ] All handlers have docstrings
- [ ] Module is importable: `from src.commands import dispatch`
- [ ] All output messages match format in baseline spec

### Command Handler Details

**cmd_add:**
- Usage: `add <title> [--description <desc>]`
- Success: `✓ Task added with ID <id>: <title>`
- Error (empty title): `✗ Task title cannot be empty`
- Returns assigned ID in success message

**cmd_list:**
- Usage: `list [--filter all|pending|completed]`
- Output: ASCII table with headers: `ID | Title | Status | Created`
- Each row format: `<id> | <title> | <status> | <timestamp>`
- Status: "pending" or "completed"
- Empty list: `ℹ No tasks yet`
- Invalid filter: `✗ Invalid filter. Use 'all', 'pending', or 'completed'.`

**cmd_show:**
- Usage: `show <id>`
- Output (success): Formatted details (ID, Title, Description, Status, Created, Completed)
- Error (not found): `✗ Task not found (ID: <id>)`
- Error (invalid ID): `✗ Invalid task ID`

**cmd_update:**
- Usage: `update <id> [--title <new>] [--description <new>] [--status pending|completed]`
- Success: `✓ Task <id> updated`
- Error (not found): `✗ Task not found (ID: <id>)`
- Error (invalid status): `✗ Invalid status. Use 'pending' or 'completed'.`
- Error (invalid ID): `✗ Invalid task ID`

**cmd_delete:**
- Usage: `delete <id>`
- Success: `✓ Task <id> deleted`
- Error (not found): `✗ Task not found (ID: <id>)`
- Error (invalid ID): `✗ Invalid task ID`

**cmd_help:**
- Usage: `help [command]`
- Without args: Show list of all commands with one-line descriptions
- With command: Show detailed help for that command (usage + description)
- Error (unknown command): `✗ Unknown command: <command>`

### Test Cases (Select)

**Test 3.1: Add command with title**
```python
store = TaskStore()
result = cmd_add(["Buy milk"], store)
assert result.startswith("✓ Task added")
assert "ID 1" in result
assert "Buy milk" in result
```

**Test 3.2: Add command with description**
```python
store = TaskStore()
result = cmd_add(["Buy milk", "--description", "whole milk"], store)
assert result.startswith("✓")
assert store.get(1).description == "whole milk"
```

**Test 3.3: List command (all)**
```python
store = TaskStore()
store.add("Task 1")
store.add("Task 2")
result = cmd_list([], store)
assert "ID" in result
assert "Task 1" in result
assert "Task 2" in result
assert "|" in result  # table format
```

**Test 3.4: List empty**
```python
store = TaskStore()
result = cmd_list([], store)
assert result.startswith("ℹ No tasks")
```

**Test 3.5: Show task**
```python
store = TaskStore()
store.add("Test task", "Test desc")
result = cmd_show(["1"], store)
assert "ID" in result
assert "Test task" in result
assert "Test desc" in result
```

**Test 3.6: Update task**
```python
store = TaskStore()
store.add("Old")
result = cmd_update(["1", "--title", "New"], store)
assert result.startswith("✓")
assert store.get(1).title == "New"
```

**Test 3.7: Delete task**
```python
store = TaskStore()
store.add("Task")
result = cmd_delete(["1"], store)
assert result.startswith("✓ Task 1 deleted")
assert store.get(1) is None
```

**Test 3.8: Help command**
```python
store = TaskStore()
result = cmd_help([], store)
assert "add" in result.lower()
assert "list" in result.lower()
assert "delete" in result.lower()
```

**Test 3.9: Dispatch to add**
```python
store = TaskStore()
result = dispatch("add", ["Task"], store)
assert result.startswith("✓")
```

**Test 3.10: Dispatch unknown command**
```python
store = TaskStore()
with pytest.raises(ValueError):
    dispatch("unknown", [], store)
```

### Code References
- **File:** `src/commands.py` (new)
- **Import:** `from src.models import Task`
- **Import:** `from src.store import TaskStore`
- **Table formatting:** Use ASCII with `|` and `-` characters

---

## Task 4: Implement Application REPL Loop

**Feature:** core  
**Layer:** Application  
**File:** `src/app.py`  
**Status:** Not Started  
**Dependencies:** Task 1, Task 2, Task 3

### Description
Implement REPL loop: prompt user, parse input, dispatch to commands, display output, handle errors gracefully.

### Acceptance Criteria
- [ ] `run()` function implemented
- [ ] Displays welcome message: "Welcome to Todo App!"
- [ ] Displays hint: "Type 'help' for available commands."
- [ ] Enters infinite REPL loop
- [ ] Displays prompt: `todo> `
- [ ] Reads user input from stdin
- [ ] Parses command and arguments (splits on spaces, handles options)
- [ ] Calls `dispatch()` from commands module
- [ ] Displays result message from dispatcher
- [ ] Loops back to prompt after each command
- [ ] Exits on `quit` or `exit` command
- [ ] Displays goodbye message on exit
- [ ] Catches and displays exceptions gracefully (no crash)
- [ ] Re-prompts after error (continues loop)
- [ ] Type hints on `run()`
- [ ] Docstring on `run()`
- [ ] Module is importable: `from src.app import run`

### Test Cases (Manual/Acceptance)

**Test 4.1: Start and quit**
```
Expected input sequence: quit
Expected output:
  Welcome to Todo App!
  Type 'help' for available commands.
  todo> <quit>
  Goodbye!
  (exit with code 0)
```

**Test 4.2: Invalid command**
```
Expected input: unknown_cmd
Expected output: Prompts and handles error gracefully, re-prompts
```

**Test 4.3: Full workflow**
```
Input sequence:
  add Buy milk --description whole milk
  list
  show 1
  update 1 --status completed
  delete 1
  quit

Expected: All commands execute, output displayed, exit cleanly
```

### Code References
- **File:** `src/app.py` (new)
- **Import:** `from src.store import TaskStore`
- **Import:** `from src.commands import dispatch`

---

## Task 5: Create Package Structure

**Feature:** core  
**Layer:** Package  
**Files:** `src/__init__.py`, `src/__main__.py`  
**Status:** Not Started  
**Dependencies:** Task 4

### Description
Create package structure files for proper Python module initialization and command-line execution.

### Acceptance Criteria
- [ ] `src/__init__.py` exists with package docstring
- [ ] `src/__init__.py` imports `Task` and `TaskStore` for public API
- [ ] `src/__main__.py` exists and imports `run()` from app module
- [ ] `src/__main__.py` calls `run()` function
- [ ] Application executable via: `python -m src`
- [ ] Type hints present where applicable
- [ ] Docstrings on all public functions

### Code References
- **Files:** `src/__init__.py` (new), `src/__main__.py` (new)
- **Entry point:** `python -m src` should start the REPL

---

## Task 6: Implement Unit Tests for Store

**Feature:** core  
**Layer:** Testing  
**File:** `tests/test_store.py`  
**Status:** Not Started  
**Dependencies:** Task 2

### Description
Implement comprehensive unit tests for `TaskStore` class covering all CRUD operations, filtering, and edge cases.

### Acceptance Criteria
- [ ] All test cases from Task 2 implemented
- [ ] Test file has pytest fixtures for store initialization
- [ ] All tests pass: `pytest tests/test_store.py -v`
- [ ] Code coverage 100% for store.py
- [ ] Clear test names describing expected behavior
- [ ] Tests are isolated and independent

### Code References
- **File:** `tests/test_store.py` (new)
- **Framework:** pytest
- **Fixtures:** TaskStore instance(s)

---

## Task 7: Implement Integration Tests for Commands

**Feature:** core  
**Layer:** Testing  
**File:** `tests/test_commands.py`  
**Status:** Not Started  
**Dependencies:** Task 3

### Description
Implement comprehensive integration tests for command handlers covering argument parsing, output formatting, and error conditions.

### Acceptance Criteria
- [ ] All test cases from Task 3 implemented
- [ ] Test file has pytest fixtures for store + command testing
- [ ] All tests pass: `pytest tests/test_commands.py -v`
- [ ] Code coverage 100% for commands.py
- [ ] Tests verify output message format (✓/✗/ℹ prefixes)
- [ ] Tests verify table formatting for list command
- [ ] Tests verify detail formatting for show command
- [ ] Error scenarios thoroughly tested

### Code References
- **File:** `tests/test_commands.py` (new)
- **Framework:** pytest
- **Fixtures:** TaskStore instance(s)

---

## Task 8: Implement Acceptance Tests for Full Workflow

**Feature:** core  
**Layer:** Testing  
**File:** `tests/test_acceptance.py`  
**Status:** Not Started  
**Dependencies:** Task 4

### Description
Implement end-to-end acceptance tests simulating real user workflows through the application.

### Acceptance Criteria
- [ ] Full workflow tests (add → list → show → update → delete → quit)
- [ ] Error recovery tests (invalid input handled gracefully)
- [ ] Complex workflow tests (multiple tasks with filtering)
- [ ] All tests pass: `pytest tests/test_acceptance.py -v`
- [ ] Test coverage includes all user interactions
- [ ] Tests validate console output format and behavior

### Code References
- **File:** `tests/test_acceptance.py` (new)
- **Framework:** pytest
- **Approach:** Capture REPL output and verify behavior

---

**Final Status:** Ready for implementation in order (Task 1 → Task 2 → ... → Task 8)
