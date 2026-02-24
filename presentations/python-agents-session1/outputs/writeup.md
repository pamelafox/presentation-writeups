# Building your first agent in Python with Microsoft Agent Framework

This talk introduces the fundamentals of building AI agents using the Microsoft Agent Framework in Python. It covers core concepts such as what constitutes an agent, how tool calling works, integrating agents with Model Context Protocol (MCP) servers, leveraging middleware to enhance agent capabilities, and constructing basic multi-agent architectures. The session also demonstrates practical usage through GitHub Codespaces, running example code, and using a developer UI (DevUI) to interact with agents and trace their internal operations.

## Table of contents

- [Overview of the Python + Agents livestream series](#overview-of-the-python-agents-livestream-series)
- [Building your first agent in Python: session topics](#building-your-first-agent-in-python-session-topics)
- [Running code examples using GitHub Codespaces](#running-code-examples-using-github-codespaces)
- [Agents 101: what is an agent?](#agents-101-what-is-an-agent)
- [Why do we need agents with tools?](#why-do-we-need-agents-with-tools)
- [Popular Python AI agent frameworks overview](#popular-python-ai-agent-frameworks-overview)
- [Tool calling without an agent framework](#tool-calling-without-an-agent-framework)
- [Understanding the tool calling flow](#understanding-the-tool-calling-flow)
- [Defining callable functions for the LLM](#defining-callable-functions-for-the-llm)
- [Extracting function calls from the LLM response](#extracting-function-calls-from-the-llm-response)
- [Invoking local Python functions based on LLM suggestions](#invoking-local-python-functions-based-on-llm-suggestions)
- [Sending tool results back to the LLM for response generation](#sending-tool-results-back-to-the-llm-for-response-generation)
- [Benefits of using the Microsoft agent framework](#benefits-of-using-the-microsoft-agent-framework)
- [Installing Microsoft agent framework packages](#installing-microsoft-agent-framework-packages)
- [Building an agent with a single tool using decorators](#building-an-agent-with-a-single-tool-using-decorators)
- [Single tool agent example: weather function](#single-tool-agent-example-weather-function)
- [Adding multiple tools to an agent to increase power](#adding-multiple-tools-to-an-agent-to-increase-power)
- [Multi-tool agent example with date, weather, and activities](#multi-tool-agent-example-with-date-weather-and-activities)
- [Using DevUI for local experimentation and debugging](#using-devui-for-local-experimentation-and-debugging)
- [Integrating agents with MCP server tools](#integrating-agents-with-mcp-server-tools)
- [Running a local MCP server example](#running-a-local-mcp-server-example)
- [Connecting to remote MCP servers for documentation queries](#connecting-to-remote-mcp-servers-for-documentation-queries)
- [Challenges with large MCP server definitions and token limits](#challenges-with-large-mcp-server-definitions-and-token-limits)
- [Agent middleware: concepts and types](#agent-middleware-concepts-and-types)
- [Middleware implementation examples](#middleware-implementation-examples)
- [Use cases and benefits of middleware](#use-cases-and-benefits-of-middleware)
- [Basic multi-agent architecture with supervisor and specialist agents](#basic-multi-agent-architecture-with-supervisor-and-specialist-agents)
- [Demonstration of multi-agent setup in code](#demonstration-of-multi-agent-setup-in-code)
- [Final slides, resources, and next steps](#final-slides-resources-and-next-steps)
- [Q&A](#qa)

## Overview of the Python + Agents livestream series

![Title slide of Python + Agents livestream series](slide_images/slide_1.png)  
[Watch from 00:53](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=53s)

This series spans six live sessions over two weeks, focusing on building AI agents and workflows with Python and the Microsoft Agent Framework. Week one emphasizes core agent building blocks: adding tools, context, and memory, plus evaluating and monitoring agents. Week two covers more advanced workflows involving conditionals, concurrent agents, consensus mechanisms, and human-in-the-loop integration. The framework supports both Python and .NET, enabling developers to build sophisticated applications atop generative AI technology.

## Building your first agent in Python: session topics

![Session topics slide](slide_images/slide_3.png)  
[Watch from 03:16](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=196s)

The session covers defining agents, understanding tools and tool calling, building agents with the Microsoft Agent Framework, integrating with MCP servers, using middleware to intercept agent execution, and creating a basic multi-agent architecture. It provides a foundation for practical agent development and integration in real-world applications.

## Running code examples using GitHub Codespaces

![GitHub Codespaces setup slide](slide_images/slide_4.png)  
[Watch from 04:25](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=265s)

Developers can follow along by opening the provided GitHub repository using Codespaces, a cloud-based VS Code environment. Codespaces automatically configures dependencies including Python packages, the agent framework, and supporting services like PostgreSQL and Redis. This setup simplifies running examples without local installation. Free GitHub models provide the underlying LLMs needed to execute the agents. Users are guided to create a Codespace from the main branch and wait a few minutes for the environment to load fully.

## Agents 101: what is an agent?

![Definition of an agent slide](slide_images/slide_6.png)  
[Watch from 07:24](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=444s)

An agent is defined as an LLM that runs tools in a loop to achieve a goal. This simple definition encapsulates a powerful concept: the LLM selects appropriate tools, calls them with suitable arguments, receives results, and iterates until the objective is met. Effective agents depend on having the right tools with accurate knowledge and a capable LLM that can orchestrate tool usage. Agents can be augmented with context, memory, explicit planning, and human feedback to enhance their capabilities beyond this core loop.

## Why do we need agents with tools?

![Agent without tools example slide](slide_images/slide_9.png)  
[Watch from 09:53](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=593s)

Agents without tools are limited to their pretrained knowledge and often hallucinate or provide outdated answers. For example, an agent asked about the weather without a weather tool cannot fetch live data and might guess incorrectly. Equipping agents with tools allows them to ground their answers in real-time, domain-specific data and reduces hallucinations. Tools empower agents to solve practical problems in specialized domains by extending beyond their base language model capabilities.

## Popular Python AI agent frameworks overview

![Python AI agent frameworks slide](slide_images/slide_7.png)  
[Watch from 13:43](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=823s)

Several Python frameworks support building AI agents, each with distinct features:

- **Microsoft Agent Framework**: Successor to AutoGen and Semantic Kernel, offering modern, flexible, and feature-rich tooling.
- **Langchain v1**: Agent-centric open-source framework integrating with Langraph for monitoring and deployment.
- **Pydantic AI**: Focuses on type safety and integrates well with Python typing.
- **OpenAI agents**: Simpler, less flexible but suitable for basic OpenAI model use cases.

This talk uses Microsoft Agent Framework for its advanced capabilities and ongoing development.

## Tool calling without an agent framework

![Tool calling without a framework slide](slide_images/slide_8.png)  
[Watch from 16:07](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=967s)

Tool calling is a core ability that enables an LLM to invoke external functions. Without a framework, developers must manually define JSON schema descriptions of tools, parse the LLM's function call responses (which include function name and arguments), invoke corresponding local functions, and feed the results back to the LLM to generate final answers. This involves careful serialization, deserialization, and error handling, which can be complex and error-prone.

## Understanding the tool calling flow

![Tool calling flow diagram slide](slide_images/slide_10.png)  
[Watch from 19:17](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=1157s)

The tool calling process involves:

1. Defining tool schemas that describe available functions and their parameters.
2. Sending the user query and tool definitions to the LLM.
3. The LLM suggesting which tool to call and with what arguments.
4. The agent code executing the specified function locally.
5. Returning the function's output to the LLM.
6. The LLM generating a natural language response based on the results.

The LLM itself never executes code but decides the tool invocation plan.

## Defining callable functions for the LLM

![Function definition and JSON schema slide](slide_images/slide_11.png)  
[Watch from 21:17](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=1277s)

Functions exposed to the LLM must be described via JSON schema, including the function name, descriptions, parameter names, types, and documentation. The LLM sees this schema, not the underlying code. Properly annotating argument types and descriptions improves the LLM's understanding of how to call the tools effectively.

## Extracting function calls from the LLM response

![Parsing LLM response slide](slide_images/slide_12.png)  
[Watch from 22:56](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=1376s)

When the LLM responds, it may include a suggested function call encoded in JSON. The agent must parse this response to extract the function name and arguments, deserialize the JSON, and verify that the function is recognized locally.

## Invoking local Python functions based on LLM suggestions

![Calling functions and returning results slide](slide_images/slide_13.png)  
[Watch from 23:41](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=1421s)

After parsing, the agent calls the corresponding local Python function with the extracted arguments. The function runs in the agent's environment, producing output that is then sent back to the LLM for further processing and to generate the final answer.

## Sending tool results back to the LLM for response generation

![LLM final response generation slide](slide_images/slide_14.png)  
[Watch from 24:27](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=1467s)

The LLM receives the tool output and integrates it into a coherent natural language response. This completes one iteration of the agent's tool-calling loop.

## Benefits of using the Microsoft agent framework

![Agent framework benefits slide](slide_images/slide_15.png)  
[Watch from 24:27](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=1467s)

The agent framework abstracts away the complexity of manual tool calling, including schema management, response parsing, error handling, and orchestration. It provides decorators to easily mark Python functions as tools, automatically generating schemas and managing calls. This reduces boilerplate and development effort, enabling rapid agent creation.

## Installing Microsoft agent framework packages

![Agent framework installation slide](slide_images/slide_16.png)  
[Watch from 25:20](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=1520s)

The framework is modular with a core package and sub-packages. For this session, only `agent-framework-core` and `agent-framework-devui` are installed. The latest development version is pulled directly from GitHub to capture rapid updates, though official versioned releases are forthcoming. Installation is managed via `uv` (a Rust-based Python environment manager) for fast and reliable setup.

## Building an agent with a single tool using decorators

![Single tool agent code example slide](slide_images/slide_17.png)  
[Watch from 27:20](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=1640s)

Agents are constructed by defining Python functions decorated with `@tool` from the agent framework. This decorator signals the framework to treat the function as a callable tool, generating appropriate JSON schema from the function's argument annotations and docstrings. Rich argument metadata helps the LLM choose and invoke the tool correctly.

## Single tool agent example: weather function

![Single tool weather agent example slide](slide_images/slide_18.png)  
[Watch from 31:14](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=1874s)

A weather agent includes a function that takes a city name as a string, annotated with descriptions to inform the LLM. The agent is created by passing the LLM client, system prompt, and a list containing this tool function. Running the agent executes the tool calling loop automatically, producing weather responses with simulated or randomized data.

## Adding multiple tools to an agent to increase power

![Multi-tool agent architecture slide](slide_images/slide_19.png)  
[Watch from 32:56](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=1976s)

Agents become significantly more capable with multiple tools. For example, a weekend planner agent may include tools to get the current date, retrieve weather conditions, and suggest activities based on location and date. The LLM decides which tools to call, in what order, and how many times, enabling dynamic and context-aware interactions.

## Multi-tool agent example with date, weather, and activities

![Multi-tool agent code example slide](slide_images/slide_20.png)  
[Watch from 33:44](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=2024s)

Each tool is defined as a decorated function with detailed type annotations and descriptions. The agent receives all tools as a list. The LLM intelligently sequences calls: it fetches the current date, then weather, then activities for specific weekend dates, sometimes invoking tools multiple times for different days. This showcases the agent’s reasoning and planning capabilities.

## Using DevUI for local experimentation and debugging

![DevUI developer UI slide](slide_images/slide_21.png)  
[Watch from 38:33](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=2313s)

DevUI is a local web-based playground included with the agent framework’s dev package. It allows interactive chatting with agents, displaying detailed logs of tool calls, arguments, responses, and token usage in real time. Developers can easily experiment with inputs, observe tool invocation sequences, and trace event streams for debugging and development without modifying code.

## Integrating agents with MCP server tools

![Agent integration with MCP servers slide](slide_images/slide_22.png)  
[Watch from 43:07](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=2587s)

The Model Context Protocol (MCP) is an open standard for LLMs to interact with external tools and data sources via defined servers. Agents can act as MCP clients, querying servers for available tools and invoking them remotely. This enables leveraging existing, possibly complex, external services as tools without embedding them locally.

## Running a local MCP server example

![Local MCP server example slide](slide_images/slide_23.png)  
[Watch from 45:29](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=2729s)

A local MCP server is launched exposing a tool, such as adding expenses to a file. The agent connects to this server via its URL, retrieves tool definitions, and can call the remote tool as if it were local. This decouples tool implementation from the agent and allows reuse of services hosted anywhere, including cloud environments.

## Connecting to remote MCP servers for documentation queries

![Remote MCP server example slide](slide_images/slide_24.png)  
[Watch from 48:36](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=2916s)

Agents can connect to public MCP servers, such as Microsoft's Learn server, which provides access to extensive documentation tools without authentication. The agent uses these tools to answer domain-specific questions, like Azure CLI commands. However, large MCP server schemas can cause token limit issues, especially with models that have lower token capacity.

## Challenges with large MCP server definitions and token limits

![Token limit challenges slide](slide_images/slide_25.png)  
[Watch from 50:21](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=3021s)

MCP server tool definitions may be large, consuming many tokens when sent to the LLM. This can result in exceeding model token limits, causing errors. Using models with higher token capacities (e.g., gpt-4.1-mini) mitigates this. Developers must be aware of token constraints and possibly optimize tool schemas or model choices accordingly.

## Agent middleware: concepts and types

![Agent middleware overview slide](slide_images/slide_35.png)  
[Watch from 53:00](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=3180s)

Middleware provides hooks to intercept and modify agent execution at three levels: agent middleware, chat middleware, and function middleware. Each operates at different abstraction layers and receives distinct context objects. Middleware enables logging, monitoring, modifying inputs/outputs, enforcing policies, and augmenting behavior dynamically during an agent's run.

## Middleware implementation examples

![Middleware code examples slide](slide_images/slide_36.png)  
[Watch from 55:00](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=3300s)

Middleware functions follow a pattern: they receive context and a next-callable, perform pre-processing, invoke the next step to continue the chain, then post-process results. They can be implemented as simple async functions or as classes inheriting from middleware base classes, supporting initialization, state, and termination control. Middleware can modify inputs, track timing, block requests, or handle errors.

## Use cases and benefits of middleware

![Middleware use cases slide](slide_images/slide_40.png)  
[Watch from 56:53](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=3413s)

Middleware is useful for logging, timing, blocking unsafe content, summarizing conversations, dynamic system prompt injection, PII redaction, model fallback strategies, token limiting, security checks, and retry logic. Middleware can be shared across agents within organizations, promoting code reuse and consistency. It greatly enhances agent flexibility and control, especially in complex production scenarios.

Middleware can set a termination flag to stop the agent's execution early, useful for safety checks, quota enforcement, or blocking undesired requests. Middleware can also be packaged and shared within organizations, allowing consistent logging, security, and behavior modifications across different agents.

## Basic multi-agent architecture with supervisor and specialist agents

![Multi-agent architecture slide](slide_images/slide_26.png)  
[Watch from 58:37](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=3517s)

Multi-agent setups involve a supervisor agent delegating tasks to specialized sub-agents based on the query. In this example, a parenting helper agent routes requests to a weekend planner agent or a meal planner agent. Each sub-agent is wrapped as a tool, allowing the supervisor to invoke them as if calling a function. This pattern supports modularity and task-specific expertise.

## Demonstration of multi-agent setup in code

![Multi-agent supervisor-agent code example slide](slide_images/slide_27.png)  
[Watch from 01:00:36](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=3636s)

The supervisor agent is instantiated with references to its sub-agents, each decorated as a tool. It receives user input and chooses which sub-agent to invoke based on the task. This simple architecture allows discrete task handling but may require more sophisticated orchestration for complex workflows, covered in later sessions.

## Final slides, resources, and next steps

![Closing resources and next steps slide](slide_images/slide_29.png)  
[Watch from 01:01:02](https://www.youtube.com/watch?v=I4vCp9cpsiI&t=3662s)

The session concludes with links to slides, code repositories, and upcoming live streams. Participants are encouraged to register for the series, join Discord office hours for questions, and explore additional resources. Future sessions will cover adding context and memory to agents and advanced workflow orchestration.

## Q&A

### What model is used in the examples?

The primary model used is an Azure-deployed gpt-5-mini. For some examples, such as those with large token requirements, gpt-4.1-mini is used. GitHub models are also available but can have token limits impacting large tool schemas.

### How does the agent choose between multiple MCP servers exposing overlapping tools?

Agents rely on clear, specific tool names and descriptions to distinguish tools. When multiple servers have overlapping capabilities, system prompts can instruct the agent which server's tool to prefer. Proper MCP server design and prompt engineering help reduce ambiguity.
