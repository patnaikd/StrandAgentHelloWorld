"""
GitHub API Integration Tools

This module provides tools for interacting with the GitHub API,
including creating issues, pull requests, and managing project boards.
"""

import os
import logging
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Note: GitHub integration requires PyGithub or requests library
# For now, we'll create the structure and placeholder implementations
# Run: uv pip install PyGithub to enable full functionality

try:
    from github import Github, GithubException
    GITHUB_AVAILABLE = True
except ImportError:
    logger.warning("PyGithub not installed. GitHub tools will use mock mode.")
    GITHUB_AVAILABLE = False
    GithubException = Exception


class GitHubClient:
    """
    Client for GitHub API operations.

    Provides methods for:
    - Creating and managing issues
    - Creating pull requests
    - Managing project boards
    - Adding labels and assignees
    """

    def __init__(self, token: Optional[str] = None, repo_name: Optional[str] = None):
        """
        Initialize GitHub client.

        Args:
            token (str, optional): GitHub personal access token
            repo_name (str, optional): Repository name in format "owner/repo"
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo_name = repo_name or os.getenv("GITHUB_REPO")
        self.logger = logging.getLogger(f"{__name__}.GitHubClient")

        if not self.token:
            self.logger.warning("No GitHub token provided. API calls will fail.")

        if GITHUB_AVAILABLE and self.token:
            self.client = Github(self.token)
            if self.repo_name:
                self.repo = self.client.get_repo(self.repo_name)
                self.logger.info(f"Connected to GitHub repo: {self.repo_name}")
        else:
            self.client = None
            self.repo = None
            self.logger.warning("GitHub client in mock mode")

    def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a GitHub issue.

        Args:
            title (str): Issue title
            body (str): Issue description
            labels (List[str], optional): List of label names
            assignees (List[str], optional): List of GitHub usernames

        Returns:
            Dict[str, Any]: Issue details including number and URL
        """
        if not GITHUB_AVAILABLE or not self.repo:
            self.logger.warning("GitHub not available. Returning mock issue.")
            return {
                "number": 1,
                "url": "https://github.com/mock/issue/1",
                "title": title,
                "state": "open"
            }

        try:
            issue = self.repo.create_issue(
                title=title,
                body=body,
                labels=labels or [],
                assignees=assignees or []
            )

            self.logger.info(f"Created issue #{issue.number}: {title}")

            return {
                "number": issue.number,
                "url": issue.html_url,
                "title": issue.title,
                "state": issue.state
            }
        except GithubException as e:
            self.logger.error(f"Failed to create issue: {str(e)}")
            raise

    def create_pull_request(
        self,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main"
    ) -> Dict[str, Any]:
        """
        Create a pull request.

        Args:
            title (str): PR title
            body (str): PR description
            head_branch (str): Branch containing changes
            base_branch (str): Target branch (default: "main")

        Returns:
            Dict[str, Any]: PR details including number and URL
        """
        if not GITHUB_AVAILABLE or not self.repo:
            self.logger.warning("GitHub not available. Returning mock PR.")
            return {
                "number": 1,
                "url": "https://github.com/mock/pull/1",
                "title": title,
                "state": "open"
            }

        try:
            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch
            )

            self.logger.info(f"Created PR #{pr.number}: {title}")

            return {
                "number": pr.number,
                "url": pr.html_url,
                "title": pr.title,
                "state": pr.state
            }
        except GithubException as e:
            self.logger.error(f"Failed to create PR: {str(e)}")
            raise

    def add_pr_comment(self, pr_number: int, comment: str) -> Dict[str, Any]:
        """
        Add a comment to a pull request.

        Args:
            pr_number (int): PR number
            comment (str): Comment text

        Returns:
            Dict[str, Any]: Comment details
        """
        if not GITHUB_AVAILABLE or not self.repo:
            self.logger.warning("GitHub not available. Returning mock comment.")
            return {"id": 1, "body": comment}

        try:
            pr = self.repo.get_pull(pr_number)
            comment_obj = pr.create_issue_comment(comment)

            self.logger.info(f"Added comment to PR #{pr_number}")

            return {
                "id": comment_obj.id,
                "body": comment_obj.body,
                "created_at": str(comment_obj.created_at)
            }
        except GithubException as e:
            self.logger.error(f"Failed to add comment: {str(e)}")
            raise

    def add_pr_review(
        self,
        pr_number: int,
        body: str,
        event: str = "COMMENT"
    ) -> Dict[str, Any]:
        """
        Add a review to a pull request.

        Args:
            pr_number (int): PR number
            body (str): Review comment
            event (str): Review event type (COMMENT, APPROVE, REQUEST_CHANGES)

        Returns:
            Dict[str, Any]: Review details
        """
        if not GITHUB_AVAILABLE or not self.repo:
            self.logger.warning("GitHub not available. Returning mock review.")
            return {"id": 1, "state": event}

        try:
            pr = self.repo.get_pull(pr_number)
            review = pr.create_review(body=body, event=event)

            self.logger.info(f"Added {event} review to PR #{pr_number}")

            return {
                "id": review.id,
                "state": review.state,
                "body": review.body
            }
        except GithubException as e:
            self.logger.error(f"Failed to add review: {str(e)}")
            raise

    def get_issue(self, issue_number: int) -> Dict[str, Any]:
        """
        Get details of a GitHub issue.

        Args:
            issue_number (int): Issue number

        Returns:
            Dict[str, Any]: Issue details
        """
        if not GITHUB_AVAILABLE or not self.repo:
            self.logger.warning("GitHub not available. Returning mock issue.")
            return {
                "number": issue_number,
                "title": "Mock Issue",
                "state": "open"
            }

        try:
            issue = self.repo.get_issue(issue_number)

            return {
                "number": issue.number,
                "title": issue.title,
                "body": issue.body,
                "state": issue.state,
                "labels": [label.name for label in issue.labels],
                "assignees": [assignee.login for assignee in issue.assignees]
            }
        except GithubException as e:
            self.logger.error(f"Failed to get issue: {str(e)}")
            raise

    def list_open_issues(self, labels: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        List open issues, optionally filtered by labels.

        Args:
            labels (List[str], optional): Filter by these labels

        Returns:
            List[Dict[str, Any]]: List of issue details
        """
        if not GITHUB_AVAILABLE or not self.repo:
            self.logger.warning("GitHub not available. Returning empty list.")
            return []

        try:
            if labels:
                issues = self.repo.get_issues(state="open", labels=labels)
            else:
                issues = self.repo.get_issues(state="open")

            return [
                {
                    "number": issue.number,
                    "title": issue.title,
                    "labels": [label.name for label in issue.labels],
                    "assignees": [assignee.login for assignee in issue.assignees]
                }
                for issue in issues
            ]
        except GithubException as e:
            self.logger.error(f"Failed to list issues: {str(e)}")
            raise

    def close_issue(self, issue_number: int, comment: Optional[str] = None) -> None:
        """
        Close a GitHub issue.

        Args:
            issue_number (int): Issue number
            comment (str, optional): Closing comment
        """
        if not GITHUB_AVAILABLE or not self.repo:
            self.logger.warning("GitHub not available. Mock closing issue.")
            return

        try:
            issue = self.repo.get_issue(issue_number)

            if comment:
                issue.create_comment(comment)

            issue.edit(state="closed")
            self.logger.info(f"Closed issue #{issue_number}")
        except GithubException as e:
            self.logger.error(f"Failed to close issue: {str(e)}")
            raise


# Convenience function to create a client
def get_github_client(
    token: Optional[str] = None,
    repo_name: Optional[str] = None
) -> GitHubClient:
    """
    Create a GitHub client instance.

    Args:
        token (str, optional): GitHub token
        repo_name (str, optional): Repository name

    Returns:
        GitHubClient: Configured client instance
    """
    return GitHubClient(token=token, repo_name=repo_name)
