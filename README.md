This project demonstrates using Strand Agents to solve simple coding problems. We will make this multi-agentic and demonstrate how teams can form a small group.

We will use git hub projects to orchestrate work.

We will have a planning agent that breaks down the problem into modules, we will have a coding agent(s) that will take ownership of each module and build it. We will have a tester agent responsible for generating unit tests, then we will have a documentation agent that writes README file and improves documentation of the code base. We will also have a reviewer agent that comments on pull requests.

Each project will create a small github project in my account with project name prefixed by agentic-


Strand Agents python API is here https://strandsagents.com/latest/documentation/docs/api-reference/agent/ and user guide here https://strandsagents.com/latest/documentation/docs/

In this project, all planning documents will be in docs folder of this project. The agentic code will be in src. When agents execute they first ask for a workspace or working directory folder.

Use uv for managing this python project. 