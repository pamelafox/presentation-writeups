# An MCP for your Postgres DB

This talk walks through building MCP servers for PostgreSQL databases using Python and FastMCP. It covers a progression from exploratory servers where agents write full SQL queries to fully typed operational servers with maximum safety, discussing tradeoffs, failure modes, and tool design strategies at each level.

## Table of contents

- [Model Context Protocol](#model-context-protocol)
  - [What is MCP?](#what-is-mcp)
- [Building MCP servers for a Postgres DB](#building-mcp-servers-for-a-postgres-db)
  - [The progression from exploratory to operational](#the-progression-from-exploratory-to-operational)
- [Free-form SQL](#free-form-sql)
  - [Schema and SQL execution tools](#schema-and-sql-execution-tools)
  - [Demo: calling free-form SQL tools](#demo-calling-free-form-sql-tools)
  - [Problem: schema bloat](#problem-schema-bloat)
  - [Schema discovery tools](#schema-discovery-tools)
  - [Demo: progressive schema discovery](#demo-progressive-schema-discovery)
  - [Problem: mutations without guardrails](#problem-mutations-without-guardrails)
- [Read-only SQL](#read-only-sql)
  - [Read-only SQL execution tool](#read-only-sql-execution-tool)
  - [Demo: calling read-only SQL tools](#demo-calling-read-only-sql-tools)
  - [Demo: blocked on DELETE](#demo-blocked-on-delete)
  - [The readOnlyHint annotation](#the-readonlyhint-annotation)
  - [AST-parsing validation](#ast-parsing-validation)
  - [DB-level read-only enforcement](#db-level-read-only-enforcement)
  - [Four layers of protection](#four-layers-of-protection)
- [Fully typed tools](#fully-typed-tools)
  - [Table-specific tools with parameterized queries](#table-specific-tools-with-parameterized-queries)
  - [Demo: multi-step tool chaining](#demo-multi-step-tool-chaining)
  - [Limitations of typed tools](#limitations-of-typed-tools)
- [Elicitation](#elicitation)
  - [Tool elicitation for destructive actions](#tool-elicitation-for-destructive-actions)
  - [Demo: elicitation in VS Code](#demo-elicitation-in-vs-code)
- [Tool selection](#tool-selection)
  - [The tool selection problem](#the-tool-selection-problem)
  - [Experiment results](#experiment-results)
  - [Don't make the agent choose](#dont-make-the-agent-choose)
- [Final words](#final-words)
  - [Which approach should you use?](#which-approach-should-you-use)

## Model Context Protocol

### What is MCP?

![Diagram showing MCP connecting an AI agent to a database, Slack, and GitHub](slide_images/slide_3.png)
[Watch from 01:57](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=117s)

MCP stands for Model Context Protocol. It is an open protocol that defines how AI apps and agents get context from external tools and data sources. Anthropic first proposed it, but it has since been adopted across the generative AI industry and is now part of the Linux Foundation. Before MCP, every integration with an AI agent required a custom implementation. With MCP, you put an MCP server in front of each data source — a database, Slack, GitHub — and that creates a common protocol for agents to access them all. One of those data sources can be a PostgreSQL database.

## Building MCP servers for a Postgres DB

### The progression from exploratory to operational

![Arrow showing progression from exploratory (free-form SQL) to operational (fully typed tools)](slide_images/slide_5.png)
[Watch from 02:46](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=166s)

There is a range of ways to build an MCP server on top of a Postgres database. On one extreme are exploratory servers where the agent writes entire SQL queries and sends them to the database — maximum flexibility but also maximum risk. On the other extreme are operational servers with fully typed, constrained tools where SQL is removed from the equation entirely. In between sit read-only SELECT enforcement and scoped WHERE approaches.

## Free-form SQL

### Schema and SQL execution tools

![Code showing FastMCP server with get_db_schema and execute_sql tools](slide_images/slide_7.png)
[Watch from 03:29](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=209s)

The simplest MCP server defines two tools. `get_db_schema()` returns the full database schema by querying `information_schema.columns`. `execute_sql(sql)` takes any SQL string and executes it against the database. The agent first calls the schema tool to learn what tables and columns exist, then constructs SQL to answer the user's question. This works — a question like "which bees are active in El Cerrito in April?" gets answered correctly. But there are serious problems.

[Full server code: servers/level1_freeform.py](https://github.com/pamelafox/mcp-for-postgres-db-demo/blob/main/servers/level1_freeform.py)

### Demo: calling free-form SQL tools

![Agent calls get_db_schema then execute_sql to answer a query about bees](slide_images/slide_8.png)
[Watch from 04:28](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=268s)

When asked "Which bees are active in El Cerrito in April?", the agent first calls `get_db_schema` to discover available tables and columns, then calls `execute_sql` with a SELECT query joining species and observations filtered by location and month. It returns a table of results ranked by observation count — Yellow-faced Bumble Bee (23 observations), Black-tailed Bumble Bee (13), Western Honey Bee (10), and several carpenter bee species.

### Problem: schema bloat

![Full schema dump showing 5 tables and 60+ columns](slide_images/slide_9.png)
[Watch from 04:59](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=299s)

The `get_db_schema()` tool dumps everything — in this demo database, 5 tables and 60+ columns. Real databases may have hundreds of tables and thousands of columns. Dumping the entire schema confuses the LLM with irrelevant information and may exceed its context window.

### Schema discovery tools

![Code showing list_tables and describe_table tools](slide_images/slide_10.png)
[Watch from 05:36](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=336s)

A better approach is progressive schema discovery. `list_tables()` returns just the table names (with optional descriptions). `describe_table(table_name)` returns columns for a specific table. The agent calls `list_tables()` first, then `describe_table()` only on the tables relevant to the current question. This requires 3 tool calls instead of 1, so it increases latency, but for large schemas it prevents context bloat. Whether the tradeoff is worth it depends on schema size.

[Full server code: servers/level1b_discovery.py](https://github.com/pamelafox/mcp-for-postgres-db-demo/blob/main/servers/level1b_discovery.py)

### Demo: progressive schema discovery

![Agent calling list_tables then describe_table for the species table](slide_images/slide_11.png)
[Watch from 05:54](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=354s)

With the same question, the agent now calls `list_tables` first and gets back just the table names. It then calls `describe_table` twice — once for the species table and once for the observations table — retrieving only the columns it needs. The tradeoff is 3 tool calls instead of 1, but the agent never sees irrelevant tables like `spatial_ref_sys` or `geometry_columns`.

### Problem: mutations without guardrails

![Screenshots showing Opus asking before deletion but Gemini deleting immediately](slide_images/slide_13.png)
[Watch from 06:47](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=407s)

When a user says "How many bee observations have quality grade 'needs_id'? Actually, delete those," the behavior depends on the model. Claude Opus 4.6 asks "are you sure you want to delete almost 20,000 rows?" But Gemini 2.5 Pro deletes all 18,633 rows immediately without asking. The problem is not the model — it's the tool surface. If your tool exposes the ability to do a deletion, some model will execute that deletion without confirmation. You cannot rely on model safety. The tools themselves must be safe.

## Read-only SQL

### Read-only SQL execution tool

![Code for execute_readonly_sql tool with validation and row cap](slide_images/slide_15.png)
[Watch from 07:58](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=478s)

One option is to enforce read-only SQL: only allow SELECT statements. The `execute_readonly_sql` tool has a `readOnlyHint` annotation, validates the SQL to ensure it is a SELECT, executes it, and caps results at 100 rows. A 30-second timeout prevents expensive queries from running indefinitely. The agent can still construct complex SELECT queries to answer questions, but cannot perform INSERT, UPDATE, or DELETE.

[Full server code: servers/level2_readonly.py](https://github.com/pamelafox/mcp-for-postgres-db-demo/blob/main/servers/level2_readonly.py)

### Demo: calling read-only SQL tools

![Agent sends a complex SELECT query through execute_readonly_sql](slide_images/slide_16.png)
[Watch from 08:34](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=514s)

The agent constructs a multi-line SELECT with JOINs, WHERE clauses filtering by county, latitude/longitude bounds, month, and quality grade, grouped and ordered by observation count. The `execute_readonly_sql` tool accepts it and returns structured JSON with columns and rows. The agent can still write arbitrarily complex queries — it just cannot mutate data.

### Demo: blocked on DELETE

![Agent attempts DELETE and gets rejected with error message](slide_images/slide_20.png)
[Watch from 11:36](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=696s)

When asked to "delete all bee observations where quality_grade is needs_id," the agent sends a DELETE statement through `execute_readonly_sql`. The tool responds: "Only SELECT statements are allowed, got DeleteStmt." The agent then explains that it cannot perform deletions and offers to help construct a SELECT query to identify the rows instead.

### The readOnlyHint annotation

![Explanation of readOnlyHint benefits and limitations](slide_images/slide_17.png)
[Watch from 08:53](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=533s)

The MCP spec allows tools to be annotated with hints like `readOnlyHint`, `idempotent`, and `destructive`. Setting `readOnlyHint=True` tells the MCP client this tool won't modify data, which may affect how the client renders the tool or handles approvals. But it is only a hint — not a contract. An untrusted server can lie about it. Actual safety must come from server-side enforcement.

### AST-parsing validation

![Code using pglast to parse SQL and reject non-SELECT statements](slide_images/slide_18.png)
[Watch from 09:54](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=594s)

The `_validate_readonly_sql` function uses `pglast` to parse the SQL into an abstract syntax tree. It checks that there is exactly one statement and that it is a `SelectStmt`. This blocks invalid SQL, multiple statements (like `SELECT 1; DELETE FROM observations`), and explicit DELETE/INSERT/UPDATE. It still allows SELECT statements through.

### DB-level read-only enforcement

![SQL commands for read-only transaction and least-privilege role](slide_images/slide_19.png)
[Watch from 10:38](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=638s)

Beyond parsing, enforce read-only at the database level. Set `default_transaction_read_only = ON` on the connection. Create a dedicated `mcp_readonly` role with only `SELECT` privileges on the public schema. This blocks INSERT, DROP, and tricky CTEs like `WITH d AS (DELETE ...) SELECT * FROM d` that pass the AST parser. The database-level enforcement is the strongest guarantee.

### Four layers of protection

![Table showing how each layer blocks different attack vectors](slide_images/slide_25.png)
[Watch from 11:58](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=718s)

Making agent-written SQL safe requires four layers working together:

1. **Parser** — blocks DELETE, INSERT, multiple statements, and invalid SQL
2. **Read-only transaction** — blocks CTEs wrapping mutations that slip past the parser
3. **Least-privilege role** — blocks dangerous Postgres functions like `pg_terminate_backend()`, `pg_read_file('/etc/passwd')`, and `pg_reload_conf()` that pass both previous layers
4. **Timeout** — kills `pg_sleep()` and expensive CROSS JOINs that pass all other layers (killed at 30 seconds)

With all four layers, every tested attack vector is blocked. But the question remains: is there still something that could slip through? If maximum confidence is required, the best option is to not expose SQL at all.

## Fully typed tools

### Table-specific tools with parameterized queries

![Code for search_species tool with typed parameters and templated SQL](slide_images/slide_28.png)
[Watch from 13:14](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=794s)

Fully typed tools remove SQL from the equation. A `search_species(q, limit)` tool takes specific parameters and uses a templated SQL query internally. The agent passes parameters like `q="carpenter bee"` — it never sees or writes SQL. A `search_observations` tool takes 6 parameters (latitude, longitude, dates, radius, taxon_id) and passes them into a template. The server enforces a max limit to prevent pulling too many rows, and returns typed `SpeciesResult` or `ObservationResult` objects.

[Full server code: servers/level4_typed.py](https://github.com/pamelafox/mcp-for-postgres-db-demo/blob/main/servers/level4_typed.py)

### Demo: multi-step tool chaining

![Agent calls search_species with q="carpenter bee" and gets typed results](slide_images/slide_29.png)
[Watch from 14:09](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=849s)

Asked "Are there carpenter bees around Berkeley?", the agent first calls `search_species(q="carpenter bee")` and gets back structured results with taxon IDs, scientific names, and observation counts for Western Carpenter Bee, Valley Carpenter Bee, Horse-fly Carpenter Bee, and Foothill Carpenter Bee.

![Agent chains search_observations with 6 typed parameters](slide_images/slide_30.png)
[Watch from 14:24](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=864s)

It then calls `search_observations` with `lat=37.8716`, `lon=-122.2727`, `start_date="2025-01-01"`, `end_date="2026-04-16"`, `radius_km=25`, and `taxon_id=70000` (Foothill Carpenter Bee). The tool returns observation records with dates, coordinates, and quality grades. The agent never writes SQL — it only provides parameter values.

### Limitations of typed tools

![Agent unable to answer "how many total observations" with typed tools](slide_images/slide_31.png)
[Watch from 14:43](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=883s)

Typed tools are the safest approach but they limit what the agent can do. When asked "how many total observations are in the database?" the agent realizes it simply does not have the tools to answer that question. If you use typed tools, monitor what users ask and add tools for common unanswered questions over time.

## Elicitation

### Tool elicitation for destructive actions

![Code showing ctx.elicit() to confirm deletion with the user](slide_images/slide_33.png)
[Watch from 15:22](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=922s)

Elicitation adds a layer of safety for destructive operations. When a `delete_observation` tool is called, the server uses `ctx.elicit()` to send a prompt back through the MCP client asking the user to confirm: "Permanently delete observation #48291? Bombus vosnesenskii on 2025-06-15." The user sees this in their editor (e.g., VS Code) and can confirm or cancel. If canceled, the tool returns "Deletion cancelled." The server can include details about what will be deleted because it has already looked up the record in the database.

### Demo: elicitation in VS Code

![VS Code showing elicitation dialog with observation details and True/False options](slide_images/slide_34.png)
[Watch from 16:19](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=979s)

In VS Code, when the user asks to delete observation 319809831, the `delete_observation` tool runs and triggers an elicitation dialog. It displays: "You're about to permanently delete: Observation #319809831 — Apis mellifera (Western Honey Bee) Observed 2025-10-09 at (37.791, -122.436) Quality: research. Proceed?" The user selects True or False and clicks Submit. This gives the user full context about what will be deleted before confirming.

Elicitation is also useful beyond destructive operations — for resolving ambiguity in user queries, refining parameters, or suggesting alternative queries when a request would be too expensive (like narrowing a 200km search radius to 50km).

[Full server code: servers/level5_elicitation.py](https://github.com/pamelafox/mcp-for-postgres-db-demo/blob/main/servers/level5_elicitation.py)

## Tool selection

### The tool selection problem

![Two similar tools for current vs. historical data](slide_images/slide_36.png)
[Watch from 17:19](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=1039s)

As you build more tools, agents must select between them. When tools are similar, agents can pick the wrong one. In this experiment, two tools exist: `search_observations` (2020-present) and `search_historical_observations` (before 2020). Both descriptions explicitly say "call both tools" for comprehensive queries spanning all years. The agent information consists of tool names, parameters, and descriptions — this is all prompt engineering.

### Experiment results

![Results showing agents fail to call both tools for ambiguous queries](slide_images/slide_40.png)
[Watch from 19:01](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=1141s)

When queries explicitly reference both time periods ("past and present," "compare 2010 vs 2024"), the agent correctly calls both tools. But for vaguer queries like "any leafcutter bees ever seen near SF?", "include all years," or "full history of observations," the agent only calls one tool. The description's suggestion to "call both" did not work. The data split is too ambiguous for the agent to reliably handle.

### Don't make the agent choose

![Recommendations for fixing tool selection problems](slide_images/slide_41.png)
[Watch from 20:01](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=1201s)

When two tools are too similar, possible fixes include: return a hint in tool results saying "this only covers 2020+, also call the other tool"; add a `search_all_observations` tool that queries both tables internally so the agent never sees the data split; or refactor the database tables to keep everything in one table. More generally, if the agent cannot reliably distinguish between tools, merge them, improve descriptions and names, or set up evaluations to measure tool selection accuracy and iterate on design.

## Final words

### Which approach should you use?

![Summary showing when to use each approach with security layers](slide_images/slide_43.png)
[Watch from 21:46](https://www.youtube.com/watch?v=3_JPHuXgDyQ&t=1306s)

Free-form SQL suits internal prototyping where you need maximum flexibility. Read-only SQL works well for data analytics use cases — add a parser, timeout, and row limit. Fully typed tools are best for production and user-facing scenarios — add elicitation for destructive operations. Across all approaches, always enforce DB-level permissions with a least-privilege role and read-only transactions. Mix and match these techniques based on your situation. Building MCP servers for databases empowers users to interact with data through natural language, but design your tools with safety in mind.

Slides: [pamelafox.github.io/mcp-for-postgres-db-demo](https://pamelafox.github.io/mcp-for-postgres-db-demo/)

Code: [github.com/pamelafox/mcp-for-postgres-db-demo](https://www.github.com/pamelafox/mcp-for-postgres-db-demo/)
