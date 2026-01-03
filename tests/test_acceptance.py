"""Acceptance Tests for End-to-End Application Flow

Tests verify complete workflows from the user's perspective,
ensuring all components work together correctly.
"""

import pytest
from io import StringIO
import sys
from src.store import TaskStore
from src.app import run
from src.commands import dispatch


class TestFullWorkflow:
    """Test complete user workflows"""

    def test_add_list_show_workflow(self) -> None:
        """Test: add task -> list -> show task"""
        store = TaskStore()

        # Add a task
        result_add = dispatch("add", ["Buy milk", "--description", "whole milk"], store)
        assert result_add.startswith("✓")
        assert "ID 1" in result_add

        # List tasks
        result_list = dispatch("list", [], store)
        assert "Buy milk" in result_list
        assert "pending" in result_list

        # Show task details
        result_show = dispatch("show", ["1"], store)
        assert "Buy milk" in result_show
        assert "whole milk" in result_show
        assert "pending" in result_show

    def test_add_update_delete_workflow(self) -> None:
        """Test: add task -> update -> delete"""
        store = TaskStore()

        # Add
        dispatch("add", ["Buy milk"], store)
        assert store.get(1) is not None

        # Update title
        result_update = dispatch("update", ["1", "--title", "Buy 2% milk"], store)
        assert result_update.startswith("✓")
        assert store.get(1).title == "Buy 2% milk"

        # Mark complete
        result_complete = dispatch(
            "update", ["1", "--status", "completed"], store
        )
        assert result_complete.startswith("✓")
        assert store.get(1).completed is True

        # Delete
        result_delete = dispatch("delete", ["1"], store)
        assert result_delete.startswith("✓")
        assert store.get(1) is None

    def test_multiple_tasks_filtering(self) -> None:
        """Test: add multiple tasks and filter by status"""
        store = TaskStore()

        # Add multiple tasks
        dispatch("add", ["Task 1"], store)
        dispatch("add", ["Task 2"], store)
        dispatch("add", ["Task 3"], store)

        # Mark some complete
        dispatch("update", ["1", "--status", "completed"], store)
        dispatch("update", ["3", "--status", "completed"], store)

        # List all
        all_tasks = dispatch("list", [], store)
        assert "Task 1" in all_tasks
        assert "Task 2" in all_tasks
        assert "Task 3" in all_tasks

        # List pending
        pending = dispatch("list", ["--filter", "pending"], store)
        assert "Task 2" in pending
        assert "Task 1" not in pending

        # List completed
        completed = dispatch("list", ["--filter", "completed"], store)
        assert "Task 1" in completed
        assert "Task 3" in completed

    def test_error_recovery_workflow(self) -> None:
        """Test that errors don't break workflow"""
        store = TaskStore()

        # Valid command
        dispatch("add", ["Task 1"], store)
        assert len(store.list()) == 1

        # Invalid command (should not crash)
        try:
            dispatch("unknown", [], store)
        except ValueError:
            pass  # Expected

        # Can still add after error
        dispatch("add", ["Task 2"], store)
        assert len(store.list()) == 2

    def test_invalid_input_handling(self) -> None:
        """Test handling of various invalid inputs"""
        store = TaskStore()

        # Invalid ID format
        result = dispatch("show", ["invalid"], store)
        assert result.startswith("✗")

        # Non-existent task
        result = dispatch("show", ["999"], store)
        assert result.startswith("✗")

        # Invalid status
        dispatch("add", ["Task"], store)
        result = dispatch("update", ["1", "--status", "invalid"], store)
        assert result.startswith("✗")

        # Empty title
        result = dispatch("add", [""], store)
        assert result.startswith("✗")

    def test_help_system(self) -> None:
        """Test help command"""
        store = TaskStore()

        # General help
        result = dispatch("help", [], store)
        assert "add" in result.lower()
        assert "list" in result.lower()

        # Command-specific help
        result_add = dispatch("help", ["add"], store)
        assert "add" in result_add.lower()


class TestConsoleInteraction:
    """Test console-level interaction patterns"""

    def test_empty_store_initial_list(self) -> None:
        """Test listing tasks from empty store"""
        store = TaskStore()
        result = dispatch("list", [], store)
        assert result.startswith("ℹ No tasks")

    def test_output_format_consistency(self) -> None:
        """Test that all output follows format spec"""
        store = TaskStore()

        # Add success message
        result_add = dispatch("add", ["Task"], store)
        assert result_add[0] in ("✓", "✗", "ℹ")

        # List result
        result_list = dispatch("list", [], store)
        if result_list.startswith("ℹ"):
            pass  # Info message
        else:
            assert "|" in result_list  # Table format

        # Error message
        result_error = dispatch("delete", ["999"], store)
        assert result_error[0] in ("✓", "✗", "ℹ")

    def test_table_formatting(self) -> None:
        """Test list command table format"""
        store = TaskStore()
        dispatch("add", ["Task 1"], store)
        dispatch("add", ["Task 2"], store)

        result = dispatch("list", [], store)
        # Check table structure
        assert "ID" in result
        assert "Title" in result
        assert "Status" in result
        assert "Created" in result
        assert "|" in result  # Table delimiter

    def test_detail_view_formatting(self) -> None:
        """Test show command detail format"""
        store = TaskStore()
        dispatch("add", ["My Task", "--description", "Task description"], store)

        result = dispatch("show", ["1"], store)
        # Check detail view structure
        assert "ID:" in result
        assert "Title:" in result
        assert "Description:" in result
        assert "Status:" in result
        assert "Created:" in result

    def test_timestamp_display(self) -> None:
        """Test that timestamps are displayed in show output"""
        store = TaskStore()
        dispatch("add", ["Task"], store)

        result = dispatch("show", ["1"], store)
        # Created timestamp should be present
        assert "Created:" in result
        # Completed should show — when not completed
        assert "Completed:" in result


class TestDataPersistenceWithinSession:
    """Test that data persists within session"""

    def test_data_survives_multiple_operations(self) -> None:
        """Test that data persists across multiple command calls"""
        store = TaskStore()

        # Add task
        dispatch("add", ["Task 1"], store)
        assert len(store.list()) == 1

        # Add another
        dispatch("add", ["Task 2"], store)
        assert len(store.list()) == 2

        # Update first
        dispatch("update", ["1", "--title", "Updated Task 1"], store)
        assert store.get(1).title == "Updated Task 1"

        # List still shows both with correct state
        tasks = store.list()
        assert len(tasks) == 2
        assert tasks[0].title == "Updated Task 1"


class TestBoundaryConditions:
    """Test boundary and edge cases"""

    def test_single_task_operations(self) -> None:
        """Test operations with single task"""
        store = TaskStore()
        dispatch("add", ["Only task"], store)

        result_list = dispatch("list", [], store)
        assert "Only task" in result_list

        result_show = dispatch("show", ["1"], store)
        assert "Only task" in result_show

        dispatch("delete", ["1"], store)
        result_after = dispatch("list", [], store)
        assert result_after.startswith("ℹ No tasks")

    def test_long_title_handling(self) -> None:
        """Test handling of long task titles"""
        store = TaskStore()
        long_title = "A" * 100

        dispatch("add", [long_title], store)
        result = dispatch("show", ["1"], store)
        assert long_title in result

    def test_special_characters_in_description(self) -> None:
        """Test handling special characters"""
        store = TaskStore()
        desc = "Special chars: !@#$%^&*()"

        dispatch("add", ["Task", "--description", desc], store)
        task = store.get(1)
        assert desc in task.description


class TestComplexWorkflows:
    """Test complex, realistic workflows"""

    def test_gtd_workflow(self) -> None:
        """Test Getting Things Done style workflow"""
        store = TaskStore()

        # Capture tasks
        dispatch("add", ["Review quarterly report"], store)
        dispatch("add", ["Plan next sprint"], store)
        dispatch("add", ["Update documentation"], store)

        # Process some
        dispatch("update", ["1", "--status", "completed"], store)

        # Organize
        dispatch("update", ["2", "--description", "Review Q1 goals"], store)

        # Review all
        result = dispatch("list", [], store)
        assert "Review quarterly report" in result

        # Filter by status
        completed = dispatch("list", ["--filter", "completed"], store)
        assert "Review quarterly report" in completed

        pending = dispatch("list", ["--filter", "pending"], store)
        assert "Plan next sprint" in pending


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
