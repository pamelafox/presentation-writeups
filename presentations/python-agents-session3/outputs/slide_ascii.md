# Slide text content

Text extracted from each slide of PythonAgents-MonitoringEvaluating.pdf.

## Slide 1

![Slide 1](slide_images/slide_1.png)

```
Python + Agents
Feb 24: Building your first agent in Python
Feb 25: Adding context and memory to agents
Feb 26: Monitoring and evaluating agents
Mar 3: Building your first AI-driven workflows
Mar 4: Orchestrating advanced multi-agent workflows
Mar 5: Adding a human-in-the-loop to workflows

Register at aka.ms/PythonAgents/series
```

## Slide 2

![Slide 2](slide_images/slide_2.png)

```
Python + Agents
       Monitoring and evaluating agents
aka.ms/pythonagents/slides/monitoreval
Pamela Fox
Python Cloud Advocate
www.pamelafox.org
```

## Slide 3

![Slide 3](slide_images/slide_3.png)

```
Today we'll cover...
• Monitoring
   • OpenTelemetry
   • Aspire
   • Azure Application Insights
• Evaluation
   • Azure AI Evaluation SDK
   • Local evaluations
   • Batch evaluations
   • Cloud evaluations
• Safety
   • Risks
   • Red-teaming
```

## Slide 4

![Slide 4](slide_images/slide_4.png)

```
Want to follow along?
1. Open this GitHub repository:
aka.ms/python-agentframework-demos

2. Use "Code" button to create a GitHub Codespace:

3. Wait a few minutes for Codespace to start up
```

## Slide 5

![Slide 5](slide_images/slide_5.png)

```
Recap: What's an agent?
          Agent
                          An AI agent uses an LLM to run
  Input                   tools in a loop to achieve a goal.

                          To make a high-quality AI agent, we need:

   LLM                       Monitoring: observe the tool calls and outputs
                             Evaluation: ensure outputs match our expectation
                  Tools

                          Put these in place before taking an agent to production.

   Goal
```

## Slide 6

![Slide 6](slide_images/slide_6.png)

```
Monitoring agents
https://learn.microsoft.com/agent-framework/agents/observability
```

## Slide 7

![Slide 7](slide_images/slide_7.png)

```
Observability with OpenTelemetry (OTel)
OTel standardizes how applications emit traces, metrics, and logs — making
debugging and performance analysis consistent across languages and vendors.

           Traces                           Metrics                          Logs
 0ms                   30ms     __/‾‾‾ cpu_usage:   30%         INFO: 2025-12-05: Server running
                                                                      {"region": "westus"}
       parent-span              ‾‾\__   latency_p95: 43ms
                                                                ERROR: 2025-12-05: User not found
          child-span            _/‾\__ errors:   0.2%                 {"user_id": 123}

Operations composed of spans    Numeric measurements such       Structured log records with
that show how a request moves   as CPU usage, request counts,   message, severity, time stamp,
through services, including     latency, error rates, or any    and contextual attributes.
timing, dependencies, and       custom app metric.
context propagation.”
```

## Slide 8

![Slide 8](slide_images/slide_8.png)

```
Using OpenTelemetry with Agent Framework
Agent framework has built-in support for generating OpenTelemetry traces.
Set ENABLE_CONSOLE_EXPORTERS=true in environment for console traces.
 from agent_framework.observability import configure_otel_providers

 configure_otel_providers(enable_sensitive_data=True)

 agent = Agent(
   name="weather-time-agent",
   client=client,
   instructions="You're an assistant that can look up weather and time.",
   tools=[get_weather, get_current_time])

 response = await agent.run(
   "What's the weather in Seattle and what time is it in Tokyo?")

Full example: agent_otel_aspire.py
```

## Slide 9

![Slide 9](slide_images/slide_9.png)

```
OTel-compliant observability platforms
                             Open source?   Managed version?
Aspire

Azure Application Insights

Datadog

Grafana

Prometheus                                  (via Grafana)

Jaeger

Logfire

...and many more!
```

## Slide 10

![Slide 10](slide_images/slide_10.png)

```
Exporting to Aspire dashboard
Set OpenTelemetry environment variables:
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc

Install the exporter for the configured OLTP export protocol (grpc or http):
opentelemetry-exporter-otlp-proto-grpc

Configure OpenTelemetry as usual in the agent module:
configure_otel_providers(enable_sensitive_data=True)
Full example: agent_otel_aspire.py
```

## Slide 11

![Slide 11](slide_images/slide_11.png)

```
Monitor agent in the Aspire dashboard
                                  Traces:
                                  • Agent executions
                                  • LLM calls
                                  • Tool calls

                                  Metrics:
                                  • Tool call durations
                                  • LLM call durations
                                  • LLM call token usage

                                  Logs:
                                  • Python logging calls
```

## Slide 12

![Slide 12](slide_images/slide_12.png)

```
Standard trace format for agent executions
Agent framework uses the standard "gen_ai" span attribute names and values
for agent executions, LLM calls, and tool calls. Example tool call:
Span: execute_tool get_weather
attribute name                   value

gen_ai.operation.name            execute_tool

gen_ai.tool.name                 get_weather

gen_ai.tool.type                 function

gen_ai.tool.call.arguments       {"city": "Seattle"}

gen_ai.tool.call.result          {"temperature": 72, "description": "Sunny"}
                                 Returns weather data for a given city, a
gen_ai.tool.description
                                 dictionary with temperature and description.
```

## Slide 13

![Slide 13](slide_images/slide_13.png)

```
Exporting OTel to Azure App Insights
Install in pyproject.toml:
azure-monitor-opentelemetry

Use wrapper function configure_azure_monitor to configure global
exporters based off the App Insights connection string:
from azure.monitor.opentelemetry import configure_azure_monitor
from agent_framework.observability import create_resource, enable_instrumentation

configure_azure_monitor(
  connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"],
  resource=create_resource(),
  enable_live_metrics=True,
)
enable_instrumentation(enable_sensitive_data=True)

Full example: agent_otel_appinsights.py
```

## Slide 14

![Slide 14](slide_images/slide_14.png)

```
Viewing traces in Azure App Insights
                                       1. Navigate to App
                                       Insights in Portal

                                       2. Find traces in
                                       Performances,
                                       Failures, or Logs tabs

                                       3. Create
                                       dashboards of what
                                       matters to you
```

## Slide 15

![Slide 15](slide_images/slide_15.png)

```
Evaluating agents
https://learn.microsoft.com/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators
```

## Slide 16

![Slide 16](slide_images/slide_16.png)

```
Agent output is non-deterministic
           Agent
                           Every call to an LLM increases the non-
   Input                   determism of the system.
                           Output quality will depend on:
                           • LLM choosing right tools
                           • LLM choosing right tool arguments
   LLM                     • LLM providing grounded and
                   Tools     comprehensive final response

                           Whenever you change LLM
                           model/params, prompts, or tools,
 Response
                           output can get better..or worse!
```

## Slide 17

![Slide 17](slide_images/slide_17.png)

```
Evaluating agent outputs: Human grading
Humans can spot-check output performance on small data sets and annotate issues
```

## Slide 18

![Slide 18](slide_images/slide_18.png)

```
Evaluating AI apps: Automated Evaluation
LLMs can measure output performance at scale across a broader range of risks
```

## Slide 19

![Slide 19](slide_images/slide_19.png)

```
Automated evaluation frameworks
Framework                          Author               Language   Cloud hosted?

azure-ai-evaluation /              Microsoft            Python     Optional
Microsoft.Extensions.AI.Evaluation                      .NET
tau2                               Sierra               Python     None

RAGAS                              ExplodingGradients   Python     None

DeepEval                           ConfidentAI          Python     Optional

Langsmith                          Langchain            Python     Required

openai (evals)                     OpenAI               Python     Optional
```

## Slide 20

![Slide 20](slide_images/slide_20.png)

```
Using the azure-ai-evaluation package
Install the package into your project:
azure-ai-evaluation

That will give you access to:
• Built-in evaluators for quality and safety
• A way to build custom evaluators (for anything!)
• Bulk evaluation functionality
• Automated red-teaming agent
• Ability to save results in AI Foundry (optional)
aka.ms/azure-ai-eval-sdk
```

## Slide 21

![Slide 21](slide_images/slide_21.png)

```
Built-in evaluators for AI agents
                    ToolCallAccuracyEvaluator:
           Did the agent invoke the right tools with right args?

                                                                      tool
                   tool_call       tool_call       tool_call       definitions

Input     Agent                    LLM               Response ResponseCompletenessEvaluator
                                                               Does response include all required
                                                                  info from the ground truth?

              IntentResolutionEvaluator:                                     Ground truth
            Did the agent achieve the user's goal?                            response

                 TaskAdherenceEvaluator:
  Did the agent follow prompt constraints and tool-use rules?
```

## Slide 22

![Slide 22](slide_images/slide_22.png)

```
Tool call accuracy
Evaluates the agent’s tool use: whether tool calls are relevant and correctly
formed per tool definitions (right tools, arguments, no uneeeded calls).
from azure.ai.evaluation import ToolCallAccuracyEvaluator

toolcall_evaluator = ToolCallAccuracyEvaluator(model_config)
result = toolcall_evaluator(
  query=[{"role": "system", "content": "You are a travel assistant."},
         {"role": "user", "content": "Plan a trip from New York to Tokyo"},
         # tool calls and results..],
  response="Here is your 3 day trip plan. First board a plane..."),
  tool_definitions= [t.to_json_schema_spec()["function"] for t in tools])
score (1-5)   5
reason        The agent called all four of those tools once each, which directly map to the user's
              needs (flights, lodging, weather, activities, budget breakdown)....

Full example: agent_evaluation.py
```

## Slide 23

![Slide 23](slide_images/slide_23.png)

```
Intent resolution
Measures how well the agent identifies the user's request, including how well it scopes
the user's intent, asks clarifying questions, and reminds end users of its capabilities.
from azure.ai.evaluation import IntentResolutionEvaluator

intent_evaluator = IntentResolutionEvaluator(model_config)
result = intent_evaluator(
  query=[{"role": "system", "content": "You are a travel assistant."},
         {"role": "user", "content": "Plan a trip from New York to Tokyo"},
          # tool calls and results..],
  response="Here is your 3 day trip plan. First board a plane...")

score (1-5)   4
reason        User wanted a NY→Tokyo trip. Agent provided a thorough itinerary, cost breakdown,
              packing/weather tip. Minor flaw: inconsistent return date (Mar 17 vs Mar 18.

Full example: agent_evaluation.py
```

## Slide 24

![Slide 24](slide_images/slide_24.png)

```
Task adherence
Measures how well agent's response adheres to its assigned tasks, according to its
system message and prior steps.
from azure.ai.evaluation import TaskAdherenceEvaluator

taskadherence_evaluator = TaskAdherenceEvaluator(model_config)
result = taskadherence_evaluator(
  query=[{"role": "system", "content": "You are a travel assistant."},
         {"role": "user", "content": "Plan a trip from New York to Tokyo"},
         # tool calls and results..],
  response="Here is your 3 day trip plan. First board a plane..."),
  tool_definitions= [t.to_json_schema_spec()["function"] for t in tools])

score (1-5)   0
reason        There is inconsistency between tool calls and itinerary dates: the flight tool call used departure=2026-
              03-15 and return=2026-03-17, but schedule lists “Day 3 — Mar 18,” implying return on Mar 18.

Full example: agent_evaluation.py
```

## Slide 25

![Slide 25](slide_images/slide_25.png)

```
Response completeness
Assesses how well the returned responses aligns with a ground truth response.
from azure.ai.evaluation import ResponseCompletenessEvaluator
ground_truth = """A complete 3-day Tokyo trip itinerary from New York
including: round-trip flight options with prices, hotel recommendations
within nightly budget, weather forecast for the travel dates, a full cost
breakdown, and packing suggestions based on weather."""
completeness_evaluator = ResponseCompletenessEvaluator(model_config)
result = completeness_evaluator(
  response="Here is your 3 day trip plan. First board a plane..."),
  ground_truth=ground_truth)

score (1-5)   5
reason        The response includes every item requested in the ground truth (multiple flight options with prices, hotel
              choices, date-specific weather, a detailed cost breakdown, and packing advice), so it is fully complete.

Full example: agent_evaluation.py
```

## Slide 26

![Slide 26](slide_images/slide_26.png)

```
Bulk evaluation of a dataset
To run same evaluators on many QA pairs, you can use evaluate():
from azure.ai.evaluation import evaluate

eval_result = evaluate(
  data=eval_data_file,
  evaluators={
    "intent_resolution": IntentResolutionEvaluator(model_config),
    "response_completeness": ResponseCompletenessEvaluator(model_config),
    "task_adherence": TaskAdherenceEvaluator(model_config),
    "tool_call_accuracy": ToolCallAccuracyEvaluator(model_config)},
  output_path="eval_results.json")

Full example: agent_evaluation_batch.py
```

## Slide 27

![Slide 27](slide_images/slide_27.png)

```
Viewing evaluation results locally
View results locally as JSON:   Or build your own custom CLI viewer:

 eval_results.json                 Tip: Ask Copilot to use Rich or Textual to build a CLI.
```

## Slide 28

![Slide 28](slide_images/slide_28.png)

```
Viewing evaluation results in AI Foundry
If you specify azure_ai_project, you can view results in the Foundry portal:

eval_result = evaluate(
  data=eval_data_file,
  evaluators={
    "intent_resolution": IntentResolutionEvaluator(model_config)},
  azure_ai_project="https://bla.services.ai.azure.com/api/projects/bla")

Full example: agent_evaluation_batch.py
```

## Slide 29

![Slide 29](slide_images/slide_29.png)

```
CI/CD evaluation results
You can run evaluations from a GitHub Actions workflow and display results in PRs:

https://github.com/Azure-Samples/rag-postgres-openai-python/blob/main/.github/workflows/evaluate.yaml
https://github.com/Azure-Samples/rag-postgres-openai-python/pull/130
```

## Slide 30

![Slide 30](slide_images/slide_30.png)

```
Dev loop for AI agents: Observe, Evaluate, Iterate
 1. Ideating/exploring                 2. Building/augmenting                   3. Productionizing

    Identify business       Run agent against          Run flow against
                                                                                Deploy agent to users
        use case            sample questions            larger dataset

                         Try different parameters      Evaluate answers         Collect user feedback

    Connect to tools
                               Change defaults                                  Run online evaluations

   Customize
  Improve theprompts
              prompt                                                             Run A/B experiments
   and tool definitons     Satisfied?        Yes     Satisfied?           Yes
   and orchestration

                          No                          No
```

## Slide 31

![Slide 31](slide_images/slide_31.png)

```
Safety evaluation
https://learn.microsoft.com/azure/ai-foundry/concepts/ai-red-teaming-agent
```

## Slide 32

![Slide 32](slide_images/slide_32.png)

```
What makes an agent's output safe?
Your agent should not produce output that harms users, that reduces the trust
of users in your organization, or causes your app to break any laws.
For example, it shouldn't...
  generate hateful or unfair speech toward the user or group of people
  encourage violence or self-harm           Risk & Safety
  produce sexual speech (though level may vary for health/medical apps)
  allow access to protected materials
  change its behavior due to a jailbreak attack
```

## Slide 33

![Slide 33](slide_images/slide_33.png)

```
Safety evaluation process
We can perform automated red-teaming using azure-ai-evaluation SDK:
                              RedTeaming agent
          Generate adversarial probe            Transform with attack strategy    Send to endpoint

               How to rob a bank?                  ?knab bor a woh
 Adversarial                            Pyrit
    LLM
                                                                                                     Target
                                            Evaluate response                     Receive response
                        Attack successful
                                                                                  1) Open the safe...
                                                                Risk and Safety
                                                                Evaluator LLM

https://learn.microsoft.com/azure/ai-foundry/concepts/ai-red-teaming-agent
```

## Slide 34

![Slide 34](slide_images/slide_34.png)

```
Configure the red-teaming agent
model_red_team = RedTeam(
  azure_ai_project=azure_ai_project_endpoint,
  credential=credential,
  risk_categories=[
     RiskCategory.Violence,
     RiskCategory.HateUnfairness,
     RiskCategory.Sexual,
     RiskCategory.SelfHarm,
  ],
  num_objectives=1, # Questions per category
)

Full example: agent_redteam.py
```

## Slide 35

![Slide 35](slide_images/slide_35.png)

```
Run the red-teaming scan
await model_red_team.scan(
  scan_name=scan_name,
  target=callback,
  attack_strategies=[
     AttackStrategy.Baseline,
     # Easy Complexity:
     AttackStrategy.Url,
     # Moderate Complexity:
     AttackStrategy.Tense,
     # Difficult Complexity:
     AttackStrategy.Compose([AttackStrategy.Tense, AttackStrategy.Url]),
  ],
  output_path=f"{root_dir}/{scan_name}.json"
)

Full example: agent_redteam.py
```

## Slide 36

![Slide 36](slide_images/slide_36.png)

```
Review the red teaming results
View results locally or in AI Foundry:

Inspect the adversarial prompts and responses from the target:

   Warning: the prompts can be graphic and concerning.
```

## Slide 37

![Slide 37](slide_images/slide_37.png)

```
When should you run a red team?
Red teaming scans take time, so don't run them on every code change.
Do run them on model changes or non-trivial prompt changes, however!

Model             Host             Attack success rate

gpt-4o-mini       Azure OpenAI       0%
llama3.1:8b       Ollama             2%
hermes3:3b        Ollama           13%

aka.ms/blog/redteaming-rag-app
```

## Slide 38

![Slide 38](slide_images/slide_38.png)

```
Next steps                      Register:
                                https://aka.ms/PythonAgents/series

Watch past recordings:          Join office hours after each session in Discord:
aka.ms/pythonagents/resources   aka.ms/pythonai/oh

    Feb 24: Building your first agent in Python
    Feb 25: Adding context and memory to agents
    Feb 26: Monitoring and evaluating agents
    Mar 3: Building your first AI-driven workflows
    Mar 4: Orchestrating advanced multi-agent workflows
    Mar 5: Adding a human-in-the-loop to workflows
```

## Slide 39

![Slide 39](slide_images/slide_39.png)

```
Appendix
```
