# Phase-I In-Memory Todo Console Application – Baseline Specification

**Project:** Todo App Phase-I  
**Feature:** core  
**Phase:** I  
**Version:** 1.0  
**Status:** Active  
**Date:** 2026-01-03  
**Author:** Specification-Driven Development Process  

---

## Executive Summary

This specification defines a Phase-I, in-memory Todo console application that demonstrates AI-native, spec-driven development principles. The system operates entirely in memory with no persistence, external dependencies, or graphical interfaces. All code is generated from this specification and derived task specifications.

---

## Objective

Define a baseline, spec-driven implementation of a Todo application that demonstrates AI-native software development principles using strict separation between specifications and generated code.

---

## Scope

**In Scope:**
- Phase-I only
- In-memory storage
- Console-based interaction
- CRUD operations on tasks
- Task status management (completed/pending)
- Basic validation and error handling

**Out of Scope:**
- Database or file persistence
- Authentication or authorization
- Natural language input
- Web or mobile interfaces
- AI agents or voice input (reserved for Phase-II)
- Performance optimization
- Async operations
- External libraries (except stdlib)

---

## Functional Requirements

### FR1: Task Creation
The system **shall** allow a user to create a task with:
- **Required:** title (non-empty string)
- **Optional:** description (string)

**Behavior:**
- System assigns a unique, auto-incrementing numeric ID starting from 1
- System records creation timestamp automatically
- User receives confirmation with assigned task ID

**Example:**
```
Input: create "Buy milk" --description "whole milk"
Output: ✓ Task created with ID 1: Buy milk
```

### FR2: Task Retrieval
The system **shall** allow users to:
1. View a list of all tasks
2. View details of a specific task by ID

**List Behavior:**
- Display all tasks in table format (ID | Title | Status | Created)
- Support filtering by status (all, completed, pending)
- Display completion status clearly

**Details Behavior:**
- Display all task attributes when viewing a specific task

**Example:**
```
Input: list
Output:
  ID | Title      | Status  | Created
  1  | Buy milk   | pending | 2026-01-03 10:15:22
  2  | Call mom   | completed | 2026-01-03 09:45:00

Input: show 1
Output:
  ID: 1
  Title: Buy milk
  Description: whole milk
  Status: pending
  Created: 2026-01-03 10:15:22
  Completed: —
```

### FR3: Task Update
The system **shall** allow users to update:
- Task title
- Task description
- Task completion status (completed ↔ pending)

**Behavior:**
- Only specified fields are updated
- System records completion timestamp when marking complete
- User receives confirmation of update

**Example:**
```
Input: update 1 --title "Buy 2% milk"
Output: ✓ Task 1 updated

Input: update 1 --status complete
Output: ✓ Task 1 updated (marked complete)
```

### FR4: Task Deletion
The system **shall** allow users to delete tasks by ID.

**Behavior:**
- Task is permanently removed from in-memory store
- User receives confirmation of deletion
- Subsequent operations with deleted ID fail gracefully

**Example:**
```
Input: delete 1
Output: ✓ Task 1 deleted
```

### FR5: Task Status Management
The system **shall** track task completion status.

**Behavior:**
- Default status on creation: incomplete (pending)
- Status options: pending, completed
- Completion timestamp is set when marked complete
- User can toggle status via update command

---

## Task Model Specification

Each task **must** include the following attributes:

| Attribute | Type | Constraints | Auto-Set |
|-----------|------|-------------|----------|
| id | integer | Unique, auto-increment starting from 1 | Yes |
| title | string | Non-empty, max reasonable length | No |
| description | string | Optional, can be empty string | No |
| completed | boolean | Default: False | No |
| created_at | datetime | Timestamp of creation | Yes |
| completed_at | datetime \| None | Timestamp when marked complete | Yes |

---

## User Interaction Model

### Console Interface
- Menu-driven, command-based interaction
- All input via stdin (keyboard)
- All output via stdout (terminal)
- Clear, deterministic prompts and messages

### Command Format
```
<command> <arguments> [--option value] [--flag]
```

### Core Commands

#### 1. create / add
**Usage:** `create <title> [--description <desc>]` or `add <title> [--description <desc>]`
- Creates a new task
- Returns assigned ID
- Error if title is empty

#### 2. list
**Usage:** `list [--filter all|pending|completed]`
- Displays all tasks in table format
- Default filter: all
- Returns empty table if no tasks exist

#### 3. show
**Usage:** `show <id>`
- Displays detailed view of single task
- Returns all attributes
- Error if task ID not found

#### 4. update
**Usage:** `update <id> [--title <new>] [--description <new>] [--status pending|completed]`
- Updates one or more task attributes
- Only specified fields change
- Error if task ID not found

#### 5. delete
**Usage:** `delete <id>`
- Permanently removes task
- Error if task ID not found

#### 6. help
**Usage:** `help [command]`
- Lists all available commands
- Optionally shows detailed help for specific command

#### 7. quit / exit
**Usage:** `quit` or `exit`
- Exits application cleanly
- No data saved (in-memory only)

---

## Validation Rules

### V1: Title Validation
- **Rule:** Task title must not be empty
- **Action:** Reject creation with clear error message
- **Message Format:** `✗ Task title cannot be empty`

### V2: ID Validation
- **Rule:** Operations referencing non-existent task IDs must fail gracefully
- **Action:** Return user-facing error message
- **Message Format:** `✗ Task not found (ID: <id>)`

### V3: Input Validation
- **Rule:** System must remain stable on invalid input
- **Action:** Parse errors result in clear guidance
- **Message Format:** `✗ Invalid command format. Type 'help' for usage.`

### V4: Status Values
- **Rule:** Only "pending" or "completed" are valid status values
- **Action:** Reject invalid status with error
- **Message Format:** `✗ Invalid status. Use 'pending' or 'completed'.`

---

## Non-Functional Requirements

### NFR1: In-Memory Storage
- All data stored in memory only
- No disk I/O
- No database connections
- Data lost on application exit (acceptable for Phase-I)

### NFR2: Deterministic Behavior
- Same input always produces same output
- Task operations are idempotent where applicable
- No randomness or timing dependencies in output

### NFR3: No External Dependencies
- Use Python standard library only
- No pip packages required
- Pure Python implementation

### NFR4: Python Version
- **Required:** Python 3.13 or later
- Leverage modern type hints and stdlib features

### NFR5: Performance
- All operations complete in <100ms
- In-memory, so no persistence overhead
- No optimization required for Phase-I

### NFR6: Code Quality
- **Type Hints:** All functions must have complete type annotations
- **Docstrings:** All public functions must have docstrings
- **Error Handling:** Defensive programming; no unhandled exceptions reach user
- **Separation of Concerns:** Business logic decoupled from I/O

---

## Architectural Constraints

The system **must** maintain clear separation between:

### AC1: Task Model
- Data structure representing a task
- Immutable after creation (except via Store methods)
- No I/O or business logic

### AC2: In-Memory Store
- Manages collection of tasks
- Implements CRUD operations
- Owns task ID generation and timestamps
- No console I/O

### AC3: Command/Business Logic
- Parses user input
- Calls Store methods
- Formats output messages
- No console I/O directly (return strings)

### AC4: Application Entrypoint
- REPL loop
- Handles console I/O
- Dispatches to command handlers
- Manages application lifecycle

**Additional Constraints:**
- No global mutable state
- No direct console I/O inside business logic components
- All messages passed as strings (not printed within logic)

---

## Console Output Specification

### Message Format
- **Success:** `✓ <message>`
- **Error:** `✗ <message>`
- **Info:** `ℹ <message>`

### Prompt Format
```
todo> 
```

### Table Format (List Command)
```
ID | Title         | Status    | Created
---+---------------+-----------+---------------------
1  | Buy milk      | pending   | 2026-01-03 10:15:22
2  | Call mom      | completed | 2026-01-03 09:45:00
```

### Detail View Format (Show Command)
```
ID:          1
Title:       Buy milk
Description: whole milk
Status:      pending
Created:     2026-01-03 10:15:22
Completed:   —
```

---

## Acceptance Criteria

- [ ] Application runs without errors from command line: `python -m src`
- [ ] All functional requirements (FR1–FR5) are satisfied
- [ ] Code is fully generated from this specification
- [ ] No manual code edits required after generation
- [ ] Behavior matches specification exactly
- [ ] All validation rules (V1–V4) are enforced
- [ ] All architectural constraints (AC1–AC4) are observed
- [ ] Console output matches specified format exactly
- [ ] Help command displays all available commands
- [ ] Application exits cleanly on `quit` or `exit`

---

## Dependencies

- **External:** None (Python stdlib only)
- **Internal:** Derived from this spec
  - `specs/plan.md` — Architecture plan
  - `specs/tasks.md` — Implementation tasks
  - `CONSTITUTION.md` — Project principles

---

## Next Steps

1. Review and approve this baseline specification
2. Generate `specs/plan.md` from this specification
3. Generate `specs/tasks.md` with testable implementation tasks
4. Claude Code generates all implementation from tasks

---

## References

- **Constitution:** `specs/CONSTITUTION.md`
- **Architecture Plan:** `specs/plan.md`
- **Implementation Tasks:** `specs/tasks.md`
- **README:** `README.md`
