"""Integration Tests for Command Handlers

Comprehensive test coverage for command parsing, dispatch, and message formatting.
Tests verify that commands correctly parse arguments, interact with the store,
and return properly formatted output messages.
"""

import pytest
from src.store import TaskStore
from src.commands import (
    dispatch,
    cmd_add,
    cmd_list,
    cmd_show,
    cmd_update,
    cmd_delete,
    cmd_help,
)


@pytest.fixture
def store_with_tasks() -> TaskStore:
    """Fixture providing a TaskStore with sample tasks"""
    store = TaskStore()
    store.add("Buy milk", "whole milk")
    store.add("Call mom")
    store.add("Write report", "quarterly report")
    store.update(2, completed=True)  # Mark "Call mom" as completed
    return store


@pytest.fixture
def empty_store() -> TaskStore:
    """Fixture providing an empty TaskStore"""
    return TaskStore()


class TestCmdAdd:
    """Test cmd_add command handler"""

    def test_add_with_title_only(self, empty_store: TaskStore) -> None:
        """Test adding task with title only"""
        result = cmd_add(["Buy milk"], empty_store)
        assert result.startswith("✓ Task added")
        assert "ID 1" in result
        assert "Buy milk" in result
        assert empty_store.get(1) is not None

    def test_add_with_description(self, empty_store: TaskStore) -> None:
        """Test adding task with description"""
        result = cmd_add(
            ["Buy milk", "--description", "whole milk"], empty_store
        )
        assert result.startswith("✓")
        task = empty_store.get(1)
        assert task.description == "whole milk"

    def test_add_empty_title(self, empty_store: TaskStore) -> None:
        """Test that empty title returns error"""
        result = cmd_add([""], empty_store)
        assert result.startswith("✗")
        assert "empty" in result.lower()

    def test_add_no_args(self, empty_store: TaskStore) -> None:
        """Test that no arguments returns error"""
        result = cmd_add([], empty_store)
        assert result.startswith("✗")

    def test_add_auto_increment(self, empty_store: TaskStore) -> None:
        """Test that multiple adds auto-increment IDs"""
        cmd_add(["Task 1"], empty_store)
        result = cmd_add(["Task 2"], empty_store)
        assert "ID 2" in result


class TestCmdList:
    """Test cmd_list command handler"""

    def test_list_all_tasks(self, store_with_tasks: TaskStore) -> None:
        """Test listing all tasks"""
        result = cmd_list([], store_with_tasks)
        assert "ID" in result
        assert "Title" in result
        assert "Buy milk" in result
        assert "Call mom" in result
        assert "Write report" in result
        assert "|" in result  # Table format

    def test_list_empty_store(self, empty_store: TaskStore) -> None:
        """Test listing from empty store"""
        result = cmd_list([], empty_store)
        assert result.startswith("ℹ No tasks")

    def test_list_filter_pending(self, store_with_tasks: TaskStore) -> None:
        """Test listing only pending tasks"""
        result = cmd_list(["--filter", "pending"], store_with_tasks)
        assert "Buy milk" in result
        assert "Write report" in result
        assert "Call mom" not in result  # This one is completed

    def test_list_filter_completed(
        self, store_with_tasks: TaskStore
    ) -> None:
        """Test listing only completed tasks"""
        result = cmd_list(["--filter", "completed"], store_with_tasks)
        assert "Call mom" in result
        assert "Buy milk" not in result

    def test_list_filter_all(self, store_with_tasks: TaskStore) -> None:
        """Test explicit all filter"""
        result = cmd_list(["--filter", "all"], store_with_tasks)
        assert "Buy milk" in result
        assert "Call mom" in result

    def test_list_invalid_filter(self, store_with_tasks: TaskStore) -> None:
        """Test that invalid filter returns error"""
        result = cmd_list(["--filter", "invalid"], store_with_tasks)
        assert result.startswith("✗")


class TestCmdShow:
    """Test cmd_show command handler"""

    def test_show_existing_task(self, store_with_tasks: TaskStore) -> None:
        """Test showing details of existing task"""
        result = cmd_show(["1"], store_with_tasks)
        assert "ID" in result
        assert "1" in result
        assert "Buy milk" in result
        assert "whole milk" in result
        assert "pending" in result

    def test_show_completed_task(self, store_with_tasks: TaskStore) -> None:
        """Test showing details of completed task"""
        result = cmd_show(["2"], store_with_tasks)
        assert "completed" in result

    def test_show_non_existent_task(self, store_with_tasks: TaskStore) -> None:
        """Test showing non-existent task"""
        result = cmd_show(["999"], store_with_tasks)
        assert result.startswith("✗ Task not found")

    def test_show_invalid_id(self, store_with_tasks: TaskStore) -> None:
        """Test showing with invalid ID format"""
        result = cmd_show(["invalid"], store_with_tasks)
        assert result.startswith("✗ Invalid task ID")

    def test_show_no_args(self, store_with_tasks: TaskStore) -> None:
        """Test showing with no arguments"""
        result = cmd_show([], store_with_tasks)
        assert result.startswith("✗ Invalid task ID")


class TestCmdUpdate:
    """Test cmd_update command handler"""

    def test_update_title(self, empty_store: TaskStore) -> None:
        """Test updating task title"""
        empty_store.add("Old")
        result = cmd_update(["1", "--title", "New"], empty_store)
        assert result.startswith("✓ Task 1 updated")
        assert empty_store.get(1).title == "New"

    def test_update_description(self, empty_store: TaskStore) -> None:
        """Test updating task description"""
        empty_store.add("Task")
        result = cmd_update(["1", "--description", "New desc"], empty_store)
        assert result.startswith("✓")
        assert empty_store.get(1).description == "New desc"

    def test_update_status_to_completed(self, empty_store: TaskStore) -> None:
        """Test marking task as completed"""
        empty_store.add("Task")
        result = cmd_update(["1", "--status", "completed"], empty_store)
        assert result.startswith("✓")
        assert empty_store.get(1).completed is True

    def test_update_status_to_pending(self, empty_store: TaskStore) -> None:
        """Test marking task as pending"""
        empty_store.add("Task")
        empty_store.update(1, completed=True)
        result = cmd_update(["1", "--status", "pending"], empty_store)
        assert result.startswith("✓")
        assert empty_store.get(1).completed is False

    def test_update_invalid_status(self, empty_store: TaskStore) -> None:
        """Test that invalid status returns error"""
        empty_store.add("Task")
        result = cmd_update(["1", "--status", "invalid"], empty_store)
        assert result.startswith("✗ Invalid status")

    def test_update_non_existent_task(self, empty_store: TaskStore) -> None:
        """Test updating non-existent task"""
        result = cmd_update(["999", "--title", "New"], empty_store)
        assert result.startswith("✗ Task not found")

    def test_update_invalid_id(self, empty_store: TaskStore) -> None:
        """Test updating with invalid ID format"""
        result = cmd_update(["invalid", "--title", "New"], empty_store)
        assert result.startswith("✗ Invalid task ID")

    def test_update_no_args(self, empty_store: TaskStore) -> None:
        """Test update with no arguments"""
        result = cmd_update([], empty_store)
        assert result.startswith("✗ Invalid task ID")


class TestCmdDelete:
    """Test cmd_delete command handler"""

    def test_delete_existing_task(self, empty_store: TaskStore) -> None:
        """Test deleting existing task"""
        empty_store.add("Task")
        result = cmd_delete(["1"], empty_store)
        assert result.startswith("✓ Task 1 deleted")
        assert empty_store.get(1) is None

    def test_delete_non_existent_task(self, empty_store: TaskStore) -> None:
        """Test deleting non-existent task"""
        result = cmd_delete(["999"], empty_store)
        assert result.startswith("✗ Task not found")

    def test_delete_invalid_id(self, empty_store: TaskStore) -> None:
        """Test delete with invalid ID format"""
        result = cmd_delete(["invalid"], empty_store)
        assert result.startswith("✗ Invalid task ID")

    def test_delete_no_args(self, empty_store: TaskStore) -> None:
        """Test delete with no arguments"""
        result = cmd_delete([], empty_store)
        assert result.startswith("✗ Invalid task ID")


class TestCmdHelp:
    """Test cmd_help command handler"""

    def test_help_all_commands(self, empty_store: TaskStore) -> None:
        """Test help with no arguments shows all commands"""
        result = cmd_help([], empty_store)
        assert "add" in result.lower()
        assert "list" in result.lower()
        assert "delete" in result.lower()
        assert "update" in result.lower()

    def test_help_specific_command(self, empty_store: TaskStore) -> None:
        """Test help for specific command"""
        result = cmd_help(["add"], empty_store)
        assert "add" in result.lower()
        assert "<title>" in result.lower() or "title" in result.lower()

    def test_help_unknown_command(self, empty_store: TaskStore) -> None:
        """Test help for unknown command"""
        result = cmd_help(["unknown"], empty_store)
        assert result.startswith("✗ Unknown command")


class TestDispatch:
    """Test command dispatch mechanism"""

    def test_dispatch_add(self, empty_store: TaskStore) -> None:
        """Test dispatching to add command"""
        result = dispatch("add", ["Task"], empty_store)
        assert result.startswith("✓")

    def test_dispatch_list(self, empty_store: TaskStore) -> None:
        """Test dispatching to list command"""
        result = dispatch("list", [], empty_store)
        assert "No tasks" in result

    def test_dispatch_help(self, empty_store: TaskStore) -> None:
        """Test dispatching to help command"""
        result = dispatch("help", [], empty_store)
        assert "add" in result.lower()

    def test_dispatch_unknown_command(self, empty_store: TaskStore) -> None:
        """Test dispatching unknown command raises error"""
        with pytest.raises(ValueError):
            dispatch("unknown", [], empty_store)

    def test_dispatch_case_insensitive(self, empty_store: TaskStore) -> None:
        """Test that dispatch is case-insensitive"""
        result1 = dispatch("ADD", ["Task"], empty_store)
        result2 = dispatch("add", ["Task2"], empty_store)
        assert both_start_with_success(result1, result2)


class TestMessageFormat:
    """Test that all messages follow the spec format"""

    def test_success_messages_have_checkmark(self, empty_store: TaskStore) -> None:
        """Test that success messages start with ✓"""
        empty_store.add("Task")
        result = cmd_delete(["1"], empty_store)
        assert result.startswith("✓")

    def test_error_messages_have_x(self, empty_store: TaskStore) -> None:
        """Test that error messages start with ✗"""
        result = cmd_delete(["999"], empty_store)
        assert result.startswith("✗")

    def test_info_messages_have_i(self, empty_store: TaskStore) -> None:
        """Test that info messages start with ℹ"""
        result = cmd_list([], empty_store)
        assert result.startswith("ℹ")


def both_start_with_success(msg1: str, msg2: str) -> bool:
    """Helper to check if both messages indicate success"""
    return msg1.startswith("✓") and msg2.startswith("✓")
