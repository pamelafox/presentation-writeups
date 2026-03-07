## Slide 1

![Slide 1](slide_images/slide_1.png)

```
RAG with JavaScript
  From Concepts to Code
aka.ms/ragjs/slides


    aka.ms/ragjs/slides

  Pamela Fox

  Principal Cloud Advocate
  www.pamelafox.org
```

## Slide 2

![Slide 2](slide_images/slide_2.png)

```
The limitations of LLMs

                            Outdated public knowledge




    No internal knowledge
```

## Slide 3

![Slide 3](slide_images/slide_3.png)

```
Integrating domain knowledge




       Fine                     Retrieval
      tuning                   Augmented
                               Generation
   Learn new skills
    (permanently)              Learn new facts
                                (temporarily)

    High cost, time
```

## Slide 4

![Slide 4](slide_images/slide_4.png)

```
RAG in the wild
                                    GitHub Copilot (RAG on VS Code workspace)
Teams Copilot (RAG on your chats)




              Copilot
    (RAG on the web)
```

## Slide 5

![Slide 5](slide_images/slide_5.png)

```
Simple RAG flow


                                                                       The Prius V has an
                                                                       acceleration of 9.51
 How fast is the Prius V?                                              seconds from 0 to 60 mph.




                                     vehicle | year | msrp | acceleration |
                                      --- | --- | --- | --- | --- | ---
                                     Prius (1st Gen) | 1997 | 24509.74 | 7.46 |
    User                    Search   Prius (2nd Gen) | 2000 | 26832.25 | 7.97 |
                                                                                  Language Model
                                     Prius (3rd Gen) | 2009 | 24641.18 | 9.6 |
   Question                          Prius V | 2011 | 27272.28 | 9.51 |
                                     Prius C | 2012 | 19006.62 | 9.35 |
                                     Prius PHV | 2012 | 32095.61 | 8.82 |
                                     Prius C | 2013 | 19080.0 | 8.7 |
                                     Prius | 2013 | 24200.0 | 10.2 |
                                     Prius Plug-in | 2013 | 32000.0 | 9.17 |
```

## Slide 6

![Slide 6](slide_images/slide_6.png)

```
RAG flow with multiturn support

 How fast is the Prius V?                                                            Here are the acceleration times for
                                                                                     the Honda Insight models:
                                                                                     - Insight (2010): 9.17 seconds
 The Prius V has an                                                                  - Insight (2011): 9.52 seconds
 acceleration of 9.51                                                                ...
 seconds from 0 to 60 mph.


 how fast is Insight?




                        "how fast is insight"            vehicle | year | msrp | acceleration | mpg
                                                         --- | --- | --- | --- | --- | ---
    User                                        Search   Insight | 2010 | 19859.16 | 9.17 | 41.0        Large
                                                         Insight | 2011 | 18254.38 | 9.52 | 41.0
   Question                                              Insight | 2012 | 18555.28 | 9.42 | 42.0      Language
                                                                                                        Model
```

## Slide 7

![Slide 7](slide_images/slide_7.png)

```
RAG flow with multiturn + query rewriting

How fast is the Prius V?

                                                                                    The 2011 Insight has an
 The Prius V has an                                                                 acceleration time of 9.52
 acceleration of 9.51                                                               seconds.
 seconds from 0 to 60 mph.


 what about the insigt?




                                      insight speed            vehicle | year | msrp | acceleration | mpg
                                                               --- | --- | --- | --- | --- | ---
    User                     Large                    Search   Insight | 2010 | 19859.16 | 9.17 | 41.0
                                                               Insight | 2011 | 18254.38 | 9.52 | 41.0
                                                                                                              Large
   Question                Language                            Insight | 2012 | 18555.28 | 9.42 | 42.0      Language
                             Model                                                                            Model
```

## Slide 8

![Slide 8](slide_images/slide_8.png)

```
RAG data source types




             Database rows                                        Documents
            (Structured data)                                 (Unstructured data)
                                                         PDFs, docx, pptx, md, html, images

You need a way to vectorize target columns      You need an ingestion process
with an embedding model.                        for extracting, splitting, vectorizing,
                                                and storing document chunks.

You need a way to search the vectorized rows.   You need a way to search the vectorized chunks.
```

## Slide 9

![Slide 9](slide_images/slide_9.png)

```
Vector embeddings
```

## Slide 10

![Slide 10](slide_images/slide_10.png)

```
Vector embeddings

A vector embedding represents an input (text/phrase/image/etc) as a list of
numbers, a vector in a multi-dimensional space.


  A big dog            Embedding               0.052703    -0.028099   4.963873
                         model
     text                                                    vector


  A small cat          Embedding               -0.009188   -0.035375   -0.009242
                         model
     text                                                    vector

A vector embedding model is trained specifically to convert inputs into a vector,
using massive training data sets and architectures similar to LLM models.
```

## Slide 11

![Slide 11](slide_images/slide_11.png)

```
Vector embedding models
Different embedding models output different embeddings with varying lengths.
The goal of all models is to capture the meaning.

 Embedding model                   Encodes                    Vector length
 Sbert (Sentence-Transformers)     text (up to ~400 words)    768
 OpenAI text-embedding-ada-002     text (up to 8191 tokens)   1536
 OpenAI text-embedding-3-small     text (up to 8191 tokens)   256 - 1536
 OpenAI text-embedding-3-large     text (up to 8191 tokens)   256 - 3072
 nomic-embed-text                  text (up to 8191 tokens)   768
 Azure AI Vision                   image or text              1024


MTEB: https://huggingface.co/spaces/mteb/leaderboard
```

## Slide 12

![Slide 12](slide_images/slide_12.png)

```
Generating an embedding in JavaScript
Configure OpenAI SDK (e.g. with models hosted on Microsoft Foundry):

import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.AZURE_OPENAI_API_KEY,
  baseURL: process.env.AZURE_OPENAI_ENDPOINT});

Generate embedding:
const response = await client.embeddings.create({
  model: "text-embedding-3-small",
  dimensions: 1536,
  input: "hello world"
});
```

## Slide 13

![Slide 13](slide_images/slide_13.png)

```
Measuring vector similarity

We compute embeddings so that we can calculate similarity between inputs.
The most common distance measurement is cosine similarity.

 function cosineSimilarity(v1, v2) {

     const dotProduct = v1.reduce(
       (sum, a, i) => sum + a * v2[i], 0);

     const magnitude =
       Math.sqrt(v1.reduce((sum, a) => sum + a ** 2, 0)) *
       Math.sqrt(v2.reduce((sum, a) => sum + a ** 2, 0));

     return dotProduct / magnitude;
 }
```

## Slide 14

![Slide 14](slide_images/slide_14.png)

```
Vector search

1       Compute the embedding vector for the query
2      Find K closest vectors for the query vector
       • Search exhaustively or using approximations


      Query                                  Query vector                         K closest vectors
                     Compute                                       Search
                  embedding vector                            existing vectors



                                           [-0.003335318, -                      [[“snake”, [-0.122, ..],
    “tortoise”       Compute               0.0176891904,…]         Search         [“frog”, [-0.045, ..]]]
                   embedding with                             existing vectors
                      OpenAI
```

## Slide 15

![Slide 15](slide_images/slide_15.png)

```
ANN (Approximate Nearest Neighbor) search
There are multiple ANN search algorithms that can speed up search time.

Algorithm              JS library                Database support

HNSW                   hnswlib-node              PostgreSQL pgvector extension
                                                 Azure AI Search
                                                 Chromadb
                                                 Weaviate

DiskANN                (server-side only)        Cosmos DB, Azure SQL,
                                                 Azure Database for PostgreSQL

IVFFlat                faiss-node                PostgreSQL pgvector extension

Faiss                  faiss-node                None, in-memory index only
```

## Slide 16

![Slide 16](slide_images/slide_16.png)

```
Optimal search strategy
```

## Slide 17

![Slide 17](slide_images/slide_17.png)

```
Vector search is NOT enough!

                                                                                Hybrid +
                                  Keyword          Vector        Hybrid
 Query type                                                               Semantic ranker
                                [NDCG@3]        [NDCG@3]      [NDCG@3]
                                                                              [NDCG@3]
  Concept seeking queries              39             45.8         46.3              59.6
 Fact seeking queries                37.8              49          49.1              63.4
 Exact snippet search                51.1             41.5           51              60.8
 Web search-like queries             41.8             46.3           50              58.9
 Keyword queries                     79.2             11.7           61              66.9
 Low query/doc term overlap            23             36.1         35.9              49.1
 Queries with misspellings           28.8             39.1         40.6              54.6
 Long queries                        42.7             41.6         48.1              59.4
 Medium queries                      38.1             44.7         46.7              59.9
 Short queries                       53.1             38.8           53              63.9


Source: Outperforming vector search with hybrid + reranking
```

## Slide 18

![Slide 18](slide_images/slide_18.png)

```
Hybrid search: The best of both worlds!

Complete search stacks do better:
  Hybrid retrieval (keywords + vectors) > pure-vector or keyword
  Hybrid + Reranking > Hybrid




           Keywords

                                      Fusion                    Reranking
                                      (RRF)                     model       Let's break
                                                                            those down...
           Vector
```

## Slide 19

![Slide 19](slide_images/slide_19.png)

```
Keyword search                                                                     Best for: exact phrase matches


Documents are stored in an inverted index which can be queried efficiently.

  ID      Name                  Description                                 Term           Document List
                                Porous soaker hose for efficient water      hose           335, 336
  335     Soaker Hose 25-foot
                                delivery directly to plant roots.           foot           335, 336
                                Heavy-duty garden hose with brass           garden         335
  334     Garden Hose 50-foot
                                fittings and kink-resistant construction.
                                                                            25             336


                                                                            ID      Document List              Relevance
                                         Full text search of
  “25 foot hose”                                                            335     Soaker Hose 25-foot        0.066
                                        name + description
                                                                            336     Expandable Hose 100-foot   0.046
                                                                            334     Garden Hose 50-foot        0.046
                                                                            312     Drain Snake 25-foot        0.040



        Tip: BM25 is the best algorithm, but other inverted index
        algorithms are also effective.
```

## Slide 20

![Slide 20](slide_images/slide_20.png)

```
Vector search                                                     Best for: conceptually similar matches



 1. Encode queries as embeddings (lists of floating point numbers)
 2. Find semantically similar documents by comparing embeddings


      Query               Compute                  Query vector                                K closest vectors
                                                                           Search
                         embedding
 “garden watering                             [-0.003335318, -        existing vectors
                           vector
     supplies”                                0.0176891904,…]



                                                                                                       Cosine
                                                                       ID    Name                      Similarity
                                                                       335   Soaker Hose 25-foot       0.51
                                                                       336   Garden Hose 50-foot       0.51
    Tip: Use approximation algorithm                                   338   Retractable Hose Hanger   0.46
    (HNSW or DiskANN) for more efficient search.
```

## Slide 21

![Slide 21](slide_images/slide_21.png)

```
RRF: Reciprocal Rank Fusion
Using text and vector search? Merge results using RRF to rank results based off their relative ranks.



                             Rank Product
                             #1   Drinking Water Safe Hose
                  Keywords
                             #2   Garden Soil Enriched
                  search
                             #3   Self-Watering Planter
                                                                                        RFF     Product
                             #4   Garden Hose 50-foot        Reciprocal Rank
“garden                                                                                 0.0318 Drinking Water Safe Hose
watering                                                     Fusion                     0.0315 Self-Watering Planter
supplies”                                                    1/(k+rank₁) +1/(k+rank₂)
                                                             (k=60)                     0.0315 Garden Hose 50-Foot
                             Rank Product
                                                                                        0.0307 Misting Sprinkler Kit
                  Vector     #1   Misting Sprinkler Kit
                  search     #2   Soaker Hose 25-foot
                             #3   Garden Hose 50-foot
                             #4   Self-Watering Planter
```

## Slide 22

![Slide 22](slide_images/slide_22.png)

```
Re-ranking
A re-ranker model gives documents a relevance score according to the query.




                           Product                                 Score    Product
 “garden                   Drinking Water Safe Hose                0.3184   Soaker Hose 25-foot
watering        Search     Self-Watering Planter       Re-ranker   0.3043   Misting Sprinkler Kit
supplies”                  Garden Hose 50-Foot                     0.2925   Drinking Water Safe Hose
                           Misting Sprinkler Kit                   0.2672   Garden Hose 50-foot




       Tip: Cross-encoder models (like Cohere Reranker) are best, but LLMs can be used as well.
```

## Slide 23

![Slide 23](slide_images/slide_23.png)

```
A complete hybrid search flow
Question: "garden watering supplies"


                         Keyword
                         results

                    Drinking Water
                1
                    Safe Hose
                                                     Fusion                      Reranking
                2   Garden Soil Enriched             (RRF)


                                                Drinking Water
                                            1                           1   Soaker Hose 25-foot
                                                Safe Hose
                         Vector
                         results            2   Self-Watering Planter   2   Misting Sprinkler Kit

                                                                            Drinking Water
                1   Misting Sprinkler Kit   3   Garden Hose 50-Foot     2
                                                                            Safe Hose

                2   Soaker Hose 25-foot     3   Misting Sprinkler Kit   2   Garden Hose 50-Foot
```

## Slide 24

![Slide 24](slide_images/slide_24.png)

```
Hybrid search is supported on many Azure databases

Database          Vector search?         Keyword search?   RRF?   Re-ranker?

Azure Database       pgvector
                                             fts                     azure_ai.rank()
for PostgreSQL       HNSW/IVF/DiskANN



Azure AI Search      HNSW                    BM25



                     VectorDistance()
Azure Cosmos DB      DiskANN
                                             BM25                    (Public preview)



                     vector_distance()
Azure SQL            DiskANN
                                             BM25
```

## Slide 25

![Slide 25](slide_images/slide_25.png)

```
Data ingestion
```

## Slide 26

![Slide 26](slide_images/slide_26.png)

```
RAG document ingestion
For long/unstructured documents, we need an ingestion flow such as this one:
                                                                                                      [{"id": "chunk1",
                                                                                                         "doc": "bee.pdf",
                                                                                                         "text": "the bee...",
                                                                                                          "vec": [0.1234..]}]

PDF      Azure Document                        Langchain                    Azure OpenAI                        JSON
           Intelligence


      Extract text from PDF              Split data into chunks          Vectorize chunks           Store chunks
      Other options for this step:       Split text based on sentence    Compute embeddings using   This is where you'd typically use
      Azure Document Intelligence,       boundaries and token lengths.   embedding model of your    a search service like
      Langchain document loaders,                                        choosing.                  Azure AI Search or a database
      OCR services, Unstructured, etc.   You could also use "semantic"                              like PostgreSQL or Cosmos DB.
                                         splitters and your own custom
                                         splitters.
```

## Slide 27

![Slide 27](slide_images/slide_27.png)

```
Why do we need to split documents?

1   LLMs have limited context              75

    windows (128K – 1M)                    70



    When an LLM receives too               65

                                Accuracy
2

    much information, it can               60
    get easily distracted by
    irrelevant details.                    55


                                           50
3   The more tokens you send,                   5             10              15               20              25               30

    the higher the cost, the                               Number of documents in input context
    slower the response.
                                    Source: Lost in the Middle: How Language Models Use Long Contexts, Liu et al. arXiv:2307.03172
```

## Slide 28

![Slide 28](slide_images/slide_28.png)

```
Optimal size of document chunk
How big should chunks be?                        Where to split chunks?

# of tokens per chunk              Recall@50     Chunk boundary strategy         Recall@50
512                                       42.4   Break at token boundary                40.9
1024                                      37.5   Preserve sentence boundaries           42.4
4096                                      36.4   10% overlapping chunks                 43.1
8191                                      34.9   25% overlapping chunks                 43.9
Source: aka.ms/ragrelevance                      Source: aka.ms/ragrelevance

A token is the unit of measurement for an        A chunking algorithm should also consider
LLM's input/output. ~1 token/word for            tables, and avoid splitting tables when
English, higher ratios for other languages.      possible.
More on token ratios: aka.ms/genai-cjk
```

## Slide 29

![Slide 29](slide_images/slide_29.png)

```
More RAG approaches
```

## Slide 30

![Slide 30](slide_images/slide_30.png)

```
Graph RAG                                                                                      https://www.microsoft.com/research/project/graphrag/

                                            Information Extraction                                       Graph Induction                                 Dataset Question Generator
                                                                                                                                                         Summarized Q&A
                                                  POK leader Sylvia                                                                                      etc.
                                                  Marek took the
                                                  stage with Lucio                   GraphRAG

                                                  Jakab, founder of
                                                  Save our
                                                  Wildlands




                                                                                                                                                                               GraphRAG
                                 - Too large for context window                                                                Hierarchy extraction
                                                                                 Graph ML
                                                                                                                   GraphRAG
                                 - “Semantic Search” works, but                                                                Graph embedding
                                   we know nothing of the                                 •    Topic detection                 Entity summarization
                                   dataset!                                      •     Representation Learning                 Community summarization


                                             Semantic Search DB


                                                                             Entity Content
                                                                                     GraphRAG




Larsson, J. (2024, May 5). *GraphRag*. YouTube. https://youtu.be/r09tJfON6kE?si=r5V-w4VlxAzFQcu5           Level 0 Community                 Level 1 Communities        Level 2 Communities
```

## Slide 31

![Slide 31](slide_images/slide_31.png)

```
RAG with graph queries                                          https://aka.ms/agentic-shop

Azure PostgreSQL + AGE can use Cypher graph queries to query across relationships:

                                                           These are the noise-cancelling
                                                           headphones with long battery life,
  I wanna buy a headphone                                  according to customer reviews:
  with noise cancellation and                              1. Vyron Wireless Bluetooth Headphone
  good reviews on battery life                             ....




                                                      find headphone
                                                      products with
                                                      noise cancellation
                                                      feature and with

      User                         Large     Graph
                                                      reviews with
                                                      positive sentiment
                                                                                      Large
     Question                    Language    query    about battery life            Language
                                   Model                                              Model
```

## Slide 32

![Slide 32](slide_images/slide_32.png)

```
Agentic RAG across multiple sources
  Azure AI Search knowledge bases use LLMs for query planning and source selection:
                                                                     Knowledge sources            Output

                                                                       Search Indexes             Merged
   Input                                                                                          results
                                    Search query 1                        OneLake
Conversation                                                                                    Activity log
                   Query
                  planning          Search query 2                       SharePoint

                                                                                                  Answer
                                                                            Bing                 synthesis

                                     Iterative retrieval

           Search step uses hybrid search with semantic re-ranking when supported by the knowledge source
```

## Slide 33

![Slide 33](slide_images/slide_33.png)

```
Evaluation
```

## Slide 34

![Slide 34](slide_images/slide_34.png)

```
What affects the quality of a RAG flow?




 Question                Search                           Large Language Model

             Search engine (ie. Azure AI Search)          • System prompt
             Search query cleaning                        • Language
                                                           • Message history
             Search options (hybrid, vector, reranker)
                                                           • Model (ie. GPT 3.5)
             Additional search options                    • Temperature (0-1)
             Data chunk size and overlap                  • Max tokens
             Number of results returned
```

## Slide 35

![Slide 35](slide_images/slide_35.png)

```
Are the answers high quality?

 Are they correct? (relative to the knowledge base)
 Are they clear and understandable?
 Are they formatted in the desired manner?
                                                                              Yes, according to the information provided in the
  Do the perks cover underwater activities?                                   PerksPlus.pdf document, underwater activities such
                                                                              as scuba diving are covered under the program.

                Yes, the perks provided by the PerksPlus Health and Wellness Reimbursement Program cover a wide
                range of fitness activities, including underwater activities such as scuba diving. The program aims to
                support employees' physical health and overall well-being, so it includes various lessons and
                experiences that promote health and wellness. Scuba diving lessons are specifically mentioned as one
                of the activities covered under PerksPlus. Therefore, if an employee wishes to pursue scuba diving as a
                fitness-related activity, they can expense it through the PerksPlus program.

  Yes, underwater activities are included as part of the PerksPlus program.
  Some of the underwater activities covered under PerksPlus include
  scuba diving lessons [PerksPlus.pdf#page=3].
```

## Slide 36

![Slide 36](slide_images/slide_36.png)

```
Manual evaluation
Humans can spot-check output for small data sets and annotate issues:
```

## Slide 37

![Slide 37](slide_images/slide_37.png)

```
Automated evaluation
AI models can measure output performance at scale across larger data sets:
```

## Slide 38

![Slide 38](slide_images/slide_38.png)

```
Automated evaluation frameworks

Framework                            Author               Language     Cloud hosted?


azure-ai-evaluation /                Microsoft            Python       Optional
Microsoft.Extensions.AI.Evaluation                        .NET
RAGAS                                ExplodingGradients   Python       None

DeepEval                             ConfidentAI          Python       Optional

Langsmith                            Langchain            Python       Required


Promptfoo                            Promptfoo            JavaScript   Optional
```

## Slide 39

![Slide 39](slide_images/slide_39.png)

```
LLM-based quality evaluation
Use an LLM-as-a-judge to score the output from the RAG flow:

                                    How grounded is               How similar is response
                                     the response?                   to ground truth?



     Query | Context | Response | Ground truth
 Do the perks cover     [PerksPlus.pdf]: Perks   Yes, underwater activities   Yes, underwater activities are
 underwater             include recreational     such as scuba diving are     included as part of the PerksPlus
 activities?            activities like...       covered under the program.   program. [PerksPlus.pdf#page=3].




                      How relevant is the response?

Run evaluation across a large data set that represents a range of user queries.
```

## Slide 40

![Slide 40](slide_images/slide_40.png)

```
Review evaluation metrics
Compare metrics across runs so you can see which increased/decreased:




Tip: Include metrics like latency and length, since a quality
increase might not be worth an increase in cost/latency.
```

## Slide 41

![Slide 41](slide_images/slide_41.png)

```
Compare individual answers
Once you see the difference in metrics, compare answers with changed scores:
```

## Slide 42

![Slide 42](slide_images/slide_42.png)

```
Lessons learnt from evaluating RAG apps

  RAG on data that you know; LLMs can be convincingly wrong.
  What works better for 3 Qs doesn't always work better for 200.
  Don't trust absolute metrics, trust relative metrics.
  Vector search can be noisy! Use wisely.
  Your model choice makes a huge difference.
  Remove the fluff from prompts; it doesn't matter.



    Subscribe to Hamel Husain for evaluation tips:
https://hamel.dev/blog/posts/evals-faq/


    https://hamel.dev/blog/posts/evals-faq/
```

## Slide 43

![Slide 43](slide_images/slide_43.png)

```
Code walkthrough
```

## Slide 44

![Slide 44](slide_images/slide_44.png)

```
Open source RAG solution
                                                                 Data type:
                                                                   Documents (PDF)

                                                                 Search:
                                                                   Cosmos DB

                                                                 LLM:
                                                                   Azure OpenAI (GPT 4o)
                                                                   Ollama (Llama3.1)

                                                                 Features:
                                                                   Multi-turn streaming chat
                                                                   Chat session history

 https://github.com/azure-samples/serverless-chat-langchainjs/
```

## Slide 45

![Slide 45](slide_images/slide_45.png)

```
Opening the project: 3 options

  GitHub Codespaces →


  VS Code with Dev Containers extension


  Your Local Environment
    Node LTS
    Azure Developer CLI
    Azure Functions Core Tools
    Git

https://github.com/azure-samples/serverless-chat-langchainjs/?tab=readme-ov-file#getting-started
```

## Slide 46

![Slide 46](slide_images/slide_46.png)

```
Deploying with the Azure Developer CLI (azd)

Prerequisites:
• Azure account and subscription
• Azure account permissions:
   • Microsoft.Authorization/roleAssignments/write
   • Microsoft.Resources/deployments/write on subscription level


Login to your Azure account:
 azd auth login



Provision resources, deploy app, and ingestion documents:
 azd up
```

## Slide 47

![Slide 47](slide_images/slide_47.png)

```
Data ingestion process

                      documents-post.ts
                      postDocuments()


       POST

      api/documents

PDF                      Azure            Langchain.js       Azure        Azure           Azure
                       Functions                            OpenAI      Cosmos DB      Blob Storage

                                           Extract text     Vectorize   Store chunks        Store
                                            from PDF         chunks                      document
                                                                                       (for citations)
                                          Split data into
                                              chunks
                                                 .
```

## Slide 48

![Slide 48](slide_images/slide_48.png)

```
Application architecture

                 Typescript frontend                               NodeJS backend
                      (Lit + Vite)                       (Azure Functions v4 + Langchain.js)
 chat.ts                api.ts            POST                chats-post.ts
 ChatComponent          getCompletion()                       postChats()
                                          chats/stream

                                                              // Search the DB
                                                              retriever.invoke()
                                                                                            Cosmos
                                                                                              DB
                                                              // Combine prompt + results
                                                              createStuffDocumentsChain()
                                                                                             Azure
                                                                                            OpenAI


                  Azure Static Web Apps                                 Azure Functions
```

## Slide 49

![Slide 49](slide_images/slide_49.png)

```
Next steps

Deploy the app and customize for your own data!
https://github.com/Azure-Samples/serverless-chat-langchainjs

Check out my RAG deep dive series:
https://aka.ms/ragdeepdive/watch

Post in the Foundry Discord when you have questions:
https://aka.ms/foundry/discord
```
