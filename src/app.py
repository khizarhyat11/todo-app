"""Todo App - Phase I: Application REPL Loop

This module implements the main application loop (REPL: Read-Eval-Print-Loop).
It handles user interaction via console input/output and delegates command execution
to the commands module.
"""

from src.store import TaskStore
from src.commands import dispatch

# Menu mappings for numeric selection
MENU_COMMANDS = {
    "1": "add",
    "2": "list",
    "3": "show",
    "4": "update",
    "5": "delete",
    "6": "help",
    "7": "quit",
}

MENU_TEXT = """
┌─────────────────────────────────┐
│     Available Commands:         │
├─────────────────────────────────┤
│ 1. add        - Create a task   │
│ 2. list       - Show all tasks  │
│ 3. show       - Task details    │
│ 4. update     - Modify task     │
│ 5. delete     - Remove task     │
│ 6. help       - Help            │
│ 7. quit       - Exit            │
└─────────────────────────────────┘
"""


def run() -> None:
    """
    Start the Todo application REPL loop.

    This function:
    1. Displays a welcome message and menu
    2. Enters an infinite loop that:
       - Prompts user for input
       - Parses command and arguments (or numeric selection)
       - Dispatches to command handlers
       - Displays results
    3. Exits on 'quit' or 'exit' command

    The loop gracefully handles errors and continues prompting the user.
    Users can enter commands by name (e.g., "add") or by number (e.g., "1").
    """
    store = TaskStore()

    print("Welcome to Todo App!")
    print("Type 'help' for available commands, or use menu numbers below:")
    print(MENU_TEXT)

    while True:
        try:
            # Get user input
            user_input = input("todo> ").strip()

            # Skip empty input
            if not user_input:
                continue

            # Check if input is a menu number (1-7)
            if user_input in MENU_COMMANDS:
                command = MENU_COMMANDS[user_input]
                args = []
                # If user selected show, update, or delete - prompt for ID
                if command in ("show", "update", "delete"):
                    task_id = input(f"  Enter task ID: ").strip()
                    if task_id:
                        args = [task_id]
                    if command == "update":
                        updates = input(f"  Enter updates (e.g., --title 'New' --status completed): ").strip()
                        if updates:
                            import shlex
                            try:
                                args.extend(shlex.split(updates))
                            except ValueError:
                                args.extend(updates.split())
                # If user selected add - prompt for title and description
                elif command == "add":
                    title = input(f"  Enter task title: ").strip()
                    if title:
                        args = [title]
                        desc = input(f"  Enter description (optional): ").strip()
                        if desc:
                            args.extend(["--description", desc])
                # If user selected list - prompt for filter
                elif command == "list":
                    filter_opt = input(f"  Filter (all/pending/completed) [all]: ").strip() or "all"
                    if filter_opt != "all":
                        args = ["--filter", filter_opt]
            else:
                # Parse command and arguments - handle quoted strings
                import shlex
                try:
                    parts = shlex.split(user_input)
                except ValueError:
                    # Fallback to simple split if shlex fails
                    parts = user_input.split()

                command = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []

            # Check for exit commands
            if command in ("quit", "exit"):
                print("Goodbye!")
                break

            # Dispatch to handler
            try:
                result = dispatch(command, args, store)
                print(result)
            except ValueError as e:
                print(f"✗ {str(e)}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"✗ An unexpected error occurred: {str(e)}")
