## Slide 1

![Slide 1](slide_images/slide_1.png)

```
Host your Python agents
on Microsoft Foundry
  Apr 27: Microsoft Agent Framework

  Apr 29: LangChain and LangGraph

  Apr 30: Quality and safety evals

Register at aka.ms/AgentsOnFoundry/series
```

## Slide 2

![Slide 2](slide_images/slide_2.png)

```
Host your agents on Foundry
      Microsoft Agent Framework
aka.ms/foundryhosted/slides/agentframework
Pamela Fox
Python Cloud Advocate
www.pamelafox.org
```

## Slide 3

![Slide 3](slide_images/slide_3.png)

```
Today we'll cover...
• Agents 101
• Building agents with Microsoft Agent Framework
• Foundry models for inference
• Foundry IQ for knowledge retrieval
• Foundry tools for cloud-hosted agentic tools
• Hosting agents on Foundry Agent Service
• Building multi-agent workflows
• Hosting workflows on Foundry Agent Service
```

## Slide 4

![Slide 4](slide_images/slide_4.png)

```
Want the code?
1. Open this GitHub repository:
aka.ms/foundry-hosted-agentframework-demos
2. Use "Code" button to create a GitHub Codespace:




3. Wait a few minutes for Codespace to start up
   Most code samples require deployment and an Azure account.
```

## Slide 5

![Slide 5](slide_images/slide_5.png)

```
Agents 101
```

## Slide 6

![Slide 6](slide_images/slide_6.png)

```
What is an agent?
          Agent           An AI agent uses an LLM to run
                          tools in a loop to achieve a goal.
   Input

                          Agents are often augmented by:
                              Context
                              Memory
   LLM
                              Planning
                  Tools
                              Humans

                          Dive into advanced agentic features
   Goal                   in our previous Python + Agents series:
                              aka.ms/pythonagents/rewatch
```

## Slide 7

![Slide 7](slide_images/slide_7.png)

```
The agentic loop in action
                             The agent keeps calling tools until goal is met:

          Agent                       You're a weather assistant.
   Input                              Weather in Tokyo?

                             LLM      get_weather("Tokyo")

                                      Sunny, 25°C
   LLM                       LLM      It's sunny in Tokyo at 25°C
                  Tools
                                      How about London?

                             LLM      get_weather("London")

   Goal                               Rainy, 12°C

                             LLM      London is rainy at 12°C
```

## Slide 8

![Slide 8](slide_images/slide_8.png)

```
Python AI agent frameworks
A framework makes it easier to handle tool calling and context management:
Framework             Description

agent-framework       A framework from Microsoft with support for agentic
                      patterns and full integration with Azure offerings.
                      (Successor to autogen and semantic-kernel)

langchain v1          An agent-centric framework built on top of Langgraph, with
                      optional Langsmith monitoring
pydantic-ai           A flexible framework designed for type safety and
                      observability (Logfire/OTel), from the creators of Pydantic

There are many frameworks, but these are popular Python frameworks.
```

## Slide 9

![Slide 9](slide_images/slide_9.png)

```
Microsoft Agent Framework                                                       Python   .NET

Open-source engine for building and orchestrating intelligent AI agents and workflows

Based on two popular frameworks from Microsoft:

         Semantic Kernel                                  AutoGen
  Full SDK designed to build AI agents with   Powerful multi-agent research
  ease, excellent for single agents and can   framework with pre-built conversation
  be extended for multi-agents with           orchestration patterns for handling
  integrations to AutoGen                     complex agent systems




 Agents • Orchestration • Memory • State • Cloud-agnostic • Enterprise-ready

     aka.ms/AgentFramework
```

## Slide 10

![Slide 10](slide_images/slide_10.png)

```
Installing Agent Framework for Python
Either install the all-in-one package:
>> pip install agent-framework


OR install more selectively. Always install core:
>> pip install agent-framework-core

Then install only the packages you need, choosing from...
agent-framework-a2a                agent-framework-claude           agent-framework-lab
agent-framework-ag-ui              agent-framework-copilotstudio    agent-framework-mem0
agent-framework-anthropic          agent-framework-declarative      agent-framework-ollama
agent-framework-azure-ai-search    agent-framework-devui            agent-framework-openai
agent-framework-azure-cosmos       agent-framework-durabletask      agent-framework-orchestrations
agent-framework-azurefunctions     agent-framework-foundry          agent-framework-purview
agent-framework-bedrock            agent-framework-foundry-local    agent-framework-redis
agent-framework-chatkit            agent-framework-github-copilot


   Always pin your versions and use a lock file!
  See example: pyproject.toml
```

## Slide 11

![Slide 11](slide_images/slide_11.png)

```
A simple local agent with tools                                     agent-framework
from agent_framework import Agent, tool
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient(
    base_url="http://localhost:11434/v1/",
    model="qwen3.5:4b",
    api_key="no-key-needed")

@tool
def get_enrollment_deadline_info() -> dict:
  """Return enrollment timeline details for health insurance plans."""
  return {"enrollment_opens": "2026-11-11", "enrollment_closes": "2026-11-30"}

agent = Agent(client=client,
  instructions=f"You're an HR helper. Today's date is {date.today().isoformat()}. ",
  tools=[get_enrollment_deadline_info])

response = await agent.run("When does benefits enrollment open?")
print(response.text)

  Full example: agents/stage0_local_model.py
```

## Slide 12

![Slide 12](slide_images/slide_12.png)

```
Building agents on
Foundry
```

## Slide 13

![Slide 13](slide_images/slide_13.png)

```
Ship AI faster with Microsoft Foundry
Microsoft Foundry
The end-to-end platform to design, customize, and deploy AI-driven applications at scale.




        Models                          IQ                     Agent Service                       Tools                 Machine Learning

     Access frontier          Ground LLMs in                 Host agents with           Connect to 1,400+                 Train and deploy
    models like Opus           domain data,                   memory, tools,              built-in service               custom ML models
    4.6 and GPT-5.4.          SharePoint, web                observability, and          connections and                for specific business
                             search, and more.                 evaluations.                MCP tools.                          needs.



                                                                    Control Plane

                       Leverage a complete signals management layer with Microsoft Security integrations

                           Microsoft Agent 365        Microsoft Defender       Microsoft Purview           Microsoft Entra



                                                 Security, compliance, and governance
```

## Slide 14

![Slide 14](slide_images/slide_14.png)

```
Foundry Models
11,000+ models, both open-source and frontier models.   See overall metrics on leaderboards:




                                                        Compare models side-by-side:
```

## Slide 15

![Slide 15](slide_images/slide_15.png)

```
An agent with Foundry models                                        agent-framework


client = OpenAIChatClient(
  base_url=f"{os.environ['AZURE_OPENAI_ENDPOINT']}/openai/v1/",
                                                                         Only the
  api_key=token_provider,                                                client
  model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"])                    changes
@tool
def get_enrollment_deadline_info() -> dict:
"""Return enrollment timeline details for health insurance plans."""
 return {"enrollment_opens": "2026-11-11", "enrollment_closes": "2026-11-30"}

agent = Agent(client=client,
  instructions= f"You're an HR helper. Today's date is {date.today().isoformat()}.",
  tools=[get_enrollment_deadline_info])

response = await agent.run("When does benefits enrollment open?")
print(response.text)

  Full example: agents/stage1_foundry_model.py
```

## Slide 16

![Slide 16](slide_images/slide_16.png)

```
Foundry IQ
Generate unified context using agentic retrieval across multiple knowledge sources (indexed and remote)

                                                            Azure AI Search Knowledge Base
                                                                  Knowledge
                                                                   sources            Merged results
                    Search
                    queries                                       Search index         uid   snippet
                                                                                             Benefits include ...
                                                                                       123
                    Query 1                                         OneLake                  We offer three ...
Input                                 MCP                                              456
        Agent                                                                          789   Each employee ...
                              knowledge_base_retrieve
                    Query 2                                        SharePoint          101   On the first of ...

                                                                                             We send weekly ...
                                                                                       131
                                                                      MCP              145   Available jobs ...
```

## Slide 17

![Slide 17](slide_images/slide_17.png)

```
Adding Foundry IQ as MCP tool                                     agent-framework


mcp_url = (f"{AZURE_AI_SEARCH_SERVICE_ENDPOINT}/knowledgebases/"
           f"{AZURE_AI_SEARCH_KNOWLEDGE_BASE_NAME}/mcp?api-version=2025-11-01-Preview")

async with MCPStreamableHTTPTool(
  name="knowledge-base",
  url=mcp_url,
  http_client=search_http_client,
  allowed_tools=["knowledge_base_retrieve"],
  ) as kb_mcp_tool:

    agent = Agent(
      client=client,
      instructions=f"You're an HR helper. Today's date is {date.today().isoformat()}. "),
      tools=[kb_mcp_tool, get_enrollment_deadline_info])

   response = await agent.run("What PerksPlus benefits are there?")
   print(response.text)
  Full example: agents/stage2_foundry_iq.py
```

## Slide 18

![Slide 18](slide_images/slide_18.png)

```
Foundry Tools
Create a toolbox on Foundry composed of Foundry Tools and MCP servers, for use by any agent.

                                                        Foundry Toolbox
Input              MCP
         Agent                        Any tool from                         Any MCP server
                                   Foundry Tool Catalog                    (auth via OAuth or
                                                                       Foundry Project connection)


                                                 Today we'll build this toolbox:

                                                        Foundry Toolbox
Input              MCP                                                                 Foundry IQ
         Agent                   Web search               Code interpreter
                                                                                        MCP
                               Powered by Bing      Sandboxed Python execution
                                                                                     Multi-source
                                                                                    agentic retrieval
```

## Slide 19

![Slide 19](slide_images/slide_19.png)

```
Creating a toolbox from code
tools = [
  {"type": "web_search", "name": "web_search"},
  {"type": "code_interpreter", "name": "code_interpreter"},
  {
   "type": "mcp",
   "server_label": "knowledge-base",
   "server_url": 'https://${search_service}.search.windows.net/knowledgebases/'
                  ${knowledge_base_name}/mcp?api-version=2025-11-01-preview',
   "project_connection_id": 'kb-mcp-connection',
   "allowed_tools": ["knowledge_base_retrieve"]}
]

resp = httpx.post(f"{PROJECT_ENDPOINT}/toolboxes/{TOOLBOX_NAME}/versions",
  params={"api-version": "v1"}, json={"tools": tools})

httpx.patch(f"{PROJECT_ENDPOINT}/toolboxes/{TOOLBOX_NAME}",
  params={"api-version": "v1"}, json={"default_version": resp.json()["version"]})

  Full code: create-toolbox.py               KB Connection made in: azure_ai_search.bicep
```

## Slide 20

![Slide 20](slide_images/slide_20.png)

```
Equip agent with toolbox                                              agent-framework

toolbox_token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
toolbox_http_client = httpx.AsyncClient(
  auth=ToolboxAuth(toolbox_token_provider),
  headers={"Foundry-Features": "Toolboxes=V1Preview"},
  timeout=120.0)

toolbox_mcp_tool = MCPStreamableHTTPTool(
  name="toolbox",
  url=f"{PROJECT_ENDPOINT}/toolboxes/{TOOLBOX_NAME}/mcp?api-version=v1",
  http_client=toolbox_http_client)

async with toolbox_mcp_tool:
    agent = Agent(
      client=client,
      tools=[
        get_enrollment_deadline_info,
        toolbox_mcp_tool
   Full
      ])code: stage3_agent_foundry_toolbox.py

  Full example: agents/stage3_foundry_toolbox.py
```

## Slide 21

![Slide 21](slide_images/slide_21.png)

```
Foundry Agent Service
Host your agents with production-grade security, reliability, and governance.



                   Prompt Agents                                                            Hosted Agents
                 Define instructions and tools                                       Use your favorite agent framework



       Foundry Tools               Foundry IQ                 Foundry Memory                             Foundry Models
                                                               Managed Memory
                                                             Managed Conversations
                                                               BYO-Memory Store




          Foundry Control Plane             Controls         Observability       Security                Fleet-wide Operations



                                                 Microsoft           Microsoft               Microsoft                       Microsoft
                                                 Agent 365           Defender                Entra                           Purview
```

## Slide 22

![Slide 22](slide_images/slide_22.png)

```
Hosted MAF Agents in Foundry Agent Service
Serve any agent using the Responses API or more generic invocations API.


   Foundry Agent Service
   Identity · Endpoint · State Scaling · Observability

       Container (in Azure Container Registry)


             Responses API Adapter              /agents/{name}/endpoint/protocols/openai/responses


                        Your code
```

## Slide 23

![Slide 23](slide_images/slide_23.png)

```
Hosted MAF Agents in Foundry Agent Service
Microsoft Agent Framework provides a built-in Adapter – just wrap your agent and run.

  Foundry Agent Service

       Container (in Azure Container Registry)      Dockerfile     agent.yaml


            Responses API Adapter
            from agent_framework_foundry_hosting import ResponsesHostServer


             Your code
              agent = Agent(
                client=FoundryChatClient(project_endpoint, model, credential),
                tools=[...])


            server = ResponsesHostServer(agent)
            server.run()
```

## Slide 24

![Slide 24](slide_images/slide_24.png)

```
A Foundry hosted MAF agent                                        agent-framework

from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer


client = FoundryChatClient(
  project_endpoint=PROJECT_ENDPOINT, model=MODEL_DEPLOYMENT_NAME, credential=credential)

agent = Agent(
  client=client,
  name="InternalHRHelper",
  instructions="You are an internal HR helper.",
  tools=[get_enrollment_deadline_info, get_current_date, toolbox_mcp_tool],
  default_options={"store": False})

server = ResponsesHostServer(agent)
server.run()



  Full example: agents/stage4_foundry_hosted.py
```

## Slide 25

![Slide 25](slide_images/slide_25.png)

```
Deploy agent to Foundry with azd
                                                    What this does:
 >> azd auth login                                  1. Provision infrastructure (AI project, model)
                                                    2. Builds image from Dockerfile (using ACR remote build)
 >> azd up                                          3. Push image to Azure Container Registry
                                                    4. Deploys new agent version to Foundry

All based off these project files:
azure.yaml                            Dockerfile                                           agent.yaml
name: ai-foundry-starter-basic       FROM python:3.12-slim                                 kind: hosted
services:                            WORKDIR /app                                          name: hosted-agentframework-agent
hosted-agentframework-agent:         COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv   protocols:
 project: ./agents                   COPY pyproject.toml uv.lock ./                           - protocol: responses
  host: azure.ai.agent               RUN uv sync --locked --no-dev                              version: 1.0.0
  language: docker                   COPY stage4_foundry_hosted.py .                       resources:
  docker:                            ENV PATH="/app/.venv/bin:$PATH"                        cpu: '0.25'
   remoteBuild: true                                                                        memory: '0.5Gi'
  config:                            EXPOSE 8088                                           environment_variables:
   startupCommand: python                                                                     ...
stage4_foundry_hosted.py             CMD ["python", "-u", "stage4_foundry_hosted.py"]
```

## Slide 26

![Slide 26](slide_images/slide_26.png)

```
Interact with Foundry agent in playground
```

## Slide 27

![Slide 27](slide_images/slide_27.png)

```
Interact with Foundry agent from code
You can make direct HTTP calls to the Responses API endpoint:
curl -X POST "$BASE_URL/agents/$AGENT_NAME/endpoint/protocols/openai/responses?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "input": "Hello! What can you do?", "store": true }'


Or use the azure-ai-projects package to send responses via an OpenAI client:
from azure.ai.projects import AIProjectClient

project = AIProjectClient(
  endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
  credential=DefaultAzureCredential(),
  allow_preview=True)

openai_client = project.get_openai_client(agent_name="hosted-agentframework-agent")
response = openai_client.responses.create(input="What PerksPlus benefits are there?")
print(response.output_text)

   Full example: agents/call_foundry_hosted.py
```

## Slide 28

![Slide 28](slide_images/slide_28.png)

```
Local development loop
                                                                          Terminal 1
>> azd ai agent run
Using startup command: python stage4_foundry_hosted.py
Installing dependencies (pyproject.toml)...
  ✓ Dependencies installed (pyproject.toml)
Starting agent on http://localhost:8088


                                                                          Terminal 2
>> azd ai agent invoke --local "What benefits are there?"
Target:       localhost:8088 (local)
Message:      "What PerksPlus benefits are there?"
Session:      6d872d38-a8e5-40bb-9813-34fb272c1785
Conversation: d47ecf0f-c2d6-485a-b628-561ec180bc92

[local] PerksPlus is Zava’s health & wellness reimbursement program. It lets employees
**expense up to $1,000** for eligible fitness/wellness-related items and activities.
```

## Slide 29

![Slide 29](slide_images/slide_29.png)

```
Observability
```

## Slide 30

![Slide 30](slide_images/slide_30.png)

```
Observability with OpenTelemetry (OTel)
OTel standardizes how applications emit traces, metrics, and logs — making
debugging and performance analysis consistent across languages and vendors.

           Traces                           Metrics                          Logs
 0ms                   30ms     __/‾‾‾ cpu_usage:   30%         INFO: 2025-12-05: Server running
                                                                      {"region": "westus"}
       parent-span              ‾‾\__   latency_p95: 43ms
                                                                ERROR: 2025-12-05: User not found
          child-span            _/‾\__ errors:   0.2%                 {"user_id": 123}


Operations composed of spans    Numeric measurements such       Structured log records with
that show how a request moves   as CPU usage, request counts,   message, severity, time stamp,
through services, including     latency, error rates, or any    and contextual attributes.
timing, dependencies, and       custom app metric.
context propagation.”
```

## Slide 31

![Slide 31](slide_images/slide_31.png)

```
Using OpenTelemetry with Agent Framework
Agent framework has built-in support for emitting OpenTelemetry traces:
from agent_framework.observability import enable_instrumentation

enable_instrumentation(enable_sensitive_data=True)
  Full example: agents/stage4_foundry_hosted.py

Agent framework uses the standard "gen_ai" span attribute names and values
for agent executions, LLM calls, and tool calls. Example tool call:
Span: execute_tool get_weather
attribute name                      value
gen_ai.operation.name               execute_tool

gen_ai.tool.name                    get_weather
gen_ai.tool.call.arguments          {"city": "Seattle"}
gen_ai.tool.call.result             {"temperature": 72, "description": "Sunny"}
 gen_ai.tool.description            Returns weather data for a given city
```

## Slide 32

![Slide 32](slide_images/slide_32.png)

```
Exporting OTel to App Insights
When the Foundry Project has an App Insights connection, Foundry agent service will
auto-inject APPLICATIONINSIGHTS_CONNECTION_STRING environment variable.

Then ResponsesHostServer configures the export to App Insights:
from agent_framework_foundry_hosting import ResponsesHostServer
from agent_framework.observability import enable_instrumentation

enable_instrumentation(enable_sensitive_data=True)

agent = Agent(...)

server = ResponsesHostServer(agent)
server.run()

  Full example: agents/stage4_foundry_hosted.py
```

## Slide 33

![Slide 33](slide_images/slide_33.png)

```
Viewing agent traces in Foundry
                                  From Foundry agent,
                                  select :
                                   Traces >
                                   Conversations


                                   See spans for:
                                   agent invocations,
                                   LLM calls,
                                   tool calls
```

## Slide 34

![Slide 34](slide_images/slide_34.png)

```
Viewing agent traces in App Insights
From Foundry agent, select Monitor > Open in Azure Monitor:
```

## Slide 35

![Slide 35](slide_images/slide_35.png)

```
Multi-agent workflows
```

## Slide 36

![Slide 36](slide_images/slide_36.png)

```
What's a workflow?
An agentic workflow is any flow that involves an agent at some point,
typically to handle decision making or answer synthesis.



               Processing                           Processing
 Input              or               Agent               or             Output
               Data Lookup                          Data Lookup
                                  Tool       Tool
```

## Slide 37

![Slide 37](slide_images/slide_37.png)

```
Building workflows in Agent Framework
A workflow is a graph with Executor nodes and edges between them:

               Executor    edge   Executor    edge    Executor
   Input                                                              Output


Each executor subclass defines handler methods that receive messages
and may send messages to next executor and/or yield outputs.




Dive deeper into MAF workflows in our previous Python + Agents series: (Week 2)
   aka.ms/pythonagents/rewatch
```

## Slide 38

![Slide 38](slide_images/slide_38.png)

```
A simple workflow                                                 agent-framework


                                  edge
 Input          Executor                        Executor                    Output
                             send_message()                yield_output()

class UpperCase(Executor):
  @handler
  async def to_upper_case(self, text: str, ctx: WorkflowContext[str]):
    await ctx.send_message(text.upper())

class ReverseText(Executor):
  @handler
  async def reverse(self, text: str, ctx: WorkflowContext[str, str]):
    await ctx.yield_output(text[::-1])

upper = UpperCase()
reverse = ReverseText()
workflow = WorkflowBuilder(start_executor=upper).add_edge(upper, reverse).build()
events = await workflow.run("hello world")
print(f"Output: {events.get_outputs()}")
  Full example: workflows/stage1_simple_executors.py
```

## Slide 39

![Slide 39](slide_images/slide_39.png)

```
Using agents inside workflows                                         agent-framework

Every Agent instance can easily be used as an Executor in a workflow:
                    AgentExecutor                     AgentExecutor
   Input                                                                    Output
                         Agent                            Agent

writer = Agent(client=client, name="Writer",
  instructions="You are a concise content writer. ")
formatter = Agent(client=client, name="Formatter",
  instructions="Format text with emojis and Markdown.")
writer_executor = AgentExecutor(writer, context_mode="last_agent")
formatter_executor = AgentExecutor(formatter, context_mode="last_agent")
workflow = (WorkflowBuilder(
  start_executor=writer_executor,
  output_executors=[formatter_executor])
  .add_edge(writer_executor, formatter_executor)
  .build())
  Full example: workflows/stage2_agent_executors.py
```

## Slide 40

![Slide 40](slide_images/slide_40.png)

```
Using workflow as an agent                                             agent-framework

A workflow can be turned into an agent for compatibility with other systems.


                                      WorkflowAgent

                     AgentExecutor          edge       AgentExecutor
  Input                                                                        Output
                          Agent                               Agent




workflow_agent = workflow.as_agent(name="Content Pipeline")

  Full example: workflows/stage3_as_agent.py
```

## Slide 41

![Slide 41](slide_images/slide_41.png)

```
A Foundry hosted MAF workflow                                 agent-framework

from agent_framework.observability import enable_instrumentation
from agent_framework_foundry_hosting import ResponsesHostServer
enable_instrumentation(enable_sensitive_data=True)

# setup agents and executors...
workflow_agent = (
  WorkflowBuilder(
    start_executor=writer_executor,
    output_executors=[format_executor])
  .add_edge(writer_executor, format_executor)
  .build()
  .as_agent()
)
server = ResponsesHostServer(workflow_agent)
server.run()

  Full example: workflows/stage4_foundry_hosted_as_agent.py
```

## Slide 42

![Slide 42](slide_images/slide_42.png)

```
Next steps                       Register:
                                 https://aka.ms/AgentsOnFoundry/series


Watch past recordings:           Join office hours after each session in Discord:
aka.ms/foundryhosted/resources   aka.ms/pythonai/oh



     Apr 27: Microsoft Agent Framework

     Apr 29: LangChain and LangGraph

     Apr 30: Quality and safety evals
```
