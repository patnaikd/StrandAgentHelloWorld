"""
Base Agent Class for Multi-Agent System

This module provides the base class for all specialized agents in the system.
Each agent extends this base class and implements specific tools and behaviors.
"""

import os
import logging
from typing import List, Optional
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.anthropic import AnthropicModel

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BaseAgent:
    """
    Base class for all agents in the multi-agent system.

    This class provides common functionality including:
    - Model configuration (Claude via Anthropic API)
    - Workspace management
    - Logging setup
    - Tool registration

    Each specialized agent should extend this class and implement:
    - get_tools(): Return list of agent-specific tools
    - execute(): Define agent-specific execution logic
    """

    def __init__(self, name: str, workspace_dir: str, model_id: Optional[str] = None):
        """
        Initialize a base agent.

        Args:
            name (str): Name of the agent (e.g., "PlanningAgent")
            workspace_dir (str): Directory path for agent's workspace
            model_id (str, optional): Specific model ID to use. Defaults to env var.
        """
        self.name = name
        self.workspace_dir = workspace_dir
        self.logger = logging.getLogger(f"{__name__}.{name}")

        # Set up workspace
        self.setup_workspace()
        self.logger.info(f"Initialized {name} with workspace: {workspace_dir}")

        # Configure the LLM model
        self.model = self.configure_model(model_id)

        # Initialize Strand Agent with tools
        self.tools = self.get_tools()
        self.agent = Agent(model=self.model, tools=self.tools)

    def configure_model(self, model_id: Optional[str] = None) -> AnthropicModel:
        """
        Configure the LLM model for this agent.

        Args:
            model_id (str, optional): Specific model ID. Uses env var if not provided.

        Returns:
            AnthropicModel: Configured Anthropic model instance
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        model_id = model_id or os.getenv("AGENT_MODEL", "claude-haiku-4-5-20251001")
        max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        temperature = float(os.getenv("AGENT_TEMPERATURE", "0.7"))

        self.logger.info(f"Configuring model: {model_id}")

        return AnthropicModel(
            client_args={"api_key": api_key},
            max_tokens=max_tokens,
            model_id=model_id,
            params={"temperature": temperature}
        )

    def setup_workspace(self) -> None:
        """
        Create and initialize workspace directory for this agent.

        Creates the workspace directory if it doesn't exist.
        """
        os.makedirs(self.workspace_dir, exist_ok=True)
        self.logger.debug(f"Workspace directory ready: {self.workspace_dir}")

    def get_tools(self) -> List:
        """
        Return list of tools available to this agent.

        This method should be overridden by subclasses to provide
        agent-specific tools.

        Returns:
            List: List of tool functions decorated with @tool

        Raises:
            NotImplementedError: If not overridden by subclass
        """
        raise NotImplementedError(
            f"{self.name} must implement get_tools() method"
        )

    def execute(self, task: str) -> str:
        """
        Execute a task using this agent.

        This method should be overridden by subclasses to provide
        agent-specific execution logic.

        Args:
            task (str): The task description or prompt for the agent

        Returns:
            str: The agent's response

        Raises:
            NotImplementedError: If not overridden by subclass
        """
        raise NotImplementedError(
            f"{self.name} must implement execute() method"
        )

    def invoke(self, message: str) -> str:
        """
        Invoke the agent with a message.

        This is a convenience method that wraps the Strand Agent's
        invocation with logging.

        Args:
            message (str): The message/task for the agent

        Returns:
            str: The agent's response
        """
        self.logger.info(f"{self.name} received task: {message[:100]}...")

        try:
            response = self.agent(message)
            self.logger.info(f"{self.name} completed task")
            return response
        except Exception as e:
            self.logger.error(f"{self.name} failed: {str(e)}")
            raise

    def get_workspace_path(self, filename: str) -> str:
        """
        Get full path to a file in the agent's workspace.

        Args:
            filename (str): Name of the file

        Returns:
            str: Full path to the file in workspace
        """
        return os.path.join(self.workspace_dir, filename)

    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"{self.name}(workspace={self.workspace_dir})"
