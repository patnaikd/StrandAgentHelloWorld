# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-agent system built with Strand Agents that demonstrates collaborative software development through specialized AI agents. The system orchestrates work through GitHub projects and creates automated development workflows.

**Strand Agents Documentation:**
- API Reference: https://strandsagents.com/latest/documentation/docs/api-reference/agent/
- User Guide: https://strandsagents.com/latest/documentation/docs/

## Project Structure

- `docs/` - Planning documents and architectural decisions
- `src/` - Agentic code implementation
- Projects created by agents are prefixed with `agentic-` in the GitHub account

## Agent Architecture

The system consists of specialized agents with distinct responsibilities:

1. **Planning Agent** - Breaks down problems into modules
2. **Coding Agent(s)** - Takes ownership of individual modules and implements them
3. **Tester Agent** - Generates unit tests for code
4. **Documentation Agent** - Writes README files and improves codebase documentation
5. **Reviewer Agent** - Comments on pull requests

Each agent requests a workspace/working directory folder upon execution.

## Development Setup

**Package Manager:** This project uses `uv` for Python package management.

To set up the project:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt  # Once created
```

## Key Concepts

- Agents work collaboratively through GitHub Projects
- Each agent has a specific role in the development lifecycle
- Work is coordinated through pull requests and reviews
- All planning happens in the `docs/` folder before implementation
- Implementation code resides in `src/`
