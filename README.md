# Todo App – Phase I

**An AI-native, spec-driven Todo application in Python.**

This project is built using [Spec-Kit Plus](https://github.com/specifyplus/specifyplus) and Claude Code. All code is generated from specifications; no manual code edits are permitted.

## Quick Start

### Prerequisites
- Python 3.13+
- WSL2 / Linux environment
- Spec-Kit Plus CLI installed

### Installation
```bash
# Clone or navigate to the project
cd ~/Desktop/todo\ app-phase1

# Install (no external dependencies for Phase I)
python -m venv venv
source venv/bin/activate
```

### Running the Application
```bash
python -m src
```

You should see:
```
Welcome to Todo App!
Type 'help' for available commands.
todo>
```

## Project Structure

```
.
├── .specify/
│   └── memory/
│       └── constitution.md        # Project constitution & principles
├── specs/
│   └── core/
│       ├── spec.md                # Feature requirements
│       ├── plan.md                # Architecture plan
│       └── tasks.md               # Implementation tasks
├── src/
│   ├── __init__.py
│   ├── __main__.py                # Application entrypoint
│   ├── app.py                     # REPL loop
│   ├── models.py                  # Domain models
│   ├── store.py                   # In-memory store
│   └── commands.py                # Command dispatch & handlers
├── tests/
│   ├── test_store.py              # Unit tests for store
│   ├── test_commands.py           # Integration tests for commands
│   └── test_acceptance.py         # End-to-end tests
├── history/
│   ├── prompts/                   # Prompt history records (PHRs)
│   └── adr/                       # Architecture decision records
└── README.md                       # This file
```

## Development Workflow

1. **Spec → Code**: All features start with spec updates in `specs/core/`
2. **Code Generation**: Claude Code generates implementation from specs
3. **Testing**: Verify against acceptance criteria
4. **Commit**: Reference spec in commit message
5. **Bugs**: Fix by updating spec, not patching code

## Commands

### Available Commands
```
add <title> [--description <desc>]   Create a new todo
list [--filter completed|pending]    Show todos
show <id>                            Display todo details
update <id> [--title <new>] ...      Modify todo
delete <id>                          Remove todo
help [command]                       Show help
quit, exit                           Exit application
```

### Example Session
```
todo> add Buy milk --description whole milk
✓ Todo added with ID 1: Buy milk

todo> list
ID | Title      | Status  | Created
1  | Buy milk   | pending | 2026-01-03 10:15:22

todo> show 1
ID:          1
Title:       Buy milk
Description: whole milk
Status:      pending
Created:     2026-01-03 10:15:22
Completed:   —

todo> update 1 --status complete
✓ Todo 1 updated

todo> delete 1
✓ Todo 1 deleted

todo> quit
Goodbye!
```

## Testing

Run all tests:
```bash
python -m pytest tests/ -v
```

Run specific test file:
```bash
python -m pytest tests/test_store.py -v
```

## Constitution

See [.specify/memory/constitution.md](.specify/memory/constitution.md) for project principles:
- **No manual code**: All from specifications
- **In-memory**: Phase I stores data only in memory
- **Console-only**: stdin/stdout interaction
- **Testable**: Clear requirements and acceptance criteria

## Phase I Scope
- ✅ CRUD operations (create, read, update, delete)
- ✅ In-memory storage
- ✅ Console UI
- ✅ Command-driven interface
- ❌ Data persistence
- ❌ Authentication
- ❌ Web/API (Phase II)

## Architecture

The application follows a layered architecture:

1. **Models** (`models.py`): Domain data structures
2. **Store** (`store.py`): In-memory data management
3. **Commands** (`commands.py`): Command parsing and execution
4. **App** (`app.py`): REPL loop and entrypoint

This design enables:
- Clear separation of concerns
- Independent testing of each layer
- Framework-agnostic business logic
- Forward-compatibility with web/API in Phase II

## References

- **Constitution**: [.specify/memory/constitution.md](.specify/memory/constitution.md)
- **Spec**: [specs/core/spec.md](specs/core/spec.md)
- **Plan**: [specs/core/plan.md](specs/core/plan.md)
- **Tasks**: [specs/core/tasks.md](specs/core/tasks.md)

---

**Phase I Version:** 1.0  
**Last Updated:** 2026-01-03  
**Status:** In Development
