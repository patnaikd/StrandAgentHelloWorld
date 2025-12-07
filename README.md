# Strand Agent Hello World

A multi-agent system demonstrating collaborative software development using [Strand Agents](https://strandsagents.com). This project showcases how AI agents can work together as a team to solve coding problems.

## Overview

This project implements a team of specialized AI agents that collaborate through GitHub Projects to build software. Each agent has a specific role in the development lifecycle, mimicking a real software development team.

**Key Design Principle**: Each problem is solved in a **single, self-contained file** that includes:
- Problem statement (in comments)
- Inline documentation
- Solution implementation
- Test cases

This approach ensures complete context and maintainability in one place.

## Agent Team Structure

The system consists of five specialized agents:

- **Planning Agent** - Analyzes problems and breaks them down into solvable tasks
- **Coding Agent(s)** - Implements solutions with inline documentation
- **Tester Agent** - Adds test cases to the same file as the solution
- **Documentation Agent** - Ensures inline documentation is clear and complete
- **Reviewer Agent** - Reviews the complete solution file and provides feedback

## Solution File Structure

Each solution file follows this pattern:

```python
"""
PROBLEM: [Problem title]

Description:
[Detailed problem description]

Requirements:
- [Requirement 1]
- [Requirement 2]

Example Input/Output:
[Examples if applicable]
"""

# SOLUTION

def solution_function():
    """
    Inline documentation explaining the approach.

    Args:
        param1: Description

    Returns:
        Description of return value
    """
    # Implementation with inline comments
    pass

# TEST CASES

def test_solution():
    """Test cases for the solution"""
    # Test case 1
    assert solution_function() == expected_result
    # Test case 2
    assert solution_function() == expected_result
```

## Project Structure

```
StrandAgentHelloWorld/
├── docs/          # Planning documents and architectural decisions
├── src/           # Agent implementation code
│   └── solutions/ # Problem solutions (one file per problem)
└── README.md      # This file
```

## Workflow

1. Agents orchestrate work using **GitHub Projects**
2. Each agent-created project is prefixed with `agentic-`
3. Agents request a workspace/working directory upon execution
4. Each problem generates a single comprehensive solution file
5. Development follows standard git workflows with pull requests and reviews

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