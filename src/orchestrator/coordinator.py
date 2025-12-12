"""
Agent Coordinator

This module orchestrates the workflow between multiple agents,
managing task assignment, agent communication, and workflow execution.
"""

import logging
from typing import Dict, List, Optional, Any
from enum import Enum

from src.orchestrator.workspace import WorkspaceManager
from src.tools.github_tools import GitHubClient

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Status of a task in the workflow."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentTask:
    """
    Represents a task assigned to an agent.

    Attributes:
        task_id (str): Unique task identifier
        agent_name (str): Name of the assigned agent
        description (str): Task description
        status (TaskStatus): Current task status
        result (Any): Task result when completed
        error (str): Error message if failed
    """

    def __init__(self, task_id: str, agent_name: str, description: str):
        """
        Initialize an agent task.

        Args:
            task_id (str): Unique task identifier
            agent_name (str): Name of the assigned agent
            description (str): Task description
        """
        self.task_id = task_id
        self.agent_name = agent_name
        self.description = description
        self.status = TaskStatus.PENDING
        self.result: Optional[Any] = None
        self.error: Optional[str] = None

    def mark_in_progress(self) -> None:
        """Mark task as in progress."""
        self.status = TaskStatus.IN_PROGRESS

    def mark_completed(self, result: Any) -> None:
        """
        Mark task as completed.

        Args:
            result (Any): The task result
        """
        self.status = TaskStatus.COMPLETED
        self.result = result

    def mark_failed(self, error: str) -> None:
        """
        Mark task as failed.

        Args:
            error (str): Error message
        """
        self.status = TaskStatus.FAILED
        self.error = error

    def __repr__(self) -> str:
        return f"AgentTask({self.task_id}, {self.agent_name}, {self.status.value})"


class AgentCoordinator:
    """
    Coordinates workflow execution across multiple agents.

    The coordinator manages:
    - Task queue and assignment
    - Agent registration and lifecycle
    - Workflow orchestration
    - Communication between agents
    - Integration with GitHub for issue/PR management
    """

    def __init__(
        self,
        workspace_manager: Optional[WorkspaceManager] = None,
        github_client: Optional[GitHubClient] = None
    ):
        """
        Initialize the agent coordinator.

        Args:
            workspace_manager (WorkspaceManager, optional): Workspace manager instance
            github_client (GitHubClient, optional): GitHub client instance
        """
        self.workspace_manager = workspace_manager or WorkspaceManager()
        self.github_client = github_client
        self.logger = logging.getLogger(f"{__name__}.AgentCoordinator")

        # Agent registry
        self.agents: Dict[str, Any] = {}

        # Task tracking
        self.tasks: Dict[str, AgentTask] = {}
        self.task_counter = 0

        self.logger.info("Agent coordinator initialized")

    def register_agent(self, agent_name: str, agent_instance: Any) -> None:
        """
        Register an agent with the coordinator.

        Args:
            agent_name (str): Unique name for the agent
            agent_instance (Any): The agent instance
        """
        self.agents[agent_name] = agent_instance
        self.logger.info(f"Registered agent: {agent_name}")

    def unregister_agent(self, agent_name: str) -> None:
        """
        Unregister an agent from the coordinator.

        Args:
            agent_name (str): Name of the agent to unregister
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            self.logger.info(f"Unregistered agent: {agent_name}")

    def create_task(self, agent_name: str, description: str) -> str:
        """
        Create a new task for an agent.

        Args:
            agent_name (str): Name of the agent to assign the task
            description (str): Task description

        Returns:
            str: Task ID

        Raises:
            ValueError: If agent is not registered
        """
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' is not registered")

        self.task_counter += 1
        task_id = f"task_{self.task_counter:04d}"

        task = AgentTask(task_id, agent_name, description)
        self.tasks[task_id] = task

        self.logger.info(f"Created {task}")
        return task_id

    def execute_task(self, task_id: str) -> Any:
        """
        Execute a task.

        Args:
            task_id (str): Task ID to execute

        Returns:
            Any: Task result

        Raises:
            ValueError: If task doesn't exist
            RuntimeError: If agent execution fails
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task '{task_id}' not found")

        task = self.tasks[task_id]
        task.mark_in_progress()

        self.logger.info(f"Executing {task}")

        try:
            agent = self.agents[task.agent_name]
            result = agent.execute(task.description)
            task.mark_completed(result)
            self.logger.info(f"Completed {task}")
            return result
        except Exception as e:
            error_msg = f"Task execution failed: {str(e)}"
            task.mark_failed(error_msg)
            self.logger.error(f"Failed {task}: {error_msg}")
            raise RuntimeError(error_msg) from e

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a task.

        Args:
            task_id (str): Task ID

        Returns:
            Dict[str, Any]: Task status information

        Raises:
            ValueError: If task doesn't exist
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task '{task_id}' not found")

        task = self.tasks[task_id]
        return {
            "task_id": task.task_id,
            "agent_name": task.agent_name,
            "description": task.description,
            "status": task.status.value,
            "result": task.result,
            "error": task.error
        }

    def execute_workflow(self, workflow_steps: List[Dict[str, str]]) -> List[Any]:
        """
        Execute a multi-step workflow across agents.

        Args:
            workflow_steps (List[Dict[str, str]]): List of workflow steps,
                each containing 'agent_name' and 'description'

        Returns:
            List[Any]: Results from each step

        Example:
            steps = [
                {"agent_name": "planning", "description": "Analyze problem"},
                {"agent_name": "coding", "description": "Implement solution"},
                {"agent_name": "testing", "description": "Add tests"}
            ]
            results = coordinator.execute_workflow(steps)
        """
        results = []

        self.logger.info(f"Executing workflow with {len(workflow_steps)} steps")

        for i, step in enumerate(workflow_steps, 1):
            agent_name = step["agent_name"]
            description = step["description"]

            self.logger.info(f"Step {i}/{len(workflow_steps)}: {agent_name}")

            task_id = self.create_task(agent_name, description)
            result = self.execute_task(task_id)
            results.append(result)

        self.logger.info("Workflow completed successfully")
        return results

    def get_pending_tasks(self, agent_name: Optional[str] = None) -> List[AgentTask]:
        """
        Get pending tasks, optionally filtered by agent.

        Args:
            agent_name (str, optional): Filter by agent name

        Returns:
            List[AgentTask]: List of pending tasks
        """
        tasks = [
            task for task in self.tasks.values()
            if task.status == TaskStatus.PENDING
        ]

        if agent_name:
            tasks = [task for task in tasks if task.agent_name == agent_name]

        return tasks

    def get_agent_tasks(self, agent_name: str) -> List[AgentTask]:
        """
        Get all tasks for a specific agent.

        Args:
            agent_name (str): Agent name

        Returns:
            List[AgentTask]: List of tasks
        """
        return [
            task for task in self.tasks.values()
            if task.agent_name == agent_name
        ]

    def get_workflow_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current workflow state.

        Returns:
            Dict[str, Any]: Workflow summary with task counts and status
        """
        total_tasks = len(self.tasks)
        status_counts = {
            "pending": sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING),
            "in_progress": sum(1 for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS),
            "completed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED),
            "failed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
        }

        return {
            "total_tasks": total_tasks,
            "registered_agents": list(self.agents.keys()),
            "status_counts": status_counts
        }

    def reset(self) -> None:
        """Reset the coordinator state, clearing all tasks."""
        self.tasks.clear()
        self.task_counter = 0
        self.logger.info("Coordinator reset")

    def __repr__(self) -> str:
        """String representation of the coordinator."""
        return (
            f"AgentCoordinator("
            f"agents={len(self.agents)}, "
            f"tasks={len(self.tasks)})"
        )
