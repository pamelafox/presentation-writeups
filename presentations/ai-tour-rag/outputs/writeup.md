# Advanced retrieval for your AI apps and agents on Azure

This talk covers how to build production-ready retrieval for AI agents on Azure. It walks through the full hybrid search stack (keyword + vector + reranking), demonstrates graph-based retrieval with Azure Database for PostgreSQL using Apache AGE, and introduces agentic retrieval with Azure AI Search knowledge bases that can plan queries, search multiple sources, and iterate to find better answers.

## Table of contents

- [Most agents need to find relevant context](#most-agents-need-to-find-relevant-context)
- [RAG grounds LLM responses in retrieved context](#rag-grounds-llm-responses-in-retrieved-context)
- [Users need agents to find all sorts of things](#users-need-agents-to-find-all-sorts-of-things)
- [Agenda](#agenda)
- [Different queries need different search strategies](#different-queries-need-different-search-strategies)
- [Hybrid search: the best of both worlds](#hybrid-search-the-best-of-both-worlds)
- [Keyword search with BM25](#keyword-search-with-bm25)
- [Vector search with embeddings](#vector-search-with-embeddings)
- [Reciprocal rank fusion merges results](#reciprocal-rank-fusion-merges-results)
- [Re-ranking scores results by relevance](#re-ranking-scores-results-by-relevance)
- [A complete hybrid search flow](#a-complete-hybrid-search-flow)
- [Hybrid search is supported on many Azure databases](#hybrid-search-is-supported-on-many-azure-databases)
- [Impact of hybrid search across query types](#impact-of-hybrid-search-across-query-types)
- [Hybrid search isn't always enough](#hybrid-search-isnt-always-enough)
- [Agentic graph RAG with Azure Database for PostgreSQL](#agentic-graph-rag-with-azure-database-for-postgresql)
- [Users ask hard questions about relational data](#users-ask-hard-questions-about-relational-data)
- [RAG with graph queries](#rag-with-graph-queries)
- [Apache AGE on Azure Database for PostgreSQL](#apache-age-on-azure-database-for-postgresql)
- [Building the graph with semantic operators](#building-the-graph-with-semantic-operators)
- [Querying the graph for complex relationships](#querying-the-graph-for-complex-relationships)
- [Demo: agentic shop with Azure Database for PostgreSQL](#demo-agentic-shop-with-azure-database-for-postgresql)
- [Azure Database for PostgreSQL resources](#azure-database-for-postgresql-resources)
- [Agentic retrieval with Azure AI Search](#agentic-retrieval-with-azure-ai-search)
- [Users ask hard questions about unstructured data](#users-ask-hard-questions-about-unstructured-data)
- [Agentic retrieval with Azure AI Search knowledge base](#agentic-retrieval-with-azure-ai-search-knowledge-base)
- [Retrieval reasoning effort levels](#retrieval-reasoning-effort-levels)
- [Minimal effort: search across sources without LLMs](#minimal-effort-search-across-sources-without-llms)
- [Example of minimal effort](#example-of-minimal-effort)
- [Low effort: query planning and answer synthesis](#low-effort-query-planning-and-answer-synthesis)
- [Example of low effort with Bing web knowledge](#example-of-low-effort-with-bing-web-knowledge)
- [Medium effort: iterative retrieval](#medium-effort-iterative-retrieval)
- [Example of medium effort](#example-of-medium-effort)
- [Demo: open source RAG chat with agentic retrieval](#demo-open-source-rag-chat-with-agentic-retrieval)
- [Azure AI Search resources](#azure-ai-search-resources)
- [Design your agentic flows carefully](#design-your-agentic-flows-carefully)
- [Q&A](#qa)

## Most agents need to find relevant context

![Four Zava agents that each need different types of data](slide_images/slide_3.png)
[Watch from 00:31](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=31s)

Most AI agents need the ability to find information to complete their tasks. Consider the agents used by Zava, a fictional home improvement store. A shopper agent finds products from a relational database. An interior design agent searches through design images. An inventory agent tracks stock levels. An HR agent searches through thousands of company documents. Agents need ways to search many types of data — relational, unstructured, and images.

## RAG grounds LLM responses in retrieved context

![RAG flow: user question → search → results → LLM → cited answer](slide_images/slide_4.png)
[Watch from 01:22](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=82s)

Retrieval-Augmented Generation (RAG) is the technique where an agent retrieves relevant information and sends it to an LLM along with the user's question. The LLM then answers the question citing the retrieved results. When a user asks "what's the best paint for bathroom walls?", the search returns multiple paint options, and the LLM recommends the Interior Semi-Gloss Paint based on its moisture resistance and washability. Citations in the response indicate the agent used RAG — the answer is grounded in real data, not just model weights.

## Users need agents to find all sorts of things

![Four example queries from general to specific to Spanish](slide_images/slide_5.png)
[Watch from 02:18](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=138s)

User queries vary enormously. Some are short and general ("garden watering supplies"), some are specific ("at least 25 feet drip hose"), and some are in a different language ("manguera de 25 pies"). An agent should find great results for all of these.

## Agenda

![Agenda: optimal search strategies, graph-based retrieval with PostgreSQL, agentic retrieval with Azure AI Search](slide_images/slide_6.png)
[Watch from 03:02](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=182s)

The talk covers three areas: optimal search strategies that work across many Azure databases, graph-based retrieval with Azure Database for PostgreSQL, and agentic retrieval with Azure AI Search.

## Different queries need different search strategies

![Table comparing vector search and keyword search for different queries](slide_images/slide_8.png)
[Watch from 03:26](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=206s)

Keyword search and vector search each handle different queries well. Keyword search excels at exact phrase matches where the query terms appear directly in the data. Vector search excels at conceptually similar matches even when exact terms don't overlap. Neither strategy alone covers all query types.

## Hybrid search: the best of both worlds

![Hybrid search stack: keywords + vectors → RRF fusion → reranking model](slide_images/slide_9.png)
[Watch from 03:49](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=229s)

The optimal search strategy is a full hybrid search stack. Run keyword search and vector search in parallel, merge the results together using fusion, and apply a reranking step to ensure the best results are at the top. Research shows that hybrid retrieval outperforms pure vector or keyword search, and adding reranking improves results further.

## Keyword search with BM25

![Keyword search diagram with inverted index, BM25, and example results](slide_images/slide_10.png)
[Watch from 04:15](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=255s)

Keyword search stores documents in an inverted index and finds results containing the query terms in the highest frequency. The best algorithm is BM25, a probabilistic ranking function that accounts for term frequency relative to document length.

In a demo using a Zava product database on Azure Database for PostgreSQL, a keyword search for "25 foot drip hose" returns a 25-foot soaker hose as the top result — a good match. But result #5 is a 25-foot drain snake, which is irrelevant. Keyword search matches on the number "25" without understanding the semantic difference between a hose and a snake.

For the general query "garden watering supplies," keyword search returns a hose as #1 but a copper pipe as #2. For the Spanish query "manguera de 25 pies," keyword search returns mostly irrelevant results because the data is stored in English — it only matches on the number "25."

## Vector search with embeddings

![Vector search diagram: query → embedding → cosine similarity → K closest vectors](slide_images/slide_11.png)
[Watch from 08:40](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=520s)

Vector search uses an embedding model (like Azure OpenAI text-embedding-3) to encode both content and queries as vectors. A vector similarity metric finds the closest vectors to the query. Approximate algorithms like HNSW or DiskANN make this efficient across millions of vectors.

For "25 foot garden hose," vector search returns a 50-foot garden hose at #1 and the 25-foot hose at #3. Embeddings don't distinguish well between specific numbers — 25, 50, and 75 are all semantically similar. What matters more in the semantic space is the concept of "garden hose."

For "garden watering supplies," vector search shines. All five results are relevant: a sprinkler kit, hoses, and a self-watering planter. The embeddings encode the concept of garden watering even though none of the words match exactly. For the Spanish query, vector search also returns mostly hoses because the OpenAI embedding models were trained across multiple languages.

However, vector search still isn't perfect. For "100 foot hose that won't break," the 100-foot hose ranks #3 behind a 75-foot and 50-foot hose. Vector embeddings don't distinguish well between specific numbers, brand names, or IDs.

## Reciprocal rank fusion merges results

![RRF diagram: keyword ranks + vector ranks → merged scores](slide_images/slide_12.png)
[Watch from 13:21](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=801s)

Since both search strategies have strengths, use both and merge results with Reciprocal Rank Fusion (RRF). RRF calculates a score for each result based on its relative rank in each result set using the formula `1/(k + rank)` with k=60. If a result ranks highly in both keyword and vector results, it ranks highly in the merged output. If it's high in one but low in the other, it lands in the middle.

In a demo searching for "garden watering supplies," a drinking water safe hose was #1 for keyword and #5 for vector, ending up #1 in RRF. The misting sprinkler kit was #1 for vector but #10 for keyword, landing at #4 in RRF.

## Re-ranking scores results by relevance

![Re-ranker reorders merged results with relevance scores](slide_images/slide_13.png)
[Watch from 16:00](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=960s)

RRF alone isn't enough because both vector and keyword search can yield noisy results. A re-ranker model examines each result against the user query and assigns a relevance score. Cross-encoder models like Cohere Reranker are best for this since they were trained on human-scored search results. LLMs can also be used with the right system prompt.

In a demo using `azure_ai.rank()` (a built-in function in Azure Database for PostgreSQL that uses the Cohere ranking model), a soaker hose moved from #7 in RRF to #1 after reranking for the query "garden watering supplies." The reranker scores also enable setting a relevance threshold to discard completely irrelevant results.

## A complete hybrid search flow

![Full flow: keyword + vector → RRF → reranking](slide_images/slide_14.png)
[Watch from 18:39](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1119s)

The complete hybrid search flow takes the user's query and performs keyword search and vector search in parallel. The results merge via RRF. Finally, a reranking model produces the best ordering and can discard irrelevant results based on a score threshold.

## Hybrid search is supported on many Azure databases

![Table of Azure databases with hybrid search support](slide_images/slide_15.png)
[Watch from 19:09](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1149s)

Hybrid search works across multiple Azure databases. Azure Database for PostgreSQL uses pgvector with HNSW/IVF/DiskANN for vector search, built-in full-text search for keywords, SQL for RRF, and `azure_ai.rank()` with a Cohere model for reranking. Azure AI Search uses HNSW for vectors, BM25 for keywords, and handles both RRF and reranking automatically (using the same reranking model as Bing search). Azure SQL uses `vector_distance()` with DiskANN for vectors and BM25 for keywords. Azure Cosmos DB has built-in vector search with DiskANN, BM25 support, and a built-in RRF function, with reranker support in private preview.

## Impact of hybrid search across query types

![NDCG@3 scores table showing hybrid + semantic ranker outperforms other strategies](slide_images/slide_16.png)
[Watch from 21:03](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1263s)

Research from the Azure AI Search team demonstrates the impact of hybrid search. Keyword search scores well on keyword queries (79.2 NDCG@3) but poorly on concept-seeking queries (39). Vector search does the opposite. Hybrid search alone provides modest gains, but hybrid with semantic reranking consistently outperforms across all query types — concept seeking (59.6), fact seeking (63.4), exact snippet (60.8), queries with misspellings (54.6), and short queries (63.9).

## Hybrid search isn't always enough

![Three categories of hard queries: external knowledge, relational, multi-part](slide_images/slide_17.png)
[Watch from 21:30](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1290s)

Even with full hybrid search, some questions remain hard. Queries requiring external knowledge ("Do you carry pesticides approved for use in Berkeley, CA?") need a web search first. Queries about relations ("I want a cheap garden hose reviewed as highly as the expensive hoses") require joining across products and reviews. Multi-part questions ("What soil amendments do I need and which veggies grow with only afternoon sunlight?") bundle multiple searches into one.

## Agentic graph RAG with Azure Database for PostgreSQL

![Section title: Agentic Graph RAG with Azure Database for PostgreSQL](slide_images/slide_18.png)
[Watch from 22:35](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1355s)

Graph-based retrieval helps answer questions that involve relationships between different parts of a database, especially when users ask about products combined with reviews, categories, and sentiment.

## Users ask hard questions about relational data

![Example queries combining products with reviews and sentiment](slide_images/slide_19.png)
[Watch from 23:00](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1380s)

Users ask questions that span multiple tables: "I want a cheap garden hose that's reviewed as highly as the expensive hoses," "I want a headphone with noise cancellation and good reviews on battery life," "Which category of hedge trimmers are reviewed more highly, electric or gas?" These all require combining product data with reviews and sentiment analysis.

## RAG with graph queries

![Graph query RAG flow: user → LLM → graph query → database → LLM answer](slide_images/slide_20.png)
[Watch from 23:57](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1437s)

Instead of complex SQL joins, a graph query can efficiently traverse relationships. An LLM generates a graph query from the user's input, sends it to the database, and uses the results to answer the question. For a headphone with noise cancellation and good battery life reviews, the graph query traverses from products to features to reviews, filtering by positive sentiment.

## Apache AGE on Azure Database for PostgreSQL

![Apache AGE: Cypher + SQL hybrid queries, graph processing, analytics](slide_images/slide_21.png)
[Watch from 24:10](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1450s)

Apache AGE is a graph database extension for PostgreSQL, available as a native plugin on Azure. It provides both SQL and Cypher in the same engine, enabling hybrid relational and graph queries. This lets you combine relational data with graph traversal and layer analytics or visualization on top.

## Building the graph with semantic operators

![Graph construction: extract features and sentiment from reviews using azure_ai.extract()](slide_images/slide_22.png)
[Watch from 24:45](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1485s)

Graph construction starts with known products, their features, and raw customer reviews. The `azure_ai.extract()` function does two things: it extracts which product features are mentioned in each review, and it classifies the sentiment as positive, negative, or neutral. From there, graph nodes are created for products, features, and reviews. Edges connect them: products have features, products have reviews, and reviews point to features with sentiment edges. This turns unstructured review text into structured, queryable graph relationships.

## Querying the graph for complex relationships

![Cypher query finding headphone reviews with positive noise cancellation sentiment](slide_images/slide_23.png)
[Watch from 25:38](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1538s)

Once the graph is built, querying is straightforward. A Cypher query finds all product reviews that mention noise cancellation positively. Instead of chaining multiple SQL joins, the query traverses from a product to its reviews, then to features, and filters for positive sentiment. The result is a ranked list of products by positive mention count. This kind of question is messy in SQL but natural in a graph.

## Demo: agentic shop with Azure Database for PostgreSQL

![Agentic Shop demo with link aka.ms/agentic-shop](slide_images/slide_24.png)
[Watch from 26:24](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1584s)

A full end-to-end open source solution demonstrates an agentic shopping experience using graph queries. In the demo, searching for headphones with great noise cancellation triggers the agent to call a `query_reviews_with_sentiments` tool, filling in arguments for headphones, the noise cancellation feature, and positive sentiment. The agent uses command routing — it chooses between a simple search, a product query, or a graph-based review query. This routing approach is a middle ground between single-table search and a full NL-to-SQL approach. The code is available at [aka.ms/agentic-shop](https://aka.ms/agentic-shop).

## Azure Database for PostgreSQL resources

![Learning resources: blog post, learning path, team blog, VS Code extension](slide_images/slide_25.png)
[Watch from 28:52](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1732s)

Resources for Azure Database for PostgreSQL include a blog post explaining the agentic approach in detail at [aka.ms/pg-ai-agents-blog](https://aka.ms/pg-ai-agents-blog), a learning path on Microsoft Learn about using PostgreSQL with AI at [aka.ms/pg-ai-learn-path](https://aka.ms/pg-ai-learn-path), the team's blog at [aka.ms/azurepostgresblog](https://aka.ms/azurepostgresblog), and a VS Code extension for PostgreSQL at [aka.ms/pgsql-vscode](https://aka.ms/pgsql-vscode).

## Agentic retrieval with Azure AI Search

![Section title: Agentic retrieval with Azure AI Search](slide_images/slide_26.png)
[Watch from 29:24](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1764s)

Azure AI Search offers agentic retrieval through AI knowledge bases, a feature designed to handle complex queries about unstructured data.

## Users ask hard questions about unstructured data

![Three hard query types: multiple questions, chained queries, external knowledge](slide_images/slide_27.png)
[Watch from 29:37](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1777s)

Some queries require multiple searches to answer fully. A multi-part question like "What type of paint for a bathroom and what's the cost range?" is really two queries bundled together. A chained query like "Explain how to paint my house efficiently, then list Zava products and prices for each supply" requires results from the first query to inform the second. Queries requiring external knowledge need web results to supplement internal data.

## Agentic retrieval with Azure AI Search knowledge base

![Knowledge base architecture: query planning → knowledge sources → results merging → iterative retrieval](slide_images/slide_28.png)
[Watch from 30:09](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1809s)

Each Azure AI Search knowledge base has an agentic retrieval engine that handles query planning, knowledge source selection, and result merging. The query planning step uses an LLM to break a conversation into multiple queries and select which knowledge sources to use. Knowledge sources can include search indexes, OneLake, SharePoint, or Bing. Each query goes to the selected sources, results merge together, and an answer is synthesized with citations. If results are insufficient, the engine repeats the query planning phase with the results it already has.

## Retrieval reasoning effort levels

![Effort spectrum: minimal (low latency, low cost) → medium (highest quality, most agentic)](slide_images/slide_29.png)
[Watch from 31:26](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1886s)

Knowledge bases provide a retrieval reasoning effort control with three levels: minimal, low, and medium. Minimal is cheapest with lowest latency. Medium provides the highest quality with the most agentic behavior. There is no high level yet — the team is still defining what would be worth the additional cost.

## Minimal effort: search across sources without LLMs

![Minimal effort diagram: skips query planning, sends to all sources](slide_images/slide_30.png)
[Watch from 32:03](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1923s)

Minimal effort does not use any LLMs. It skips query planning, knowledge source selection, web sources, answer synthesis, and iterative retrieval. The search intent is sent directly to all configured knowledge sources, and results are merged. This is useful for switching an existing agent to knowledge bases before taking advantage of advanced features.

## Example of minimal effort

![Minimal effort example: paint query sent to search index and SharePoint](slide_images/slide_31.png)
[Watch from 32:33](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=1953s)

For "What's best Zava paint for bathroom walls?", minimal effort sends the query directly to both a search index and SharePoint. The search index returns product data (Interior Semi-Gloss Paint at $47.00 with a reranker score of 2.95) and SharePoint returns a blog post about semi-gloss paint for bathrooms (reranker score of 3.07). Results merge and return to the agent without synthesis.

## Low effort: query planning and answer synthesis

![Low effort diagram: includes query planning and answer synthesis](slide_images/slide_32.png)
[Watch from 33:20](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=2000s)

Low effort adds query planning, source selection, and answer synthesis. It does not include iterative retrieval. The LLM breaks the user question into sub-queries and selects which knowledge sources to query.

## Example of low effort with Bing web knowledge

![Low effort example with query planning: paint question → two sub-queries → web + index → synthesized answer](slide_images/slide_33.png)
[Watch from 33:38](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=2018s)

For "What's best Zava paint for bathroom walls, and how does it compare to other brand paints?", the knowledge base plans two queries: "paint for bathroom" and "cost of bathroom paint." It sends these to both the search index and Bing web. The search index returns product data, and Bing returns comparison articles. The engine synthesizes a complete answer with citations recommending semi-gloss interior paint for its moisture resistance, noting the $47.00 price point.

## Medium effort: iterative retrieval

![Medium effort diagram: adds iterative retrieval to low effort capabilities](slide_images/slide_34.png)
[Watch from 34:35](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=2075s)

Medium effort adds iterative retrieval on top of everything in low effort. After the first pass of query planning and search, the engine evaluates whether the results are sufficient. If not, it performs additional rounds of query planning and search.

## Example of medium effort

![Medium effort example: house painting query with two rounds of search](slide_images/slide_35.png)
[Watch from 35:06](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=2106s)

For "Explain how to paint my house most efficiently. Give me a list of Zava products and prices for each supply," the knowledge base first plans queries for "efficient house painting" and "Zava paint supplies prices," searching both the index and Bing. After reviewing results, it determines it needs more information and issues a second round of queries for "paint brushes rollers trays." The final synthesized answer covers painting technique (work top-down, rollers for large areas, brushes for detail) and lists specific Zava products with prices, all with citations to both internal product data and web sources.

## Demo: open source RAG chat with agentic retrieval

![Demo: RAG chat solution with links](slide_images/slide_36.png)
[Watch from 36:05](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=2165s)

An open source solution showcases agentic retrieval for conversational RAG applications. The demo shows the complex house painting query returning a detailed answer with citations from both web sources and internal product data. The thought process view reveals the initial query planning pass and the second pass with additional queries. The code is available at [aka.ms/ragchat](https://aka.ms/ragchat) with documentation at [aka.ms/ragchat/knowledgebase](https://aka.ms/ragchat/knowledgebase).

## Azure AI Search resources

![Get started links: Azure AI Search, Foundry IQ preview, quickstart notebook](slide_images/slide_37.png)
[Watch from 37:11](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=2231s)

To get started with Azure AI Search, visit [aka.ms/AISearch-new](https://aka.ms/AISearch-new). The Foundry IQ public preview is at [aka.ms/FoundryIQ](https://aka.ms/FoundryIQ). A Python quickstart notebook for agentic retrieval is available at [aka.ms/AISearch-ar-pyn](https://aka.ms/AISearch-ar-pyn).

## Design your agentic flows carefully

![Advice: evaluate at each step, retrieval affects quality, use automated evaluations](slide_images/slide_39.png)
[Watch from 37:39](https://www.youtube.com/watch?v=7W2xVNo2m6o&t=2259s)

When developing agentic flows or RAG systems, evaluate the system based on both its final output and how it arrived at that output. Retrieval is often the biggest factor affecting output quality. Improving retrieval might mean changing search strategies, adding more complex approaches, or changing the data preparation process. Use the Azure AI Evaluation SDK to set up automated evaluations that scientifically measure the impact of different search approaches, data preparation techniques, and models.

## Q&A
