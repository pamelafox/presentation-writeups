# Monitoring and evaluating agents

This talk provides a comprehensive guide on building robust AI agents using the Microsoft Agent Framework, focusing on monitoring, evaluating, and ensuring the safety of agents in production environments. It covers setting up observability with OpenTelemetry, exporting telemetry data to platforms like Aspire and Azure Application Insights, and performing rigorous evaluations with the Azure AI Evaluation SDK, including automated red teaming to detect unsafe outputs. These processes enable developers to gain insight into agent behavior, measure output quality, and maintain safety standards.

## Table of contents

- [Overview of the Python + Agents series and session topics](#overview-of-the-python-agents-series-and-session-topics)
- [Introducing monitoring and evaluating agents session](#introducing-monitoring-and-evaluating-agents-session)
- [Agenda covering monitoring, evaluation, and safety](#agenda-covering-monitoring-evaluation-and-safety)
- [Following along with GitHub repo and Codespace setup](#following-along-with-github-repo-and-codespace-setup)
- [Recap of what an AI agent is and importance of monitoring and evaluation](#recap-of-what-an-ai-agent-is-and-importance-of-monitoring-and-evaluation)
- [Monitoring agents with observability and OpenTelemetry](#monitoring-agents-with-observability-and-opentelemetry)
- [Using OpenTelemetry with the Agent Framework including example code](#using-opentelemetry-with-the-agent-framework-including-example-code)
- [Overview of OpenTelemetry-compliant observability platforms](#overview-of-opentelemetry-compliant-observability-platforms)
- [Exporting telemetry data to Aspire dashboard with environment variables](#exporting-telemetry-data-to-aspire-dashboard-with-environment-variables)
- [Monitoring an agent in Aspire dashboard showing traces and metrics](#monitoring-an-agent-in-aspire-dashboard-showing-traces-and-metrics)
- [Exporting OpenTelemetry data to Azure Application Insights with example code](#exporting-opentelemetry-data-to-azure-application-insights-with-example-code)
- [Viewing traces in Azure Application Insights portal](#viewing-traces-in-azure-application-insights-portal)
- [Importance of GenAI OpenTelemetry standard](#importance-of-genai-opentelemetry-standard)
- [Using dashboards and alerts in Application Insights](#using-dashboards-and-alerts-in-application-insights)
- [Agent framework metrics and custom instrumentation](#agent-framework-metrics-and-custom-instrumentation)
- [Evaluating agents: challenges of non-deterministic LLM-based agents](#evaluating-agents-challenges-of-non-deterministic-llm-based-agents)
- [Human grading for agent evaluation](#human-grading-for-agent-evaluation)
- [Automated evaluation of AI apps using Azure AI Foundry](#automated-evaluation-of-ai-apps-using-azure-ai-foundry)
- [Automated evaluation frameworks overview](#automated-evaluation-frameworks-overview)
- [Using azure-ai-evaluation package with features](#using-azure-ai-evaluation-package-with-features)
- [Built-in evaluators for AI agents](#built-in-evaluators-for-ai-agents)
- [Tool call accuracy evaluator example with code and scoring](#tool-call-accuracy-evaluator-example-with-code-and-scoring)
- [Intent resolution and task adherence evaluators example code](#intent-resolution-and-task-adherence-evaluators-example-code)
- [Response completeness evaluator with ground truth comparison](#response-completeness-evaluator-with-ground-truth-comparison)
- [Running agent evaluation code demo](#running-agent-evaluation-code-demo)
- [Tips for running evaluations and model selection](#tips-for-running-evaluations-and-model-selection)
- [Viewing evaluation results locally and bulk evaluation](#viewing-evaluation-results-locally-and-bulk-evaluation)
- [Saving and using real user data for evaluation](#saving-and-using-real-user-data-for-evaluation)
- [Safety evaluation introduction and AI red teaming concepts](#safety-evaluation-introduction-and-ai-red-teaming-concepts)
- [Automated red teaming with adversarial LLMs](#automated-red-teaming-with-adversarial-llms)
- [Configuring and running red teaming scans](#configuring-and-running-red-teaming-scans)
- [Reviewing red teaming results and handling offensive content](#reviewing-red-teaming-results-and-handling-offensive-content)
- [Best practices for red teaming and model changes](#best-practices-for-red-teaming-and-model-changes)
- [Closing slide with next steps and series recap](#closing-slide-with-next-steps-and-series-recap)
- [Q&A](#qa)

## Overview of the Python + Agents series and session topics

![Overview slide of the Python + Agents series](slide_images/slide_1.png)  
[Watch from 00:06](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=6s)

The Python + Agents series spans multiple sessions that progressively build knowledge on creating AI agents. The first week focuses on building agents with the Microsoft Agent Framework. Subsequent weeks explore multi-agent workflows and more advanced orchestration. This particular session addresses monitoring and evaluating agents—key practices needed to manage agents effectively in production. It sets the foundation for understanding how agents operate and how developers can observe and improve their behavior.

## Introducing monitoring and evaluating agents session

![Title slide for monitoring and evaluating agents](slide_images/slide_2.png)  
[Watch from 00:58](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=58s)

This session zeroes in on three pillars: monitoring agent activity via observability tools, evaluating agent output quality using evaluation frameworks, and ensuring safety through guardrails and red teaming. Monitoring reveals agent decisions and tool usage in real time, evaluation quantifies output effectiveness, and safety checks prevent harmful or undesirable responses. Together, these capabilities form a comprehensive approach for managing AI agents reliably.

## Agenda covering monitoring, evaluation, and safety

![Agenda slide listing monitoring, evaluation, safety topics](slide_images/slide_3.png)  
[Watch from 01:24](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=84s)

The agenda outlines three main content areas: first, monitoring agents by integrating OpenTelemetry for trace, metrics, and log collection; second, evaluating agents using automated and human-in-the-loop methods to measure correctness and adherence to goals; and third, ensuring agent safety via automated red teaming techniques that simulate adversarial attacks. These topics collectively address the lifecycle of agent management.

## Following along with GitHub repo and Codespace setup

![Instruction slide for GitHub repo and Codespace](slide_images/slide_4.png)  
[Watch from 03:00](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=180s)

The session’s code examples are hosted in a GitHub repository with support for VS Code Codespaces, allowing users to run and test samples in a cloud-hosted development environment preconfigured with dependencies. While many LLM-based examples run freely, integrating Azure resources requires an Azure subscription due to associated costs. Users are encouraged to clone the repo, open a Codespace for instant access, and configure their own Azure credentials to execute all examples fully.

## Recap of what an AI agent is and importance of monitoring and evaluation

![Slide defining an AI agent and importance of monitoring](slide_images/slide_5.png)  
[Watch from 04:23](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=263s)

An AI agent combines a large language model (LLM) with a set of tools to accomplish a user-specified goal. The LLM dynamically decides which tools to invoke, possibly iterating multiple times to gather information or perform actions before producing a final output. Because agents behave non-deterministically—varying in tool calls, sequence, and length—monitoring is essential to trace their decision paths and tool usage. Evaluation complements monitoring by assessing output correctness and alignment with user intent to ensure high-quality results.

## Monitoring agents with observability and OpenTelemetry

![Monitoring agents using OpenTelemetry](slide_images/slide_6.png)  
[Watch from 06:20](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=380s)

Observability is crucial for understanding what an agent is doing, especially given its non-deterministic nature. OpenTelemetry is an open industry standard for collecting telemetry data—including traces, metrics, and logs—that facilitates consistent, structured monitoring across systems. Employing OpenTelemetry enables developers to record detailed information about agent events, resource usage, and errors, which can then be exported to various observability platforms for visualization and analysis.

## Using OpenTelemetry with the Agent Framework including example code

![Code example showing OpenTelemetry setup in Agent Framework](slide_images/slide_7.png)  
[Watch from 08:14](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=494s)

The Microsoft Agent Framework natively supports OpenTelemetry tracing. By importing its `configure_otel_providers` function, developers can easily enable telemetry data emission with options to include sensitive data like tool calls. Since logging tool calls may expose private information, users must balance observability benefits against privacy risks, potentially filtering sensitive data via middleware. The configuration relies on environment variables to customize exporters and sampling rates, allowing flexible integration with different telemetry backends.

## Overview of OpenTelemetry-compliant observability platforms

![Table of OpenTelemetry-compatible platforms](slide_images/slide_8.png)  
[Watch from 13:59](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=839s)

Numerous observability platforms support OpenTelemetry data ingestion. Open source options like Aspire (used locally) and managed services like Azure Application Insights are common choices. Other popular platforms include DataDog, Grafana (now with Application Insights support), Prometheus, Jaeger, and Logfire. Selecting a platform depends on deployment needs, whether local development or production-grade monitoring, and personal or organizational preferences.

## Exporting telemetry data to Aspire dashboard with environment variables

![Setup instructions for Aspire dashboard export](slide_images/slide_9.png)  
[Watch from 15:18](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=918s)

Aspire is a local, open source observability dashboard compatible with OpenTelemetry. To export telemetry to Aspire, an environment variable specifying the OTLP endpoint must point to the locally running Aspire server. The required OpenTelemetry OTLP gRPC exporter package must be installed, as reflected in the project dependencies. Aspire runs as a service within the development container (for example, in GitHub Codespaces) and listens on a dedicated port exposed to the user environment.

## Monitoring an agent in Aspire dashboard showing traces and metrics

![Aspire dashboard showing agent traces with spans and metrics](slide_images/slide_10.png)  
[Watch from 18:23](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=1103s)

The Aspire dashboard visualizes agent telemetry as traces composed of spans, representing discrete operations such as LLM calls or tool invocations. Each trace’s duration and sequence are displayed, highlighting that LLM calls typically consume the most time. A special agent-oriented view reconstructs the conversational flow, showing user inputs, tool calls, and agent outputs. Aspire also tracks metrics like token usage and function invocation durations, enabling performance monitoring. This setup is ideal for local development and debugging.

## Exporting OpenTelemetry data to Azure Application Insights with example code

![Azure Application Insights export setup code snippet](slide_images/slide_11.png)  
[Watch from 23:28](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=1408s)

For production monitoring, exporting telemetry to Azure Application Insights provides a managed cloud service with rich visualization and alerting features. This requires adding the Azure Monitor OpenTelemetry exporter package and configuring it with an Application Insights connection string via environment variables. The agent framework’s instrumentation functions are called to enable telemetry export. Unlike Aspire, Azure Application Insights is typically set up locally during development with credentials or in production environments with secure configurations.

## Viewing traces in Azure Application Insights portal

![Azure Application Insights portal showing agent trace and spans](slide_images/slide_12.png)  
[Watch from 26:28](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=1588s)

Within the Azure Application Insights portal, agent telemetry traces appear under performance or dependencies tabs. Traces show a hierarchical breakdown of agent operations, including LLM calls and tool executions, similar to Aspire’s visualization. Application Insights renders traces in a developer-friendly conversational style rather than raw JSON, making it easier to interpret agent behavior. Each span includes attributes that conform to the GenAI OpenTelemetry standard, enabling specialized rendering for AI-based applications.

## Importance of GenAI OpenTelemetry standard

![GenAI OpenTelemetry standard attributes and example](slide_images/slide_13.png)  
[Watch from 28:12](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=1692s)

The GenAI OpenTelemetry standard defines attributes specific to generative AI applications, such as operation names, tool names, and token usage, prefixed with `gen_ai`. Adhering to this standard allows observability platforms to recognize AI-specific telemetry and render it with enhanced clarity, such as conversational views. Both Aspire and Azure Application Insights rely on this standard to provide meaningful visualizations. Using GenAI-compliant telemetry is critical for gaining actionable insights into agent internals.

## Using dashboards and alerts in Application Insights

![Sample dashboards and alert configuration in Application Insights](slide_images/slide_14.png)  
[Watch from 29:22](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=1762s)

Once telemetry data flows into Azure Application Insights, users can create custom dashboards to track key metrics like token usage, response times, and error rates. Alerts can be configured to notify teams of anomalies or performance degradations. This facilitates proactive monitoring and operational insight into agent health. Coupled with the GenAI standard, these dashboards provide a comprehensive picture of agent activity and quality in production.

## Agent framework metrics and custom instrumentation

![Agent framework spans and metrics overview](slide_images/slide_15.png)  
[Watch from 30:01](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=1801s)

The Agent Framework automatically emits spans such as `invoke_agent`, `chat`, and `execute_tool`, along with metrics like operation duration and token usage. Developers can extend this by instrumenting additional components—such as FastAPI endpoints or Azure SDK calls—to capture a full observability picture. OpenTelemetry’s flexibility allows custom spans and metrics to be defined, ensuring comprehensive monitoring that spans all relevant parts of an agent-based application.

## Evaluating agents: challenges of non-deterministic LLM-based agents

![Challenges of evaluating non-deterministic agents](slide_images/slide_16.png)  
[Watch from 31:40](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=1900s)

LLM-based agents exhibit inherent non-determinism due to stochastic model behavior and variable tool usage. Each LLM call adds uncertainty, complicating assurance of output quality. Evaluating agents involves verifying that they select appropriate tools in the correct sequence with proper arguments and produce responses grounded in tool outputs without hallucinations. Establishing rigorous evaluation processes is critical to maintaining confidence in agent reliability and performance.

## Human grading for agent evaluation

![Human grading interface for agent responses](slide_images/slide_17.png)  
[Watch from 33:06](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=1986s)

Human evaluators with domain expertise provide valuable qualitative feedback by reviewing agent outputs and indicating correctness or errors. They can diagnose why an output is wrong, guiding the development of automated evaluation criteria. However, human grading is limited by scale and time, making it impractical for extensive datasets but essential for initial calibration and complex cases where nuanced judgment is required.

## Automated evaluation of AI apps using Azure AI Foundry

![Automated evaluation metrics and framework overview](slide_images/slide_18.png)  
[Watch from 35:16](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=2116s)

Automated evaluation frameworks enable scalable, repeatable quality assessment of agent outputs. Azure AI Evaluation SDK offers built-in evaluators that leverage LLMs as judges to score outputs on intent resolution, task adherence, response completeness, and tool call accuracy. Results can be exported to Azure AI Foundry for collaborative review. Automated evaluation accelerates iteration, regression detection, and continuous improvement with quantitative metrics.

## Automated evaluation frameworks overview

![Table of evaluation frameworks including Azure AI Evaluation SDK](slide_images/slide_19.png)  
[Watch from 35:54](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=2154s)

Besides Azure AI Evaluation SDK, other frameworks include Tao (Python for customer service agents), Ragos (research-focused Python), DeepEval (Python with hosted service), Langsmith (for Langchain users), and OpenAI’s eval package. Most use LLMs as judges and support exporting results for visualization. Framework choice depends on ecosystem, use case, and integration needs.

## Using azure-ai-evaluation package with features

![Azure AI Evaluation SDK architecture and features](slide_images/slide_20.png)  
[Watch from 37:22](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=2242s)

The Azure AI Evaluation SDK, installable via Python package, provides a suite of evaluators, bulk evaluation capabilities, red teaming tools, and optional integration with Foundry. It supports custom evaluator creation to target specific failure modes. The SDK streamlines evaluation workflows, enabling consistent scoring and feedback mechanisms essential for high-quality agent development.

## Built-in evaluators for AI agents

![List of built-in agent evaluators: tool call accuracy, intent resolution, etc.](slide_images/slide_21.png)  
[Watch from 38:02](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=2282s)

Key evaluators include:

- Tool call accuracy: Checks if the agent invoked correct tools with appropriate arguments without unnecessary calls.

- Intent resolution: Assesses whether the agent achieved the user’s intended goal.

- Task adherence: Verifies compliance with system prompt constraints and tool usage rules.

- Response completeness: Measures alignment with ground truth responses to detect hallucinations.

Each evaluator uses an LLM judge to score outputs and provide reasoning.

## Tool call accuracy evaluator example with code and scoring

![Code snippet demonstrating tool call accuracy evaluator usage](slide_images/slide_22.png)  
[Watch from 41:33](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=2493s)

The tool call accuracy evaluator requires detailed input: system prompts, user queries, tool call logs, tool definitions (as JSON schemas), and agent responses. It uses an LLM judge to assign a score from 1 to 5 with an explanatory reason. This granular evaluation helps identify specific mistakes such as incorrect tool usage or argument errors, enabling targeted improvements.

## Intent resolution and task adherence evaluators example code

![Code snippets for intent resolution and task adherence evaluators](slide_images/slide_23.png)  
[Watch from 44:03](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=2643s)

Intent resolution evaluates overall goal achievement by analyzing the full conversation without needing tool definitions. Scores range from 1 to 5, with 4 or 5 typically considered passing. Task adherence focuses on whether the agent respected prompt constraints and tool rules, flagging violations that might still achieve the goal but break system policies. These evaluations complement each other by covering different aspects of agent correctness.

## Response completeness evaluator with ground truth comparison

![Example of response completeness evaluator comparing to ground truth](slide_images/slide_24.png)  
[Watch from 46:22](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=2782s)

Response completeness requires a ground truth reference answer for comparison. The evaluator judges whether the agent’s output includes all necessary information and avoids hallucinations. Ground truth-based evaluation is preferred for detecting factual inaccuracies and ensuring comprehensive responses, critical for high-stakes domains.

## Running agent evaluation code demo

![Screenshot of running agent evaluation script](slide_images/slide_25.png)  
[Watch from 46:30](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=2790s)

Running evaluation scripts involves executing agents to generate responses, then feeding those interactions into the evaluators. Since evaluators use LLMs as judges, each evaluation consumes tokens and time. This process can be slow and resource-intensive, especially for large datasets, requiring careful orchestration such as asynchronous or cloud-based batch processing to avoid blocking development.

## Tips for running evaluations and model selection

![Slide with tips on evaluation runtime and choosing models](slide_images/slide_26.png)  
[Watch from 48:47](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=2927s)

Evaluations consume tokens and may exceed free-tier limits on some models like GitHub-hosted ones. Using Azure-hosted models such as GPT-4 or GPT-3.5 variants is recommended for reliability. Selecting lighter models (e.g., GPT-3.5 Turbo Mini) may help with token limits but can affect judgment quality. Running evaluations in the background, in the cloud, or as part of CI pipelines improves workflow efficiency.

## Viewing evaluation results locally and bulk evaluation

![CLI and Foundry views of evaluation results](slide_images/slide_27.png)  
[Watch from 50:47](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=3047s)

Evaluation results can be viewed as raw JSON locally or through custom CLI viewers built with libraries like Rich or Textual. More sophisticated analysis and collaboration use Azure AI Foundry, which displays passes, fails, scores, and detailed reasons for each evaluator. Bulk evaluation involves running large datasets (e.g., 200+ agent calls) to comprehensively assess performance and detect regressions.

## Saving and using real user data for evaluation

![Slide describing saving evaluation data and using real user inputs](slide_images/slide_28.png)  
[Watch from 53:17](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=3197s)

Capturing real user interactions from production logs enriches evaluation datasets to reflect actual use cases and edge conditions. This practice prevents model drift by ensuring evaluation data matches live traffic characteristics. Until sufficient real data accumulates, simulated inputs generated by LLMs like GitHub Copilot can bootstrap evaluation sets. Continuous updating of datasets improves robustness.

## Safety evaluation introduction and AI red teaming concepts

![Safety evaluation and red teaming introduction slide](slide_images/slide_29.png)  
[Watch from 57:24](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=3444s)

Safety evaluation ensures agents avoid producing harmful outputs such as hate speech, violence, illegal instructions, or biased content. Human red teaming traditionally involves experts attempting to provoke unsafe behavior. Automated red teaming simulates this using adversarial LLMs to generate challenging prompts designed to bypass guardrails, allowing systematic safety testing at scale.

## Automated red teaming with adversarial LLMs

![Diagram illustrating automated red teaming workflow](slide_images/slide_30.png)  
[Watch from 58:09](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=3489s)

Automated red teaming employs an adversarial LLM with disabled safety filters to produce harmful or tricky inputs. These inputs are transformed using attack strategies like text reversal, Morse code, Caesar cipher, or URL encoding to mimic real-world evasion attempts. The hostile inputs are sent to the agent, and a separate LLM judge evaluates the agent’s responses for safety. Successful attacks identify vulnerabilities in agent guardrails.

## Configuring and running red teaming scans

![Code example configuring red teaming agent and running scan](slide_images/slide_31.png)  
[Watch from 59:16](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=3556s)

The Azure AI Evaluation SDK’s red team module requires a Foundry project due to the sensitive adversarial LLM. Developers specify risk categories of concern (e.g., sexual content, violence) and select attack transformations to apply. Running the scan executes multiple adversarial queries with transformations, producing results that highlight successful and failed attacks. This process takes time similar to evaluation and is best run periodically.

## Reviewing red teaming results and handling offensive content

![Foundry UI showing red teaming results with warnings](slide_images/slide_32.png)  
[Watch from 01:00:49](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=3649s)

Red teaming results are reviewed in Foundry, filtering for successful attacks requiring remediation. The adversarial inputs can be highly offensive and triggering, so reviewers should prepare mentally. Detailed inspection of failures informs prompt engineering, model choice, or tool adjustments to improve safety. This review is essential before deploying models in sensitive or public-facing applications.

## Best practices for red teaming and model changes

![Recommendations for when to run red team scans](slide_images/slide_33.png)  
[Watch from 01:02:27](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=3747s)

Red team scans should be run whenever models or prompts undergo significant changes, as these can introduce new vulnerabilities. It is unnecessary to run red teams on every code change but recommended after upgrading models, modifying tool definitions, or altering safety constraints. Results guide iterative improvements to maintain robust safety postures over time.

## Closing slide with next steps and series recap

![Closing slide summarizing next steps and upcoming sessions](slide_images/slide_34.png)  
[Watch from 01:03:41](https://www.youtube.com/watch?v=3yS-G-NEBu8&t=3821s)

The session concludes with a preview of upcoming topics, including building multi-agent workflows with the Microsoft Agent Framework. Attendees are encouraged to join office hours for questions and to access recordings and resources through the provided links. Continuous learning and community engagement are emphasized to master AI agent development.

## Q&A

### Does enabling OpenTelemetry add latency to agent execution?  
OpenTelemetry exporting involves network requests to observability platforms, which introduces some latency. However, these calls are typically fast and optimized for minimal impact. Sampling strategies can reduce overhead by sending only a subset of traces, balancing observability with performance.

### Can the Agent Framework automatically set up all necessary spans and metrics?  
Yes, the Agent Framework emits standard spans such as invoking the agent, chat completions, and tool executions, along with metrics like operation duration and token usage. Developers can also instrument additional components or create custom spans and metrics for comprehensive monitoring.

### How do token consumption and model choice affect evaluation runtime?  
Evaluations use LLMs as judges, which consume tokens and time proportional to conversation length. Free-tier models like GitHub-hosted LLMs have stricter token limits and rate limits, potentially causing errors. Azure-hosted models (e.g., GPT-4, GPT-3.5) handle larger token counts more reliably. Choosing lighter models can help but may reduce evaluation accuracy.

### What is the best way to build evaluation datasets?  
Starting with simulated user inputs generated by LLMs can bootstrap datasets. Over time, incorporating real production data, especially examples of poor agent behavior identified via monitoring, improves evaluation relevance. Maintaining datasets aligned with live traffic prevents model drift.

### How should red teaming be integrated into development workflows?  
Red team scans are resource-intensive and should run when models or prompts change significantly. They simulate adversarial attacks to identify safety vulnerabilities. Results inform prompt tuning, model selection, and safety guardrail improvements. Running red teams regularly ensures ongoing safety compliance.

### Can evaluation results be shared with team members?  
Yes, exporting evaluation results to Azure AI Foundry enables collaborative review with detailed scores and reasoning. Custom dashboards and reports facilitate transparency and joint decision-making on agent improvements.

---

This annotated post distills the talk’s detailed guidance on monitoring, evaluating, and safely operating AI agents, providing a roadmap for developers deploying agents with Microsoft’s Agent Framework and supporting tools.