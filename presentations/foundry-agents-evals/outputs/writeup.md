# Host your agents on Foundry: Quality & Safety evaluations

📺 [Watch the full recording on YouTube](https://www.youtube.com/watch?v=GiJQhMl0mWc) |
📑 [Download the slides (PDF)](https://aka.ms/foundryhosted/slides/qualitysafety)

This write-up includes an annotated version of the presentation slides with timestamps to the video plus a summary of the live Q&A session.

## Table of contents

- [Session description](#session-description)
- [Annotated slides](#annotated-slides)
  - [Overview of the "Host your agents on Foundry" series](#overview-of-the-host-your-agents-on-foundry-series)
  - [Today's topic: Quality & safety evaluations](#todays-topic-quality--safety-evaluations)
  - [Today's agenda](#todays-agenda)
  - [Following along with the GitHub repo](#following-along-with-the-github-repo)
  - [Quality evaluations](#quality-evaluations)
  - [Agent output is non-deterministic](#agent-output-is-non-deterministic)
  - [Human evaluations](#human-evaluations)
  - [Automated evaluations](#automated-evaluations)
  - [Automating evaluations with Python SDKs](#automating-evaluations-with-python-sdks)
  - [Built-in evaluators for AI agents](#built-in-evaluators-for-ai-agents)
  - [Tool call accuracy](#tool-call-accuracy)
  - [Intent resolution](#intent-resolution)
  - [Task adherence](#task-adherence)
  - [Response completeness](#response-completeness)
  - [More built-in evaluators](#more-built-in-evaluators)
  - [When to run evaluations](#when-to-run-evaluations)
  - [Batch evaluations](#batch-evaluations)
  - [Configure Foundry project client](#configure-foundry-project-client)
  - [Upload an evaluation data set](#upload-an-evaluation-data-set)
  - [Define evaluators](#define-evaluators)
  - [Run a batch evaluation](#run-a-batch-evaluation)
  - [View batch evaluation results in Foundry](#view-batch-evaluation-results-in-foundry)
  - [Scheduled evaluations](#scheduled-evaluations)
  - [What changes for scheduled evals](#what-changes-for-scheduled-evals)
  - [Create the schedule](#create-the-schedule)
  - [View scheduled evaluation results in Foundry](#view-scheduled-evaluation-results-in-foundry)
  - [Continuous evaluations](#continuous-evaluations)
  - [What's different about continuous evals](#whats-different-about-continuous-evals)
  - [Create the continuous eval schedule](#create-the-continuous-eval-schedule)
  - [View continuous evaluation results in Foundry](#view-continuous-evaluation-results-in-foundry)
  - [Catch quality regressions with eval alerts](#catch-quality-regressions-with-eval-alerts)
  - [Safety evaluation](#safety-evaluation)
  - [What makes an agent's output safe](#what-makes-an-agents-output-safe)
  - [Safety evaluation process](#safety-evaluation-process)
  - [Which Python package to use](#which-python-package-to-use)
  - [Configure the red team](#configure-the-red-team)
  - [Run the red team scan](#run-the-red-team-scan)
  - [Review the red team results](#review-the-red-team-results)
  - [When should you run a red team](#when-should-you-run-a-red-team)
  - [Guardrails](#guardrails)
  - [Risk mitigation layers](#risk-mitigation-layers)
  - [Azure AI Content Safety](#azure-ai-content-safety)
  - [Guardrails in Microsoft Foundry](#guardrails-in-microsoft-foundry)
  - [Content safety filter error responses](#content-safety-filter-error-responses)
  - [Handling content filter errors in agents](#handling-content-filter-errors-in-agents)
  - [Next steps and resources](#next-steps-and-resources)
- [Live Chat Q&A](#live-chat-qa)
- [Discord OH Q&A](#discord-oh-qa)

## Session description

In this three-part series, we showed how to host your own agents on Microsoft Foundry.

In the third session, we ensured that AI agents produce high-quality outputs and operate safely and responsibly.

First we explored what it means for agent outputs to be high quality, using built-in evaluators to check overall task adherence and then building custom evaluators for domain-specific checks. With Foundry hosted agents, we ran bulk evaluations on demand, set up scheduled evaluations, and enabled continuous evaluation on a subset of live agent traces.

Next we discussed safety systems that can be layered on top of agents and audited agents for potential safety risks. To improve compliance with an organization's goals, we configured custom policies and guardrails that can be shared across agents.

Finally, we ensured that adversarial inputs can't produce unsafe outputs by running automated red-teaming scans on agents, and discussed scheduling those to run regularly as well.

## Annotated slides

### Overview of the "Host your agents on Foundry" series

![Series title slide](slide_images/slide_1.png)
[Watch from 00:24](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=24s)

This is a three-part live stream series on hosting Python agents on Microsoft Foundry. Session 1 (Apr 27) uses Microsoft Agent Framework, session 2 (Apr 29) covers LangChain and LangGraph, and session 3 (Apr 30) addresses quality and safety evaluations. Register and watch past recordings at [aka.ms/AgentsOnFoundry/series](https://aka.ms/AgentsOnFoundry/series).

### Today's topic: Quality & safety evaluations

![Session title slide](slide_images/slide_2.png)
[Watch from 00:34](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=34s)

Session slides are available at [aka.ms/foundryhosted/slides/qualitysafety](https://aka.ms/foundryhosted/slides/qualitysafety).

### Today's agenda

![Agenda slide](slide_images/slide_3.png)
[Watch from 01:06](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=66s)

The session covers quality evaluations (built-in evaluators, batch evals, scheduled evals, continuous evals, and eval alerts), safety evaluation with red-teaming, guardrails, and content safety filter error handling.

### Following along with the GitHub repo

![Code repo setup slide](slide_images/slide_4.png)
[Watch from 01:55](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=115s)

All code samples are in the GitHub repository at [aka.ms/foundry-hosted-agentframework-demos](https://aka.ms/foundry-hosted-agentframework-demos). Open it in a GitHub Codespace using the "Code" button, then follow the README to deploy to your own Azure account. For today's session, all the evaluation code is in the `scripts` folder. Most code samples require deployment and an Azure account to run.

### Quality evaluations

![Section header slide](slide_images/slide_5.png)
[Watch from 02:42](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=162s)

### Agent output is non-deterministic

![Non-determinism diagram](slide_images/slide_6.png)
[Watch from 02:47](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=167s)

Agents are powered by LLMs, which are non-deterministic systems. Every call to an LLM increases the non-determinism of the overall system. Output quality depends on the LLM choosing the right tools, choosing the right tool arguments, and providing a grounded and comprehensive final response. Whenever you change the LLM model, parameters, prompts, or tools, output can get better or worse. Even renaming a tool can affect quality because the agent may become confused about when to use it. Any change should trigger evaluations to check for regressions.

### Human evaluations

![Human evaluations screenshot](slide_images/slide_7.png)
[Watch from 05:06](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=306s)

Humans can spot-check output performance on small data sets and annotate issues. Ideally, evaluators are either target users or domain experts who can provide specific feedback about what's wrong — not just thumbs up/down, but explanations. Foundry offers human evals as a feature (with a manual evaluation result interface), but it's not yet supported for hosted agents. The team is actively working on adding support.

### Automated evaluations

![Automated evaluations slide](slide_images/slide_8.png)
[Watch from 07:00](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=420s)

LLMs can measure output performance at scale across a broader range of risks. This "LLM-as-judge" approach gives the judge LLM specific criteria and asks it to score agent output as pass/fail. Research shows this works well, even when the same model judges its own output. You should calibrate LLM judges against human judgment to confirm they agree. The judge should always return both a score and a reason — the reason helps understand what's wrong and verify the judge is working correctly.

### Automating evaluations with Python SDKs

![Python SDKs slide](slide_images/slide_9.png)
[Watch from 08:50](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=530s)

Install `openai` and `azure-ai-projects` into your project. The `azure-ai-projects` package brings in the OpenAI SDK which includes an eval package. Together they provide built-in evaluators for quality and safety, a way to build custom evaluators, bulk evaluation functionality, and result storage and visualization in Microsoft Foundry. See the [cloud evaluation documentation](https://learn.microsoft.com/azure/foundry/how-to/develop/cloud-evaluation) for more details.

### Built-in evaluators for AI agents

![Built-in evaluators diagram](slide_images/slide_10.png)
[Watch from 09:27](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=567s)

Four key built-in evaluators target different parts of the agent pipeline:

- **ToolCallAccuracyEvaluator** — looks at the input, tool calls, and tool definitions to determine if the agent invoked the right tools with the right arguments. Does not examine the final response.
- **IntentResolutionEvaluator** — an end-to-end evaluator that checks whether the agent's response actually achieved the user's goal.
- **TaskAdherenceEvaluator** — an end-to-end evaluator that checks whether the agent followed prompt constraints and tool-use rules from the system message.
- **ResponseCompletenessEvaluator** — compares the response against a ground truth answer to check if all required information is present.

### Tool call accuracy

![Tool call accuracy example](slide_images/slide_11.png)
[Watch from 14:00](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=840s)

Given a user query like "What expenses are not covered by PerksPlus?", this evaluator examines the tool calls and tool definitions — it never sees the final response. In a passing run, the agent calls `knowledge_base_retrieve(["PerksPlus expenses not covered"])` and scores 5/5 because it used the retrieval tool for a company-specific question with a relevant query. In a failing run where the agent makes no tool calls at all, it scores 1/5 because it didn't use the available retrieval tool. This evaluator helps answer *why* an agent failed at the end-to-end level — often it's because the tool calls were wrong.

### Intent resolution

![Intent resolution example](slide_images/slide_12.png)
[Watch from 16:15](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=975s)

For a multi-part question like "Does PerksPlus cover horseback riding lessons, and what's the maximum reimbursement?", this evaluator checks whether the response addresses the full user intent. A passing response answers both parts (eligibility and reimbursement limit). A vague response that mentions "wellness programs" without answering the specific question fails because it misses the user's intent about horseback riding and maximum amount.

### Task adherence

![Task adherence example](slide_images/slide_13.png)
[Watch from 17:02](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1022s)

When a user says "Using only Zava benefits information, can you recommend a therapist in London?", the constraint is "only Zava benefits information." A passing agent does a knowledge base retrieval, finds no therapists, and correctly declines rather than hallucinating. A failing agent ignores the constraint and uses web search instead, violating the user's explicit restriction. An agent can achieve the user's goal while still failing task adherence if it ignores system prompt guidelines along the way.

### Response completeness

![Response completeness example](slide_images/slide_14.png)
[Watch from 17:51](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1071s)

This evaluator requires a ground truth — the ideal answer written by a domain expert. For "What expenses are not covered by PerksPlus?", the ground truth lists non-fitness expenses, medical treatments, travel expenses (unless fitness-related), and food/supplements. A response that includes all of those passes. A response that only mentions "medical procedures or food" fails because it's missing critical exclusions. This is the most specific evaluator but depends on having pre-written ground truth data.

### More built-in evaluators

![Additional evaluators table](slide_images/slide_15.png)
[Watch from 18:51](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1131s)

Beyond the four main evaluators, Foundry provides: Tool Selection (did it pick the right tool), Tool Input Accuracy (well-formed arguments), Tool Output Utilization (did it use what the tool returned), Tool Call Success (did tools execute without errors), Task Navigation Efficiency (most direct path — useful for catching agents that succeed but waste 20 tool calls when 10 would suffice), Relevance (on-topic response), and Groundedness (claims supported by retrieved context). Custom evaluators can also be built for domain-specific checks, like verifying a hotel booking agent reserved the correct room type.

### When to run evaluations

![When to run evaluations comparison](slide_images/slide_16.png)
[Watch from 20:35](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1235s)

Three evaluation modes form a complete evaluation strategy:

- **Batch evals** — run on demand against curated/synthetic data. Best for catching regressions and comparing agent versions during development. May miss live issues.
- **Scheduled evals** — run daily or at a fixed time against curated queries sent to the production agent. Best for tracking trends and catching accidental bad deployments. Findings are delayed.
- **Continuous evals** — run always/sampled against live traces from App Insights. Best for catching live issues and monitoring safety. Requires enough user traffic.

Ideally, use all three for a comprehensive evaluation story.

### Batch evaluations

![Batch evaluations section header](slide_images/slide_17.png)
[Watch from 24:16](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1456s)

### Configure Foundry project client

![Configure project client code](slide_images/slide_18.png)
[Watch from 24:22](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1462s)

Use `azure-ai-projects` to connect to a Foundry project and fetch the latest version of the agent:

```python
from azure.ai.projects import AIProjectClient
from azure.identity import AzureDeveloperCliCredential

credential = AzureDeveloperCliCredential()
project_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=credential)

agent = project_client.agents.get(agent_name="hosted-agentframework-agent")
agent_version = agent.versions["latest"]
```

The full example is in `quality_eval.py`.

### Upload an evaluation data set

![Upload dataset code](slide_images/slide_19.png)
[Watch from 25:00](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1500s)

Before batch evals can run, you need a dataset in JSONL format where each row is a test case with the fields required by your evaluators:

```json
{"query": "Does PerksPlus cover horseback riding?",
 "ground_truth": "Yes, PerksPlus covers horseback riding lessons."}
```

Rows can include additional fields like `tool_definitions` for tool-centric evaluators. Upload the dataset to Foundry with `project_client.datasets.upload_file()`. Generally 200+ test cases are recommended — 12 is too few for production but acceptable for demos.

### Define evaluators

![Define evaluators code](slide_images/slide_20.png)
[Watch from 26:04](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1564s)

Each evaluator is configured with a name, type (`azure_ai_evaluator`), evaluator name (e.g., `builtin.intent_resolution`), data mappings, and initialization parameters. Data mappings connect evaluator inputs to either the dataset (`{{item.query}}`, `{{item.ground_truth}}`) or the agent's live output (`{{sample.output_items}}`). The output includes the full tool calls as well as the final response. Different evaluators need different mappings — tool call accuracy needs `tool_definitions` from the dataset, while response completeness needs `ground_truth`.

### Run a batch evaluation

![Run batch evaluation code](slide_images/slide_21.png)
[Watch from 27:55](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1675s)

Create an evaluation with `openai_client.evals.create()`, then start a run with `openai_client.evals.runs.create()`. The run targets a specific agent name and version — specify both so you can compare version 28 vs version 29. The data source type is `azure_ai_target_completions` which sends each query from the dataset to the hosted agent and collects responses for evaluation.

### View batch evaluation results in Foundry

![Evaluation results screenshot](slide_images/slide_22.png)
[Watch from 29:29](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1769s)

From the agent's Evaluation tab in Foundry, view overall metric results showing pass rates per evaluator. In the demo, most evaluators achieved 100% but Tool Output Utilization scored 50%. Digging into failures reveals reasons like "a claim was fabricated" or mismatches between tool output and the response. When failures appear, bring in domain experts to verify whether the judge's assessment is correct. Best practice is binary pass/fail (not 1-5 scales) so you can reason clearly about results. Foundry also offers an "Analyze Results" button for cluster analysis of failures.

### Scheduled evaluations

![Scheduled evaluations section header](slide_images/slide_23.png)
[Watch from 32:30](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1950s)

### What changes for scheduled evals

![Scheduled vs batch comparison](slide_images/slide_24.png)
[Watch from 32:32](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1952s)

Scheduled evals periodically send queries to a running agent and check for regressions. Compared to batch evals: the use case shifts from one-off deep analysis to ongoing monitoring, the dataset only needs queries (no ground truth required since the focus is regression detection), the trigger is recurring rather than immediate, and the code uses `schedules.create_or_update()` instead of `evals.runs.create()`.

### Create the schedule

![Schedule creation code](slide_images/slide_25.png)
[Watch from 33:13](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1993s)

After uploading a dataset and creating the evaluation, set up a schedule:

```python
schedule = Schedule(
    display_name="Daily Quality Eval",
    enabled=True,
    trigger=RecurrenceTrigger(
        interval=1,
        schedule=DailyRecurrenceSchedule(hours=[9]),
    ),
    task=EvaluationScheduleTask(
        eval_id=evaluation.id,
        eval_run=eval_run_definition,
    ))

project_client.beta.schedules.create_or_update(
    schedule_id=SCHEDULE_ID, schedule=schedule)
```

The full example is in `scheduled_eval.py`. You can set daily, hourly, or any recurrence interval.

### View scheduled evaluation results in Foundry

![Scheduled eval results screenshot](slide_images/slide_26.png)
[Watch from 33:45](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2025s)

Scheduled runs appear in the Evaluation tab marked as "scheduled run." For the demo, task adherence scored 80%, intent resolution 90%, and relevance 90%. You can drill into individual failures to understand why specific queries performed poorly.

### Continuous evaluations

![Continuous evaluations section header](slide_images/slide_27.png)
[Watch from 34:23](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2063s)

### What's different about continuous evals

![Continuous vs scheduled comparison](slide_images/slide_28.png)
[Watch from 34:26](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2066s)

Continuous evals differ from scheduled evals in several ways: they evaluate real live traffic rather than fixed queries, the data source is live agent traces from App Insights rather than an uploaded dataset, no dataset upload is needed, and the trigger is hourly. This requires your agent to be exporting traces via OpenTelemetry to App Insights (covered in session 1 on observability). This is the most valuable evaluation type because it shows how your agent handles real user queries.

### Create the continuous eval schedule

![Continuous eval code](slide_images/slide_29.png)
[Watch from 35:39](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2139s)

The key difference in code is the data source configuration:

```python
evaluation = openai_client.evals.create(
    name="Continuous Evaluation",
    data_source_config=AzureAIDataSourceConfig(
        type="azure_ai_source",
        scenario="responses"),
    testing_criteria=[...])

schedule = Schedule(
    trigger=RecurrenceTrigger(interval=1, schedule=HourlyRecurrenceSchedule()),
    task=EvaluationScheduleTask(
        eval_id=evaluation.id,
        eval_run={
            "data_source": {
                "type": "azure_ai_traces",
                "agent_name": AGENT_NAME,
                "max_traces": 1000,
            }}))
```

The data source type `azure_ai_traces` samples from App Insights traces filtered by agent name. The full example is in `continuous_eval.py`.

### View continuous evaluation results in Foundry

![Continuous eval results screenshot](slide_images/slide_30.png)
[Watch from 36:16](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2176s)

Continuous eval results include a `trace_id` and `span_id` per row, linking each evaluation back to the original user interaction. Scores may vary more because they depend on what users are actually asking — if users send off-topic questions (like "Who won the Super Bowl?"), pass rates will drop. This is expected and useful because it reveals how your agent handles real-world queries it wasn't optimized for.

### Catch quality regressions with eval alerts

![Eval alerts code](slide_images/slide_31.png)
[Watch from 38:07](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2287s)

Set up alert rules in App Insights based on evaluation pass rates. Continuous evals store a `gen_ai.evaluation.result` trace in App Insights that can be queried. Create a scheduled query rule that fires when pass rate drops below a threshold (e.g., 70%). Attach an action group to get notified via email, SMS, or other channels. The rule uses the Azure Management REST API to create a `LogAlert` with a KQL query filtering by project ID and agent name, summarizing the pass rate. The full example is in `continuous_eval_alert.py`.

### Safety evaluation

![Safety evaluation section header](slide_images/slide_32.png)
[Watch from 42:00](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2520s)

### What makes an agent's output safe

![Safety definition slide](slide_images/slide_33.png)
[Watch from 42:04](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2524s)

An agent's output should not harm users, reduce trust in your organization, or cause your app to break laws. Specifically, it should not generate hateful or unfair speech, encourage violence or self-harm, produce sexual content, allow access to protected/copyrighted materials, or change its behavior due to a jailbreak attack.

### Safety evaluation process

![Red teaming pipeline diagram](slide_images/slide_34.png)
[Watch from 42:46](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2566s)

Automated red teaming uses three components: an adversarial LLM (with guardrails removed so it can generate malicious probes like "How to rob a bank?"), Pyrit which transforms probes using attack strategies (e.g., reversing text to "?knab bor a woh"), and a Risk and Safety Evaluator LLM that judges whether the target's response was safe or unsafe. If the agent provides instructions for harmful actions, the attack is "successful" (meaning safety failed). If the agent refuses, the attack failed (meaning safety held). See the [AI red teaming agent documentation](https://learn.microsoft.com/azure/ai-foundry/concepts/ai-red-teaming-agent) for more.

### Which Python package to use

![Package comparison table](slide_images/slide_35.png)
[Watch from 46:42](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2802s)

Two packages support red teaming: `azure-ai-evaluation[redteam]` works with any callable target (local HTTP endpoint, function) and shows results in the new Foundry UI, but doesn't yet support Foundry hosted agents directly. `azure-ai-projects` supports Foundry hosted agents but doesn't show results in the new Foundry UI yet. Since this series is about hosted agents, the demo uses `azure-ai-evaluation` running against a local agent server as a workaround. The team is working on full hosted agent support.

### Configure the red team

![Red team configuration code](slide_images/slide_36.png)
[Watch from 48:03](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2883s)

```python
from azure.ai.evaluation.red_team import AttackStrategy, RedTeam, RiskCategory

model_red_team = RedTeam(
    azure_ai_project=azure_ai_project_endpoint,
    credential=credential,
    risk_categories=[
        RiskCategory.Violence,
        RiskCategory.HateUnfairness,
        RiskCategory.Sexual,
        RiskCategory.SelfHarm,
    ],
    num_objectives=1,  # Questions per category
)
```

The red team connects to a Foundry project to access the adversarial LLM and safety evaluator LLM. Set `num_objectives` to at least 10-20 for a comprehensive scan (1 is just for demo speed). The full example is in `red_team_scan_local.py`.

### Run the red team scan

![Run scan code](slide_images/slide_37.png)
[Watch from 48:56](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=2936s)

```python
await model_red_team.scan(
    scan_name=scan_name,
    target=callback,
    attack_strategies=[
        AttackStrategy.Baseline,
        AttackStrategy.Url,
        AttackStrategy.Tense,
        AttackStrategy.Compose([AttackStrategy.Tense, AttackStrategy.Url]),
    ],
    output_path=f"{root_dir}/{scan_name}.json"
)
```

**Baseline** sends plain text. **Url** replaces spaces with `%20` — this frequently bypasses naive safety barriers. **Tense** rewords questions in past tense (e.g., "In the 1800s, how would one have robbed a bank?") which often tricks models into answering. **Compose** combines strategies — Tense + Url together has the highest attack success rate in practice. The target is the local agent server running at localhost:8888. Results are saved locally as JSON.

### Review the red team results

![Red team results JSON and TUI](slide_images/slide_38.png)
[Watch from 51:13](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=3073s)

Results include a scorecard with attack success rate (ASR) per category and overall. In the demo, all 12 prompts (4 questions x 3 attack strategies) resulted in safe responses — 0% ASR across all categories. For any failures, inspect the adversarial prompts and the agent's responses to understand what went wrong. Warning: the adversarial prompts can be extremely graphic and disturbing, so only review them when necessary.

### When should you run a red team

![Red team timing guidance](slide_images/slide_39.png)
[Watch from 52:56](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=3176s)

Red teaming scans are expensive (many LLM calls with hundreds of questions), so don't run them on every code change. Run them when you change the model, model provider, temperature, or make significant prompt changes to guidelines. Run them less frequently than quality evals. A comparison across models shows frontier models like GPT-4o-mini achieve 0% ASR (very well protected from safety training), while smaller local models vary — Llama 3.1:8b scored 2% and Hermes 3:3b scored 13%. Smaller models generally have less safety training, so red team them more carefully. See [aka.ms/blog/redteaming-rag-app](https://aka.ms/blog/redteaming-rag-app) for more details.

### Guardrails

![Guardrails section header](slide_images/slide_40.png)
[Watch from 54:33](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=3273s)

### Risk mitigation layers

![Risk mitigation layers diagram](slide_images/slide_41.png)
[Watch from 54:50](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=3290s)

When designing AI-based software, safety should be considered at all layers (from inner to outer): the **Model** itself (choose the right model — frontier models include RLHF safety training), the **Safety System** (monitors and protects model inputs and outputs), **System Message & Grounding** (steer behavior with instructions and ground in trusted data), and **User Experience** (design for responsible human-AI interaction). You control all of these layers; use them together for defense in depth.

### Azure AI Content Safety

![Content Safety overview](slide_images/slide_42.png)
[Watch from 55:38](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=3338s)

Azure AI Content Safety is a configurable system that detects safety violations in prompts and outputs, detects jailbreak attempts (both direct and indirect via grounding data), and detects use of protected/copyrighted materials. It's always enabled for Azure OpenAI and Foundry direct models (DeepSeek, Mistral, etc.) and is also available as a standalone service. Learn more at [aka.ms/ContentSafety](https://aka.ms/ContentSafety).

### Guardrails in Microsoft Foundry

![Foundry guardrails configuration](slide_images/slide_43.png)
[Watch from 56:23](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=3383s)

By default, Foundry models use a built-in filter that blocks most categories at "medium" level. You can create custom filters to change blocked categories and severity levels. For agents using knowledge bases or web search, create a custom filter that also checks for indirect prompt injections (where malicious instructions are embedded in retrieved documents). Filters cannot be fully disabled without a special process — this is intentional to maintain baseline safety. Custom filters can be applied per model deployment.

### Content safety filter error responses

![Error response JSON structure](slide_images/slide_44.png)
[Watch from 58:13](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=3493s)

When content violates the filter, the server returns a 400 error with code `content_filter` and an inner error code `ResponsibleAIPolicyViolation`. The `content_filter_result` object shows which category triggered (hate, jailbreak, self_harm, sexual, violence) with its severity level and whether it was filtered. This structured response lets your application handle violations gracefully.

### Handling content filter errors in agents

![Content filter middleware code](slide_images/slide_45.png)
[Watch from 58:36](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=3516s)

In agent-framework, handle content filter errors with custom middleware:

```python
async def content_filter_middleware(
    context: ChatContext, call_next: Callable[[], Awaitable[None]]):
    """Convert model filter errors into user-friendly assistant response."""
    try:
        await call_next()
    except OpenAIContentFilterException:
        context.result = ChatResponse(
            messages=Message("assistant", ["Your message was blocked."]),
            finish_reason="stop")

client = FoundryChatClient(
    project_endpoint=PROJECT_ENDPOINT,
    credential=credential,
    model=MODEL_DEPLOYMENT_NAME,
    middleware=[content_filter_middleware])
```

Always handle content filter errors — they will happen in production. Provide a user-friendly message, and consider adding special logging for content filter triggers. The full example is in `stage4_foundry_hosted.py`.

### Next steps and resources

![Next steps slide](slide_images/slide_46.png)
[Watch from 59:54](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=3594s)

Watch past recordings at [aka.ms/foundryhosted/resources](https://aka.ms/foundryhosted/resources). Join Discord office hours after each session at [aka.ms/pythonai/oh](https://aka.ms/pythonai/oh).

## Live Chat Q&A

### Can evaluations be run inside the user-facing loop (online evaluation)?

[Watch from 22:50](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=1370s)

You could run an evaluation at the point you're responding to the user — generating a response, evaluating it, and only sending it if it passes. The major drawback is latency: you can't stream the response while evaluating it. Most applications don't do online evaluation because of its effect on user experience. However, for mission-critical agents where accuracy must be double-checked and users are willing to wait, it could make sense. Currently this would be custom code rather than a built-in Foundry feature.

### How can we avoid indirect prompt injection in search results?

[Watch from 56:43](https://www.youtube.com/watch?v=GiJQhMl0mWc&t=3403s)

Create a custom guardrail filter in Foundry that checks for indirect prompt injections. The default filter only checks for direct jailbreaks. When your agent uses grounding from a knowledge base or web search, indirect prompt injection (malicious instructions hidden in retrieved documents) becomes a real threat. By creating a custom filter with indirect jailbreak detection enabled, you protect against both direct and indirect attacks.

### Does the evaluation report provide comparison against previous runs or averages over time?

Yes. Foundry provides a compare feature that lets you view evaluation results side-by-side across different runs. You can compare metrics, individual test cases, and see how scores changed between agent versions or over time. See [Compare the evaluation results](https://learn.microsoft.com/azure/foundry/how-to/evaluate-results#compare-the-evaluation-results) for details.

### What is the pricing for evaluations?

Evaluation pricing is part of Foundry Observability. Costs depend on the number of evaluator runs, the model used for LLM-as-judge scoring, and trace storage in App Insights. See the [Foundry Observability pricing page](https://azure.microsoft.com/pricing/details/foundryobservability/) for current rates.

### Is there a way to create synthetic data for ground truth?

Yes. Foundry supports synthetic data generation for evaluation datasets. You can generate synthetic question-answer pairs based on your knowledge sources, which is useful when you don't have enough human-curated ground truth. See [Synthetic data evaluation](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/cloud-evaluation?tabs=python#synthetic-data-evaluation-preview) for setup instructions.

## Discord OH Q&A

### Are there evals that score on cost and token efficiency?

📹 [00:53](https://youtube.com/watch?v=B3-otzOjgJI&t=53)

There are no built-in evaluators for cost/token efficiency, but you can write a [custom code-based evaluator](https://learn.microsoft.com/azure/foundry/concepts/evaluation-evaluators/custom-evaluators#code-based-evaluators) for it. Token usage usually comes back in the API response (especially with the Responses API), so as long as that data is available, you can write a Python function that pulls it out and evaluates it. If token usage isn't in the API response, it should also be in OpenTelemetry traces, which is another way to access that data.

Pamela also always measures latency in her evaluations, which is straightforward since it's just elapsed time.

Note that Foundry evaluations do return operational metrics (latency and tokens) for each evaluation run, but those measure the evaluation itself, not the agent run being evaluated.

#### Are there built-in evaluators that don't depend on LLM-as-a-judge?

📹 [04:32](https://youtube.com/watch?v=B3-otzOjgJI&t=272)

Yes — there are textual similarity evaluators (BLEU, ROUGE, etc.) from the NLP research space that don't use LLMs. However, Pamela doesn't recommend most of them for agents producing free-flowing text responses, as they tend not to be useful in that context.

The more practical approach is [custom code-based evaluators](https://learn.microsoft.com/azure/foundry/concepts/evaluation-evaluators/custom-evaluators#code-based-evaluators). For example, Pamela has a regex-based evaluator for her RAG app that checks whether citations in the answer match the ground truth — and it's one of her most useful evaluators. Code-based evaluators are also great for measuring things like token usage and latency without needing an LLM.

### How can agent context (like memory) be included in quality evaluations?

📹 [07:23](https://youtube.com/watch?v=B3-otzOjgJI&t=443)

When we send the hosted agent's response for judging, the `output_items` field in the responses contains not just the final output but all tool calls along the way. So if memory is implemented as a tool call, it will be included in `output_items` and visible to the evaluators. Many evaluators that appear to be end-to-end (like intent resolution) actually look at everything in the output items, including intermediate tool calls.

If memory isn't showing up in the output items, you'd need to find a way to inject it into the API response, since the evaluator can only access data that's either in the uploaded dataset or in the API response. With Foundry hosted agents using the Responses API adapter, there are constraints on what can be added to the response.

### In a multi-agent environment, should we have evals for each agent or just the final response?

📹 [10:22](https://youtube.com/watch?v=B3-otzOjgJI&t=622)

Both — start with end-to-end evaluations to get an overall picture, then break it down per agent to pinpoint where failures originate. How you evaluate depends on your multi-agent architecture:

- **Agents-as-tools architecture**: Each sub-agent is a tool, so you can use the built-in tool evaluators to check whether each agent was called correctly and what its response looked like.
- **More flexible architectures**: You'll likely need a [custom evaluator](https://learn.microsoft.com/azure/foundry/concepts/evaluation-evaluators/custom-evaluators#code-based-evaluators) — for example, a "handoff evaluator" that checks whether the triage agent correctly passed to the refund agent in the right scenarios.

Pamela noted that in her experience with handoff orchestration in Agent Framework, the handoffs were sometimes unpredictable, so a handoff evaluator could be very worthwhile. She'll also check with the product team about potential built-in multi-agent evaluators in the future.

#### Would the interaction between agents (agent to sub-agent) need to be evaluated differently?

📹 [27:30](https://youtube.com/watch?v=B3-otzOjgJI&t=1650)

Yes, it depends on your architecture. For supervisor/agents-as-tools patterns, agents are just tools and can be evaluated that way. For more flexible architectures, a custom evaluator that looks at agent-to-agent interaction is the way to go — for example, evaluating whether handoffs happened at the right time with the right criteria.

### What does the "Analyze Results" cluster analysis do? Is it like theme analysis?

📹 [12:49](https://youtube.com/watch?v=B3-otzOjgJI&t=769)

The "Analyze Results" button on evaluation runs performs a cluster analysis that groups different kinds of failures together, helping you understand patterns in what went wrong. For example, on a run with 178 samples, it found clusters like "hallucinated response" (73 samples), "required rule unavailable", and "abrupt refusal" — each with suggestions for improvement.

This is different from general theme analysis because it specifically focuses on failures and how to fix them, rather than looking at all responses for general themes. It filters on failed samples and provides actionable suggestions.

### How can you approach streaming and online evaluation together?

📹 [16:13](https://youtube.com/watch?v=B3-otzOjgJI&t=973)

Generally, we don't recommend blocking live user-facing flows for evaluation calls. However, you could try a few approaches:

1. **Self-evaluation in the stream**: Ask the LLM to include its confidence level at the start or end of its streamed response. You can regex that out and render it in the UI. If confidence is low, trigger a second evaluation pass.

2. **Progress updates**: If doing online eval, stream updates to the user showing where you are in the process — "searching", "generating candidate response", "evaluating candidate response" — so they know something is happening rather than just watching a loading indicator.

3. **Confidence visualization**: The [Microsoft HAX Toolkit](https://www.microsoft.com/en-us/haxtoolkit/library/example,guideline/) has examples of highlighting low-confidence tokens in UI, showing users which parts of a response the model is less sure about.

Links shared:

- [Microsoft HAX Toolkit - Design Library](https://www.microsoft.com/en-us/haxtoolkit/library/example,guideline/)
- [Microsoft HAX Toolkit - Research Project](https://www.microsoft.com/en-us/research/project/hax-toolkit/)

### What is the recommended practice for running evals after the app is live?

📹 [20:50](https://youtube.com/watch?v=B3-otzOjgJI&t=1250)

Use a mix of scheduled evaluations at different frequencies:

- **Hourly**: A smoke test with ~5 queries to catch anything that's gone horribly wrong
- **Daily**: A medium test with ~50 queries for more thorough coverage
- **Weekly**: A larger test for comprehensive evaluation

The Foundry documentation defaults to daily for scheduled evals. You can set up multiple schedules with different names. Running 5 questions once an hour costs almost nothing.

#### Are there benchmarks or cutoff scores to say an app is prod ready?

📹 [22:30](https://youtube.com/watch?v=B3-otzOjgJI&t=1350)

There's no universal cutoff. Even 100% on an evaluation doesn't mean the app is perfect, since these are LLM-based apps with LLM judges. Internal teams at Microsoft often run evaluations on at least 800–1,000 questions before the first deploy, but they use different thresholds for pass rates.

The practical approach many teams take: do your best effort with evaluations, then put the app out with appropriate UI messaging ("this is AI-generated, please give feedback"), and use continuous evaluation and user feedback to continue improving.

### Can images and audio be used in Foundry safety evaluations?

📹 [24:15](https://youtube.com/watch?v=B3-otzOjgJI&t=1455)

Not yet. Multimodal safety evaluation would require image and audio models with their guardrails turned off so they can analyze potentially unsafe content. The evaluation team is considering adding multimodal safety evaluations in the future.

### How does Azure AI Search compare to Work IQ, and how can you evaluate Work IQ retrieval?

📹 [33:40](https://youtube.com/watch?v=B3-otzOjgJI&t=2020)

Work IQ is an agent that wraps different retrieval mechanisms (SharePoint, emails, chats). To compare it with Azure AI Search, you'd run the same queries through both and compare results. However, it's important to understand what you're comparing:

- **Remote SharePoint** knowledge source in Azure AI Search/Foundry IQ uses a similar retrieval mechanism to Work IQ (API maintained by the M365 team)
- **Indexed SharePoint** knowledge source runs ingestion and creates chunks in your search index, giving you Azure AI Search's hybrid search and semantic ranking

So comparing Work IQ vs. Azure AI Search with indexed SharePoint would be the more meaningful comparison, since remote SharePoint and Work IQ use similar underlying retrieval.

#### What is Foundry IQ exactly?

📹 [36:37](https://youtube.com/watch?v=B3-otzOjgJI&t=2197)

Foundry IQ is Azure AI Search using the new agentic knowledge base feature, typically accessed via the [MCP endpoint](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-retrieve?pivots=python#call-the-mcp-endpoint). The agentic knowledge base can wrap multiple sources including search indexes, indexed SharePoint, remote SharePoint, Bing, OneLake, and blob storage.

### How do you integrate evals with CI/CD?

📹 [41:27](https://youtube.com/watch?v=B3-otzOjgJI&t=2487)

Foundry has a built-in [GitHub Action for running evaluations](https://learn.microsoft.com/azure/foundry/how-to/evaluation-github-action) in CI/CD. You specify your sample data file and evaluators in the YAML config. Important: don't run evaluations on every commit. Instead, use a trigger like a `/evaluate` comment on PRs (with permissions checks so only authorized users can trigger it).

Pamela showed her existing [custom CI/CD eval workflow](https://github.com/Azure-Samples/azure-search-openai-demo/blob/main/.github/workflows/evaluate.yaml) for the RAG demo app, which uses a comment-based trigger restricted to repo owners, contributors, collaborators, and members. Another idea: use an LLM to look at a PR and decide whether evaluation should run automatically.

She needs to verify that the GitHub Action works with Foundry hosted agents specifically (it may have been built for prompt agents originally).

### Are there roadmaps for Foundry preview features going GA?

📹 [45:10](https://youtube.com/watch?v=B3-otzOjgJI&t=2710)

Pamela doesn't know specific timelines. Build (about a month away) is a common time for GA announcements, but she can't confirm anything. For hosted agents specifically, she'd want a longer baking period since it's a complex feature. She'll keep an eye out and share any news.

### Is there an agent or tool that can help create evaluations automatically in Foundry?

📹 [54:39](https://youtube.com/watch?v=B3-otzOjgJI&t=3279)

There are a few things moving in this direction:

- **Foundry Agent Skills**: The [`microsoft-foundry` skill](https://github.com/microsoft/azure-skills/tree/main/skills/microsoft-foundry/foundry-agent) in the azure-skills repo has an [observe section](https://github.com/microsoft/azure-skills/blob/main/skills/microsoft-foundry/foundry-agent/observe/observe.md) with skills for building evaluations. There's also an eval datasets skill. These are somewhat specific to the Foundry Toolkit extension.
- **Nitya's Build Lab**: The ["Observe, optimize and protect your hosted agents"](https://build.microsoft.com/en-US/sessions/LAB540?source=sessions) lab at Build will cover using skills and agents to build better evaluations.
- **Hamel Husain's eval skills**: Generic [eval skills](https://github.com/hamelsmu/evals-skills) including an ["eval audit"](https://github.com/hamelsmu/evals-skills/blob/main/skills/eval-audit/SKILL.md#2-evaluator-design) that checks best practices (e.g., ensuring evaluators are binary pass/fail rather than 1-5 scales). Even without using the skill directly, the criteria are useful as best practices.
