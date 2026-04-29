# Host your agents on Foundry: LangChain and LangGraph

📺 [Watch the full recording on YouTube](https://www.youtube.com/watch?v=mFZHq5mTt0A) |
📑 [Download the slides (PDF)](https://aka.ms/foundryhosted/slides/langchain)

This write-up includes an annotated version of the presentation slides with timestamps to the video plus a summary of the live Q&A session.

## Table of contents

- [Session description](#session-description)
- [Annotated slides](#annotated-slides)
  - [Overview of the "Host your agents on Foundry" series](#overview-of-the-host-your-agents-on-foundry-series)
  - [Welcome to today's topic: Langchain](#welcome-to-todays-topic-langchain)
  - [Today's agenda](#todays-agenda)
  - [Following along with the GitHub repo](#following-along-with-the-github-repo)
  - [Agents 101](#agents-101)
  - [What is an agent](#what-is-an-agent)
  - [The agentic loop in action](#the-agentic-loop-in-action)
  - [Python AI agent frameworks](#python-ai-agent-frameworks)
  - [LangChain and LangGraph](#langchain-and-langgraph)
  - [Installing LangChain for Python](#installing-langchain-for-python)
  - [A simple local agent with tools](#a-simple-local-agent-with-tools)
  - [Building agents on Foundry](#building-agents-on-foundry)
  - [Ship AI faster with Microsoft Foundry](#ship-ai-faster-with-microsoft-foundry)
  - [Using LangChain with Foundry](#using-langchain-with-foundry)
  - [What langchain-azure-ai provides](#what-langchain-azure-ai-provides)
  - [Foundry Models](#foundry-models)
  - [An agent with Foundry models](#an-agent-with-foundry-models)
  - [Foundry IQ](#foundry-iq)
  - [Adding Foundry IQ as MCP tool](#adding-foundry-iq-as-mcp-tool)
  - [Foundry Tools](#foundry-tools)
  - [Creating a toolbox from code](#creating-a-toolbox-from-code)
  - [Equipping the agent with the toolbox](#equipping-the-agent-with-the-toolbox)
  - [Foundry Agent Service](#foundry-agent-service)
  - [Hosted BYO agents: architecture](#hosted-byo-agents-architecture)
  - [Hosted BYO agents: LangGraph adapter](#hosted-byo-agents-langgraph-adapter)
  - [How the adapter works](#how-the-adapter-works)
  - [A Foundry hosted LangGraph agent](#a-foundry-hosted-langgraph-agent)
  - [Deploying with azd](#deploying-with-azd)
  - [Interacting with the agent in the playground](#interacting-with-the-agent-in-the-playground)
  - [Interacting with the agent from code](#interacting-with-the-agent-from-code)
  - [Local development loop](#local-development-loop)
  - [Observability](#observability)
  - [Observability with OpenTelemetry](#observability-with-opentelemetry)
  - [Using OpenTelemetry with LangChain](#using-opentelemetry-with-langchain)
  - [Exporting OTel to App Insights](#exporting-otel-to-app-insights)
  - [Viewing agent traces in Foundry](#viewing-agent-traces-in-foundry)
  - [Viewing agent traces in App Insights](#viewing-agent-traces-in-app-insights)
  - [Multi-agent workflows](#multi-agent-workflows)
  - [What is an agent workflow](#what-is-an-agent-workflow)
  - [Building workflows in LangGraph](#building-workflows-in-langgraph)
  - [A simple workflow](#a-simple-workflow)
  - [Using LLM calls inside workflows](#using-llm-calls-inside-workflows)
  - [A Foundry hosted LangGraph workflow](#a-foundry-hosted-langgraph-workflow)
  - [Next steps and resources](#next-steps-and-resources)
- [Live Chat Q&A](#live-chat-qa)

## Session description

In this three-part series, we showed how to host your own agents on Microsoft Foundry.

In the second session, we deployed agents built with the popular open-source libraries LangChain and LangGraph. Starting with a simple agent, we added Foundry tools like Bing Web Search, grounded the agent in Foundry IQ, then deployed more complex agents using the LangGraph orchestration framework.

Along the way, we used the Foundry UI to interact with the hosted agent, testing it out in the playground and observing the traces from the reasoning and tool calls.

## Annotated slides

### Overview of the "Host your agents on Foundry" series

![Series title slide](slide_images/slide_1.png)
[Watch from 00:55](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=55s)

This is a three-part live stream series on hosting Python agents on Microsoft Foundry. Session 1 (Apr 27) uses Microsoft Agent Framework, session 2 (Apr 29) covers LangChain and LangGraph, and session 3 (Apr 30) addresses quality and safety evaluations. Register and watch past recordings at [aka.ms/AgentsOnFoundry/series](https://aka.ms/AgentsOnFoundry/series).

### Welcome to today's topic: Langchain

![Session title slide](slide_images/slide_2.png)
[Watch from 02:02](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=122s)

Session slides are available at [aka.ms/foundryhosted/slides/langchain](https://aka.ms/foundryhosted/slides/langchain). The session covers building agents with LangChain, integrating Foundry components (models, IQ, tools), hosting agents on Foundry Agent Service, and building multi-agent workflows with LangGraph.

### Today's agenda

![Agenda slide](slide_images/slide_3.png)
[Watch from 02:15](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=135s)

The session covers Agents 101, building agents with LangChain, Foundry Models for inference, Foundry IQ for knowledge retrieval, Foundry Tools for cloud-hosted agentic tools, hosting agents on Foundry Agent Service, building multi-agent workflows with LangGraph, and hosting workflows on Foundry Agent Service.

### Following along with the GitHub repo

![Code repo setup slide](slide_images/slide_4.png)
[Watch from 02:34](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=154s)

All code samples are in the GitHub repository at [aka.ms/foundry-hosted-langchain-demos](https://aka.ms/foundry-hosted-langchain-demos). Open it in a GitHub Codespace using the "Code" button, then follow the README to deploy to your own Azure account. Most code samples require deployment and an Azure account. This is a separate repo from the Agent Framework session because it uses LangChain-specific packages.

### Agents 101

![Agents 101 section header](slide_images/slide_5.png)
[Watch from 03:05](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=185s)

### What is an agent

![What is an agent diagram](slide_images/slide_6.png)
[Watch from 03:08](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=188s)

An AI agent uses an LLM to run tools in a loop to achieve a goal. The loop is what makes agents powerful: the LLM can call one tool or twenty, depending on the complexity of the problem. Agents are commonly augmented with memory (short-term, long-term, dynamic), planning (or a reasoning model with built-in planning), and human-in-the-loop checkpoints where the agent pauses to confirm before executing a tool call. For a deeper dive into agentic patterns, the previous Python + Agents series is at [aka.ms/pythonagents/rewatch](https://aka.ms/pythonagents/rewatch).

### The agentic loop in action

![Agentic loop diagram](slide_images/slide_7.png)
[Watch from 04:01](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=241s)

When the user asks a weather assistant "What's the weather in Tokyo?", the LLM selects `get_weather("Tokyo")`, receives the result, and responds. When the user follows up with "How about London?", the LLM calls the tool again for London and responds with that result. The agent keeps calling tools until the goal is met.

### Python AI agent frameworks

![Agent frameworks comparison table](slide_images/slide_8.png)
[Watch from 04:26](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=266s)

Using an agent framework rather than raw LLM calls handles tool-call parsing, context window management, and the agentic loop automatically. Three popular Python frameworks are:

- **agent-framework** — Microsoft's framework, successor to AutoGen and Semantic Kernel, with agentic patterns and full Azure integration.
- **langchain v1** — An agent-centric framework built on top of LangGraph, with optional LangSmith monitoring.
- **pydantic-ai** — A flexible framework designed for type safety and observability (Logfire/OTel), from the creators of Pydantic.

### LangChain and LangGraph

![LangChain and LangGraph overview slide](slide_images/slide_9.png)
[Watch from 05:21](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=321s)

LangChain and LangGraph are two complementary open-source libraries. LangChain is a composable framework with 100+ integrations for quickly building agents, chatbots, and RAG pipelines. LangGraph provides graph-based orchestration for stateful, multi-step agents with cycles, branching, and human-in-the-loop. LangChain v1 is actually built on top of LangGraph — it's the easy way to build a single agent with tools. Once you need multi-agent workflows with multiple nodes, you move to LangGraph directly. Find them at [langchain.com](https://langchain.com).

### Installing LangChain for Python

![Installation options slide](slide_images/slide_10.png)
[Watch from 07:20](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=440s)

Install the main `langchain` package for agent building, `langgraph` for workflow orchestration, and `langchain-openai` as the provider package for any OpenAI-compatible endpoint (which covers all models used in this session). Many other provider packages exist for Anthropic, etc., but `langchain-openai` suffices for Azure-deployed models since they all expose OpenAI-compatible endpoints.

Always pin your versions and use a lock file. With uv, `pyproject.toml` specifies minimum versions and `uv.lock` pins exact versions, so upgrades are explicit. This prevents both backwards-incompatible breakage and supply-chain attacks where compromised package versions get pushed to PyPI.

### A simple local agent with tools

![Local agent code slide](slide_images/slide_11.png)
[Watch from 10:30](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=630s)

The simplest LangChain agent uses `ChatOpenAI` pointed at a local model endpoint (e.g., Ollama at `http://localhost:11434/v1/`). Define a Python function decorated with `@tool` from LangChain — the function name, type annotations, and docstring all become the tool schema sent to the LLM, so they are a form of prompt engineering. Create the agent with `create_agent(model=client, system_prompt=..., tools=[...])` and run with `await agent.ainvoke(...)`. The LLM sees the tool, decides to call it, gets the result, and answers based on the tool output. Full example: [agents/stage0_local_model.py](https://github.com/Azure-Samples/foundry-hosted-langchain-demos/blob/main/agents/stage0_local_model.py).

### Building agents on Foundry

![Section header slide](slide_images/slide_12.png)
[Watch from 14:37](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=877s)

### Ship AI faster with Microsoft Foundry

![Microsoft Foundry overview diagram](slide_images/slide_13.png)
[Watch from 14:50](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=890s)

Microsoft Foundry is the end-to-end platform for designing, customizing, and deploying AI-driven applications. Key components used in this session:

- **Models** — Frontier models such as GPT-5.4 and Claude Opus 4.6, plus 11,000+ open-source models.
- **IQ** — Ground LLMs in domain data from Azure AI Search, SharePoint, OneLake, web search, and more.
- **Agent Service** — Host agents with memory, tools, observability, and evaluations.
- **Tools** — 1,400+ built-in service connections and MCP tools.

Security, compliance, and governance flow through Microsoft Entra, Defender, and Purview.

### Using LangChain with Foundry

![langchain-azure-ai package slide](slide_images/slide_14.png)
[Watch from 15:53](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=953s)

Install `langchain-azure-ai`, the Microsoft-supported package that provides tight integrations between LangChain and Azure/Foundry. It has extras for additional functionality:

- `langchain-azure-ai[opentelemetry]` — Emit traces to Application Insights.
- `langchain-azure-ai[tools]` — Integrate with Foundry Toolbox.

Sibling packages cover other Azure services: `langchain-azure-cosmosdb`, `langchain-azure-postgresql`, `langchain-azure-storage`, `langchain-sqlserver`, and `langchain-azure-dynamic-sessions`.

### What langchain-azure-ai provides

![Feature table slide](slide_images/slide_15.png)
[Watch from 17:43](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=1063s)

The `langchain-azure-ai` package provides Foundry Tools integration (connect agents to the Foundry tool catalog and toolboxes), Foundry Agent Service integrations (use hosted Foundry agents as reusable LangGraph nodes), OpenTelemetry tracing (export LangChain/LangGraph traces to Application Insights), document ingestion and RAG utilities (document loaders, retrievers, vector store helpers), and AI Content Safety middleware (text/image moderation, prompt injection detection, groundedness checks).

### Foundry Models

![Foundry Models UI screenshot](slide_images/slide_16.png)
[Watch from 18:12](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=1092s)

Foundry exposes 11,000+ models, including open-source models from Hugging Face and frontier models from OpenAI, Anthropic, Mistral, and others. From the model catalog you can search, view quality and safety leaderboards, and compare models side by side. For choosing between models for a specific application, write evaluations for your domain rather than relying on generic benchmarks.

### An agent with Foundry models

![Foundry model agent code slide](slide_images/slide_17.png)
[Watch from 19:33](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=1173s)

Switching from a local model to a Foundry-deployed model requires only changing the `ChatOpenAI` constructor. Point `base_url` at the Azure OpenAI endpoint (`{AZURE_OPENAI_ENDPOINT}/openai/v1/`), pass an Entra token provider for keyless auth, and specify the deployment name as the model. Everything else — tools, agent creation, invocation — stays the same.

```python
client = ChatOpenAI(
    base_url=f"{os.environ['AZURE_OPENAI_ENDPOINT']}/openai/v1/",
    api_key=token_provider,
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"])
```

Full example: [agents/stage1_foundry_model.py](https://github.com/Azure-Samples/foundry-hosted-langchain-demos/blob/main/agents/stage1_foundry_model.py).

### Foundry IQ

![Foundry IQ architecture diagram](slide_images/slide_18.png)
[Watch from 22:30](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=1350s)

Foundry IQ is Azure AI Search's agentic knowledge base, accessible through Foundry. A knowledge base is composed of multiple knowledge sources — Azure AI Search indexes, OneLake, SharePoint, and (in private preview) arbitrary MCP servers. The agent sends queries to the knowledge base, which fans them out across all sources in parallel, merges the results, and reranks them using a ranking model. The knowledge base is exposed to the agent as an MCP server with a single tool called `knowledge_base_retrieve` that accepts an array of queries.

### Adding Foundry IQ as MCP tool

![Foundry IQ MCP code slide](slide_images/slide_19.png)
[Watch from 24:38](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=1478s)

Connect the agent to Foundry IQ using `MultiServerMCPClient` from the `langchain-mcp-adapters` package. The MCP URL follows the pattern `{AZURE_AI_SEARCH_SERVICE_ENDPOINT}/knowledgebases/{KNOWLEDGE_BASE_NAME}/mcp?api-version=2025-11-01-Preview`. Pass authentication credentials, get the tools from the server, and add them to the agent alongside local tools:

```python
kb_client = MultiServerMCPClient({
    "knowledge-base": {
        "url": mcp_url,
        "transport": "streamable_http",
        "auth": _AzureTokenAuth(search_token_provider),
    }
})
kb_tools = await kb_client.get_tools()

agent = create_agent(
    model=client,
    tools=[get_enrollment_deadline_info, *kb_tools],
    system_prompt=f"You're an HR helper. Today is {date.today().isoformat()}.")
```

When the agent starts, it does an MCP handshake to discover available tools. The agent can then use both local and remote tools to answer questions — calling the knowledge base for domain-specific answers and local tools for structured data. Full example: [agents/stage2_foundry_iq.py](https://github.com/Azure-Samples/foundry-hosted-langchain-demos/blob/main/agents/stage2_foundry_iq.py).

### Foundry Tools

![Foundry Toolbox overview diagram](slide_images/slide_20.png)
[Watch from 28:22](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=1702s)

Foundry Tools lets you build a **Foundry Toolbox** — a named collection of tools from the Foundry Tool Catalog and MCP servers. The toolbox exposes a unified MCP server endpoint, so any agent can connect to one endpoint and access all bundled tools. Useful built-in tools:

- **Web search** — Bing-powered real-time web search.
- **Code interpreter** — Sandboxed Python execution for math, data analysis, and image manipulation.
- **Foundry IQ** — The knowledge base MCP server (can be added to the toolbox or used separately).

### Creating a toolbox from code

![Toolbox creation code slide](slide_images/slide_21.png)
[Watch from 30:10](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=1810s)

The Foundry Toolbox API is currently only available via REST (no SDK yet). Create a toolbox by POSTing a list of tool definitions to the toolboxes endpoint, then PATCH to set it as the default version:

```python
tools = [
    {"type": "web_search", "name": "web_search"},
    {"type": "code_interpreter", "name": "code_interpreter"},
    {"type": "mcp", "server_label": "knowledge-base",
     "server_url": "https://${search_service}.search.windows.net/knowledgebases/...",
     "project_connection_id": "kb-mcp-connection",
     "allowed_tools": ["knowledge_base_retrieve"]}
]
resp = httpx.post(f"{PROJECT_ENDPOINT}/toolboxes/{TOOLBOX_NAME}/versions", ...)
httpx.patch(f"{PROJECT_ENDPOINT}/toolboxes/{TOOLBOX_NAME}", ...,
            json={"default_version": resp.json()["version"]})
```

The knowledge base project connection is defined in `azure_ai_search.bicep`. Full code: [create-toolbox.py](https://github.com/Azure-Samples/foundry-hosted-langchain-demos/blob/main/infra/create-toolbox.py).

### Equipping the agent with the toolbox

![Toolbox agent code slide](slide_images/slide_22.png)
[Watch from 31:01](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=1861s)

The `langchain-azure-ai` package has built-in support for Foundry Toolbox via `AzureAIProjectToolbox`. Just provide the toolbox name and credential, get the tools, and pass them to the agent:

```python
from langchain_azure_ai.tools import AzureAIProjectToolbox

toolbox = AzureAIProjectToolbox(
    toolbox_name=TOOLBOX_NAME,
    credential=DefaultAzureCredential())
toolbox_tools = await toolbox.get_tools()

agent = create_agent(
    model=client,
    tools=[get_enrollment_deadline_info, *toolbox_tools])
```

Since the toolbox is an MCP server, the agent does a handshake at startup to discover tools (e.g., web search and code interpreter), then uses them as needed. Full example: [agents/stage3_foundry_toolbox.py](https://github.com/Azure-Samples/foundry-hosted-langchain-demos/blob/main/agents/stage3_foundry_toolbox.py).

### Foundry Agent Service

![Foundry Agent Service overview diagram](slide_images/slide_23.png)
[Watch from 33:19](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=1999s)

Foundry Agent Service hosts agents with production-grade security, reliability, and governance. It supports two agent types:

- **Prompt agents** — Defined by instructions and tools using the Azure AI Project SDK. Limited customization since the agentic loop runs as a cloud service.
- **Hosted agents** — Bring your own agent framework (LangChain, Agent Framework, Pydantic AI, etc.) packaged as a container. More flexibility for developers.

Both types can use Foundry Tools, IQ, Memory, and Models. The control plane provides observability, security (Entra, Defender, Purview), and fleet-wide operations.

### Hosted BYO agents: architecture

![Hosted agent architecture diagram](slide_images/slide_24.png)
[Watch from 36:10](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2170s)

A hosted agent runs inside a container in Azure Container Registry. Foundry Agent Service pulls the container and runs it on a fast microVM platform that provides low startup latency and strong session isolation. To get full Foundry functionality (playground, evaluations, traces), the agent must expose the OpenAI Responses API protocol at:

```text
/agents/{name}/endpoint/protocols/openai/responses
```

There's also a more generic invocations API for agents that just need an HTTP endpoint, but the Responses API unlocks more Foundry features.

### Hosted BYO agents: LangGraph adapter

![LangGraph adapter architecture slide](slide_images/slide_25.png)
[Watch from 38:42](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2322s)

A community-written adapter bridges LangGraph to the Responses API protocol. Import `AzureAIResponsesAgentHost` from `langchain_azure_ai_runtime`, wrap your agent, and call `host.run()`. The container also needs a `Dockerfile` and an `agent.yaml` declaring the agent name, protocol, and resource requirements.

```python
from langchain_azure_ai_runtime import AzureAIResponsesAgentHost

agent = create_agent(model=ChatOpenAI(...), tools=[...])
host = AzureAIResponsesAgentHost(graph=agent, stream_mode="messages",
    responses_history_count=20)
host.run()
```

### How the adapter works

![Adapter translation diagram](slide_images/slide_26.png)
[Watch from 39:37](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2377s)

The adapter translates between Responses API message types and LangGraph/LangChain types. For input: `MessageContentInputTextContent` becomes `HumanMessage`, `MessageContentOutputTextContent` becomes `AIMessage`, and `system`/`developer` role becomes `SystemMessage`. For output: `AIMessage(tool_calls=[...])` becomes `function_call`, and `AIMessage(content="...")` becomes `output_text`. This bidirectional translation lets the Foundry platform interact with LangChain agents using the standard Responses API.

### A Foundry hosted LangGraph agent

![Hosted agent Python code slide](slide_images/slide_27.png)
[Watch from 42:30](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2550s)

The full hosted agent code brings together all the pieces: enable tracing, create the LLM client pointing at the Foundry project endpoint, create the agent with tools (local tools plus toolbox tools), and wrap it in the responses host:

```python
from langchain.agents import create_agent
from langchain_azure_ai.callbacks.tracers import enable_auto_tracing
from langchain_azure_ai.tools import AzureAIProjectToolbox
from langchain_openai import ChatOpenAI
from vendor.langchain_azure_ai_runtime import AzureAIResponsesAgentHost

enable_auto_tracing(auto_configure_azure_monitor=True, agent_id="hr-agent")

llm = ChatOpenAI(base_url=f"{PROJECT_ENDPOINT}/openai/v1", api_key=token_provider,
    model=MODEL_DEPLOYMENT_NAME, use_responses_api=True)

agent = create_agent(model=llm,
    tools=[get_enrollment_deadline_info, get_current_date, *toolbox_tools],
    system_prompt="You are an internal HR helper.")

host = AzureAIResponsesAgentHost(graph=agent, stream_mode="messages")
host.run()
```

Full example: [agents/stage4_foundry_hosted.py](https://github.com/Azure-Samples/foundry-hosted-langchain-demos/blob/main/agents/stage4_foundry_hosted.py).

### Deploying with azd

![azd deployment config slide](slide_images/slide_28.png)
[Watch from 42:48](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2568s)

`azd up` provisions infrastructure (AI project, model deployments, search service, container registry), builds the Docker image using ACR remote build, pushes it to Azure Container Registry, and deploys a new agent version to Foundry. Three config files drive the deployment:

- **`azure.yaml`** — Lists services; each hosted agent entry specifies the project folder, host (`azure.ai.agent`), language (`docker`), and `remoteBuild: true`.
- **`Dockerfile`** — Standard Python slim container using uv for dependency installation; runs the agent file on startup.
- **`agent.yaml`** — Declares the agent name, `responses` protocol, CPU/memory resources for the microVM, and environment variables to inject.

A monorepo can have multiple agents and workflows deployed as separate Foundry agents, each with its own Dockerfile and agent.yaml referenced from the root azure.yaml.

### Interacting with the agent in the playground

![Foundry playground screenshot](slide_images/slide_29.png)
[Watch from 45:15](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2715s)

The Foundry playground lets you chat with the deployed agent and watch a live log stream from the microVM container. The log stream shows every tool call and LLM request in real time. Anyone in your tenant can access the playground, making it easy for team members to experiment with each other's agents.

### Interacting with the agent from code

![Code interaction slide](slide_images/slide_30.png)
[Watch from 47:02](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2822s)

Call the hosted agent via direct HTTP or the `azure-ai-projects` SDK. With the SDK, use `project.get_openai_client(agent_name=...)` to get an OpenAI-compatible client, then call `responses.create()`:

```python
from azure.ai.projects import AIProjectClient

project = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
                          credential=DefaultAzureCredential(), allow_preview=True)
openai_client = project.get_openai_client(agent_name="hosted-langchain-agent")
response = openai_client.responses.create(input="What PerksPlus benefits are there?")
print(response.output_text)
```

Any client that can call the OpenAI Responses API works with hosted agents. Full example: [agents/call_foundry_hosted.py](https://github.com/Azure-Samples/foundry-hosted-langchain-demos/blob/main/agents/call_foundry_hosted.py).

### Local development loop

![Local dev loop slide](slide_images/slide_31.png)
[Watch from 47:52](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2872s)

Test the hosted agent locally before deploying. `azd ai agent run` starts the Responses server locally on port 8088 using the same startup command as the container. `azd ai agent invoke --local` sends a message to that local server:

```text
>> azd ai agent run
Starting agent on http://localhost:8088

>> azd ai agent invoke --local "What PerksPlus benefits are there?"
[local] PerksPlus is Zava's health & wellness reimbursement program...
```

Use this local loop during development so you only deploy once everything works well.

### Observability

![Observability section header](slide_images/slide_32.png)
[Watch from 48:56](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2936s)

### Observability with OpenTelemetry

![OTel overview slide](slide_images/slide_33.png)
[Watch from 49:00](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2940s)

OpenTelemetry (OTel) is the open standard for application observability across languages and vendors. It covers three signal types:

- **Traces** — Parent/child spans showing how a request moves through services, with timing and context propagation.
- **Metrics** — Numeric measurements such as CPU usage, request count, latency percentiles, and error rates.
- **Logs** — Structured log records with message, severity, timestamp, and contextual attributes.

### Using OpenTelemetry with LangChain

![OTel + LangChain code slide](slide_images/slide_34.png)
[Watch from 49:10](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2950s)

Enable OTel instrumentation by calling `enable_auto_tracing` from the `langchain-azure-ai` package at the start of your code:

```python
from langchain_azure_ai.callbacks.tracers import enable_auto_tracing

enable_auto_tracing(enable_content_recording=True)
```

The emitted traces use the standard `gen_ai` span attribute names for agent executions, LLM calls, and tool calls. Each tool call produces a span like:

| Attribute | Value |
| --- | --- |
| `gen_ai.operation.name` | `execute_tool` |
| `gen_ai.tool.name` | `get_weather` |
| `gen_ai.tool.call.arguments` | `{"city": "Seattle"}` |
| `gen_ai.tool.call.result` | `{"temperature": 72, "description": "Sunny"}` |

Content recording includes tool call arguments which could be sensitive — disable it in production if needed.

### Exporting OTel to App Insights

![App Insights export slide](slide_images/slide_35.png)
[Watch from 50:09](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=3009s)

When the Foundry project has an Application Insights connection, Foundry Agent Service auto-injects the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable into the container. Then configure the export:

```python
enable_auto_tracing(
    auto_configure_azure_monitor=True,
    enable_content_recording=False,
    trace_all_langgraph_nodes=True,
    agent_id="hr-agent")
```

This configures the OTel exporter to send traces to Azure Monitor based on the connection string. Full example: [agents/stage4_foundry_hosted.py](https://github.com/Azure-Samples/foundry-hosted-langchain-demos/blob/main/agents/stage4_foundry_hosted.py).

### Viewing agent traces in Foundry

![Foundry traces view screenshot](slide_images/slide_36.png)
[Watch from 50:17](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=3017s)

From the Foundry agent, go to **Traces > Conversations** to see all conversations. Clicking a conversation shows the full span tree: agent invocation → LLM call → tool calls → LLM call. Each span includes `gen_ai` attributes showing the agent version, tool names, duration, and call sequence — useful for understanding how the agent answered a particular question.

### Viewing agent traces in App Insights

![App Insights agents tab screenshot](slide_images/slide_37.png)
[Watch from 51:33](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=3093s)

From the Foundry agent, select **Monitor > Open in Azure Monitor** to reach the new **Agents** tab in Application Insights. Because all traces follow the standard `gen_ai` conventions, App Insights provides ready-made dashboards showing agent run counts, tool call frequency, errors, and average duration across all frameworks.

### Multi-agent workflows

![Multi-agent workflows section header](slide_images/slide_38.png)
[Watch from 52:02](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=3122s)

### What is an agent workflow

![Workflow definition diagram](slide_images/slide_39.png)
[Watch from 52:05](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=3125s)

An agent workflow is any flow that involves an agent at some point — typically for decision-making or answer synthesis. A workflow might include non-agent processing steps (data lookup, transformation) before and after the agent nodes.

### Building workflows in LangGraph

![StateGraph explanation slide](slide_images/slide_40.png)
[Watch from 52:23](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=3143s)

In LangGraph, a workflow is a `StateGraph` with node functions and edges between them. Each node is a function that receives state, modifies it, and returns updated state. Edges define the flow, including conditional edges for branching. You define start, intermediate, and end nodes, compile the graph, then invoke it with input. See the [LangChain docs on workflows and agents](https://langchain.com).

### A simple workflow

![Simple workflow code slide](slide_images/slide_41.png)
[Watch from 52:53](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=3173s)

A minimal two-node workflow converts text to uppercase then reverses it:

```python
class TextState(TypedDict):
    text: str

def upper_case(state: TextState) -> dict:
    return {"text": state["text"].upper()}

def reverse_text(state: TextState) -> dict:
    return {"text": state["text"][::-1]}

graph = (StateGraph(TextState)
    .add_node(upper_case).add_node(reverse_text)
    .add_edge(START, "upper_case")
    .add_edge("upper_case", "reverse_text")
    .add_edge("reverse_text", END)
    .compile())
result = graph.invoke({"text": "hello world"})
```

The state (`TextState`) is a typed dictionary passed between nodes. Each node receives the state and returns a dictionary with the updated fields. Full example: [workflows/stage1_simple_nodes.py](https://github.com/Azure-Samples/foundry-hosted-langchain-demos/blob/main/workflows/stage1_simple_nodes.py).

### Using LLM calls inside workflows

![LLM workflow nodes slide](slide_images/slide_42.png)
[Watch from 54:42](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=3282s)

Each node can make LLM calls — just invoke the model inside the function. A writer node asks the LLM to generate content, then a formatter node asks the LLM to add emoji and Markdown formatting:

```python
async def writer(state: TextState) -> dict:
    response = await llm.ainvoke([
        {"role": "system", "content": "You are a concise content writer."},
        {"role": "user", "content": state["text"]}])
    return {"text": response.content}

async def formatter(state: TextState) -> dict:
    response = await llm.ainvoke([
        {"role": "system", "content": "Format text with emojis and Markdown."},
        {"role": "user", "content": state["text"]}])
    return {"text": response.content}
```

Full example: [workflows/stage2_agent_nodes.py](https://github.com/Azure-Samples/foundry-hosted-langchain-demos/blob/main/workflows/stage2_agent_nodes.py).

### A Foundry hosted LangGraph workflow

![Hosted workflow code slide](slide_images/slide_43.png)
[Watch from 55:50](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=3350s)

Hosting a workflow on Foundry uses the same pattern as hosting a single agent: build the graph, wrap it in `AzureAIResponsesAgentHost`, and run:

```python
from langchain_azure_ai.callbacks.tracers import enable_auto_tracing
from langchain_azure_ai_runtime import AzureAIResponsesAgentHost

enable_auto_tracing(auto_configure_azure_monitor=True, agent_id="slogan-workflow")

graph = (StateGraph(MessagesState)
    .add_node(writer).add_node(formatter)
    .add_edge(START, "writer").add_edge("writer", "formatter")
    .add_edge("formatter", END)
    .compile())

host = AzureAIResponsesAgentHost(graph=graph, stream_mode="messages")
host.run()
```

The workflow lives in its own subfolder with its own `Dockerfile` and `agent.yaml`. The root `azure.yaml` lists both agents and workflows as separate services, so `azd up` deploys everything in one command. Full example: [workflows/stage3_foundry_hosted_as_agent.py](https://github.com/Azure-Samples/foundry-hosted-langchain-demos/blob/main/workflows/stage3_foundry_hosted_as_agent.py).

### Next steps and resources

![Next steps slide](slide_images/slide_44.png)
[Watch from 57:27](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=3447s)

- Register for the series: [aka.ms/AgentsOnFoundry/series](https://aka.ms/AgentsOnFoundry/series)
- Watch past recordings and get resources: [aka.ms/foundryhosted/resources](https://aka.ms/foundryhosted/resources)
- Join Discord office hours after each session: [aka.ms/pythonai/oh](https://aka.ms/pythonai/oh)

This is all very new — the new version of Foundry hosted agents launched just one week before this session. File issues in the GitHub repo or in the Foundry Discord to help improve the platform during public preview.

## Live Chat Q&A

### Can we use Foundry Short Term memory in a LangGraph agent for multi-turn conversations?

[Watch from 35:19](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2119s)

Foundry does have a hosted memory service. There are code examples showing how to use the managed Foundry memory store class. It was not demonstrated in this session, but it is another Foundry component you can integrate alongside Models, IQ, and Tools. Check the documentation for examples of making agents stateful with Foundry memory.

### Why is the response adapter required? Why can't we use LangChain's ainvoke method?

[Watch from 38:42](https://www.youtube.com/watch?v=mFZHq5mTt0A&t=2322s)

Foundry Agent Service expects agents to speak the OpenAI Responses API protocol. LangChain uses its own message types (HumanMessage, AIMessage, etc.) and its own invocation interface. The adapter is a translation layer that converts between the two: it receives Responses API input, translates it to LangChain messages, runs the agent, then translates the output back to Responses API format. Without it, Foundry wouldn't know how to communicate with a LangChain agent.
