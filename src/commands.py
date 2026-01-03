"""Todo App - Phase I: Command Handlers and Dispatcher

This module provides command parsing and execution handlers.
Each command is a pure function that takes arguments and a store, returning a message string.
Messages are prefixed with ✓ (success), ✗ (error), or ℹ (info).
"""

from src.store import TaskStore


def cmd_add(args: list[str], store: TaskStore) -> str:
    """
    Create a new task.

    Usage: add <title> [--description <desc>]

    Args:
        args: Command arguments (title and optional --description flag)
        store: TaskStore instance

    Returns:
        Message string with ✓/✗ prefix
    """
    if not args or not args[0].strip():
        return "✗ Task title cannot be empty"

    title = args[0]
    description = ""

    # Parse optional --description flag
    if len(args) > 1 and args[1] == "--description" and len(args) > 2:
        description = args[2]

    try:
        task = store.add(title, description)
        return f"✓ Task added with ID {task.id}: {task.title}"
    except ValueError as e:
        return f"✗ {str(e)}"


def cmd_list(args: list[str], store: TaskStore) -> str:
    """
    List all tasks with optional filtering.

    Usage: list [--filter all|pending|completed]

    Args:
        args: Command arguments (optional --filter flag)
        store: TaskStore instance

    Returns:
        Formatted table or message string
    """
    filter_by = "all"

    # Parse optional --filter flag
    if len(args) > 0 and args[0] == "--filter" and len(args) > 1:
        filter_by = args[1]

    try:
        tasks = store.list(filter_by)
    except ValueError as e:
        return f"✗ {str(e)}"

    if not tasks:
        return "ℹ No tasks yet"

    # Build ASCII table
    lines = []
    lines.append("ID | Title                | Status    | Created")
    lines.append("-" * 60)

    for task in tasks:
        status = "completed" if task.completed else "pending"
        created = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
        # Display full title
        lines.append(
            f"{task.id:<2} | {task.title:<20} | {status:<9} | {created}"
        )

    return "\n".join(lines)


def cmd_show(args: list[str], store: TaskStore) -> str:
    """
    Display detailed information about a specific task.

    Usage: show <id>

    Args:
        args: Command arguments (task ID)
        store: TaskStore instance

    Returns:
        Formatted task details or error message
    """
    if not args:
        return "✗ Invalid task ID"

    try:
        task_id = int(args[0])
    except ValueError:
        return "✗ Invalid task ID"

    task = store.get(task_id)
    if task is None:
        return f"✗ Task not found (ID: {task_id})"

    status = "completed" if task.completed else "pending"
    created = task.created_at.strftime("%Y-%m-%d %H:%M:%S")
    completed = (
        task.completed_at.strftime("%Y-%m-%d %H:%M:%S")
        if task.completed_at
        else "—"
    )

    lines = [
        f"ID:          {task.id}",
        f"Title:       {task.title}",
        f"Description: {task.description if task.description else '—'}",
        f"Status:      {status}",
        f"Created:     {created}",
        f"Completed:   {completed}",
    ]

    return "\n".join(lines)


def cmd_update(args: list[str], store: TaskStore) -> str:
    """
    Update one or more fields of a task.

    Usage: update <id> [--title <new>] [--description <new>] [--status pending|completed]

    Args:
        args: Command arguments (task ID and optional field updates)
        store: TaskStore instance

    Returns:
        Message string with ✓/✗ prefix
    """
    if not args:
        return "✗ Invalid task ID"

    try:
        task_id = int(args[0])
    except ValueError:
        return "✗ Invalid task ID"

    changes = {}
    i = 1
    while i < len(args):
        if args[i] == "--title" and i + 1 < len(args):
            changes["title"] = args[i + 1]
            i += 2
        elif args[i] == "--description" and i + 1 < len(args):
            changes["description"] = args[i + 1]
            i += 2
        elif args[i] == "--status" and i + 1 < len(args):
            status_val = args[i + 1]
            if status_val not in ("pending", "completed"):
                return "✗ Invalid status. Use 'pending' or 'completed'."
            changes["completed"] = status_val == "completed"
            i += 2
        else:
            i += 1

    try:
        store.update(task_id, **changes)
        return f"✓ Task {task_id} updated"
    except KeyError:
        return f"✗ Task not found (ID: {task_id})"


def cmd_delete(args: list[str], store: TaskStore) -> str:
    """
    Delete a task by ID.

    Usage: delete <id>

    Args:
        args: Command arguments (task ID)
        store: TaskStore instance

    Returns:
        Message string with ✓/✗ prefix
    """
    if not args:
        return "✗ Invalid task ID"

    try:
        task_id = int(args[0])
    except ValueError:
        return "✗ Invalid task ID"

    if store.delete(task_id):
        return f"✓ Task {task_id} deleted"
    else:
        return f"✗ Task not found (ID: {task_id})"


def cmd_help(args: list[str], store: TaskStore) -> str:
    """
    Display help information about commands.

    Usage: help [command]

    Args:
        args: Optional command name for detailed help
        store: TaskStore instance (unused, required by signature)

    Returns:
        Help text
    """
    help_text = {
        "add": "add <title> [--description <desc>]\n  Create a new task",
        "list": "list [--filter all|pending|completed]\n  Show all tasks or filtered list",
        "show": "show <id>\n  Display task details",
        "update": "update <id> [--title <new>] [--description <new>] [--status pending|completed]\n  Update task fields",
        "delete": "delete <id>\n  Remove a task",
        "help": "help [command]\n  Show this help or help for a command",
        "quit": "quit (or exit)\n  Exit the application",
    }

    if args and args[0] in help_text:
        return help_text[args[0]]

    if args:
        return f"✗ Unknown command: {args[0]}"

    # Show all commands
    lines = ["Available commands:"]
    for cmd, text in help_text.items():
        short_desc = text.split("\n")[1].strip()
        lines.append(f"  {cmd:<10} - {short_desc}")

    return "\n".join(lines)


# Command registry: maps command names to handler functions
COMMAND_REGISTRY: dict[str, callable] = {
    "add": cmd_add,
    "list": cmd_list,
    "show": cmd_show,
    "update": cmd_update,
    "delete": cmd_delete,
    "help": cmd_help,
}


def dispatch(command: str, args: list[str], store: TaskStore) -> str:
    """
    Parse command and dispatch to appropriate handler.

    Args:
        command: Command name to execute
        args: List of command arguments
        store: TaskStore instance to pass to handler

    Returns:
        Message string from handler

    Raises:
        ValueError: If command is not recognized
    """
    command_lower = command.lower().strip()

    if command_lower not in COMMAND_REGISTRY:
        raise ValueError(f"Unknown command: {command}")

    handler = COMMAND_REGISTRY[command_lower]
    return handler(args, store)
