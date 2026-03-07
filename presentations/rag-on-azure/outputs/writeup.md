# Building a RAG app to chat with your data

This talk covers how to build a Retrieval Augmented Generation (RAG) chat application on Azure. It introduces large language models, explains why RAG is needed and how hybrid search works, walks through an open-source RAG solution using Azure AI Search and OpenAI, and covers evaluation and observability techniques for production RAG apps.

## Table of contents

- [About the speaker](#about-the-speaker)
- [Agenda](#agenda)
- [What is a large language model](#what-is-a-large-language-model)
- [LLMs in use today](#llms-in-use-today)
- [GPT and the Transformer architecture](#gpt-and-the-transformer-architecture)
- [Using OpenAI GPT models in Azure Studio](#using-openai-gpt-models-in-azure-studio)
- [Using OpenAI GPT models in Python](#using-openai-gpt-models-in-python)
- [The limitations of LLMs](#the-limitations-of-llms)
- [Incorporating domain knowledge](#incorporating-domain-knowledge)
- [RAG: Retrieval Augmented Generation](#rag-retrieval-augmented-generation)
- [The benefit of RAG](#the-benefit-of-rag)
- [The importance of the search step](#the-importance-of-the-search-step)
- [Optimal search: hybrid search](#optimal-search-hybrid-search)
- [RAG with hybrid search](#rag-with-hybrid-search)
- [What is the RAG searching](#what-is-the-rag-searching)
- [Ways to build a RAG chat app on Azure](#ways-to-build-a-rag-chat-app-on-azure)
- [Copilot Studio: no-code RAG](#copilot-studio-no-code-rag)
- [Azure Studio On Your Data: low-code RAG](#azure-studio-on-your-data-low-code-rag)
- [Open-source RAG chat app solution](#open-source-rag-chat-app-solution)
- [Prerequisites](#prerequisites)
- [Opening the project](#opening-the-project)
- [Deploying with the Azure Developer CLI](#deploying-with-the-azure-developer-cli)
- [Application architecture on Azure](#application-architecture-on-azure)
- [Local data ingestion](#local-data-ingestion)
- [Integrated vectorization](#integrated-vectorization)
- [Code walkthrough](#code-walkthrough)
- [RAG orchestration libraries](#rag-orchestration-libraries)
- [More RAG chat app starter repositories](#more-rag-chat-app-starter-repositories)
- [Evaluating RAG chat apps](#evaluating-rag-chat-apps)
- [What affects the quality](#what-affects-the-quality)
- [Manual experimentation of settings](#manual-experimentation-of-settings)
- [Automated evaluation of app settings](#automated-evaluation-of-app-settings)
- [Ground truth data](#ground-truth-data)
- [Improving ground truth data sets](#improving-ground-truth-data-sets)
- [Running evaluations and comparing results](#running-evaluations-and-comparing-results)
- [Reviewing metrics across runs](#reviewing-metrics-across-runs)
- [Comparing answers across runs](#comparing-answers-across-runs)
- [Observability for RAG chat apps](#observability-for-rag-chat-apps)
- [Integration with Azure Monitor](#integration-with-azure-monitor)
- [Integration with Langfuse](#integration-with-langfuse)
- [Next steps](#next-steps)
- [Q&A](#qa)

## About the speaker

![About the speaker](slide_images/slide_2.png)
[Watch from 00:00](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=0s)

Pamela Fox is a Python Cloud Advocate at Microsoft. She previously worked at UC Berkeley, Khan Academy, Woebot, Coursera, and Google.

## Agenda

![Agenda overview](slide_images/slide_3.png)
[Watch from 00:43](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=43s)

The talk covers five topics: large language models (LLMs), Retrieval Augmented Generation (RAG), a deep dive into an open-source RAG chat app solution, evaluating RAG apps, and observability for RAG apps.

## What is a large language model

![LLM definition with sentiment analysis example](slide_images/slide_5.png)
[Watch from 00:43](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=43s)

A large language model (LLM) is a model large enough to achieve general-purpose language understanding and generation. Given a few examples of a task (like classifying movie review sentiment), an LLM can generalize and perform that task on new input without explicit programming. This capability is called few-shot learning — the model learns from examples provided in the prompt rather than from dedicated training data.

## LLMs in use today

![Table of popular LLMs with parameter counts](slide_images/slide_6.png)
[Watch from 02:42](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=162s)

The most widely used LLMs include OpenAI's GPT-3.5 (175 billion parameters) and GPT-4, Google's PaLM (540 billion parameters) and Gemini, Anthropic's Claude (130 billion parameters), Meta's open-source LLaMA (70 billion parameters), and Mistral AI's Mistral-7B and Mixtral. These models power products like ChatGPT, various Copilot features, and developer APIs. Open-source models like LLaMA and Mistral can also run locally using tools like Ollama, which is useful for development and testing without cloud costs.

## GPT and the Transformer architecture

![GPT and the Transformer architecture](slide_images/slide_7.png)
[Watch from 06:17](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=377s)

GPT stands for Generative Pre-trained Transformer. It is based on the Transformer architecture from the 2017 paper "Attention is all you need." The key innovation of Transformers is the attention mechanism, which allows the model to weigh the relevance of different parts of the input when generating output. For deeper understanding, Andrej Karpathy's talks "State of GPT" and "Let's build GPT: from scratch, in code" are recommended resources.

## Using OpenAI GPT models in Azure Studio

![Azure Studio chat completion demo](slide_images/slide_8.png)
[Watch from 08:08](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=488s)

Azure OpenAI Studio provides a playground for interacting with GPT models. A chat completion request consists of a system message (which sets the model's behavior and personality) and a user question. The model generates a response based on both. The studio provides a web interface for experimenting with different system prompts, models, and parameters before writing code. Azure OpenAI is a managed service that hosts the same OpenAI models but runs within Azure's infrastructure, providing enterprise features like virtual network support, content filtering, and managed identity authentication.

## Using OpenAI GPT models in Python

![Python code for chat completions](slide_images/slide_9.png)
[Watch from 12:01](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=721s)

The OpenAI Python SDK provides a straightforward API for calling GPT models. The `chat.completions.create()` method accepts a list of messages (system and user roles) and returns a streaming response. Setting `stream=True` allows processing tokens as they arrive rather than waiting for the complete response.

```python
response = openai.chat.completions.create(
    stream=True,
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "What food would magical kitties eat?"}
    ]
)
for event in response:
    print(event.choices[0].delta.content)
```

## The limitations of LLMs

![LLM limitations: outdated and no internal knowledge](slide_images/slide_10.png)
[Watch from 13:01](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=781s)

LLMs have two fundamental limitations. First, their knowledge is frozen at training time — they cannot access information published after their training cutoff date. Second, they have no access to private or internal data, such as company documents, HR policies, or proprietary databases. These limitations mean LLMs alone cannot answer questions about recent events or organization-specific information.

## Incorporating domain knowledge

![Three approaches: prompt engineering, fine-tuning, RAG](slide_images/slide_11.png)
[Watch from 13:50](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=830s)

There are three approaches to give an LLM access to domain-specific knowledge. **Prompt engineering** (in-context learning) includes relevant information directly in the prompt — effective but limited by context window size. **Fine-tuning** permanently teaches the model new skills or styles through additional training on curated datasets — useful for specialized behavior but expensive and time-consuming. **Retrieval Augmented Generation (RAG)** dynamically retrieves relevant facts at query time and includes them in the prompt — the most practical approach for accessing large or frequently updated knowledge bases.

## RAG: Retrieval Augmented Generation

![RAG flow diagram with perks example](slide_images/slide_13.png)
[Watch from 16:49](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=1009s)

RAG works in three steps. First, a user asks a question (e.g., "Do my company perks cover underwater activities?"). Second, a search system retrieves relevant documents from the knowledge base (e.g., the PerksPlus.pdf mentioning scuba diving lessons). Third, the retrieved content is passed to the LLM along with the original question, and the model generates an answer grounded in the search results. The LLM can now confidently answer that company perks cover scuba diving because the evidence is right there in the retrieved document.

## The benefit of RAG

![Benefits: up-to-date, internal, and brand-specific knowledge](slide_images/slide_14.png)
[Watch from 21:35](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=1295s)

RAG overcomes the core LLM limitations by providing access to three categories of knowledge that models lack. Up-to-date public knowledge covers recent information beyond the model's training cutoff. Internal (private) knowledge includes company documents, policies, and databases not available on the public internet. Brand-specific knowledge enables the model to respond in a company's voice with accurate product details rather than generic or hallucinated information.

## The importance of the search step

![Search quality affects answer quality](slide_images/slide_15.png)
[Watch from 27:42](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=1662s)

The search step is the most critical part of RAG. If the search results do not contain relevant information, the LLM either cannot answer or produces incorrect responses — garbage in, garbage out. However, providing too many search results also degrades performance. Research from the paper "Lost in the Middle: How Language Models Use Long Contexts" (Liu et al., arXiv:2307.03172) shows that accuracy drops as the number of documents in the input context increases, with models paying less attention to information in the middle of long contexts. The optimal approach is to return a small number of highly relevant results.

## Optimal search: hybrid search

![Hybrid search combining vector and keyword search](slide_images/slide_16.png)
[Watch from 30:52](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=1852s)

The best search strategy for RAG combines multiple retrieval methods. Vector search excels at finding semantically similar content — it understands that "underwater activities" relates to "scuba diving" even without exact keyword matches. Keyword search is better for exact matches like proper nouns, product codes, and specific numbers. Hybrid search combines both approaches using Reciprocal Rank Fusion (RRF) to merge the result lists. A reranking model then re-scores the combined results to produce the final ordering. This combination consistently outperforms either approach alone. More details are available at [aka.ms/ragrelevance](https://aka.ms/ragrelevance).

## RAG with hybrid search

![Full RAG pipeline with embedding model and hybrid search](slide_images/slide_17.png)
[Watch from 38:30](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=2310s)

The full RAG pipeline with hybrid search works as follows. The user question is sent to an embedding model that converts it into a vector (a list of floating-point numbers). This vector is used for the vector search component. Simultaneously, the raw text query is used for keyword search. The hybrid search system combines both result sets, and the top results are passed to the LLM along with the original question to generate the final answer.

## What is the RAG searching

![Documents vs database rows](slide_images/slide_18.png)
[Watch from 39:24](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=2364s)

RAG can search over two types of data sources. Unstructured documents (PDFs, DOCX, PPTX, Markdown, HTML, images) require an ingestion pipeline to extract text, split it into chunks, generate vector embeddings, and store the chunks in a search index. On Azure, this uses Azure AI Search with Document Intelligence and OpenAI embedding models. Structured database rows (PostgreSQL, MongoDB, etc.) require vectorizing and indexing target columns. Azure options for structured data include Azure AI Search (by copying data into it), PostgreSQL with the pgvector extension, Cosmos DB for MongoDB with vector support, and Container Apps hosting services like Milvus, Qdrant, or Weaviate.

## Ways to build a RAG chat app on Azure

![Three approaches: no code, low code, high code](slide_images/slide_19.png)
[Watch from 45:35](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=2735s)

Azure offers three levels of abstraction for building RAG applications, ranging from no-code to high-code.

## Copilot Studio: no-code RAG

![Copilot Studio On Your Data interface](slide_images/slide_20.png)
[Watch from 45:52](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=2752s)

[Copilot Studio](https://copilotstudio.preview.microsoft.com/) provides a no-code interface for building RAG applications with documents. It handles the search and LLM integration automatically, requiring only document upload and basic configuration.

## Azure Studio On Your Data: low-code RAG

![Azure Studio On Your Data configuration](slide_images/slide_21.png)
[Watch from 47:13](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=2833s)

[Azure Studio On Your Data](https://learn.microsoft.com/azure/ai-services/openai/concepts/use-your-data) supports multiple data types (uploaded documents, URLs, or Azure Blob Storage) and multiple search providers (Azure AI Search, Cosmos DB for MongoDB vCore, Azure AI ML Index, Elasticsearch, and Pinecone). It works with GPT-3.5 and GPT-4 models and generates deployable code. Azure Studio can also generate Python or C# code for calling the RAG endpoint, which can be used as a starting point for a custom application.

## Open-source RAG chat app solution

![azure-search-openai-demo features](slide_images/slide_22.png)
[Watch from 51:57](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=3117s)

The open-source [azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo/) (aka.ms/ragchat) provides a full-featured RAG chat application. It searches documents using Azure AI Search, supports GPT-3.5 and GPT-4, includes multi-turn chat conversations, user authentication with access control lists (ACLs), and can process image documents. This is the most customizable option and serves as the foundation for the deep dive portion of the talk.

## Prerequisites

![Prerequisites for deploying the RAG chat app](slide_images/slide_24.png)
[Watch from 54:21](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=3261s)

Deploying the RAG chat app requires an Azure account and subscription (a free account works but with limitations), access to Azure OpenAI (request access at [aka.ms/oaiapply](https://aka.ms/oaiapply)), and Azure account permissions for `Microsoft.Authorization/roleAssignments/write` and `Microsoft.Resources/deployments/write` at the subscription level.

## Opening the project

![Three options for opening the project](slide_images/slide_25.png)
[Watch from 54:58](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=3298s)

There are three ways to set up the development environment: GitHub Codespaces (fully cloud-based, no local setup), VS Code with Dev Containers (requires Docker), or a local environment with Python 3.9+, Node 14+, and the Azure Developer CLI installed.

## Deploying with the Azure Developer CLI

![azd commands for deployment](slide_images/slide_26.png)
[Watch from 55:13](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=3313s)

The Azure Developer CLI (`azd`) simplifies deployment to three commands: `azd auth login` to authenticate, `azd env new` to create a new environment for tracking deployment parameters, and `azd up` to provision all Azure resources and deploy the application. The `azd up` command combines `azd provision` (infrastructure) and `azd deploy` (application code) into a single step.

## Application architecture on Azure

![Architecture diagram showing App Service, Storage, OpenAI, and AI Search](slide_images/slide_27.png)
[Watch from 55:54](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=3354s)

The application has two main flows. The chat app runs on Azure App Service (or a local server during development) and connects to Azure Storage, Azure OpenAI, and Azure AI Search. Data ingestion can use either integrated vectorization (handled entirely within Azure AI Search) or a local script that additionally uses Azure Document Intelligence for text extraction.

## Local data ingestion

![Local data ingestion pipeline steps](slide_images/slide_28.png)
[Watch from 56:27](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=3387s)

The local ingestion pipeline (implemented in `prepdocs.py`) processes documents through five steps. Documents are uploaded to Azure Blob Storage (needed for clickable citations in the chat UI). Azure Document Intelligence extracts text from PDFs, HTML, DOCX, PPTX, XLSX, and images with OCR support. Python code splits the extracted text into chunks based on sentence boundaries and token lengths. Azure OpenAI computes vector embeddings for each chunk. Finally, the chunks and embeddings are indexed in Azure AI Search, which supports document-level indexing, chunk-level indexing, or both.

## Integrated vectorization

![Integrated vectorization pipeline in Azure AI Search](slide_images/slide_29.png)
[Watch from 01:07:10](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=4030s)

Integrated vectorization is an end-to-end data processing pipeline built directly into Azure AI Search. It handles the entire ingestion workflow: accessing data from sources (Blob Storage, ADLS v2, SQL DB, Cosmos DB), cracking file formats (PDFs, Office documents, JSON), chunking text into passages while propagating document metadata, vectorizing chunks using OpenAI embeddings or a custom model, and indexing the results. It also supports incremental change tracking so only modified documents are reprocessed. This approach eliminates the need for custom ingestion code.

## Code walkthrough

![Code structure showing frontend and backend](slide_images/slide_30.png)
[Watch from 01:08:37](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=4117s)

The application consists of a TypeScript/React frontend and a Python/Quart backend. On the frontend, `chat.tsx` calls `makeApiRequest()`, which hits `chatApi()` in `api.ts`. On the backend, `app.py` routes to `chat()`, which calls the `run()` method in `chatreadretrieveread.py`. This orchestration function executes the RAG pipeline: `get_search_query()` generates a search-optimized query from the conversation history, `compute_text_embedding()` vectorizes the query, `search()` performs hybrid search against Azure AI Search, `get_messages_from_history()` assembles the prompt with search results and conversation context, and `chat.completions.create()` calls the LLM for the final response. Multi-turn conversations are handled by including prior messages in the prompt and using the LLM to reformulate follow-up questions into standalone search queries.

## RAG orchestration libraries

![RAG orchestration libraries with language support](slide_images/slide_31.png)
[Watch from 01:14:47](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=4487s)

Several orchestration libraries can simplify RAG implementation. [LangChain](https://www.langchain.com/) supports Python, TypeScript, and Java. [LlamaIndex](https://docs.llamaindex.ai/) supports Python and TypeScript. Microsoft's [Semantic Kernel](https://github.com/microsoft/semantic-kernel) supports Python and .NET. Microsoft's [PromptFlow](https://github.com/microsoft/promptflow) supports Python. The azure-search-openai-demo uses plain Python by default but includes optional support for LangChain, LlamaIndex, and Semantic Kernel as alternative orchestration approaches.

## More RAG chat app starter repositories

![Additional starter repos in different languages](slide_images/slide_32.png)
[Watch from 01:17:02](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=4622s)

Beyond the Python/TypeScript demo, additional RAG starter repositories are available for different technology stacks: a JavaScript version with a Node.js backend and Web Components frontend, a C# version with a .NET backend and Blazor WebAssembly frontend, a Java version with a React frontend, the code powering Azure AI Studio's "On Your Data" feature, and a .NET/Semantic Kernel version with a React frontend.

## Evaluating RAG chat apps

![Quality questions for RAG answers](slide_images/slide_34.png)
[Watch from 01:19:18](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=4758s)

RAG answer quality has three dimensions: correctness (relative to the knowledge base), clarity and understandability, and formatting. The same question can produce very different quality answers depending on configuration. A good answer is concise and cites its source. A mediocre answer may be correct but overly verbose. A great answer is short, accurate, and includes a citation link.

## What affects the quality

![Factors on search side and LLM side](slide_images/slide_35.png)
[Watch from 01:20:34](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=4834s)

Answer quality is influenced by both the search and LLM sides. Search-side factors include the search engine, query cleaning, search mode (hybrid, vector, keyword), additional search options, data chunk size and overlap, and the number of results returned. LLM-side factors include the system prompt, language, message history, model choice (e.g., GPT-3.5 vs GPT-4), temperature (0–1), and max tokens. Changing any of these parameters can significantly impact answer quality.

## Manual experimentation of settings

![Developer Settings UI panel](slide_images/slide_36.png)
[Watch from 01:21:56](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=4916s)

The RAG chat app includes a "Developer Settings" panel that exposes all configurable parameters: search mode, retrieval mode, whether to use a semantic ranker, the number of search results to retrieve (top-k), and various prompt overrides. This allows manual experimentation to see how different settings affect answer quality in real time.

## Automated evaluation of app settings

![ai-rag-chat-evaluator tool overview](slide_images/slide_37.png)
[Watch from 01:22:22](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=4942s)

The [ai-rag-chat-evaluator](https://github.com/Azure-Samples/ai-rag-chat-evaluator) (aka.ms/rag/eval) automates the evaluation of RAG answer quality. It provides tools to generate ground truth data, run evaluations with different parameter configurations, and compare metrics and answers across evaluation runs. It is built on the `azure-ai-generative` SDK.

## Ground truth data

![Ground truth generation pipeline](slide_images/slide_38.png)
[Watch from 01:22:45](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=4965s)

Ground truth data consists of ideal question-answer pairs used to evaluate RAG performance. The evaluator tool can generate these automatically by querying the search index for documents, passing them to Azure OpenAI to create question-answer pairs, and saving them in JSONL format. The command `python3 -m scripts generate --output=example_input/qa.jsonl --numquestions=200 --persource=5` generates 200 questions with up to 5 per source document. Manual curation of the generated data is recommended for higher quality evaluations.

## Improving ground truth data sets

![Thumbs up/down feedback button for live apps](slide_images/slide_39.png)
[Watch from 01:24:08](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=5048s)

Ground truth data can be improved over time by adding a thumbs up/down feedback button to the live application ([aka.ms/rag/thumbs](https://aka.ms/rag/thumbs)). User feedback enables manually debugging answers that received negative ratings and adding real user questions to the ground truth dataset. This creates a feedback loop where production usage directly improves evaluation quality.

## Running evaluations and comparing results

![Evaluation metrics: coherence, groundedness, relevance](slide_images/slide_40.png)
[Watch from 01:24:08](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=5048s)

Running an evaluation computes both GPT-based metrics and custom metrics for every question in the ground truth set. The command `python3 -m scripts evaluate --config=example_config.json` sends each question to the local RAG endpoint, then compares the response and ground truth using Azure OpenAI. GPT-based metrics include coherence, groundedness, and relevance. Custom metrics include response length and whether citations are present.

## Reviewing metrics across runs

![Summary command showing metrics table](slide_images/slide_41.png)
[Watch from 01:25:30](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=5130s)

After running multiple evaluations with different configurations, `python3 -m review_tools summary example_results` displays a comparison table of all metrics across runs. This makes it easy to identify which parameter changes improved or degraded answer quality.

## Comparing answers across runs

![Diff command comparing two evaluation runs](slide_images/slide_42.png)
[Watch from 01:25:50](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=5150s)

The command `python3 -m review_tools diff example_results/baseline_1 example_results/baseline_2` compares individual answers between two evaluation runs side by side. This helps understand not just which run performed better on aggregate, but exactly how specific answers changed between configurations.

## Observability for RAG chat apps

![Observability section divider](slide_images/slide_43.png)
[Watch from 01:26:07](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=5167s)

Observability is essential for understanding how a RAG application behaves in production — tracking which searches are performed, what results are returned, and how the LLM generates its responses.

## Integration with Azure Monitor

![Azure Monitor OpenTelemetry integration code](slide_images/slide_44.png)
[Watch from 01:26:46](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=5206s)

Azure Monitor integration sends OpenAI traces to Application Insights using OpenTelemetry. The setup requires three instrumentors: `OpenAIInstrumentor` to track OpenAI SDK requests, `AioHttpClientInstrumentor` for aiohttp HTTP requests, and `HTTPXClientInstrumentor` for httpx HTTP requests. The `configure_azure_monitor()` call initializes the connection using the `APPLICATIONINSIGHTS_CONNECTION_STRING` environment variable. This provides visibility into token usage, latency, and error rates. The [opentelemetry-instrumentation-openai](https://pypi.org/project/opentelemetry-instrumentation-openai/) package handles the OpenAI-specific instrumentation.

## Integration with Langfuse

![Langfuse integration and Azure deployment](slide_images/slide_45.png)
[Watch from 01:27:24](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=5244s)

[Langfuse](https://pypi.org/project/langfuse/) is an open-source observability tool that provides detailed tracing of LLM interactions. Integration requires replacing the standard OpenAI import with the Langfuse wrapper: `from langfuse.openai import AsyncAzureOpenAI`. Langfuse can be [deployed to Azure](https://github.com/Azure-Samples/langfuse-on-azure/) using Azure Container Apps with PostgreSQL Flexible Server for storage. The deployment uses `azd` with authentication enabled via `azd env set AZURE_USE_AUTHENTICATION true`.

## Next steps

![Next steps with resource links](slide_images/slide_46.png)
[Watch from 01:28:13](https://www.youtube.com/watch?v=3Zh9MEuyTQo&t=5293s)

To get started: create an LLM/RAG app using the free tier at [aka.ms/ragchat/free](https://aka.ms/ragchat/free), run the evaluator tools at [aka.ms/rag/eval](https://aka.ms/rag/eval), report any issues or suggest improvements on the GitHub repositories, and share your learnings with the community.

## Q&A

### How does RAG compare to fine-tuning for adding domain knowledge?

RAG is generally preferred for factual knowledge retrieval because it does not require retraining the model and the knowledge base can be updated at any time. Fine-tuning is better suited for changing the model's behavior, writing style, or teaching it specialized skills. RAG retrieves facts temporarily at query time, while fine-tuning permanently alters the model's weights.

### Can you run these models locally instead of using Azure?

Yes. Open-source models like LLaMA and Mistral can be run locally using tools like Ollama. This is useful for development, testing, and scenarios where cloud costs are a concern. However, local models generally have fewer parameters and may produce lower quality results compared to GPT-4.

### How much does it cost to run a RAG application on Azure?

The main cost components are Azure OpenAI (charged per token), Azure AI Search (starting around $100/month for paid tiers), and the hosting service (App Service or Container Apps). For development and experimentation, costs are relatively low — individual API calls cost fractions of a penny. The GPT-3.5 Turbo model is significantly cheaper than GPT-4. Costs can be reduced by caching common responses, using cheaper models for simple queries, and skipping the LLM call when search results alone are sufficient.

### What is the "Lost in the Middle" problem?

Research shows that when LLMs receive long contexts with many documents, they tend to pay more attention to information at the beginning and end of the context, losing track of content in the middle. This is why returning fewer, higher-quality search results is better than flooding the context with many marginally relevant documents.

### How do you handle multi-turn conversations in RAG?

The RAG chat app includes prior conversation messages in the prompt and uses the LLM to reformulate follow-up questions. For example, if a user asks "What are the perks?" and then follows up with "Do they cover scuba diving?", the system reformulates the second question into "Do the company perks cover scuba diving?" so the search step can find relevant results without relying on conversation context.
