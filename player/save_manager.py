"""
SaveManager - Abstraction layer for save/load functionality.

Provides two implementations:
- SaveManager: Uses local JSON files in saves/ directory (for local dev)
- BrowserSaveManager: Uses browser localStorage via NiceGUI (for web deployment)
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any


class BrowserSaveManager:
    """Manages save games using browser localStorage via NiceGUI.

    Each player's saves are stored in their own browser, so players
    can only see their own saves when deployed as a web app.
    """

    STORAGE_KEY = "arcanum_saves"

    def __init__(self):
        """Initialize BrowserSaveManager."""
        # Note: We don't access app.storage.browser here because
        # it's only available during request handling
        pass

    def _get_storage(self):
        """Get the browser storage dict, initializing if needed."""
        from nicegui import app

        if self.STORAGE_KEY not in app.storage.browser:
            app.storage.browser[self.STORAGE_KEY] = {}
        return app.storage.browser[self.STORAGE_KEY]

    def save_game(self, save_name: str, engine_state: dict[str, Any]) -> dict:
        """
        Save game state to browser localStorage.

        Args:
            save_name: User-provided name for the save
            engine_state: Complete engine state from engine.save_state()

        Returns:
            Dict with save metadata (save_id, etc.)
        """
        saves = self._get_storage()

        # Add user-provided save name to the state
        save_data = engine_state.copy()
        save_data["save_name"] = save_name
        save_data["user_timestamp"] = save_data.get("timestamp")

        # Generate unique save ID (timestamp-based)
        save_id = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Store in browser localStorage
        saves[save_id] = save_data

        # Trigger storage sync by reassigning
        from nicegui import app
        app.storage.browser[self.STORAGE_KEY] = saves

        return {
            "success": True,
            "save_id": save_id,
            "metadata": {
                "save_name": save_name,
                "passage": save_data.get("current_passage_id", "Unknown"),
                "timestamp": save_data.get("timestamp"),
            },
        }

    def load_game(self, save_id: str) -> dict[str, Any]:
        """
        Load a saved game from browser localStorage.

        Args:
            save_id: The save ID

        Returns:
            The saved engine state

        Raises:
            KeyError: If save doesn't exist
        """
        saves = self._get_storage()

        if save_id not in saves:
            raise KeyError(f"Save not found: {save_id}")

        return saves[save_id]

    def list_saves(self) -> list[dict]:
        """
        List all available saves from browser localStorage.

        Returns:
            List of save metadata dicts, sorted by timestamp (newest first)
        """
        saves = self._get_storage()
        result = []

        for save_id, save_data in saves.items():
            result.append({
                "save_id": save_id,
                "save_name": save_data.get("save_name", "Unnamed Save"),
                "story_name": save_data.get("story_name", "Unknown Story"),
                "story_id": save_data.get("story_id", "unknown"),
                "passage": save_data.get("current_passage_id", "Unknown"),
                "timestamp": save_data.get("timestamp"),
                "date_display": self._format_timestamp(save_data.get("timestamp")),
            })

        # Sort by timestamp (newest first)
        result.sort(key=lambda s: s.get("timestamp", ""), reverse=True)

        return result

    def delete_save(self, save_id: str) -> bool:
        """
        Delete a save from browser localStorage.

        Args:
            save_id: The save ID

        Returns:
            True if deleted successfully

        Raises:
            KeyError: If save doesn't exist
        """
        saves = self._get_storage()

        if save_id not in saves:
            raise KeyError(f"Save not found: {save_id}")

        del saves[save_id]

        # Trigger storage sync
        from nicegui import app
        app.storage.browser[self.STORAGE_KEY] = saves

        return True

    def _format_timestamp(self, timestamp: str | None) -> str:
        """Format ISO timestamp for display."""
        if not timestamp:
            return "Unknown date"

        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime("%B %d, %Y at %I:%M %p")
        except Exception:
            return timestamp


class SaveManager:
    """Manages save game files."""

    def __init__(self, saves_dir: str | Path):
        """Initialize SaveManager with a saves directory."""
        self.saves_dir = Path(saves_dir)
        self.saves_dir.mkdir(exist_ok=True)

    def save_game(self, save_name: str, engine_state: dict[str, Any]) -> dict:
        """
        Save game state to a file.

        Args:
            save_name: User-provided name for the save
            engine_state: Complete engine state from engine.save_state()

        Returns:
            Dict with save metadata (save_id, save_path, etc.)
        """
        # Add user-provided save name to the state
        save_data = engine_state.copy()
        save_data["save_name"] = save_name
        save_data["user_timestamp"] = save_data.get("timestamp")

        # Generate unique save ID (timestamp-based)
        save_id = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        save_path = self.saves_dir / f"{save_id}.json"

        # Write to disk
        with open(save_path, "w") as f:
            json.dump(save_data, f, indent=2)

        return {
            "success": True,
            "save_id": save_id,
            "save_path": str(save_path),
            "metadata": {
                "save_name": save_name,
                "passage": save_data.get("current_passage_id", "Unknown"),
                "timestamp": save_data.get("timestamp"),
            },
        }

    def load_game(self, save_id: str) -> dict[str, Any]:
        """
        Load a saved game.

        Args:
            save_id: The save file ID (without .json extension)

        Returns:
            The saved engine state

        Raises:
            FileNotFoundError: If save file doesn't exist
        """
        save_path = self.saves_dir / f"{save_id}.json"

        if not save_path.exists():
            raise FileNotFoundError(f"Save file not found: {save_id}")

        with open(save_path) as f:
            save_data = json.load(f)

        return save_data

    def list_saves(self) -> list[dict]:
        """
        List all available save files.

        Returns:
            List of save metadata dicts, sorted by timestamp (newest first)
        """
        saves = []

        for save_file in self.saves_dir.glob("save_*.json"):
            try:
                with open(save_file) as f:
                    save_data = json.load(f)

                saves.append(
                    {
                        "save_id": save_file.stem,
                        "save_name": save_data.get("save_name", "Unnamed Save"),
                        "story_name": save_data.get("story_name", "Unknown Story"),
                        "story_id": save_data.get("story_id", "unknown"),
                        "passage": save_data.get("current_passage_id", "Unknown"),
                        "timestamp": save_data.get("timestamp"),
                        "date_display": self._format_timestamp(
                            save_data.get("timestamp")
                        ),
                    }
                )

            except Exception as e:
                print(f"Warning: Could not read save file {save_file}: {e}")
                continue

        # Sort by timestamp (newest first)
        saves.sort(key=lambda s: s.get("timestamp", ""), reverse=True)

        return saves

    def delete_save(self, save_id: str) -> bool:
        """
        Delete a save file.

        Args:
            save_id: The save file ID (without .json extension)

        Returns:
            True if deleted successfully

        Raises:
            FileNotFoundError: If save file doesn't exist
        """
        save_path = self.saves_dir / f"{save_id}.json"

        if not save_path.exists():
            raise FileNotFoundError(f"Save file not found: {save_id}")

        save_path.unlink()
        return True

    def _format_timestamp(self, timestamp: str | None) -> str:
        """Format ISO timestamp for display."""
        if not timestamp:
            return "Unknown date"

        try:
            dt = datetime.fromisoformat(timestamp)
            return dt.strftime("%B %d, %Y at %I:%M %p")
        except Exception:
            return timestamp
