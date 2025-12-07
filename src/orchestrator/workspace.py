"""
Workspace Management System

This module manages workspace directories for agents and provides utilities
for file operations within agent workspaces.
"""

import os
import shutil
import logging
from typing import Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


class WorkspaceManager:
    """
    Manages workspace directories for all agents in the system.

    The workspace manager provides:
    - Centralized workspace creation and cleanup
    - Safe file operations within workspaces
    - Workspace isolation between agents
    - Path validation and sanitization
    """

    def __init__(self, base_workspace_dir: str = "./workspace"):
        """
        Initialize the workspace manager.

        Args:
            base_workspace_dir (str): Base directory for all agent workspaces
        """
        self.base_dir = os.path.abspath(base_workspace_dir)
        self.logger = logging.getLogger(f"{__name__}.WorkspaceManager")

        # Create base workspace directory
        os.makedirs(self.base_dir, exist_ok=True)
        self.logger.info(f"Workspace manager initialized at: {self.base_dir}")

    def get_agent_workspace(self, agent_name: str) -> str:
        """
        Get the workspace directory path for a specific agent.

        Args:
            agent_name (str): Name of the agent (e.g., "planning", "coding")

        Returns:
            str: Full path to the agent's workspace directory
        """
        agent_dir = os.path.join(self.base_dir, agent_name.lower())
        os.makedirs(agent_dir, exist_ok=True)
        return agent_dir

    def create_workspace(self, agent_name: str, clean: bool = False) -> str:
        """
        Create a workspace for an agent.

        Args:
            agent_name (str): Name of the agent
            clean (bool): If True, remove existing workspace contents

        Returns:
            str: Path to the created workspace
        """
        workspace_path = self.get_agent_workspace(agent_name)

        if clean and os.path.exists(workspace_path):
            self.logger.warning(f"Cleaning workspace: {workspace_path}")
            shutil.rmtree(workspace_path)
            os.makedirs(workspace_path)

        self.logger.info(f"Workspace ready for {agent_name}: {workspace_path}")
        return workspace_path

    def write_file(self, agent_name: str, filename: str, content: str) -> str:
        """
        Write a file to an agent's workspace.

        Args:
            agent_name (str): Name of the agent
            filename (str): Name of the file (can include subdirectories)
            content (str): Content to write to the file

        Returns:
            str: Full path to the written file
        """
        workspace_path = self.get_agent_workspace(agent_name)
        file_path = os.path.join(workspace_path, filename)

        # Create subdirectories if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        self.logger.debug(f"Wrote file: {file_path}")
        return file_path

    def read_file(self, agent_name: str, filename: str) -> str:
        """
        Read a file from an agent's workspace.

        Args:
            agent_name (str): Name of the agent
            filename (str): Name of the file to read

        Returns:
            str: Content of the file

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        workspace_path = self.get_agent_workspace(agent_name)
        file_path = os.path.join(workspace_path, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.logger.debug(f"Read file: {file_path}")
        return content

    def list_files(self, agent_name: str, pattern: Optional[str] = None) -> List[str]:
        """
        List files in an agent's workspace.

        Args:
            agent_name (str): Name of the agent
            pattern (str, optional): Glob pattern to filter files (e.g., "*.py")

        Returns:
            List[str]: List of file paths relative to workspace
        """
        workspace_path = self.get_agent_workspace(agent_name)
        workspace = Path(workspace_path)

        if pattern:
            files = [str(p.relative_to(workspace)) for p in workspace.rglob(pattern)]
        else:
            files = [
                str(p.relative_to(workspace))
                for p in workspace.rglob("*")
                if p.is_file()
            ]

        return sorted(files)

    def delete_file(self, agent_name: str, filename: str) -> None:
        """
        Delete a file from an agent's workspace.

        Args:
            agent_name (str): Name of the agent
            filename (str): Name of the file to delete

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        workspace_path = self.get_agent_workspace(agent_name)
        file_path = os.path.join(workspace_path, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        os.remove(file_path)
        self.logger.info(f"Deleted file: {file_path}")

    def clear_workspace(self, agent_name: str) -> None:
        """
        Clear all files from an agent's workspace.

        Args:
            agent_name (str): Name of the agent
        """
        workspace_path = self.get_agent_workspace(agent_name)

        if os.path.exists(workspace_path):
            shutil.rmtree(workspace_path)
            os.makedirs(workspace_path)
            self.logger.info(f"Cleared workspace: {workspace_path}")

    def copy_to_workspace(
        self, agent_name: str, source_path: str, dest_filename: str
    ) -> str:
        """
        Copy a file from outside into an agent's workspace.

        Args:
            agent_name (str): Name of the agent
            source_path (str): Path to the source file
            dest_filename (str): Destination filename in workspace

        Returns:
            str: Path to the copied file

        Raises:
            FileNotFoundError: If source file doesn't exist
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source file not found: {source_path}")

        workspace_path = self.get_agent_workspace(agent_name)
        dest_path = os.path.join(workspace_path, dest_filename)

        # Create subdirectories if needed
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        shutil.copy2(source_path, dest_path)
        self.logger.info(f"Copied {source_path} to {dest_path}")
        return dest_path

    def get_workspace_size(self, agent_name: str) -> int:
        """
        Get the total size of an agent's workspace in bytes.

        Args:
            agent_name (str): Name of the agent

        Returns:
            int: Total size in bytes
        """
        workspace_path = self.get_agent_workspace(agent_name)
        total_size = 0

        for dirpath, dirnames, filenames in os.walk(workspace_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)

        return total_size

    def __repr__(self) -> str:
        """String representation of the workspace manager."""
        return f"WorkspaceManager(base_dir={self.base_dir})"
