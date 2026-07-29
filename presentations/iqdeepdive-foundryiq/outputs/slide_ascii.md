## Slide 1

![Slide 1](slide_images/slide_1.png)

```
Microsoft IQ Deep Dive
with Python
July 28: Foundry IQ
July 29: Work IQ
                               Stay
July 30: Fabric IQ         GROUNDED
Register at aka.ms/IQDeepDivePython/series
```

## Slide 2

![Slide 2](slide_images/slide_2.png)

```
Microsoft IQ Deep Dive:
Foundry IQ
aka.ms/iqdeepdive/slides/foundryiq


               Pamela Fox
               Principal Cloud Advocate
               Microsoft / GitHub
               www.pamelafox.org
```

## Slide 3

![Slide 3](slide_images/slide_3.png)

```
Today we'll cover...
• Foundry IQ knowledge bases
• Data ingestion process
• Web IQ for web retrieval
• Foundry IQ inside agents
• Foundry IQ in Foundry Toolbox
• Deploying agents with Foundry IQ
```

## Slide 4

![Slide 4](slide_images/slide_4.png)

```
Want the code?
1. Open this GitHub repository:
https://aka.ms/iqdeepdive
2. Use "Code" button to create a GitHub Codespace:




3. Wait a few minutes for Codespace to start up
    All code samples require deployment and an Azure account.
```

## Slide 5

![Slide 5](slide_images/slide_5.png)

```
Microsoft IQ
```

## Slide 6

![Slide 6](slide_images/slide_6.png)

```
Microsoft IQ Platform
                               Unified intelligence for enterprise AI




      Work IQ                    Fabric IQ                 Web IQ                  Foundry IQ
      How your                      How your             How you connect            How your agents
    employees work              business operates       to web intelligence         unlock knowledge



     Context on people,         Context on business     Context from the web,       Context on policies,
collaboration, and workflows    entities, systems of   news, images and video   authoritative documents, and
                                record, and actions                                  knowledge bases



    Deep dive:                 Deep dive:                            Covering today:
    Session 2                  Session 3                                Session 1
```

## Slide 7

![Slide 7](slide_images/slide_7.png)

```
Foundry IQ
```

## Slide 8

![Slide 8](slide_images/slide_8.png)

```
Knowledge is everywhere
            PDF files                                Email threads


 Relational tables                                       Teams chats


    Analytics data
                                 ?                     Calendar events

            Web article                              Meeting notes

                          SharePoint documents

                                        …But how does an agent get to it?
```

## Slide 9

![Slide 9](slide_images/slide_9.png)

```
Foundry IQ makes knowledge agent-ready
            PDF files                            Email threads
                              Foundry IQ
                           (Azure AI Search)
 Relational tables              Route                Teams chats
                               Retrieve
    Analytics data              Merge              Calendar events
                              Synthesize

            Web article                          Meeting notes

                          SharePoint documents
```

## Slide 10

![Slide 10](slide_images/slide_10.png)

```
Inside a Foundry IQ knowledge base

                                            Knowledge sources    Output

   Input                                    Search Index         Merged
                                                                 results
Conversation
                           Search query 1   MCP         NEW
                                                                Activity log
               Retrieval
  Steering                 Search query 2   Work IQ     NEW
instructions
               planning

                                                                  Answer
                                            Fabric IQ   NEW
                                                                 synthesis

 One question. Every source. One answer.
```

## Slide 11

![Slide 11](slide_images/slide_11.png)

```
Indexed knowledge
```

## Slide 12

![Slide 12](slide_images/slide_12.png)

```
Data ingestion for unstructured data

For unstructured documents, we need a data ingestion flow:

 Document        Extraction        Chunking          Embedding                Index

 PDF, HTML,      Text, tables,    Text split into     Each chunk    Each chunk becomes a
                  and figures     chunks based      embedded with      row in the index.
   DOCX,
                extracted from     on sentence         a vector
  PPT, XLSX,      binary file    boundaries and       embedding      field        type
 MD, TXT,…                         chunk sizes.         model.
                                                                     id           str
                                                                     parent_id    str
                                                                     path         str
                                                                     chunk        str
                                                                     vector       float[]
```

## Slide 13

![Slide 13](slide_images/slide_13.png)

```
Two ways to add indexed knowledge
Choose based on how much control you need over ingestion:

         File Knowledge Source                     Indexed Knowledge Source

 You bring: Files                        You bring: A data source (Blob, DB, …)

  Automatic ingestion pipeline:          Your custom configured ingestion pipeline:
  Extract → Chunk → Embed → Index        Data source → Indexer → Skillset → Index
     Zero ingestion code                    Full schema and pipeline control
     Just upload the files and go           Custom enrichments and skillsets
     Fixed index schema                     Works with existing data sources
     Less flexibility                       More custom code to maintain
  Best for: quick start, prototyping,    Best for: production data, custom schemas,
  small documents                        domain-specific customizations
```

## Slide 14

![Slide 14](slide_images/slide_14.png)

```
Indexed Knowledge Ingestion
   Data sources

    Azure Blob                  Indexer                     Skillset          Search Index

      ADLSv2                    Runs on a                   Built-in skills
                              schedule.
    Azure Table
                            Change tracking to              Content
                           detect additions,              Understanding
    Cosmos DB             deletions, updates.

     Azure SQL                                               Split Skill

     OneLake                                              Embedding Skill

    SharePoint                                           …and many more!


https://learn.microsoft.com/azure/search/search-indexer-overview
```

## Slide 15

![Slide 15](slide_images/slide_15.png)

```
Hybrid retrieval on indexed knowledge
A complete search stack gives the best results. Hybrid > pure vector or keyword!

                           Keyword
                           results

                      Drinking Water
Question          1
                      Safe Hose
”Best supplies                                          Fusion                      Reranking
                  2   Garden Soil Enriched              (RRF)
for watering my
garden?”
                                                   Drinking Water
                                               1                           1   Soaker Hose 25-foot
                                                   Safe Hose
                           Vector
                           results             2   Self-Watering Planter   2   Misting Sprinkler Kit

                                                                               Drinking Water
                  1   Misting Sprinkler Kit    3   Garden Hose 50-Foot     3
                                                                               Safe Hose

                  2   Soaker Hose 25-foot      4   Misting Sprinkler Kit   4   Garden Hose 50-Foot
```

## Slide 16

![Slide 16](slide_images/slide_16.png)

```
Knowledge bases
```

## Slide 17

![Slide 17](slide_images/slide_17.png)

```
Knowledge base retrieval reasoning effort



   MINIMAL                   LOW              MEDIUM




 Low latency                                  Highest quality
 Less model usage                           Increased stages
 Lowest cost                                   More agentic
```

## Slide 18

![Slide 18](slide_images/slide_18.png)

```
Knowledge base with minimal effort
Minimal effort does not use any LLM, but still uses re-ranker model for merging.

                                                         Knowledge sources

                                 Input                    Search Index               Output

                           Search intent 1                MCP         NEW           Merged
                                                                                    results

                           Search intent 2                Work IQ     NEW
                                                                                   Activity log


                                                          Fabric IQ   NEW


                                                        All intents are sent
                                                        to all sources
```

## Slide 19

![Slide 19](slide_images/slide_19.png)

```
Example of minimal effort
Input    "what's best Zava paint for bathroom walls?"                       * You may optionally pass in multiple intents.


                          Activity log                               Merged results

                                                              .pdf
           Step                        Details
                                                              Interior Semi-Gloss Paint, price


Output
           Search ""what's best Zava                          $47.0\r\n\r\n ##
                                       Source: Search index   Brand\r\nZavaTech Hardware...
           paint for bathroom
                                       Results: 8
           walls?"
                                                                 Re-ranker score: 2.95
           Search ""what's best Zava
                                       Source: SharePoint
           paint for bathroom
                                       Results: 2
           walls?"                                            ZavaBathroomPost.pdf
                                                              Refresh Your Bathroom with
                                                              Confidence: Why Semi-Gloss
               Intent is sent to all sources.                 Paint Makes All the Difference
                                                              When it comes to painting
                                                              projects, bathrooms are...

                                                                 Re-ranker score: 3.07
```

## Slide 20

![Slide 20](slide_images/slide_20.png)

```
Knowledge base with low effort
  Low effort uses an LLM for retrieval planning and optional answer synthesis.
                                                                     Knowledge sources    Output

   Input                                                              Search Index        Merged
                                                                                          results
Conversation
                                   Search query 1                     MCP
                                                                                         Activity log
                 Retrieval
  Steering                         Search query 2                     Work IQ
instructions
                 planning

                                                                                          Answer
                                                                      Fabric IQ          synthesis
                  Retrieval
                Instructions


               Retrieval planning generates queries and selects sources.
```

## Slide 21

![Slide 21](slide_images/slide_21.png)

```
Example of low effort with knowledge source selection
Input    What Zava paint can I use to paint my bathroom and how much does it cost?


                         Activity log                                 Merged results                       Answer synthesis

           Step                          Details                PFIP000003.pdf                     A semi-gloss interior paint is
                                                                                                   suitable for use in a bathroom
                                                                Interior Semi-Gloss Paint, price
                                                                                                   because it offers moisture

Output
                                         Input tokens: 2113     $47.0\r\n\r\n ##
           Query planning                                                                          resistance, is washable, and stands
                                         Output tokens: 75      Brand\r\nZavaTech Hardware...
                                                                                                   up well to humidity and frequent
           Search "Zava paint suitable   Source: Search index      Re-ranker score: 3.03           cleaning. This type of paint is
           for bathroom use"             Results: 6                                                specifically recommended for
                                                                                                   bathrooms, kitchens, and trim work
                                         Source: Search index   PFIP0000005.pdf                    due to its durability and ease of
           Search "Zava paint prices"                                                              maintenance [ref_id:1]. The typical
                                         Results: 14
                                                                One-Coat Interior Paint, price     cost for a can of Interior Semi-Gloss
                                         Reasoning: 20K         $50.00r\n\r\n ##                   Paint from ZavaTech Hardware
           Agentic reasoning                                                                       Solutions is $47.00 [ref_id:2].
                                         Effort: Low            Brand\r\nZavaTech Hardware

                                         Input tokens: 7921        Re-ranker score: 2.95           Answer synthesis is optional.
           Model answer synthesis
                                         Output tokens: 108
```

## Slide 22

![Slide 22](slide_images/slide_22.png)

```
Knowledge base with medium effort
  Medium effort adds a second retrieval, only when it still needs more context to answer the query.

                                                                          Knowledge sources            Output

   Input                                                                   Search Index                Merged
                                                                                                       results
Conversation
                                        Search query 1                     MCP
                                                                                                      Activity log
                      Retrieval
  Steering                              Search query 2                     Work IQ
instructions
                      planning

                                                                                                       Answer
                                                                           Fabric IQ                  synthesis


                                         Iterative retrieval

               Medium effort adds a second retrieval, only when it still needs more context to answer the query.
```

## Slide 23

![Slide 23](slide_images/slide_23.png)

```
Example of medium effort
Input
         Explain how to paint my house most efficiently. Then give me a list of the Zava products and prices for each supply



                              Activity log                                      Merged results                                Answer synthesis
          Step                                   Details               PFEP000007.pdf                                The most efficient way to paint a house
                                                 Input tokens: 1484    Exterior Acrylic Paint, price                 is to work from the top down: start by
          Query planning                                                                                             prepping all surfaces, then paint
                                                 Output tokens: 115    $57.0\r\n\r\n## Brand\r\nZavaTech...



Output
                                                                                                                     ceilings first, followed by trim and
          Search "efficient house painting"      Source: manuals          Re-ranker score: 2.85
                                                                                                                     baseboards, and finish with the walls,
          Search "Zava paint supplies prices"    Source: manuals                                                     using rollers for large areas and
                                                                       francoisestmoi.com
          Search "efficient house painting"      Source: web                                                         brushes or pads for detail work to
                                                                       Url: http://francoisetmoi.com/diy/top-5-      minimize drips and touch-ups
          Search "Zava paint prices"             Source: web           ways-to-paint-more-efficiently
                                                                                                                     [ref_id:5][ref_id:3][ref_id:4]. For exterior
                                                 Input tokens: 1169    Title: Top 5 Ways to Paint More Efficiently   painting, clean and repair surfaces,
          Query planning
                                                 Output tokens: 249                                                  prime exposed areas, and always paint
          Search "paint brushes rollers trays"   Source: manuals       qualitypreferred.com
                                                                                                                     from high to low, finishing with doors
                                                                                                                     and trim [ref_id:5][ref_id:6].
          Search "paint brushes rollers trays"   Source: web           Url:
                                                                       https://www.qualitypreferred.com/choosi
                                                 Reasoning: 65K        ng-the-right-method-the-best-way-to-          Below is a list of Zava paint supplies:
          Agentic reasoning
                                                 Effort: Medium        paint-a-house                                 * Exterior Acrylic Paint: $57.0
                                                 Input tokens: 12676                                                 [ref_id:1]
          Model answer synthesis                                       Title: The Best Way to Paint a House
                                                 Output tokens: 196
```

## Slide 24

![Slide 24](slide_images/slide_24.png)

```
Foundry IQ multi-source knowledge base
Create a knowledge base with multiple knowledge sources:
knowledge_base = KnowledgeBase(
  name="multisource-search-knowledge-base",
  description="Multi-source knowledge base over HR and health document indexes",
  models=[KnowledgeBaseAzureOpenAIModel(azure_open_ai_parameters=aoai_params)],
  knowledge_sources=[KnowledgeSourceReference(name="hrdocs-knowledge-source"),
                       KnowledgeSourceReference(name="healthdocs-knowledge-source")],
  retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort(),
  output_mode=KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS
Create
)
       a knowledge base that includes the Web IQ MCP knowledge source:
index_client.create_or_update_knowledge_base(knowledge_base)

Query the knowledge base with user query:
retrieval_request = KnowledgeBaseRetrievalRequest(
  messages=[KnowledgeBaseMessage(role="user",
            content=[KnowledgeBaseMessageTextContent(text="How many vacation weeks do we get?")])],
  include_activity=True)

result = knowledge_base_client.retrieve(retrieval_request=retrieval_request)

  Full example: notebooks/foundryiq-basic.ipynb
```

## Slide 25

![Slide 25](slide_images/slide_25.png)

```
Web IQ
```

## Slide 26

![Slide 26](slide_images/slide_26.png)

```
Microsoft Web IQ
A web search service designed specifically for agents:

 Web Search            News         Finance     Video          Sports        Browse



               Very low latency                             Full payload

~164ms P95                                    Results includes full Markdown, HTML, or
2.5x faster than today’s best alternative     summaries, all in one response.


https://webiq.microsoft.ai/
```

## Slide 27

![Slide 27](slide_images/slide_27.png)

```
Retrieval with Microsoft Web IQ MCP server
Question                               Web IQ MCP               Result
                                                                            Mental Health Technology Sector
What are industry                      Tool:     web            Title:
                                                                            Overview
benchmarks for mental health
benefits at tech companies?                                                 https://multiples.vc/coverage/m
                                                                URL:
                                                                            ental-health-technology
                                                                            Mental health technology delivers
                                                                Content:    psychiatric care, therapy, crisis
                                                                            intervention, and wellness tools
                                                                            through telehealth platforms,
                                                                            measurement-based care systems,
                                                                            practice management software...
Web IQ requires private preview access
                                                                Crawled:    2026-05-10T20:07:00Z
Web IQ is currently available to allow-listed customers only.
You need a WEB_IQ_KEY to use the MCP server.
                                                                Language:   en
https://webiq.microsoft.ai/documentation/mcp/
```

## Slide 28

![Slide 28](slide_images/slide_28.png)

```
Foundry IQ + Web IQ knowledge source
Create an MCP knowledge source for WebIQ MCP server:
web_knowledge_source = McpServerKnowledgeSource(
  name="web-knowledge-source", description="Web IQ (live web search)",
  mcp_server_parameters=McpServerKnowledgeSourceParameters(
    server_url="https://api.microsoft.ai/v3/mcp",
    authentication=McpServerStoredHeadersAuthentication(
      stored_headers_parameters=McpServerStoredHeadersParameters({"headers": {"x-apikey": WEB_IQ_KEY}})),
  tools=[McpServerTool(name="web", output_parsing=McpServerAutoOutputParsing())]))

Create a knowledge base that includes the Web IQ MCP knowledge source:
knowledge_base = KnowledgeBase(
  name="multisource-web-knowledge-base",
  description="Multi-source knowledge base combining indexed company documents and live web results" ,
  models=[KnowledgeBaseAzureOpenAIModel(azure_open_ai_parameters=aoai_params)],
  knowledge_sources=[KnowledgeSourceReference(name="web-knowledge-source"),
                     KnowledgeSourceReference(name="hrdocs-knowledge-source")])

Query the knowledge base with user query:
result = knowledge_base_client.retrieve(KnowledgeBaseRetrievalRequest(
     messages=[KnowledgeBaseMessage(role="user", content=[KnowledgeBaseMessageTextContent(text=question)])])

  Full example: notebooks/foundryiq-webiq.ipynb
```

## Slide 29

![Slide 29](slide_images/slide_29.png)

```
Foundry IQ inside Agents
```

## Slide 30

![Slide 30](slide_images/slide_30.png)

```
What is an agent?
                           An AI agent uses an LLM to run tools in a
           Agent           loop to achieve a goal.

   Input
                                  You're an internal HR helper assistant.

                                 How long til benefits sign-up closes?

                           LLM   get_current_datetime()
   LLM
                                 Tues, July 28, 2026, 10:15 AM
                   Tools
                           LLM    search_kb(“benefits deadline”)

                                  Enrollments deadline in August 1st…
   Goal
                           LLM    You have only 3 days to sign up!
```

## Slide 31

![Slide 31](slide_images/slide_31.png)

```
Using Foundry IQ as a tool for AI agents
                           Option 1:
           Agent           Write a custom tool that calls the KB via API
   Input                      Full control over parameters and response
                              Less portability across agents

                           Option 2:
                           Point agent directly at the KB MCP endpoint
                              Less code to maintain
   LLM                        Can’t customize retrieval parameters
                   Tools      Can’t access references and activity log

                           Option 3:
                           Point agent at Foundry Toolbox with KB MCP
   Goal                       Easier to add on more tools
                              Managed authorization flow for auth’d sources
                              Same drawbacks as MCP server
```

## Slide 32

![Slide 32](slide_images/slide_32.png)

```
Which retrieval effort to use with agents?
The deployed agents in this repository use a minimal knowledge base,
then let the Python agent itself handle query rewriting and iteration.



   MINIMAL                                  LOW                            MEDIUM




 Low latency                                                               Highest quality
 Less model usage                                                        Increased stages
 Lowest cost                                                                More agentic
```

## Slide 33

![Slide 33](slide_images/slide_33.png)

```
Using Foundry IQ as a tool: Custom code
Define a tool that uses KB SDK:
@tool
async def retrieve_company_knowledge(queries: list[str]) -> dict[str, Any]:
  """Retrieve grounded company and HR information from the Foundry IQ knowledge base."""
  request = KnowledgeBaseRetrievalRequest(
    intents=[KnowledgeRetrievalSemanticIntent(search=query) for query in queries],
    include_activity=True)
  result = await knowledge_base_client.retrieve(request)
  return {"response": serialize_models(result.response),
          "references": serialize_models(result.references),
          "activity": serialize_models(result.activity)}

Create an agent with the tool:
agent = Agent(client=client, name="InternalHRApiHelper",
  instructions="You are an internal HR helper.",
  tools=[retrieve_company_knowledge])


  Full example: src/agent-foundryiq-api/main.py
```

## Slide 34

![Slide 34](slide_images/slide_34.png)

```
Using Foundry IQ as a tool                                                  DEMO

                                                 Run local agent:
                                                 azd ai agent run agent-foundryiq-api



                                                 Ask question with playground or CLI:
                                                 azd ai agent invoke agent-foundryiq-api
                                                 --local "What benefits are available,
                                                 and when do I need to enroll?"




 Full example: src/agent-foundryiq-api/main.py
```

## Slide 35

![Slide 35](slide_images/slide_35.png)

```
Using Foundry IQ as a tool: MCP server
  The MCP endpoint returns merged results with citations (but no activity log or separate references).

                                                                  Azure AI Search Knowledge Base

                                                                    Knowledge sources
                                                                                              Merged results
                     Search
                     queries                                          Search index           uid   snippet
                                                                                             123   Benefits include ...

                     Query 1
Input                                     MCP                             MCP                456   We offer three ...

        Agent
                                knowledge_base_retrieve                                      789   Each employee ...

                     Query 2                                            Fabric IQ            101   On the first of ...


                                                                                             131   We send weekly ...


                                                                         Work IQ             145   Available jobs ...
```

## Slide 36

![Slide 36](slide_images/slide_36.png)

```
Using Foundry IQ as a tool: MCP server
knowledge_base_endpoint = (f"{SEARCH_ENDPOINT}/knowledgebases/{KNOWLEDGE_BASE_NAME}
                            /mcp?api-version=2026-05-01-preview")

knowledge_base_http_client = httpx.AsyncClient(
  auth=AzureTokenCredentialAuth(credential, SEARCH_SCOPE))

knowledge_base_mcp_tool = MCPStreamableHTTPTool(
  name="knowledge-base",
  url=knowledge_base_endpoint,
  http_client=knowledge_base_http_client,
  allowed_tools=["knowledge_base_retrieve"],
  load_prompts=False)

agent = Agent(
  client=client,
  name="InternalHRHelper",
  instructions="You are an internal HR helper.",
  tools=[knowledge_base_mcp_tool])

  Full example: src/agent-foundryiq-mcp/main.py
```

## Slide 37

![Slide 37](slide_images/slide_37.png)

```
Using Foundry IQ as an MCP server                                           DEMO

                                                 Run local agent:
                                                 azd ai agent run agent-foundryiq-mcp



                                                 Ask question with playground or CLI:
                                                 azd ai agent invoke agent-foundryiq-mcp
                                                 --local "What benefits are available,
                                                 and when do I need to enroll?"




 Full example: src/agent-foundryiq-mcp/main.py
```

## Slide 38

![Slide 38](slide_images/slide_38.png)

```
Foundry Toolbox
Create a toolbox on Foundry composed of Foundry Tools and MCP servers, for use by any agent.

                                                           Foundry Toolbox
Input                MCP
          Agent                           Any tool from                          Any MCP server
                                       Foundry Tool Catalog                     (auth via OAuth or
                                                                            Foundry Project connection)


                                                              Example toolbox:

                                                           Foundry Toolbox
Input                MCP                                                                 Foundry IQ MCP
         Agent                        Web search              Code interpreter

                                   Powered by Bing     Sandboxed Python execution         Multi-source
                                                                                         agentic retrieval
```

## Slide 39

![Slide 39](slide_images/slide_39.png)

```
Creating a Foundry Toolbox from code
tools = [
  WebSearchToolboxTool(name="web_search", description="Search the web for current information."),
  CodeInterpreterToolboxTool(name="code_interpreter", description="Run Python in a sandbox."),
  MCPToolboxTool(server_label="knowledge-base",
   server_url=knowledge_base_mcp_url,
   server_description="Retrieve grounded company and HR information.",
   project_connection_id=search_connection_name,
   allowed_tools=["knowledge_base_retrieve"],
   require_approval="never")]

project = AIProjectClient(endpoint=endpoint, credential=credential)

version = project.toolboxes.create_version(
  name=toolbox_name, tools=tools, description=toolbox_description)

project.toolboxes.update(name=toolbox_name, default_version=version.version)

  Full code: infra/create-toolbox-foundryiq.py

  Toolbox <> KB connection made in: infra/core/ai/ai-project.bicep
```

## Slide 40

![Slide 40](slide_images/slide_40.png)

```
Using Foundry Toolbox inside agent
Microsoft Agent Framework has built-in support for the Foundry Toolbox MCP server:
toolbox = FoundryToolbox(
  url=f"{PROJECT_ENDPOINT}/toolboxes/{TOOLBOX_NAME}/mcp?api-version=v1",
  credential=credential,
  load_prompts=False)

agent = Agent(
  client=client,
  name="InternalHRToolboxHelper",
  instructions="""You are an internal HR helper focused on employee benefits and company info.
  Use the knowledge base tool to answer company questions and ground answers in provided context.
  Use web search only when the knowledge base does not contain the needed current information.
  Use code interpreter when calculations or structured data analysis would improve the answer.""",
  tools=[toolbox])

   Full example: src/agent-toolbox-foundryiq/main.py
```

## Slide 41

![Slide 41](slide_images/slide_41.png)

```
Using Foundry IQ inside Toolbox                                                    DEMO

                                                      Run local agent:
                                                      azd ai agent run agent-toolbox-foundryiq



                                                      Ask question with playground or CLI:
                                                      azd ai agent invoke agent-toolbox-foundryiq
                                                      --local "What benefits are available, and
                                                      when do I need to enroll?"




  Full example: src/agent-toolbox-foundryiq/main.py
```

## Slide 42

![Slide 42](slide_images/slide_42.png)

```
Agent deployment
```

## Slide 43

![Slide 43](slide_images/slide_43.png)

```
Foundry Agent Service
Host your agents with production-grade security, reliability, and governance.


                        Prompt Agents                                                          Hosted Agents
                    Define instructions and tools                                        Use your favorite agent framework



        Foundry Tools                  Foundry IQ                 Foundry Memory                              Foundry Models
                                                                   Managed Memory
                                                                 Managed Conversations
                                                                  BYO-Memory Store




            Foundry Control Plane               Controls        Observability       Security                 Fleet-wide Operations


                                                    Microsoft           Microsoft                Microsoft                      Microsoft
                                                    Agent 365           Defender                 Entra                          Purview
```

## Slide 44

![Slide 44](slide_images/slide_44.png)

```
Foundry Hosted Agents
Serve any agent using the Responses API or more generic invocations API.

 Foundry Agent Service
 Identity · Endpoint · State Scaling · Observability


     Azure Container Apps Sandbox


           Responses API Adapter                /agents/{name}/endpoint/protocols/openai/responses


                       Your code
```

## Slide 45

![Slide 45](slide_images/slide_45.png)

```
Foundry Hosted Agents with MAF
Microsoft Agent Framework provides a built-in Adapter – just wrap your agent and run.
from agent_framework import Agent
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


    Full example: src/agent-toolbox-foundryiq/main.py
```

## Slide 46

![Slide 46](slide_images/slide_46.png)

```
Using hosted agent on Foundry                                                      DEMO

                                                      Deploy agent
                                                      azd deploy agent-toolbox-foundryiq



                                                      Ask question with playground or CLI:
                                                      azd ai agent invoke agent-toolbox-foundryiq
                                                      "What benefits are available, and when do I
                                                      need to enroll?"




  Full example: src/agent-toolbox-foundryiq/main.py
```

## Slide 47

![Slide 47](slide_images/slide_47.png)

```
Use hosted agent in Teams                                                          DEMO

Every hosted agent includes the option to publish to Teams.
1️⃣ Publish from                               3️⃣ Chat with the agent in Teams:
Foundry UI:




2️⃣ Azure Bot
service is
auto-created:
```

## Slide 48

![Slide 48](slide_images/slide_48.png)

```
Next steps
Join office hours after in Discord:
aka.ms/pythonai/oh

Grab all session resources:
aka.ms/iqdeepdive/resources

July 28: Foundry IQ
July 29: Work IQ                         Stay
July 30: Fabric IQ                    GROUNDED
Register at aka.ms/IQDeepDivePython/series
```

## Slide 49

![Slide 49](slide_images/slide_49.png)

```
JOIN US LIVE




Bi-weekly episodes on Microsoft Reactor, from Aug 6 to Nov 12, 2026.


     Register → aka.ms/MicrosoftIQLive




Follow Microsoft Reactor on YouTube to catch every stream.
```
