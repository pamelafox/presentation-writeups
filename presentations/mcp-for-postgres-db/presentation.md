# An MCP for your Postgres DB

- **Date:** 2026-06-16
- **Video:** https://www.youtube.com/watch?v=3_JPHuXgDyQ
- **Slides:** https://pamelafox.github.io/mcp-for-postgres-db-demo/
- Code: https://github.com/pamelafox/mcp-for-postgres-db-demo

## Abstract

In this talk, we're exploring what it looks like to build an MCP server for a PostgreSQL database. Using Python and FastMCP, we'll look at how different tool designs affect how accurately, efficiently, and safely an LLM can turn user requests into database queries.

We'll compare multiple approaches, from free-form SQL to read-only SQL to fully typed tools, and discuss the tradeoffs of each. Along the way, we'll look at common failure modes like accidental mutations, expensive queries, and mismatches between user intent and executed SQL, then show how elicitation and careful tool design can make database-connected agents more reliable.