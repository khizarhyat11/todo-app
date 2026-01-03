# Phase-I In-Memory Todo Console Application – Architecture Plan

**Feature:** core  
**Phase:** I  
**Version:** 1.0  
**Status:** Active  
**Date:** 2026-01-03  
**Baseline Specification:** `specs/spec.md`

---

## Scope and Dependencies

### In Scope
- In-memory task storage (no persistence)
- CRUD operations on tasks
- Console command parser and dispatcher
- Command execution engine
- Task status management (pending/completed)
- Error handling and validation
- Help system

### Out of Scope
- Data persistence (file/database)
- Authentication/authorization
- Async operations
- Network communication
- Web/GUI interface
- Natural language input
- Performance optimization

### External Dependencies
- **Required:** Python 3.13+ (stdlib only)
- **Modules:** datetime, typing, sys
- **Third-party:** None (Phase I constraint)

## Architectural Decisions

### ADR-001: Layered Architecture for Forward Compatibility

**Decision:** Implement a strict 4-layer architecture: Models → Store → Commands → App

**Options Evaluated:**
1. Single monolithic module
2. Layered architecture (Models → Store → Commands → App) ← **Selected**
3. MVC pattern

**Rationale:**
- Clear layer boundaries enable future refactoring to web/API without business logic changes
- Each layer independently testable and verifiable
- Business logic (Store) completely decoupled from UI (Commands)
- Forward-compatible with AI agent extensibility (Phase II)
- Aligns with architectural constraint AC1–AC4 in baseline spec

**Trade-offs:**
- More files/modules than monolithic approach
- Slight verbosity in layer coordination
- **Benefit:** Maintainability, testability, and extensibility outweigh verbosity

**Accepted:** Yes

### ADR-002: Class-Based Store with Encapsulation

**Decision:** Implement in-memory storage as `TodoStore` class with public methods (add, get, list, update, delete)

**Options Evaluated:**
1. Simple dict of tasks keyed by ID
2. Class-based Store with encapsulation ← **Selected**
3. ORM-like abstraction

**Rationale:**
- Encapsulation allows transparent database swap in Phase II without API changes
- Type hints enable static analysis and IDE support
- Testable in isolation with no global state
- Supports auto-increment ID generation and timestamp management

**Trade-offs:**
- Slightly more code than dict approach
- **Benefit:** Enables persistence layer swap without breaking commands

**Accepted:** Yes

### ADR-003: Function Lookup Table for Command Dispatch

**Decision:** Use function registry (dict mapping command names to handler functions) for command dispatch

**Options Evaluated:**
1. String matching with if/elif chains
2. Function lookup table (registry dict) ← **Selected**
3. Command class hierarchy (polymorphic)

**Rationale:**
- Simple and direct for Phase I
- Extensible via dict registration (Phase II can add plugins)
- Minimal boilerplate; easy to read and maintain
- Pure function approach aligns with functional programming principles

**Trade-offs:**
- Requires explicit handler registration
- **Benefit:** Simplicity and maintainability for Phase I

**Accepted:** Yes

### ADR-004: String-Based Error Reporting

**Decision:** Errors reported as exception messages with user-facing strings

**Options Evaluated:**
1. Exception hierarchies with codes
2. String-based error messages ← **Selected**
3. Result/Either types

**Rationale:**
- Simplicity for Phase I
- Human-readable error messages
- Command handlers return strings; errors as exceptions

**Trade-offs:**
- Less structured than error codes
- **Benefit:** Simplicity and clarity for Phase I

**Accepted:** Yes

---

## System Architecture

### Layer Overview

```
┌─────────────────────────────────────────────┐
│         Application Layer (app.py)          │
│      REPL Loop + Console I/O                │
└─────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│      Commands Layer (commands.py)           │
│  Command Parsing + Business Logic           │
└─────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│        Store Layer (store.py)               │
│   In-Memory CRUD + ID Generation            │
└─────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│       Models Layer (models.py)              │
│   Task Data Structure                       │
└─────────────────────────────────────────────┘
```

---

## Layer Responsibilities

### Layer 1: Models (`src/models.py`)

**Responsibility:** Domain data structures (no I/O, no business logic)

**Components:**
- `Task` dataclass:
  - `id: int | None` – Unique identifier (None until assigned by Store)
  - `title: str` – Non-empty task title
  - `description: str` – Optional task details
  - `completed: bool` – Completion status (default: False)
  - `created_at: datetime` – Timestamp of creation
  - `completed_at: datetime | None` – Timestamp when marked complete (None if not completed)

**Constraints:**
- Immutable after creation (use dataclass with frozen=True consideration)
- Type hints required for all fields
- Docstrings required for dataclass

---

### Layer 2: Store (`src/store.py`)

**Responsibility:** In-memory data management and CRUD operations

**Components:**
- `TaskStore` class:
  - `__init__()` – Initialize empty store
  - `add(title: str, description: str = "") -> Task` – Create and return new task with auto-incremented ID
  - `get(id: int) -> Task | None` – Retrieve task by ID or None
  - `list(filter: str = "all") -> list[Task]` – List tasks by filter (all, pending, completed)
  - `update(id: int, **changes) -> Task` – Update task and return modified object
  - `delete(id: int) -> bool` – Remove task, return True if found else False

**Behavior:**
- Auto-increment ID generation starting from 1
- Auto-set `created_at` timestamp on add
- Auto-set `completed_at` when status changes to completed
- Clear `completed_at` when status changes to pending
- Raises `ValueError` if title is empty or invalid
- Raises `KeyError` if task ID not found (except get() returns None)

**Constraints:**
- Type hints required for all methods
- Docstrings required for all public methods
- No direct console I/O
- No global mutable state

---

### Layer 3: Commands (`src/commands.py`)

**Responsibility:** Command parsing, validation, and dispatching to store operations

**Components:**
- Command handlers (functions):
  - `cmd_add(args: list[str], store: TaskStore) -> str` – Create task
  - `cmd_list(args: list[str], store: TaskStore) -> str` – List tasks
  - `cmd_show(args: list[str], store: TaskStore) -> str` – Show task details
  - `cmd_update(args: list[str], store: TaskStore) -> str` – Modify task
  - `cmd_delete(args: list[str], store: TaskStore) -> str` – Delete task
  - `cmd_help(args: list[str], store: TaskStore) -> str` – Help information

- `dispatch(command: str, args: list[str], store: TaskStore) -> str`
  - Route commands to appropriate handler
  - Raise ValueError for unknown command

- `COMMAND_REGISTRY` dict
  - Maps command names to handler functions
  - Example: `{"add": cmd_add, "list": cmd_list, ...}`

**Behavior:**
- Parse arguments from list (command line split)
- Handle flags and options (e.g., `--title`, `--status`)
- Validate input before calling Store
- Return formatted messages with ✓, ✗, or ℹ prefix
- Raise exceptions on validation failure

**Constraints:**
- Type hints required for all functions
- Docstrings required for all handlers
- No direct console I/O (return strings only)
- No global mutable state
- Pure functions (same input → same output)

---

### Layer 4: Application (`src/app.py`)

**Responsibility:** REPL loop, console I/O, and application lifecycle

**Components:**
- `run() -> None` function:
  1. Display welcome message: "Welcome to Todo App!"
  2. Display hint: "Type 'help' for available commands."
  3. Enter REPL loop:
     - Display prompt: `todo> `
     - Read user input from stdin
     - Parse: extract command and arguments
     - Call `dispatch()` from commands module
     - Display result message
     - Continue loop
  4. Exit on "quit" or "exit" command with goodbye message
  5. Catch exceptions and display user-facing error messages

- `__main__` entrypoint:
  - Create TaskStore instance
  - Call `run()`

**Behavior:**
- Deterministic output format
- Graceful error recovery (re-prompt after error)
- No crash on invalid input
- Clean exit on quit/exit

**Constraints:**
- Type hints required
- Docstrings required
- No business logic (only I/O and dispatch)
- All error handling in this layer

---

## API Contracts and Interfaces

### Store API (`src/store.py`)

```python
from datetime import datetime

@dataclass
class Task:
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None
    id: int | None = None

class TaskStore:
    def add(self, title: str, description: str = "") -> Task:
        """Create a new task with auto-incremented ID. Returns the created Task."""
        
    def get(self, id: int) -> Task | None:
        """Retrieve task by ID. Returns Task or None if not found."""
        
    def list(self, filter: str = "all") -> list[Task]:
        """List tasks filtered by status: 'all', 'pending', or 'completed'."""
        
    def update(self, id: int, **changes) -> Task:
        """Update task fields. Returns updated Task. Raises KeyError if not found."""
        
    def delete(self, id: int) -> bool:
        """Delete task. Returns True if found and deleted, False otherwise."""
```

### Command Handler Signature (`src/commands.py`)

```python
def cmd_<name>(args: list[str], store: TaskStore) -> str:
    """
    Command handler. 
    Returns human-readable message with ✓, ✗, or ℹ prefix.
    Never prints; always returns string.
    """

def dispatch(command: str, args: list[str], store: TaskStore) -> str:
    """
    Parse command name and dispatch to appropriate handler.
    Returns message string or raises ValueError for unknown command.
    """
```

### Error Handling Strategy

**Exceptions (developer-facing):**
- `ValueError` – Invalid input or state (e.g., empty title, invalid filter)
- `KeyError` – Task not found (raised by Store on update/delete with invalid ID)

**Messages (user-facing):**
- Success: `✓ <message>` (e.g., `✓ Task added with ID 1: Buy milk`)
- Error: `✗ <message>` (e.g., `✗ Task not found (ID: 5)`)
- Info: `ℹ <message>` (e.g., `ℹ No tasks yet`)

**REPL error recovery:**
- Catch all exceptions in app.py main loop
- Display user-facing error message
- Re-prompt user and continue (no crash)

---

## Non-Functional Requirements – How Addressed

### NFR1: In-Memory Storage
- **Approach:** All tasks held in `TaskStore` instance (Python memory)
- **Implication:** Data lost on application exit (acceptable for Phase I)
- **Phase II:** Replace with file/database backend without API changes

### NFR2: Deterministic Behavior
- **Approach:** No randomness; same input always produces same output
- **Implementation:** Consistent timestamps, deterministic sorting
- **Verification:** Testable with fixed inputs → expected outputs

### NFR3: No External Dependencies
- **Approach:** Python stdlib only (datetime, typing, sys, collections)
- **Implication:** Zero pip dependencies; maximizes portability
- **Trade-off:** No async, no advanced CLI framework

### NFR4: Python 3.13+ Only
- **Approach:** Leverage modern type hints (Union → |, dataclasses)
- **Implication:** Assumes Python 3.13+ installed
- **Benefit:** Clean syntax, best IDE support

### NFR5: Performance
- **Target:** Commands complete in <100ms
- **Achievable:** In-memory operations on small dataset (Phase I)
- **No optimization:** Required; simple algorithms sufficient

### NFR6: Code Quality
- **Type Hints:** All functions must have complete type annotations
- **Docstrings:** All public functions and classes require docstrings
- **Error Handling:** Defensive programming; no unhandled exceptions escape to user
- **Separation:** Business logic completely independent of I/O

---

## Data Management

### Storage Strategy
- `TaskStore` holds tasks in a list (order preserved)
- IDs auto-incremented: 1, 2, 3... per session
- No persistence; data lost on exit (Phase I design)

### ID Assignment
- Start from 1 (not 0)
- Increment on each add
- Never reuse deleted IDs within session (acceptable for Phase I)
- Next ID tracked separately from task list

### Timestamps
- `created_at` set automatically when task added
- `completed_at` set when task marked complete
- Clear `completed_at` when task marked pending again

---

## Definition of Done (DoD)

### Layer 1: Models (`src/models.py`)
- [ ] `Task` dataclass defined with all required fields
- [ ] Type hints for all fields
- [ ] Docstring for dataclass

### Layer 2: Store (`src/store.py`)
- [ ] `TaskStore` class implemented
- [ ] All methods: add, get, list, update, delete
- [ ] Auto-increment ID generation works correctly
- [ ] Timestamps managed properly
- [ ] Type hints on all methods
- [ ] Docstrings on all public methods
- [ ] Unit tests pass (100% coverage)

### Layer 3: Commands (`src/commands.py`)
- [ ] All command handlers implemented: add, list, show, update, delete, help
- [ ] Command dispatch mechanism working
- [ ] Argument parsing and validation correct
- [ ] All output messages formatted with ✓/✗/ℹ prefixes
- [ ] Type hints on all functions
- [ ] Docstrings on all public functions
- [ ] Integration tests pass (100% coverage)

### Layer 4: Application (`src/app.py`)
- [ ] `run()` function implements REPL loop
- [ ] Welcome message displayed
- [ ] Prompt shown after each command
- [ ] Error recovery working (no crashes)
- [ ] Exit on quit/exit command
- [ ] `__main__` entrypoint created
- [ ] Application runs: `python -m src`

### Package Structure
- [ ] `src/__init__.py` exists (can be empty)
- [ ] `src/__main__.py` exists and calls app.run()
- [ ] All imports work correctly

### Testing
- [ ] Unit tests pass: `pytest tests/test_store.py -v`
- [ ] Integration tests pass: `pytest tests/test_commands.py -v`
- [ ] Acceptance tests pass: `pytest tests/test_acceptance.py -v`
- [ ] All acceptance criteria from spec.md satisfied

### Quality Gate
- [ ] All code has type hints
- [ ] All public functions have docstrings
- [ ] No unhandled exceptions reach user
- [ ] Console output matches spec exactly
- [ ] No external dependencies used

---

## Risk Analysis

### Risk 1: Command Parser Ambiguity
**Scenario:** User types invalid command format  
**Blast Radius:** User confusion, unclear error  
**Mitigation:**
- Clear help text for each command
- Consistent syntax: `command [args] [--option value]`
- Explicit usage hints in error messages

### Risk 2: Concurrent Modifications
**Scenario:** Multiple users or threads  
**Blast Radius:** Data corruption (not applicable)  
**Mitigation:** N/A — Phase I is single-threaded, single-user

### Risk 3: Large Data Sets
**Scenario:** Thousands of tasks in memory  
**Blast Radius:** Memory usage and performance  
**Mitigation:** Phase I accepts unlimited tasks; Phase II adds persistence/pagination

### Risk 4: Silent Failure on Delete
**Scenario:** User deletes non-existent task  
**Blast Radius:** User confusion  
**Mitigation:** Always show error message: `✗ Task not found (ID: X)`

---

## References

**Baseline Specification:** [specs/spec.md](spec.md)  
**Implementation Tasks:** [specs/tasks.md](tasks.md)  
**Constitution:** [specs/CONSTITUTION.md](CONSTITUTION.md)  

---

## Summary

This plan establishes a strict 4-layer architecture enabling:
1. **Clear separation of concerns** (Models → Store → Commands → App)
2. **Independent testing** of each layer
3. **Business logic reusability** (Phase II: web/API without changes)
4. **Forward compatibility** with AI agents and future frameworks

**All implementation tasks are generated from this plan and the baseline specification.**

---

**Version History:**
- 1.0 (2026-01-03): Initial active plan aligned with baseline spec

**Status:** Active – Ready for implementation
