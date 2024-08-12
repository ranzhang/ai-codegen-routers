# Automated networking script development with AI agents

A typical software development project may involve a number of iterative tasks, such as gathering requirements, designing the architecture, breaking down the project into units, writing and debuggin code, writing and performing unit tests, writing and performing system tests, documentation. Collaborative AI agents are showing potentials in accomplishing these tasks automatically with little human intervention, especially for projects with limited scope and complexity. 

This project leverages the Microsoft Autogen, an LLM-based agent framework, to perform software  development to create a working Python script to do the following networking tasks:
1. Login to Cisco routers
2. Collect the BGP running configuration
3. Compare it with BGP best practices
4. Generate a recommendations report 

The framework will validate the script using actual routers. A sample generated code is provided in main.py. As with any LLM applications, you may get different results with each run, with different LLMs, or with different instructions.

A mixture of models (MoD) is used but they can be easily replaced with other models of your choice:
- OpenAI GPT4o
- OpenAI GPT4 Turbo

A total of 4 AI agents are used for specific roles in the project:
- The Planner agent to kickoff the project with a detailed project plan and role assignment
- The Coder agent to write and debug code
- The Critic agent to review the code and make suggestions for enhancement
- The Reporter agent to summarize the test results and write the final report.

These agents collaborate as a team to iteratively work on the project, creating the plan, writing code, checking errors, running the tests, and reporting results. This process significantly increases the success rate over a single LLM agent. Human input may also be valuable to speeding up the development by suggesting fixes or providing instructions interactively. Note that your results may be different, or the process may not always produce ideal results.

For demonstration purpose, sample log files are provided for the following agents:
- plannerlog.txt
- coderlog.txt
- criticlog.txt and criticlog2.txt
- reporterlog.txt and reporterlog2.txt

Inputs required:
- your own .env file for LLM API key and endpoint (if you use Azure OpenAI but you can use other LLMs)
- your own routers.csv file (a sample is provided)
- your own version of BGP best practices file (a sample is provided)
- create a working directiory of tmp_dir and place the above routers.csv file there
