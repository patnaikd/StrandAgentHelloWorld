# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-agent system built with Strand Agents that demonstrates collaborative software development through specialized AI agents. The system orchestrates work through GitHub projects and creates automated development workflows.

**Project Documentation:**
- [Design Document](docs/design-document.md) - Complete system design and architecture
- [Phase 1 Summary](docs/phase1-summary.md) - Foundation components implementation status

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

**Package Manager:** This project uses `uv` for Python package management with `pyproject.toml`.

To set up the project:
```bash
uv sync                    # Install all dependencies
uv sync --all-extras       # Include dev dependencies
uv run python src/demo_phase1.py  # Run Phase 1 demo
```

## Key Concepts

### Single-File Solution Approach
Each problem is solved in a **single, self-contained file** that includes:
- Problem statement (documented in comments at the top)
- Solution implementation with inline documentation
- Test cases in the same file

This approach eliminates separate test files and keeps all context together.

### Workflow
- Agents work collaboratively through GitHub Projects
- Each agent has a specific role in the development lifecycle
- Work is coordinated through pull requests and reviews
- All planning happens in the `docs/` folder before implementation
- Solution files reside in `src/solutions/`
- Agent implementations in `src/agents/`

### Phase 1 Status (Completed ✅)
- Base agent class with Strand Agents integration
- Workspace management system
- GitHub API integration
- Agent orchestrator for workflow coordination
