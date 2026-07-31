# Microsoft IQ Deep Dive with Python: Fabric IQ

📺 [Watch the full recording on YouTube](https://www.youtube.com/watch?v=MC97CXno8FI) |
📑 [Download the slides (PDF)](https://aka.ms/iqdeepdive/slides/fabriciq)

This write-up includes an annotated version of the presentation slides with timestamps to the video plus a summary of the live Q&A.

## Table of contents

- [Session description](#session-description)
- [Annotated slides](#annotated-slides)
  - [Microsoft IQ Deep Dive with Python series](#microsoft-iq-deep-dive-with-python-series)
  - [Microsoft IQ Deep Dive: Fabric IQ](#microsoft-iq-deep-dive-fabric-iq)
  - [Today's agenda](#todays-agenda)
  - [Getting the code](#getting-the-code)
  - [Microsoft IQ](#microsoft-iq)
  - [The Microsoft IQ platform](#the-microsoft-iq-platform)
  - [Fabric IQ](#fabric-iq)
  - [Microsoft Fabric and OneLake](#microsoft-fabric-and-onelake)
  - [Unifying data in OneLake](#unifying-data-in-onelake)
  - [Fabric IQ components](#fabric-iq-components)
  - [Fabric IQ: Ontology](#fabric-iq-ontology)
  - [What is a Fabric IQ ontology](#what-is-a-fabric-iq-ontology)
  - [Ontology example: retail store](#ontology-example-retail-store)
  - [Demo: exploring ontologies in Fabric UI](#demo-exploring-ontologies-in-fabric-ui)
  - [Querying ontologies from agents](#querying-ontologies-from-agents)
  - [Ontology MCP server](#ontology-mcp-server)
  - [Demo: Ontology MCP server with GitHub Copilot](#demo-ontology-mcp-server-with-github-copilot)
  - [Foundry IQ knowledge base recap](#foundry-iq-knowledge-base-recap)
  - [Foundry IQ with Fabric ontology knowledge source](#foundry-iq-with-fabric-ontology-knowledge-source)
  - [Creating a Foundry IQ knowledge base with Fabric ontology](#creating-a-foundry-iq-knowledge-base-with-fabric-ontology)
  - [Fabric IQ: Graph](#fabric-iq-graph)
  - [Graph nodes and edges](#graph-nodes-and-edges)
  - [From OneLake to a queryable graph](#from-onelake-to-a-queryable-graph)
  - [Demo: exploring graphs in Fabric UI](#demo-exploring-graphs-in-fabric-ui)
  - [Querying graphs with GQL](#querying-graphs-with-gql)
  - [Querying graphs from agents](#querying-graphs-from-agents)
  - [Fabric IQ: Semantic models](#fabric-iq-semantic-models)
  - [What is a semantic model](#what-is-a-semantic-model)
  - [Star schema for analytics](#star-schema-for-analytics)
  - [Defining semantic models with TMDL](#defining-semantic-models-with-tmdl)
  - [Demo: exploring semantic models in Fabric UI](#demo-exploring-semantic-models-in-fabric-ui)
  - [Anatomy of a Power BI report](#anatomy-of-a-power-bi-report)
  - [Creating Power BI reports with Fabric SDK](#creating-power-bi-reports-with-fabric-sdk)
  - [Demo: Power BI reports in Fabric UI](#demo-power-bi-reports-in-fabric-ui)
  - [Querying semantic models from agents](#querying-semantic-models-from-agents)
  - [Fabric IQ: Data agent](#fabric-iq-data-agent)
  - [Data agent architecture](#data-agent-architecture)
  - [Data agent MCP server](#data-agent-mcp-server)
  - [Demo: Data agent MCP server with GitHub Copilot](#demo-data-agent-mcp-server-with-github-copilot)
  - [Foundry IQ knowledge base recap (data agent)](#foundry-iq-knowledge-base-recap-data-agent)
  - [Foundry IQ with Fabric data agent knowledge source](#foundry-iq-with-fabric-data-agent-knowledge-source)
  - [Creating a Foundry IQ knowledge base with Fabric data agent](#creating-a-foundry-iq-knowledge-base-with-fabric-data-agent)
  - [Microsoft IQ platform overview](#microsoft-iq-platform-overview)
  - [Microsoft IQ Live](#microsoft-iq-live)
  - [Next steps](#next-steps)
- [Live Chat Q&A](#live-chat-qa)

## Session description

In the final session of the Microsoft IQ Deep Dive with Python series, we explored Fabric IQ and how it connects AI experiences to structured business data stored in Microsoft Fabric's OneLake.

We introduced the key components of Fabric IQ — ontologies, graphs, semantic models, and data agents — and showed how each one helps describe, organize, and reason over operational data.

Ontologies provide a shared business vocabulary that maps entity types, properties, and relationships to actual OneLake data. Graphs offer dedicated graph database capabilities for queries requiring extensive relationship traversal. Semantic models expose Power BI analytics through DAX measures on star-schema tables. Data agents combine all of these behind a single conversational interface that selects the right source and query language automatically.

For each component, we demonstrated the Ontology MCP server and Data Agent MCP server for agent integration, and showed how to add each as a knowledge source to Foundry IQ knowledge bases for multi-source retrieval.

All code demos used Python and the Microsoft Fabric API SDK, and are available in an open-source repository for you to deploy yourself.

## Annotated slides

### Microsoft IQ Deep Dive with Python series

![Series title slide](slide_images/slide_1.png)
[Watch from 00:55](https://www.youtube.com/watch?v=MC97CXno8FI&t=55s)

This is a three-part live stream series covering all four members of the Microsoft IQ family, with a focus on using them programmatically from Python. Session 1 (July 28) covers Foundry IQ and Web IQ, session 2 (July 29) covers Work IQ, and session 3 (July 30) covers Fabric IQ. Register at [aka.ms/IQDeepDivePython/series](https://aka.ms/IQDeepDivePython/series).

### Microsoft IQ Deep Dive: Fabric IQ

![Session title slide](slide_images/slide_2.png)
[Watch from 01:30](https://www.youtube.com/watch?v=MC97CXno8FI&t=90s)

Slides are at [aka.ms/iqdeepdive/slides/fabriciq](https://aka.ms/iqdeepdive/slides/fabriciq) and are free to reuse. Presented by Pamela Fox, Principal Cloud Advocate at Microsoft and GitHub, focused on building AI applications and agents in Python.

### Today's agenda

![Agenda slide](slide_images/slide_3.png)
[Watch from 02:24](https://www.youtube.com/watch?v=MC97CXno8FI&t=144s)

The session covers Fabric IQ's four main components: ontologies, graphs, semantic models, and data agents, plus integration of each with Foundry IQ knowledge bases.

### Getting the code

![Code repo slide](slide_images/slide_4.png)
[Watch from 02:46](https://www.youtube.com/watch?v=MC97CXno8FI&t=166s)

All code across the three sessions lives in one repository at [aka.ms/iqdeepdive](https://aka.ms/iqdeepdive) — Jupyter notebooks, agents, and infrastructure-as-code. Use the "Code" button to open a GitHub Codespace. Running the code requires an Azure account and a Fabric license with the ability to create Fabric items. All notebook output is checked into the repo, so you can read results without running anything.

### Microsoft IQ

![Microsoft IQ section header](slide_images/slide_5.png)
[Watch from 03:57](https://www.youtube.com/watch?v=MC97CXno8FI&t=237s)

### The Microsoft IQ platform

![Microsoft IQ platform diagram](slide_images/slide_6.png)
[Watch from 04:04](https://www.youtube.com/watch?v=MC97CXno8FI&t=244s)

Microsoft IQ is a unified intelligence layer that provides different kinds of context for grounding AI applications. Work IQ covers Microsoft 365 data: Teams, email, calendar, SharePoint, and Office documents. Fabric IQ covers business operations data stored in OneLake. Web IQ connects to live web intelligence — news, weather, images, and video. Foundry IQ unlocks knowledge from policies, authoritative documents, and knowledge bases, and can also route to the other three. Together, these four IQs let you build applications that are grounded in accurate, domain-specific information.

### Fabric IQ

![Fabric IQ section header](slide_images/slide_7.png)
[Watch from 05:52](https://www.youtube.com/watch?v=MC97CXno8FI&t=352s)

### Microsoft Fabric and OneLake

![Microsoft Fabric platform diagram](slide_images/slide_8.png)
[Watch from 05:55](https://www.youtube.com/watch?v=MC97CXno8FI&t=355s)

Before Microsoft Fabric, data lived across Azure Data Lake, Azure SQL, Databricks, Power BI, and Azure ML — five services with five storage accounts, five auth models, and manual ETL between each pair. Microsoft Fabric unifies everything under OneLake, a single shared storage layer. On top of OneLake sit Data Factory, Data Engineering (Spark notebooks and pipelines), Power BI, Databases, Graphs, and Fabric IQ.

### Unifying data in OneLake

![OneLake shortcut and mirroring sources](slide_images/slide_9.png)
[Watch from 07:14](https://www.youtube.com/watch?v=MC97CXno8FI&t=434s)

OneLake connects to external data through shortcuts (direct links) and mirroring (copying data or metadata). Supported sources include Azure SQL, Azure Blob Storage, Azure Cosmos DB, Azure PostgreSQL, SQL Server, SharePoint/OneDrive, SAP Datasphere, Snowflake, Google Cloud Storage, Amazon S3, Databricks Catalog, Google BigQuery, Oracle DB, and S3-compatible storage. The exact strategy depends on what you're bringing in and whether you need a single file or an entire catalog.

### Fabric IQ components

![Fabric IQ component diagram](slide_images/slide_10.png)
[Watch from 08:23](https://www.youtube.com/watch?v=MC97CXno8FI&t=503s)

Fabric IQ sits on top of OneLake and includes seven components: Ontology (shared business vocabulary), Semantic Model (curated business metrics for Power BI analytics), Graph (relationship traversal), Data Agent (AI analyst for domain-specific questions), Plan (collaborative planning and forecasting), Digital Twin Builder (digital representations of real-world entities), and Operations Agent (monitors live data, detects issues, remediates). This session covers the first four.

### Fabric IQ: Ontology

![Ontology section header](slide_images/slide_11.png)
[Watch from 09:40](https://www.youtube.com/watch?v=MC97CXno8FI&t=580s)

### What is a Fabric IQ ontology

![Ontology definition slide](slide_images/slide_12.png)
[Watch from 09:44](https://www.youtube.com/watch?v=MC97CXno8FI&t=584s)

An ontology describes the data in OneLake with a richer vocabulary so agents can understand it better rather than guessing at relationships from table and column names. An ontology consists of four parts: entity types (the business concepts like Product, Category, Store), properties (named facts about each entity type like Product.name and Product.sku), relationships (typed links between entity types like Category → contains → Product), and data bindings (connections to actual data in OneLake, mapping ontology properties to lakehouse columns).

### Ontology example: retail store

![Retail store ontology diagram](slide_images/slide_13.png)
[Watch from 11:16](https://www.youtube.com/watch?v=MC97CXno8FI&t=676s)

A retail store ontology has five entity types: Store (storeId, storeName, city), Inventory (inventoryId, storeId, sku, quantityOnHand), Product (name, sku, price), Category (categoryName), and Supplier (supplierId, supplierName). Four relationships connect them: Store holds Inventory, Inventory recordsStockFor Product, Category contains Product, and Supplier supplies Product. With this ontology bound to lakehouse data, an agent can answer questions like "which store has the most hammers" by following relationships rather than guessing at joins.

### Demo: exploring ontologies in Fabric UI

![Ontology Fabric UI demo slide](slide_images/slide_14.png)
[Watch from 12:17](https://www.youtube.com/watch?v=MC97CXno8FI&t=737s)

The Fabric UI provides an ontology explorer that visualizes entities, their relationships, and data bindings. Clicking an entity shows its properties and their bound lakehouse columns. The binding matters because real data is often messy — multiple similarly named fields can exist, and the ontology explicitly declares which column is authoritative. The UI also shows data previews so you can verify that bindings are correct. Ontologies can be created in the Fabric UI or programmatically in Python using the Fabric SDK (see `create-lakehouse.py` in the repo).

### Querying ontologies from agents

![Agents with ontology support](slide_images/slide_15.png)
[Watch from 15:46](https://www.youtube.com/watch?v=MC97CXno8FI&t=946s)

Many Microsoft agents have built-in ontology support: Copilot Studio, Fabric data agent, Fabric operations agent, Foundry IQ, and Foundry hosted agents via Foundry Toolbox. For other agents, use the Ontology MCP server. Reference: [Tutorial: Create a data agent with ontology](https://learn.microsoft.com/fabric/iq/ontology/tutorial-4-create-data-agent).

### Ontology MCP server

![Ontology MCP server details](slide_images/slide_16.png)
[Watch from 16:44](https://www.youtube.com/watch?v=MC97CXno8FI&t=1004s)

The Ontology MCP server URL is `https://api.fabric.microsoft.com/v1/mcp/dataPlane/workspaces/WORKSPACE_ID/items/ONTOLOGY_ID/ontologyEndpoint`. It exposes two tools:

- `list_ontology_entity_types(includeProperties)` — returns all entity types and optionally their properties, for discovery.
- `search_ontology(naturalLanguageQuery, naturalLanguageResponse)` — takes a natural language question, queries the ontology, and returns raw results plus optionally a synthesized answer (which uses an internal LLM and adds latency).

Authorization uses an OAuth bearer token for a user with access to the Fabric workspace. Full example: `notebooks/fabriciq-ontology-mcp.ipynb`. Reference: [How to use the Ontology MCP server](https://learn.microsoft.com/fabric/iq/ontology/how-to-use-ontology-mcp-server).

### Demo: Ontology MCP server with GitHub Copilot

![Ontology MCP + GitHub Copilot demo](slide_images/slide_17.png)
[Watch from 21:41](https://www.youtube.com/watch?v=MC97CXno8FI&t=1301s)

The Ontology MCP server works with any MCP-compatible client that can pass Entra authorization: VS Code, GitHub Copilot CLI, and the GitHub Copilot App. In the demo, GitHub Copilot first called `list_ontology_entity_types` to discover the schema, then constructed a specific `search_ontology` query to find products with the lowest inventory. Different models and different runs may choose different tool-calling strategies. The server may not work with non-Microsoft clients like Claude Desktop because of the OAuth pre-authorization requirements of Microsoft Entra.

### Foundry IQ knowledge base recap

![Foundry IQ knowledge base architecture](slide_images/slide_18.png)
[Watch from 25:03](https://www.youtube.com/watch?v=MC97CXno8FI&t=1503s)

As covered in session 1, Foundry IQ knowledge bases perform multi-source retrieval. The input is a conversation plus steering instructions. Retrieval planning generates search queries and selects which sources to hit. Sources run in parallel — search indexes, MCP servers, Work IQ, or Fabric IQ. Results are merged, reranked, and optionally synthesized into a single answer. Rewatch session 1 for the full Foundry IQ deep dive.

### Foundry IQ with Fabric ontology knowledge source

![Foundry IQ + Fabric ontology flow](slide_images/slide_19.png)
[Watch from 25:34](https://www.youtube.com/watch?v=MC97CXno8FI&t=1534s)

Adding a Fabric ontology as a knowledge source to a Foundry IQ knowledge base makes the ontology queryable alongside other sources. When a question like "What are the stock levels for our hammers?" arrives, the knowledge base routes it to the ontology. The ontology resolves entity relationships (Product → Inventory → Store), queries the lakehouse, and returns structured results (SKU, name, available quantity, store ID) that get merged with results from other sources. Reference: [Fabric ontology knowledge source](https://learn.microsoft.com/azure/search/agentic-knowledge-source-how-to-fabric-ontology).

### Creating a Foundry IQ knowledge base with Fabric ontology

![Python code for Fabric ontology knowledge source](slide_images/slide_20.png)
[Watch from 25:48](https://www.youtube.com/watch?v=MC97CXno8FI&t=1548s)

```python
fabric_knowledge_source = FabricOntologyKnowledgeSource(
  name="fabric-ontology-knowledge-source",
  description="Operational data including stores, inventory, products",
  fabric_ontology_parameters=FabricOntologyKnowledgeSourceParameters(
    workspace_id=FABRIC_WORKSPACE_ID, ontology_id=FABRIC_ONTOLOGY_ID))
```

Create a knowledge base with the ontology plus other sources, and provide retrieval instructions that tell the knowledge base when to use each source (e.g., "Use Fabric Ontology for products. Use search indexes for HR and health policy docs."). The knowledge base's source selection will skip sources that are irrelevant to a given query — if a question is purely about products, only the ontology is hit. A user token with access to the Fabric workspace must be passed as `query_source_authorization`. Full example: `notebooks/foundryiq-fabriciq-ontology.ipynb`.

### Fabric IQ: Graph

![Graph section header](slide_images/slide_21.png)
[Watch from 29:55](https://www.youtube.com/watch?v=MC97CXno8FI&t=1795s)

### Graph nodes and edges

![Graph data model diagram](slide_images/slide_22.png)
[Watch from 30:05](https://www.youtube.com/watch?v=MC97CXno8FI&t=1805s)

Fabric IQ graphs are for scenarios requiring extensive graph traversal — when you know you'll run many queries that hop across relationships, a graph database is more efficient than ontology queries. Nodes represent things (with labels for classification and properties for business context). Edges represent relationships between nodes. In a product reviews graph: a Product node has properties name and sku; it connects via a HAS_REVIEW edge to a Review node (user_id); and reviews connect via MENTIONS edges (with sentiment +/-) to Feature nodes (name). Ontologies and graphs overlap conceptually (entities/relationships vs nodes/edges), but use graphs when you specifically need optimized graph traversal performance.

### From OneLake to a queryable graph

![Graph creation pipeline](slide_images/slide_23.png)
[Watch from 31:53](https://www.youtube.com/watch?v=MC97CXno8FI&t=1913s)

Building a graph starts with source data in OneLake lakehouse tables (products, reviews, features, review_feature_mentions). You define a graph model specifying node types, edge types, and table mappings. Edges get their own table — for example, `review_feature_mentions` becomes a MENTIONS edge connecting Review nodes to Feature nodes, with origin and target columns mapping to node keys. The result is a queryable graph optimized for fast traversal. Graphs can be created in the Fabric UI or programmatically in Python.

### Demo: exploring graphs in Fabric UI

![Graph explorer demo slide](slide_images/slide_24.png)
[Watch from 32:36](https://www.youtube.com/watch?v=MC97CXno8FI&t=1956s)

The Fabric UI graph explorer visualizes nodes, edges, source table bindings, and label-to-column mappings. For each edge, you can see the origin node key and target node key that define how the relationship connects two node types.

### Querying graphs with GQL

![GQL query example](slide_images/slide_25.png)
[Watch from 34:09](https://www.youtube.com/watch?v=MC97CXno8FI&t=2049s)

GQL (Graph Query Language — not GraphQL) uses pattern matching syntax for traversal:

```
MATCH (p:`Product`) -[:`HAS_REVIEW`]-> (r:`Review`) -[m:`MENTIONS`]-> (f:`Feature`)
FILTER m.sentiment = 'negative'
RETURN p.name AS productName, r.rating AS rating, f.featureName AS feature,
       m.sentiment AS sentiment, m.confidence AS confidence
ORDER BY confidence DESC
LIMIT 20
```

Execute GQL queries via the REST API at `POST .../executeQuery?preview=true` with an authorization bearer token for the Fabric workspace. No LLM is involved — it's a direct data query returning tabular results in about two seconds. Full example: `notebooks/fabriciq-graph.ipynb`. Reference: [GQL query API](https://learn.microsoft.com/fabric/graph/gql-query-api).

### Querying graphs from agents

![NL2GQL via Fabric data agent](slide_images/slide_26.png)
[Watch from 37:11](https://www.youtube.com/watch?v=MC97CXno8FI&t=2231s)

For natural-language-to-GQL (NL2GQL), add the graph as a data source to a Fabric data agent. The data agent handles the translation. You could also build a custom tool that constructs GQL and calls the graph REST API directly — anything you can programmatically access can become an agent tool. Most users will just add the graph to a data agent. Reference: [Graph-powered AI reasoning](https://blog.fabric.microsoft.com/blog/graph-powered-ai-reasoning-preview/).

### Fabric IQ: Semantic models

![Semantic models section header](slide_images/slide_27.png)
[Watch from 38:26](https://www.youtube.com/watch?v=MC97CXno8FI&t=2306s)

### What is a semantic model

![Semantic model components](slide_images/slide_28.png)
[Watch from 38:29](https://www.youtube.com/watch?v=MC97CXno8FI&t=2309s)

A semantic model is a Power BI tabular analytical model optimized for aggregation and reporting. It contains tables (business entities like Sessions, Page Views, Channels, Date), relationships (how tables connect), measures (reusable DAX calculations like Total Sessions or Bounce Rate), and a data source (DirectLake connection to OneLake). Power BI reports query semantic models directly for interactive analytics dashboards.

### Star schema for analytics

![Star schema diagram](slide_images/slide_29.png)
[Watch from 39:26](https://www.youtube.com/watch?v=MC97CXno8FI&t=2366s)

Semantic models use a star schema with facts and dimensions. Facts are the rows to aggregate — typically events like page views or sessions that happen continuously. Dimensions are the rows to group or filter by — things like date, device category, geography, or page. In a web analytics model, Sessions is the fact table (with keys pointing to dimensions), while Date, Channels, Devices, Geography, and Pages are dimension tables. This structure enables fast slice-and-dice reporting.

### Defining semantic models with TMDL

![TMDL format example](slide_images/slide_30.png)
[Watch from 40:32](https://www.youtube.com/watch?v=MC97CXno8FI&t=2432s)

TMDL is a declarative format for Power BI semantic models in Fabric. A fact table definition includes the table name, a DirectLake partition pointing to a lakehouse entity, and DAX measures (e.g., `measure 'Total Sessions' = COUNTROWS(Sessions)`). A dimension table definition includes typed columns mapped to source columns and its own DirectLake partition. Models can be created programmatically with the Fabric SDK:

```python
semantic_model = client.semanticmodel.items.create_semantic_model(
  FABRIC_WORKSPACE_ID,
  CreateSemanticModelRequest(display_name=SEMANTIC_MODEL_NAME, definition=definition))
```

Model definitions: `data/semantic-models/web-analytics`. Full code: `infra/create-semantic-model.py`.

### Demo: exploring semantic models in Fabric UI

![Semantic model Fabric UI demo](slide_images/slide_31.png)
[Watch from 42:41](https://www.youtube.com/watch?v=MC97CXno8FI&t=2561s)

The Fabric UI shows the semantic model's tables (fact and dimension), DAX measures (indicated by the epsilon symbol), column definitions, and relationships. The visual layout roughly resembles the star shape, with the fact table in the center connected to surrounding dimension tables.

### Anatomy of a Power BI report

![Power BI report structure](slide_images/slide_32.png)
[Watch from 43:43](https://www.youtube.com/watch?v=MC97CXno8FI&t=2623s)

A Power BI report contains pages; pages contain visuals (cards, line charts, bar charts) and filters (date range, category). Visuals bind to semantic models for interactive analytics. In the demo web analytics dashboard, cards show metrics like Bounce Rate and Revenue, line charts show sessions over time, and a date-range filter controls the view. Report definitions use PBIR JSON format. PBIR definitions: `data/reports/web-analytics`.

### Creating Power BI reports with Fabric SDK

![Report creation code](slide_images/slide_33.png)
[Watch from 43:51](https://www.youtube.com/watch?v=MC97CXno8FI&t=2631s)

The PBIR manifest binds the report to a semantic model via a `datasetReference` with a `connectionString` containing the semantic model ID. Pages, visuals, and filters are separate definition parts. The Fabric SDK uploads all parts as a single report definition:

```python
report = client.report.items.create_report(
  workspace_id,
  CreateReportRequest(
    display_name=REPORT_NAME,
    definition=ReportDefinition(format="PBIR", parts=parts)))
```

Full code: `infra/create-web-analytics-report.py`.

### Demo: Power BI reports in Fabric UI

![Power BI report demo slide](slide_images/slide_34.png)
[Watch from 44:18](https://www.youtube.com/watch?v=MC97CXno8FI&t=2658s)

The Fabric UI displays the programmatically created report with cards, charts, and interactive filters. Filters on the side control date ranges and other dimensions, dynamically updating all visuals.

### Querying semantic models from agents

![NL2DAX via Fabric data agent](slide_images/slide_35.png)
[Watch from 45:01](https://www.youtube.com/watch?v=MC97CXno8FI&t=2701s)

For NL2DAX (natural language to DAX), add the semantic model as a data source to a Fabric data agent. A question like "What were the top five pages by session count last week?" gets translated to a DAX EVALUATE/SUMMARIZECOLUMNS expression. To maximize NL2DAX accuracy: model as a star schema, use business-friendly names, define explicit DAX measures, and configure an AI data schema using Prep for AI. You could also build a custom agent tool that does NL2DAX directly. Reference: [Semantic model best practices](https://learn.microsoft.com/fabric/data-science/semantic-model-best-practices).

### Fabric IQ: Data agent

![Data agent section header](slide_images/slide_36.png)
[Watch from 46:37](https://www.youtube.com/watch?v=MC97CXno8FI&t=2797s)

### Data agent architecture

![Data agent pipeline diagram](slide_images/slide_37.png)
[Watch from 46:40](https://www.youtube.com/watch?v=MC97CXno8FI&t=2800s)

The Fabric data agent is a conversational agent that queries across multiple Fabric data sources. Its pipeline: (1) question validation — checks policies, PII, syntax; (2) source selection — picks which data source to query; (3) query generation — constructs the appropriate language for the selected source: DAX for semantic models, SQL for lakehouses, KQL for eventhouses, GQL for graph models, SQL for data warehouses. The data agent currently selects one source per question. Having it handle multiple sources with different query languages is its key value.

### Data agent MCP server

![Data agent MCP server details](slide_images/slide_38.png)
[Watch from 48:06](https://www.youtube.com/watch?v=MC97CXno8FI&t=2886s)

The Data Agent MCP server URL is `https://api.fabric.microsoft.com/v1/mcp/workspaces/WORKSPACE_ID/dataagents/DATA_AGENT_ID/agent`. It exposes a single tool named after your data agent (e.g., `DataAgent_ContosoDIY`) with one argument: `userQuestion`. The tool name and description come from what you configured when creating the data agent — useful for disambiguation when running multiple agents.

The MCP server returns both structured content (JSON with a deep-link URL to the Fabric UI for debugging the query) and free-text content (the natural language answer). There is currently a VS Code issue where mixed structured + text content is not fully displayed to the agent. Full example: `notebooks/fabriciq-dataagent-mcp.ipynb`. Reference: [Data agent MCP server](https://learn.microsoft.com/fabric/data-science/data-agent-mcp-server).

### Demo: Data agent MCP server with GitHub Copilot

![Data agent MCP + GitHub Copilot demo](slide_images/slide_39.png)
[Watch from 51:25](https://www.youtube.com/watch?v=MC97CXno8FI&t=3085s)

The Data Agent MCP server was added to the GitHub Copilot App (HTTP type, triggered Entra login). Asking "What is the total website revenue and conversion rate?" invoked the data agent tool, which selected the semantic model source and generated DAX. The deep-link URL in the response opens the Fabric UI showing the generated query, selected source, and whether the result was complete or incomplete — essential for debugging during development.

### Foundry IQ knowledge base recap (data agent)

![Foundry IQ recap slide](slide_images/slide_40.png)
[Watch from 52:19](https://www.youtube.com/watch?v=MC97CXno8FI&t=3139s)

Same Foundry IQ architecture as before: multiple knowledge sources queried in parallel with merged results. This time, the Fabric data agent is one of those sources.

### Foundry IQ with Fabric data agent knowledge source

![Foundry IQ + data agent flow](slide_images/slide_41.png)
[Watch from 52:30](https://www.youtube.com/watch?v=MC97CXno8FI&t=3150s)

Adding a Fabric data agent as a Foundry IQ knowledge source introduces another level of agent reasoning. The knowledge base sends the query to the data agent, which then decides whether to route it to ontology, graph, or semantic models. This is most useful when you have multiple Fabric data sources behind the data agent. If you only have an ontology, add the ontology directly as a knowledge source — don't put a data agent in the middle unnecessarily.

### Creating a Foundry IQ knowledge base with Fabric data agent

![Python code for data agent knowledge source](slide_images/slide_42.png)
[Watch from 53:30](https://www.youtube.com/watch?v=MC97CXno8FI&t=3210s)

```python
fabric_knowledge_source = FabricDataAgentKnowledgeSource(
  name="fabric-data-agent-knowledge-source",
  description="Product inventory, reviews, website analytics",
  fabric_data_agent_parameters=FabricDataAgentKnowledgeSourceParameters(
    workspace_id=FABRIC_WORKSPACE_ID, data_agent_id=FABRIC_DATA_AGENT_ID))
```

Give the knowledge base retrieval instructions like "Use data agent for product, inventory, analytics. Use search index for HR docs." In the demo, a complex question asking about both product inventory (data agent) and job roles (search index) was correctly routed to both sources, with each source contributing its portion of the answer. The knowledge base sends the full question to the data agent and lets it decide what to do. Full example: `notebooks/foundryiq-fabriciq-dataagent.ipynb`.

### Microsoft IQ platform overview

![Microsoft IQ platform recap](slide_images/slide_43.png)
[Watch from 57:54](https://www.youtube.com/watch?v=MC97CXno8FI&t=3474s)

Foundry IQ can consume Work IQ, Fabric IQ, and Web IQ as knowledge sources, making it a "one IQ to rule them all" for multi-source knowledge bases. Alternatively, each IQ can be used independently. The choice depends on your use case: whether you want agent-mediated access, direct structured results, latency requirements, and which sources you need to combine. Set up evaluations to measure accuracy and latency across the different options.

### Microsoft IQ Live

![Microsoft IQ Live announcement](slide_images/slide_44.png)
[Watch from 59:52](https://www.youtube.com/watch?v=MC97CXno8FI&t=3592s)

Microsoft IQ Live is a bi-weekly YouTube series on Microsoft Reactor running from August 6 to November 12, 2026, covering the evolving Microsoft IQ platform. Register at [aka.ms/MicrosoftIQLive](https://aka.ms/MicrosoftIQLive) and follow Microsoft Reactor on YouTube.

### Next steps

![Next steps slide](slide_images/slide_45.png)
[Watch from 1:00:26](https://www.youtube.com/watch?v=MC97CXno8FI&t=3626s)

- Join office hours after the session in Discord: [aka.ms/pythonai/oh](https://aka.ms/pythonai/oh)
- Register for the series: [aka.ms/IQDeepDivePython/series](https://aka.ms/IQDeepDivePython/series)
- Fabric data advocates are available in Discord for follow-up questions about Fabric IQ specifically.

## Live Chat Q&A

### Can I use Fabric IQ ontologies from a Teams bot?

Yes — deploy a Foundry hosted agent with the ontology added via Foundry Toolbox, then publish that agent to Teams. The authenticating user must have access to the Fabric workspace containing the ontology.

### What is the deep-link URL in data agent MCP responses?

The data agent MCP server returns both structured content (JSON containing a deep-link URL) and free-text content (the natural language answer). The deep link opens the Fabric UI query debugger showing the generated query, selected source, and whether the result was complete. This is essential during development. There is currently a VS Code issue where mixed structured + text MCP content is not fully shown to the model.

### Does the Ontology MCP server work with non-Microsoft clients like Claude Desktop?

Likely not without extra setup. The Ontology MCP server requires Microsoft Entra OAuth pre-authorization, which is built into GitHub Copilot, VS Code, and the Copilot CLI. Non-Microsoft clients would need to configure an Entra client ID and handle the OAuth flow manually.
