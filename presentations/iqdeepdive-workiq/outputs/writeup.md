# Microsoft IQ Deep Dive with Python: Work IQ

📺 [Watch the full recording on YouTube](https://www.youtube.com/watch?v=xI3wMCC0oBY) |
📑 [Download the slides (PDF)](https://aka.ms/iqdeepdive/slides/workiq)

This write-up includes an annotated version of the presentation slides with timestamps to the video plus a summary of the live chat Q&A.

## Table of contents

- [Session description](#session-description)
- [Annotated slides](#annotated-slides)
  - [Microsoft IQ Deep Dive with Python series](#microsoft-iq-deep-dive-with-python-series)
  - [Microsoft IQ Deep Dive: Work IQ](#microsoft-iq-deep-dive-work-iq)
  - [Today's agenda](#todays-agenda)
  - [Getting the code](#getting-the-code)
  - [Microsoft IQ](#microsoft-iq)
  - [The Microsoft IQ platform](#the-microsoft-iq-platform)
  - [Work IQ](#work-iq)
  - [Work IQ is an agent for work data](#work-iq-is-an-agent-for-work-data)
  - [Why Work IQ](#why-work-iq)
  - [Work IQ vs Microsoft Graph](#work-iq-vs-microsoft-graph)
  - [The Work IQ API surface](#the-work-iq-api-surface)
  - [Protocol strategy: when to use A2A, MCP, REST](#protocol-strategy-when-to-use-a2a-mcp-rest)
  - [Retrieval with Work IQ](#retrieval-with-work-iq)
  - [Building with Work IQ](#building-with-work-iq)
  - [Work IQ retrieval with ask](#work-iq-retrieval-with-ask)
  - [The A2A agent card](#the-a2a-agent-card)
  - [Work IQ via the A2A protocol](#work-iq-via-the-a2a-protocol)
  - [Ten generic tools, progressive disclosure](#ten-generic-tools-progressive-disclosure)
  - [Work IQ via the MCP protocol](#work-iq-via-the-mcp-protocol)
  - [The write path and its guardrails](#the-write-path-and-its-guardrails)
  - [Taking action with do_action](#taking-action-with-do_action)
  - [Foundry IQ + Work IQ](#foundry-iq--work-iq)
  - [One knowledge base, every source](#one-knowledge-base-every-source)
  - [Work IQ as a knowledge source](#work-iq-as-a-knowledge-source)
  - [Using Work IQ as a knowledge source in Python](#using-work-iq-as-a-knowledge-source-in-python)
  - [Agents + Work IQ](#agents--work-iq)
  - [What is an agent](#what-is-an-agent)
  - [Two ways to use Work IQ as an agent tool](#two-ways-to-use-work-iq-as-an-agent-tool)
  - [Work IQ as a tool in Microsoft Agent Framework](#work-iq-as-a-tool-in-microsoft-agent-framework)
  - [Agent 365 autopilots](#agent-365-autopilots)
  - [What is an Agent 365 autopilot](#what-is-an-agent-365-autopilot)
  - [How the autopilot is wired](#how-the-autopilot-is-wired)
  - [Hosting the autopilot: the activity host](#hosting-the-autopilot-the-activity-host)
  - [The autopilot acts as itself, not as you](#the-autopilot-acts-as-itself-not-as-you)
  - [Making a hosted agent an autopilot](#making-a-hosted-agent-an-autopilot)
  - [Publish and get approved](#publish-and-get-approved)
  - [Demo: the Work Mate autopilot](#demo-the-work-mate-autopilot)
  - [Next steps and resources](#next-steps-and-resources)
  - [Microsoft IQ Live](#microsoft-iq-live)
- [Live Chat Q&A](#live-chat-qa)

## Session description

In the second session of the Microsoft IQ Deep Dive with Python series, we focused on Work IQ and how it brings workplace context into AI-powered experiences.

We compared Work IQ to Microsoft Graph, then explored all three protocols it speaks — A2A, MCP, and REST — with runnable Python notebooks for each. We walked through the 10 generic tools that Work IQ exposes over MCP, including `ask`, which calls Microsoft 365 Copilot directly, and `do_action`, the only write path.

We also connected Work IQ to a Foundry IQ knowledge base as a knowledge source, so a single query returns a blended answer across indexed HR documents and live work context.

Then we wired Work IQ into a Microsoft Agent Framework agent as an MCP tool, and finished with Agent 365 autopilots — agents that get their own Microsoft 365 identity, mailbox, and place in the org chart, and act as themselves rather than on behalf of you. A live demo showed the Work Mate autopilot reading its own mailbox in Teams and emailing a customer directly.

All code demos use Python and are available in an open-source repository for you to deploy yourself.

## Annotated slides

### Microsoft IQ Deep Dive with Python series

![Series title slide](slide_images/slide_1.png)
[Watch from 00:56](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=56s)

This is a three-part series covering the Microsoft IQ family, one IQ per day. Session 1 (July 28) covered Foundry IQ plus a look at Web IQ, session 2 (July 29) covers Work IQ, and session 3 (July 30) covers Fabric IQ. Register for the whole series at [aka.ms/IQDeepDivePython/series](https://aka.ms/IQDeepDivePython/series).

### Microsoft IQ Deep Dive: Work IQ

![Session title slide](slide_images/slide_2.png)
[Watch from 01:50](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=110s)

Presented by Ayça Baş, Senior Cloud Advocate at Microsoft and GitHub ([github.com/aycabas](https://github.com/aycabas)). Slides are at [aka.ms/iqdeepdive/slides/workiq](https://aka.ms/iqdeepdive/slides/workiq) and are free to reuse if you want to present this content yourself.

### Today's agenda

![Agenda slide](slide_images/slide_3.png)
[Watch from 02:16](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=136s)

Seven topics: a Work IQ overview, API concepts and the three protocols (A2A, MCP, REST), A2A integration patterns, MCP integration and `do_action` as the only write path, building with Work IQ tools, Work IQ inside a Microsoft Agent Framework agent, and shipping that agent as an Agent 365 autopilot.

Office hours run on Discord straight after each session at [aka.ms/pythonai/oh](https://aka.ms/pythonai/oh).

### Getting the code

![Code repo slide](slide_images/slide_4.png)
[Watch from 04:08](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=248s)

All three sessions share one repository at [aka.ms/iqdeepdive](https://aka.ms/iqdeepdive) — every Foundry IQ, Work IQ, and Fabric IQ notebook and agent lives there. Use the "Code" button to open a GitHub Codespace. Most samples require an Azure account and a deployment, and the Work IQ samples additionally require a Microsoft 365 tenant.

### Microsoft IQ

![Microsoft IQ section header](slide_images/slide_5.png)
[Watch from 04:40](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=280s)

### The Microsoft IQ platform

![Microsoft IQ platform diagram](slide_images/slide_6.png)
[Watch from 04:55](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=295s)

Microsoft IQ is a unified intelligence layer made of four members. Work IQ covers how your employees work — context on people, collaboration, and workflows. Fabric IQ covers how your business operates, exposing business entities and systems of record. Web IQ connects to real-time web intelligence: news, images, and video. Foundry IQ unlocks knowledge from policies, authoritative documents, and knowledge bases.

Session 1 deep-dived into Foundry IQ, this session covers Work IQ, and session 3 covers Fabric IQ.

### Work IQ

![Work IQ section header](slide_images/slide_7.png)
[Watch from 05:28](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=328s)

### Work IQ is an agent for work data

![Work IQ architecture diagram](slide_images/slide_8.png)
[Watch from 05:50](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=350s)

Work IQ supplies the human context that the other IQs miss. When a customer asks for a refund, the policy and the order record are one thing, but the Teams thread where the case was discussed and the Outlook escalation are another — that conversational history is what Work IQ brings in.

Architecturally it is a routing orchestrator over Microsoft 365, reachable over MCP, A2A, or REST, exposing two API families. The Agentic Context API retrieves context in one agentic, multi-step call rather than a sequence of hand-written data fetches. The Agentic Tool APIs take actions on the user's behalf.

### Why Work IQ

![Five benefits of Work IQ](slide_images/slide_9.png)
[Watch from 08:13](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=493s)

Work IQ is not plain retrieval. There is an intelligence layer behind it: a semantic index, memory, schema, and the people and org graph.

Speed comes from being built for agent consumption rather than human consumption, so a question resolves in fewer round-trips. Efficiency comes from packaging context and trimming tokens in the runtime. Scale means continuous, high-frequency, multi-step workloads are practical.

Security is the biggest one. Your data never leaves the Microsoft 365 tenant boundary. You do not export M365 data and index it somewhere else — retrieval happens in place.

### Work IQ vs Microsoft Graph

![Comparison table of Microsoft Graph and Work IQ](slide_images/slide_10.png)
[Watch from 10:01](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=601s)

Microsoft Graph is a set of data-access APIs over Microsoft 365. Work IQ is an intelligence layer on top of the same data, and the two are complementary rather than replacements.

Graph is built for apps and users and supports both app-only and delegated auth. Work IQ is built for agents and is delegated-only, so it always runs as a signed-in user.

Ask Graph for emails and you get raw emails matching a keyword, and you stitch them together yourself. Ask Work IQ and you get a grounded, summarized answer with references attached.

Graph has hundreds of typed endpoints and leaves paging and throttling to you. Work IQ exposes 10 generic tools over MCP and handles paging, throttling, and governance in place.

### The Work IQ API surface

![Work IQ API surface slide](slide_images/slide_11.png)
[Watch from 12:50](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=770s)

Four capability areas sit behind one intelligence layer. Chat lets you converse with people and other agents — `ask` routes to Microsoft 365 Copilot, and A2A lets other agents delegate to Work IQ. Context provides grounded org understanding across mail, meetings, documents, and chats. Tools provide governed retrieve-and-act over Microsoft 365 through generic verbs. Workspaces give agents a persistent place to hold state across long-running tasks.

All four are reachable through three protocols: A2A, MCP, and REST.

### Protocol strategy: when to use A2A, MCP, REST

![Protocol strategy slide](slide_images/slide_12.png)
[Watch from 13:52](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=832s)

Pick by scenario. A2A is agent-to-agent: use it for multi-agent orchestration when one agent delegates a whole work-context task to another. MCP is agent-to-tool: use it when your agent needs to ground itself and act through Work IQ, which is the right choice whenever `do_action` is involved. REST is human- or device-to-agent: use it when a mobile or web app queries Work IQ for a user.

### Retrieval with Work IQ

![Retrieval example slide](slide_images/slide_13.png)
[Watch from 15:24](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=924s)

Asking "what did my manager email me about this week?" does not return three email records. Work IQ resolves the source (Outlook) and the person (Priya Sharma), then returns a summary — three emails about the Q3 budget review, headcount numbers needed by Friday, team sync moved to Thursday 2pm — with numbered attributions linking back to each original message.

### Building with Work IQ

![Building with Work IQ section header](slide_images/slide_14.png)
[Watch from 16:23](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=983s)

### Work IQ retrieval with ask

![ask code snippet](slide_images/slide_15.png)
[Watch from 16:33](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=993s)

```python
from notebooks._shared import get_user_token, ask

token = get_user_token()

# `ask` is a Work IQ MCP tool over /mcp - no REST chat route.
resp = ask(token,
    "Summarize my 5 most recent emails - who sent "
    "each and what they need from me.")

print(resp["result"]["structuredContent"]["answer"])
```

Every protocol path starts the same way: acquire a delegated user token. Then call the tool you need.

`ask` is special because it routes the question to Microsoft 365 Copilot, so the response comes back as an LLM answer with summaries and references rather than a list of message records. Note that `ask` is an MCP tool over `/mcp` — there is no REST chat route for it.

Full source: `part1-workiq-api-concepts.ipynb`.

### The A2A agent card

![A2A agent card JSON](slide_images/slide_16.png)
[Watch from 19:52](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=1192s)

Discovery in A2A is standard: `GET {gateway}/a2a/.well-known/agent-card.json`. Work IQ publishes a normal agent card naming itself the "Work IQ Relay Agent", declaring protocol version 0.3.0, JSONRPC as preferred transport, streaming support, and an `ask_work_iq` skill with example prompts. Any A2A client that already knows how to read agent cards can discover and use Work IQ without special-casing it.

### Work IQ via the A2A protocol

![A2A code snippet](slide_images/slide_17.png)
[Watch from 20:34](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=1234s)

```python
# Work IQ publishes a standard A2A agent card + message/send.
rpc = {"jsonrpc": "2.0", "id": "1", "method": "message/send",
  "params": {"message": {"kind": "message", "role": "user",
   "parts": [{"kind": "text", "text": "My recent Teams chats?"}],
   "messageId": "m1"}}}

r = requests.post(f"{WORK_IQ_GATEWAY}/a2a/", json=rpc,
   headers={"Authorization": f"Bearer {token}",
    "Accept": "application/json, text/event-stream"})

# Reply streams over SSE as a `task` whose artifacts hold the text.
task = parse_sse_task(r.text)
```

A JSON-RPC `message/send` posts to the gateway's `/a2a/` endpoint. The reply streams back over server-sent events as a `task`, and the answer text lives in that task's artifacts.

The intelligence is identical to the MCP path: asking for recent Teams chats returns summarized descriptions of what each conversation is about, plus reference links, not raw message payloads.

Full source: `part2-workiq-a2a.ipynb`.

### Ten generic tools, progressive disclosure

![Ten generic tools slide](slide_images/slide_18.png)
[Watch from 22:40](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=1360s)

The 10 tools fall into four groups. Chat has `ask` and `list_agents`. Schema has `search_paths` and `get_schema`. Entity read has `fetch` and `call_function`. Entity write has `create`, `update`, `delete`, and `do_action`.

They are designed for progressive disclosure: `search_paths` discovers which Microsoft 365 resource paths are available, `get_schema` returns the OpenAPI shape of a path so you learn its structure before acting, and then `fetch` or `do_action` reads or writes. Filtering `search_paths` matters — without a filter the list of everything Work IQ can reach is very long.

`list_agents` returns the agents registered in your tenant. In the demo tenant that included the Planner agent, M365 Admin, Surveys, and Workmate.

### Work IQ via the MCP protocol

![MCP code snippet](slide_images/slide_19.png)
[Watch from 23:16](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=1396s)

```python
from notebooks._shared import get_user_token, call_mcp, call_tool

token = get_user_token()

# Work IQ speaks MCP (JSON-RPC 2.0) at {gateway}/mcp over SSE.
tools = call_mcp(token, "tools/list", {})
for t in tools["result"]["tools"]:
    print(t["name"], t["inputSchema"].get("required", []))

# fetch reads M365 entities by path via `entityUrls`.
msgs = call_tool(token, "fetch",
    {"entityUrls": ["/me/messages?$top=5&$select=subject,from"]})
```

Work IQ speaks MCP as JSON-RPC 2.0 at `{gateway}/mcp` over SSE. `tools/list` returns the 10 tools and their required inputs, and `fetch` reads entities by path via `entityUrls`, accepting normal Graph query parameters like `$top` and `$select`.

`ask`, `fetch`, and `do_action` are the three used most often. `fetch` is the right choice when you want a direct, deterministic read rather than an LLM-summarized answer. `call_function` goes further and calls Graph functions directly with filters like start and end time, with no LLM in the path at all — there is no wall between Work IQ and Microsoft Graph, so you can drop down to a fully custom Graph call when you need one.

Full source: `part3-workiq-mcp.ipynb`.

### The write path and its guardrails

![Write path guardrails slide](slide_images/slide_20.png)
[Watch from 25:08](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=1508s)

`do_action` is the write path, and it expects you to discover first: `search_paths` to find the path, then `get_schema` with `operationType` of `create` or `update` to learn the payload shape, then `do_action` to execute.

Allowed path prefixes are `/me/`, `/users/`, and `/sites/`. Blocked prefixes include `/authentication/` and `/servicePrincipals/`, so Work IQ cannot be used to change auth configuration or service principals. Everything runs under the signed-in user, and `jsonBody` is passed as a JSON-encoded string rather than an object.

### Taking action with do_action

![do_action code snippet](slide_images/slide_21.png)
[Watch from 25:58](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=1558s)

```python
# do_action is the ONLY write path (jsonBody = JSON string).
action_url = "/me/sendMail"
json_body = json.dumps({
    "Message": {
        "subject": "Re: your note",
        "body": {"contentType": "Text", "content": "<approved draft>"},
        "toRecipients": [
            {"emailAddress": {"address": "manager@contoso.com"}}],
    },
    "SaveToSentItems": True,
})
call_tool(token, "do_action",
    {"actionUrl": action_url, "jsonBody": json_body})
```

The shape of `jsonBody` follows whatever the target path expects — a message envelope for `/me/sendMail`, a calendar event structure for creating an invite. That is exactly what `get_schema` gives you before you write the call.

Full source: `part4-workiq-tools-actions.ipynb`.

### Foundry IQ + Work IQ

![Foundry IQ plus Work IQ section header](slide_images/slide_22.png)
[Watch from 30:37](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=1837s)

### One knowledge base, every source

![Knowledge base blending sources diagram](slide_images/slide_23.png)
[Watch from 31:07](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=1867s)

Foundry IQ knowledge bases combine knowledge sources from many places, and Work IQ is one of the available source types. A single knowledge base can hold HR policy documents, health plan coverage documents, and your live work context, then answer one query across all of them with the results ranked together.

That means you do not need to wire Work IQ separately into your agent's tool set — the knowledge base already handles questions that need work context.

### Work IQ as a knowledge source

![Work IQ knowledge source flow](slide_images/slide_24.png)
[Watch from 31:57](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=1917s)

Setup and query use different credentials. Registering `WorkIQKnowledgeSource` with the knowledge base is an admin operation using the Azure AI Search admin key via `AzureKeyCredential`.

At query time you pass a delegated `search.azure.com` token as the query authorization, so retrieval runs on behalf of the signed-in user and respects that user's access. A question like "our leave policy, and how much PTO do I have?" is answered from the indexed HR documents and the user's own work context, ranked together into one blended answer.

### Using Work IQ as a knowledge source in Python

![Knowledge source code snippet](slide_images/slide_25.png)
[Watch from 33:04](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=1984s)

```python
work_source = WorkIQKnowledgeSource(
    name="workiq-knowledge-source",
    description="Contoso Work IQ knowledge source",
)
index_client.create_or_update_knowledge_source(work_source)

kb = KnowledgeBase(
    name="multisource-workiq-knowledge-base",
    knowledge_sources=[
        KnowledgeSourceReference(name="hrdocs-knowledge-source"),
        KnowledgeSourceReference(name="healthdocs-knowledge-source"),
        KnowledgeSourceReference(name="workiq-knowledge-source"),
    ],
    output_mode=OutputMode.ANSWER_SYNTHESIS,
)
index_client.create_or_update_knowledge_base(kb)
```

Three knowledge sources — two Azure AI Search indexes and Work IQ — are referenced by one knowledge base with answer synthesis turned on.

In the demo, a query asking about recent Teams messages regarding a product, what colleagues were saying, what actions were requested, and which Contoso roles own inventory required all three sources at once. The Teams discussion about a Seattle stock outage came from Work IQ, while the inventory availability and job role details came from the search indexes, and the answer came back blended into readable prose instead of being split by source. The retrieval activity log shows exactly which sources were hit, including SharePoint documents and Teams messages pulled through Work IQ.

Full example: `notebooks/foundryiq-workiq.ipynb`.

### Agents + Work IQ

![Agents plus Work IQ section header](slide_images/slide_26.png)
[Watch from 36:08](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=2168s)

### What is an agent

![Agent loop diagram](slide_images/slide_27.png)
[Watch from 36:19](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=2179s)

An AI agent uses an LLM to run tools in a loop to achieve a goal. Given "when's my next deadline?", the agent first calls `get_current_datetime()` to establish today's date, then calls `work_iq.ask("what's due this week?")`, gets back that headcount numbers are due August 1st, and replies that only three days remain.

The second call is what makes this more than data retrieval — because `ask` routes to Microsoft 365 Copilot, the agent receives an already-reasoned answer about what is outstanding rather than a pile of calendar and mail records to interpret.

### Two ways to use Work IQ as an agent tool

![Two options slide](slide_images/slide_28.png)
[Watch from 37:30](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=2250s)

Option 1 points the agent directly at the Work IQ MCP endpoint. Everything is pre-built and agent-optimized, so there is less code to maintain, but you cannot customize retrieval parameters or reach the references and activity log.

Option 2 writes a custom tool that calls Work IQ via API. You get full control over parameters and the response shape, at the cost of portability across agents and less agentic optimization out of the box.

### Work IQ as a tool in Microsoft Agent Framework

![Agent Framework code snippet](slide_images/slide_29.png)
[Watch from 38:23](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=2303s)

```python
work_iq_tool = MCPStreamableHTTPTool(
    name="work-iq",
    url=work_iq_endpoint,
    http_client=work_iq_http_client,
    allowed_tools=["ask", "fetch", "get_schema", "do_action"],
    load_prompts=False)

agent = Agent(
    client=client,
    name="ContosoWorkmate",
    instructions="You are Contoso's workmate assistant.",
    tools=[get_current_date, work_iq_tool],
)
```

Wiring Work IQ into a Microsoft Agent Framework agent is one `MCPStreamableHTTPTool` in the `tools` list. `allowed_tools` narrows which of the 10 tools the agent can reach — some scenarios only need `ask`, others need `fetch` plus `do_action` because the agent has to write.

The same tool can go into a Foundry Toolbox instead of being attached to a single agent. A toolbox is a reusable bundle you define once and share across agents, and it can hold the Work IQ MCP endpoint alongside custom MCP servers, Fabric IQ, Web IQ, and anything else.

Full example: `src/workmate-agent-maf/main.py`.

### Agent 365 autopilots

![Agent 365 autopilots section header](slide_images/slide_30.png)
[Watch from 40:54](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=2454s)

### What is an Agent 365 autopilot

![Autopilot definition slide](slide_images/slide_31.png)
[Watch from 41:17](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=2477s)

An Agent 365 autopilot is a digital worker with its own Microsoft 365 identity: its own mailbox, calendar, and Teams presence, and a place in the org chart reporting to a manager. This is different from publishing an agent to Teams as an app.

It is registered once as an agent blueprint in Foundry and governed like any other identity. You @mention it in Teams like a coworker and it works in the background. The hosted agent you already built is what runs behind the activity endpoint, and it reasons over real work context via Work IQ.

Work IQ is close to mandatory here: an autopilot lives inside your tenant, so it needs tenant context — chats, SharePoint, mail — to be useful at all.

### How the autopilot is wired

![Autopilot wiring diagram](slide_images/slide_32.png)
[Watch from 43:44](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=2624s)

A Teams message in a thread goes inbound to Azure Bot Service, which routes to the Foundry activity endpoint, which reaches your container speaking activity protocol v1. Inside the container the Responses API reasons and grounds via the Work IQ MCP, and the grounded reply flows back into the same Teams thread. One container, one identity, one governed surface.

### Hosting the autopilot: the activity host

![Activity host diagram](slide_images/slide_33.png)
[Watch from 44:20](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=2660s)

The container's `main.py` entrypoint runs a Bot Framework activity host built from `CloudAdapter`, `MsalConnectionManager`, and `Authorization`, wrapping a `FoundryDigitalWorkerAgent` that does the reasoning, grounding, and acting.

Compared to a normal hosted agent, the tool wiring is unchanged. The one thing that differs is the authentication layer: the token is the agent's own token, not yours.

### The autopilot acts as itself, not as you

![Playground versus Teams comparison](slide_images/slide_34.png)
[Watch from 45:36](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=2736s)

In the Foundry playground you are the signed-in user, so the agent runs on-behalf-of you — your mailbox, your permissions, your identity. The same agent reached through Teams as an autopilot acts as its own identity, with its own mailbox and address, and consent granted to its service identity.

That difference is most visible with `do_action`: an email sent from Teams comes from the autopilot's mailbox, not yours. The mental model is "digital coworker", not "an assistant signed in as me".

### Making a hosted agent an autopilot

![Five-step pipeline slide](slide_images/slide_35.png)
[Watch from 47:15](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=2835s)

Five steps, scripted in `publish-autopilot.ps1`. Deploy the hosted agent with `azd deploy` against the Responses API. Build the container image with `az acr build` using activity protocol v1. Pin that image as a new agent version through the Foundry versions API. Create an Azure Bot with an `activityprotocol` endpoint. Then submit for publishing, which a Microsoft 365 global admin approves.

The last step is the one that needs someone else if you are not a global admin yourself. A one-click Teams publish makes an assistant app; this pipeline makes an autopilot that is a new identity in the tenant.

### Publish and get approved

![Governed lifecycle diagram](slide_images/slide_36.png)
[Watch from 49:06](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=2946s)

Register the agent blueprint and the Azure Bot for the activity endpoint. Grant the service identity its Work IQ and Agent 365 MCP scopes — this is where you define what the new identity is allowed to reach. Submit to the Microsoft 365 admin center for approval. Once approved, the autopilot shows up in Teams. From then on it is fully auditable and revocable, like any other worker.

### Demo: the Work Mate autopilot

![Work Mate autopilot demo slide](slide_images/slide_37.png)
[Watch from 50:13](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=3013s)

Workmate appears in Teams with its own contact card, its own email address, and a spot in the org chart reporting to its owner — not in the apps list.

Asked about pending tasks in its mailbox, Workmate reads its own mailbox and reports a refund request from Maria Garcia. Checking Outlook confirms the message exists in Workmate's mailbox and not in the presenter's. Given `do_action` and the instruction to issue the refund and let the customer know, Workmate replies to Maria Garcia directly, with the presenter not on the thread at all.

Access follows the same rules as a human coworker: an autopilot can only read a Word document or presentation that has been shared with it.

One blueprint can back many instances. The blueprint carries the Entra agent ID and is unified across instances, but each person creates their own Workmate instance with its own email address and mailbox, all running the same source code. Each instance needs a license assigned like any user — an E5 or equivalent to appear in Teams and the org chart, plus whatever else it needs, such as Power Automate or Microsoft 365 Copilot.

Full source: `src/workmate-autopilot/`.

### Next steps and resources

![Next steps slide](slide_images/slide_38.png)
[Watch from 56:43](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=3403s)

- Join office hours right after each session in Discord: [aka.ms/pythonai/oh](https://aka.ms/pythonai/oh)
- Register for the series: [aka.ms/IQDeepDivePython/series](https://aka.ms/IQDeepDivePython/series)
- All resources — slides, recordings, and write-ups: [aka.ms/iqdeepdive/resources](https://aka.ms/iqdeepdive/resources)

Session 1 covered Foundry IQ and session 3 covers Fabric IQ.

### Microsoft IQ Live

![Microsoft IQ Live slide](slide_images/slide_39.png)
[Watch from 57:29](https://www.youtube.com/watch?v=xI3wMCC0oBY&t=3449s)

The IQ content continues past this week. Microsoft IQ Live runs bi-weekly episodes on Microsoft Reactor from Aug 6 to Nov 12, 2026, stopping just before Ignite. Register at [aka.ms/MicrosoftIQLive](https://aka.ms/MicrosoftIQLive) and follow Microsoft Reactor on YouTube to catch every stream.

## Live Chat Q&A

### Is Work IQ generally available yet?

Yes, Work IQ has been GA since June 2026. It is an AI technology, so it is still evolving quickly.

### How isolated is our tenant data? Can tenant B access tenant A's data?

Data is tenant bounded. Permission inheritance, DLP, and regulatory compliance all apply, and Work IQ answers using each user's own context, memory, and preferences.

### Does Work IQ work the same way as Microsoft Graph semantic search (Graph Retrieval / the Copilot data endpoint)?

It is more than Graph semantic search. Graph semantic search returns matching content; Work IQ adds an intelligence layer that reasons over that content and returns grounded answers with references, plus the tool APIs for taking action.

### Do all three protocols let you set parameters and options on the request?

Yes. Each protocol has its own syntax, but you can supply options and parameters in all of them.

### Can Work IQ fetch emails from all users, or only the signed-in user?

Only what the signed-in user is allowed to see. There is no app-only mode, so a company-wide agent cannot read everyone's mailbox through Work IQ.

### Does Work IQ reach Microsoft To Do and Planner tasks?

Planner should be reachable through Work IQ. Coverage is continuously expanding.

### What is Work IQ for — why not just use Graph?

Work IQ is designed so that any agent, including third-party agents, can consume an organization's knowledge and intelligence without you hand-building the retrieval logic.

### What identity does Work IQ use? Is it on-behalf-of?

Work IQ works with the identity of the current user via a delegated access token. Agent 365 autopilots are the exception in effect, since their delegated identity is the autopilot's own Microsoft 365 identity rather than yours.

### Would we write code against these tools directly, or does the agent discover them through MCP?

Most of the time the agent discovers the available tools over MCP and decides which to call. That is why Work IQ ships so many discovery and schema tools. Calling them directly in a notebook is how you learn what is there.

### Work IQ hides which underlying source produced an answer — how do you debug a wrong answer?

It depends on what you build the agent with. Declarative agents have a debug mode for inspecting MCP tool calls, and Foundry IQ knowledge bases expose a retrieval activity log showing which sources were queried.

### Does Work IQ reach everything the user can reach — OneDrive, mail and attachments, SharePoint sites, Teams channels and messages?

Generally, yes.

### Work IQ is described as retrieval — can it take actions like sending mail or creating a meeting?

Yes. `do_action` is the write path and covers actions such as `/me/sendMail` and creating calendar events, under the allowed path prefixes `/me/`, `/users/`, and `/sites/`.

### Are there security checks on an agent before it is published?

Publishing an autopilot requires Microsoft 365 admin approval, the service identity only gets the scopes you explicitly grant it, and the resulting identity is fully auditable and revocable.

### How does autopilot licensing work?

Each autopilot instance is licensed like a user. To show up in Teams and the org chart it needs an E5 or equivalent license, and any additional capability it uses — Power Automate, Microsoft 365 Copilot — requires the matching license too. Since every person creates their own instance from the shared blueprint, each instance needs its own licenses.
