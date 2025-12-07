# Strand Agent Hello World

A multi-agent system demonstrating collaborative software development using [Strand Agents](https://strandsagents.com). This project showcases how AI agents can work together as a team to solve coding problems.

## Overview

This project implements a team of specialized AI agents that collaborate through GitHub Projects to build software. Each agent has a specific role in the development lifecycle, mimicking a real software development team.

## Agent Team Structure

The system consists of five specialized agents:

- **Planning Agent** - Analyzes problems and breaks them down into manageable modules
- **Coding Agent(s)** - Takes ownership of individual modules and implements them
- **Tester Agent** - Generates comprehensive unit tests for all code
- **Documentation Agent** - Writes README files and maintains code documentation
- **Reviewer Agent** - Reviews pull requests and provides feedback

## Project Structure

```
StrandAgentHelloWorld/
├── docs/          # Planning documents and architectural decisions
├── src/           # Agent implementation code
└── README.md      # This file
```

## Workflow

1. Agents orchestrate work using **GitHub Projects**
2. Each agent-created project is prefixed with `agentic-`
3. Agents request a workspace/working directory upon execution
4. Development follows standard git workflows with pull requests and reviews

## Development Setup

This project uses [`uv`](https://github.com/astral-sh/uv) for Python package management.

```bash
# Install dependencies
uv sync

# Run the application
uv run <script>
```

## Resources

- **API Reference**: https://strandsagents.com/latest/documentation/docs/api-reference/agent/
- **User Guide**: https://strandsagents.com/latest/documentation/docs/

## License

This is a demonstration project for exploring multi-agent collaboration patterns. 