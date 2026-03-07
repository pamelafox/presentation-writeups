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
     Orchestrating advanced multi-agent workflows
aka.ms/pythonagents/slides/advancedworkflows
Pamela Fox
Python Cloud Advocate
www.pamelafox.org
```

## Slide 3

![Slide 3](slide_images/slide_3.png)

```
Today we'll cover...
• Concurrent workflows with fan-out and fan-in edges
• Aggregation patterns: summary, ranking, voting, extraction
• Conditional routing with concurrent execution
• Built-in orchestrations:
   • ConcurrentBuilder
   • MagenticBuilder for dynamic planning
   • HandoffBuilder for dynamic routing
• E2E application with workflows
```

## Slide 4

![Slide 4](slide_images/slide_4.png)

```
Want to follow along?
1. Open this GitHub repository:
aka.ms/python-agentframework-demos
2. Use "Code" button to create a GitHub Codespace:




3. Wait a few minutes for Codespace to start up
4. Run git pull to ensure you have the latest changes
```

## Slide 5

![Slide 5](slide_images/slide_5.png)

```
Recap: What's an agentic workflow?
An agentic workflow is a flow that involves an agent at some point,
typically to handle decision making or answer synthesis.
                                          Agent
               Processing                                 Processing
 Input              or                    LLM                  or         Output
               Data Lookup                                Data Lookup
                                   Tool         Tool



In agent-framework, a workflow is a graph with Executor nodes and edges between:

               Executor     edge    Executor           edge   Executor
   Input                                                                 Output
```

## Slide 6

![Slide 6](slide_images/slide_6.png)

```
Concurrent execution
```

## Slide 7

![Slide 7](slide_images/slide_7.png)

```
Sequential execution vs. Concurrent execution
               Input                                  Input


             Executor
                                           Executor            Executor

             Executor

                                                      Output
              Output
                                            Executors run in parallel
Only one executor runs at a given time.   and outputs are aggregated.
```

## Slide 8

![Slide 8](slide_images/slide_8.png)

```
Anatomy of a concurrent workflow
This is a common topology, where inputs fan-out and outputs fan-in to aggregator:

                                                     aggregator
                            Executor
    Input                                             Executor         Output
                            Executor


 Also possible:
 • workflows with dynamic fan-out (optional executors)
 • workflows without an explicit aggregator
```

## Slide 9

![Slide 9](slide_images/slide_9.png)

```
agent-framework

Using fan-in/fan-out edges in workflows



Use WorkflowBuilder with add_fan_out_edges and add_fan_in_edges:
 workflow = (WorkflowBuilder(
       name="FanOutFanInEdges",
       description="Explicit fan-out/fan-in using edge groups.",
       start_executor=dispatcher,
     output_executors=[aggregator])
    .add_fan_out_edges(dispatcher, [researcher, marketer, legal])
    .add_fan_in_edges([researcher, marketer, legal], aggregator)
    .build())
Full example: workflow_fan_out_fan_in_edges.py
```

## Slide 10

![Slide 10](slide_images/slide_10.png)

```
agent-framework

Aggregating results from fan-out edges



class AggregateInsights(Executor):
   @handler
   async def aggregate(
       self,
       results: list[AgentExecutorResponse],
       ctx: WorkflowContext[Never, str]):
       for result in results:
         # Process result.executor_id and result.agent_response.text
       await ctx.yield_output(consolidated)
Full example: workflow_fan_out_fan_in_edges.py
```

## Slide 11

![Slide 11](slide_images/slide_11.png)

```
Aggregation
```

## Slide 12

![Slide 12](slide_images/slide_12.png)

```
Aggregation patterns for fan-in agents
                                      Agent A
                                                                                                    Final
      Input                                                              Aggregator
                                                                                                   output
                                      Agent B

Pattern               Aggregator implementation            Final output     When to use?
Concatenation         String operations or template        Formatted str You control the layout exactly

Output synthesis      LLM call to summarize outputs        Natural prose You want a human-readable summary
                                                           Pydantic
Structured extraction LLM call with structured outputs                      Downstream code needs typed data
                                                           model
Score & rank          LLM-as-a-judge call to score outputs Ranked list      Generate N options, pick the best

Majority vote         Count most common output label       Winner label     Multiple judges classify same input
```

## Slide 13

![Slide 13](slide_images/slide_13.png)

```
agent-framework

Aggregation with LLM summary
                   "Research shows.."          LLM
                                                             The aggregator node uses an
                                                             LLM call to aggregate the
                   "The competitors..."   "In summary,..."   combined outputs from agents.

                   "According to laws,"

class SummarizerExecutor(Executor):
  def __init__(self, client: OpenAIChatClient, id: str):
      super().__init__(id=id)
      self.agent = Agent(client=client, name=id, instructions="Summarize...")
  @handler
  async def run(self, results, ctx):
      sections = [f"[{r.executor_id}]\n{r.agent_response.text}"
                    for r in results]
      response = await self.agent.run("\n".join(sections))
      await ctx.yield_output(response.text)
Full example: workflow_aggregator_summary.py
```

## Slide 14

![Slide 14](slide_images/slide_14.png)

```
agent-framework

Aggregation with structured extraction
                                                                          class CandidateReview(BaseModel):
                                                                            technical_score: int
                    "Strong coding..."           LLM                        technical_reason: str
                                                                            behavioral_score: int
                                                                            behavioral_reason: str
                    "Lacked leadership.."   "recommendation": "no hire"     recommendation: Literal[
                                            "technical_score": 9             "strong hire", "no hire",
                                            "behavioral_score": 5            "hire with reservations"]
                    "A bit snarky..."

 class ExtractReview(Executor):
    @handler
    async def extract(self, results, ctx):
       combined = "\n".join(r.agent_response.text for r in results)
       messages = [Message(role="system", text="Review candidate."),
                     Message(role="user", text=combined)]
       response = await self._client.get_response(messages,
                               options={"response_format": CandidateReview})
       await ctx.yield_output(response.value)
Full example: workflow_aggregator_structured.py
```

## Slide 15

![Slide 15](slide_images/slide_15.png)

```
agent-framework

Aggregation with LLM-ranking
                      "Conquer your commute!"
                                                            LLM
                                                                            The aggregator node uses an
                                                                            LLM call to rank the outputs
                      "Reliable. Affordable."         BoldWriter: 9
                                                                            from the agents.
                                                      MinimalistWriter: 7
                                                      EmotionalWriter: 6
                      "Affordable electric freedom"


class RankerExecutor(Executor):
  @handler
  async def run(self, results, ctx):
    slogans = [f"{r.executor_id}: \"{r.agent_response.text}\"" for r in results]
    messages = [Message(role="system", text=("Score each slogan 1-10 with a reason")),
                Message(role="user", text="Candidate slogans:\n" + "\n".join(slogans))]
    response = await self._client.get_response(messages,
                                               options={"response_format": RankedSlogans})
    await ctx.yield_output(response.value)

Full example: workflow_aggregator_ranked.py
```

## Slide 16

![Slide 16](slide_images/slide_16.png)

```
agent-framework

Aggregation with majority vote
                       category: "feature"
                                                                Each agent outputs their vote,
                                                                and the aggregator calculates
                      category: "bug"         category: "bug"   the most popular choice.

                      category: "bug"

class TallyVotes(Executor):
  @handler
  async def tally(self, results: list[AgentExecutorResponse],
                        ctx: WorkflowContext[Never, str]):
    votes = []
    for result in results:
      classification: Classification= result.agent_response.value
      votes.append(classification.category.value)
    winner, count = Counter(votes).most_common(1)[0]
    await ctx.yield_output(winner)
Full example: workflow_aggregator_voting.py
```

## Slide 17

![Slide 17](slide_images/slide_17.png)

```
Conditional routing + concurrency
```

## Slide 18

![Slide 18](slide_images/slide_18.png)

```
Conditional routing with concurrent execution

                                                     Agent A


    Input            selection                       Agent B


                                                     Agent C



 The input is sent to any number of concurrent executors based off a selection function.
```

## Slide 19

![Slide 19](slide_images/slide_19.png)

```
agent-framework

Workflows with multi-selection edge groups

                                                Based off the selection_func, the
                                                workflow sends the input to the selected
                                                executors for concurrent processing.


workflow = (WorkflowBuilder(name="MultiSelectionEdgeGroup",
                             start_executor=parse_ticket)
            .add_multi_selection_edge_group(
               parse_ticket,
               [support, engineering, billing],
               selection_func=select_targets)
            .build())
Full example: workflow_multi_selection_edge_group.py
```

## Slide 20

![Slide 20](slide_images/slide_20.png)

```
Built-in workflow orchestrations
https://learn.microsoft.com/agent-framework/workflows/orchestrations/

   https://learn.microsoft.com/agent-framework/workflows/orchestrations/
```

## Slide 21

![Slide 21](slide_images/slide_21.png)

```
ConcurrentBuilder
https://learn.microsoft.com/agent-framework/workflows/orchestrations/concurrent
```

## Slide 22

![Slide 22](slide_images/slide_22.png)

```
agent-framework

Using the built-in ConcurrentBuilder workflow
from agent_framework.orchestrations import ConcurrentBuilder

workflow = ConcurrentBuilder(
            participants=[researcher, marketer, legal]).build()




The workflow assumes that participants accept and emit conversation-shaped data,
so executors must be Agents or custom Executors that process conversations.
The extra start/end nodes normalize input and output to list[Message].
Full example: workflow_agents_concurrent.py
```

## Slide 23

![Slide 23](slide_images/slide_23.png)

```
MagenticBuilder for dynamic planning
https://learn.microsoft.com/agent-framework/workflows/orchestrations/magentic
```

## Slide 24

![Slide 24](slide_images/slide_24.png)

```
Magentic-One workflow orchestration
     Magentic-One orchestrator
                                                                                        Task        Yes
                                                                                      complete?
                                                                                                          Final
              Task ledger                        Progress ledger
                                                                                                          result
              •        Given or verified facts   •   Task complete?
              •        Facts to look up          •   Is progress being made?                  No
              •        Facts to derive           •   What's next agent?
              •        Task plan                 •   Next agent instruction


                                                     Yes      Stall              No      Progress
                                                             count                        being
                                                               >1                         made?

                                                                                      Yes




                         Agent A                 Agent B                       Agent C
https://arxiv.org/abs/2411.04468

   https://arxiv.org/abs/2411.04468
```

## Slide 25

![Slide 25](slide_images/slide_25.png)

```
Magentic-One: Initial plan development
The orchestrator uses this prompt to plan:
                    To address this request we have assembled the following team:
                    - local_agent: A local assistant that can suggest local activities or



Specialist agents
                    places to visit.
                    - language_agent: A helpful assistant that can provide language tips
                    for a given destination.
                    - travel_summary_agent: A helpful assistant that can summarize the
                    travel plan.
                    Based on the team composition, and known and unknown facts, please
                    devise a short bullet-point plan for addressing the original request.
                    Remember, there is no requirement to involve all team members. A team
                    member's particular expertise may not be needed for this task.
```

## Slide 26

![Slide 26](slide_images/slide_26.png)

```
Magentic-One: Progress ledger updates
The orchestrator assesses progress after every turn, picks the next agent and tells it what to do.

          Has the task been done?    {"is_request_satisfied": {
                                          "answer": "no", "reason": "..."
                                       },
 Are agents repeating themselves?      "is_in_loop": {
                                          "answer": "no", "reason": "..."
                                       },
           Are we moving forward?      "is_progress_being_made": {
                                          "answer": "yes", "reason": "...",
                                       },
              Who should go next?      "next_speaker": {
                                               "answer": "travel_summary_agent", "reason": "...",
                                          },
             What should they do?         "instruction_or_question": {
                                            "answer": "Summarize the proposal", "reason": "...",
                                     }}
```

## Slide 27

![Slide 27](slide_images/slide_27.png)

```
agent-framework

Using the built-in MagenticBuilder workflow
     orchestrator
                                        The MagenticOrchestrator node
                                        contains a StandardMagenticManager,
                                        which wraps the provided manager_agent,
                                        and plans and delegates tasks.


magentic_workflow = MagenticBuilder(
  participants=[local_agent, language_agent, travel_summary_agent],
  manager_agent=manager_agent,
  max_round_count=10,
  max_stall_count=1,
  max_reset_count=1,
  ).build()

Full example: workflow_magenticone.py
```

## Slide 28

![Slide 28](slide_images/slide_28.png)

```
Magentic orchestration vs. Agent-as-tools
     plan
                         Manager                                Supervisor Agent
     ledger



               Agent A                 Agent B
                                                            Agent A                   Agent B

                              chat
                           history
 Planning Explicit (plan with progress ledger)      Implicit (reactive tool call decisions)

     Loop Progress ledger checks is_in_loop         No built-in loop detection
 detection
    Agent Full shared chat history                  Isolated per-call context
   context
Token cost Higher (plan + ledger+ shared history)   Lower
```

## Slide 29

![Slide 29](slide_images/slide_29.png)

```
Dynamic routing with HandoffBuilder
```

## Slide 30

![Slide 30](slide_images/slide_30.png)

```
From fixed graphs to dynamic routing
 FIXED GRAPH                                               DYNAMIC ROUTING
 Developer defines edges. LLM picks a path.                Agents decide the next step at runtime.

                                      edge(B, C)
                                                                                   agent decides
                                                                                                           B
                edge(A, B)   B                     C
       A                                                         A                     ?                   C
               edge(A, D)    D
                                                                                                           D

 • All edges declared at build time                        • No predefined edges between agents
 • LLM selects which branch, not which agent               • Routing emerges from conversation state
 • Topology is static — predictable and testable           • Topology is dynamic — flexible and adaptive

 WorkflowBuilder · SequentialBuilder · ConcurrentBuilder   HandoffBuilder
```

## Slide 31

![Slide 31](slide_images/slide_31.png)

```
Handoff orchestration
                                                      The start agent just
                                                      kicks off the flow.
                                       Agent B
    start agent
                                                      Any agent can hand off
                                                      control to any other
     Agent A                       handoff            agent at runtime.

                                       Agent C        The receiving agent fully
                                                      owns the conversation
                                                      until it hands back.

 No edges are defined up front – routing emerges from conversation state.
```

## Slide 32

![Slide 32](slide_images/slide_32.png)

```
agent-framework

Using the built-in HandoffBuilder workflow
                                           By default, all agents in a
   start agent                             handoff orchestration can
                                           handoff to every other agent.
                                           In autonomous mode, they will
                                           never ask the user for input.


workflow = (HandoffBuilder(
    name="content_pipeline",
    participants=[triage, researcher, writer, editor],
    termination_condition=lambda conversation: (len(conversation) > 0
        and conversation[-1].text.strip().startswith("FINAL:")))
  .with_start_agent(triage)
  .with_autonomous_mode()
  .build())
Full example: workflow_handoffbuilder.py
```

## Slide 33

![Slide 33](slide_images/slide_33.png)

```
agent-framework

HandoffBuilder with handoff rules
    start agent




workflow = (HandoffBuilder(
  participants=[triage_agent, order_agent, return_agent, refund_agent],
  termination_condition=lambda conversation: (
    len(conversation) > 0 and "goodbye" in conversation[-1].text.lower()))
    .with_start_agent(triage_agent)
    .add_handoff(triage_agent, [order_agent, return_agent])
    .add_handoff(return_agent, [refund_agent, triage_agent])
    .add_handoff(order_agent, [triage_agent])
    .add_handoff(refund_agent, [triage_agent])
    .with_autonomous_mode().build())
Full example: workflow_handoffbuilder_rules.py
```

## Slide 34

![Slide 34](slide_images/slide_34.png)

```
Handoff orchestration vs. Agent-as-tools
                    Delegated ownership                          Centralized ownership

                           Start agent                              Supervisor Agent




                              handoff
                 Agent A                 Agent B               Agent A                  Agent B
                              handoff

     Control Active agent transfers control to another   Supervisor calls sub-agent tools,
       Flow agent (peer-to-peer).                        control returns to supervisor.
       Task Ownership moves to receiving agent.          Supervisor retains ownership end-to-end.
  Ownership
    Context Conversation context is handed over.         Supervisor selects what context each tool gets.
Management
```

## Slide 35

![Slide 35](slide_images/slide_35.png)

```
End-to-end application
```

## Slide 36

![Slide 36](slide_images/slide_36.png)

```
Agentic AI investment analysis
                                                                         Agent Framework*
                                                                         FastAPI
                                                                         Azure OpenAI
                                                                         Azure Cosmos DB
                                                                         Azure Blob Storage




                                                                         *Uses an older MAF version,
                                                                         upgrades are pending.

https://github.com/Azure-Samples/Agentic-AI-Investment-Analysis-Sample
```

## Slide 37

![Slide 37](slide_images/slide_37.png)

```
Investment workflow with fan-out/fan-in
workflow = WorkflowBuilder()
  .set_start_executor(data_prep_executor)
  .add_fan_out_edges(data_prep_executor,
     [financial_analyst, risk_analyst,
      market_analyst, compliance_analyst])
  .add_fan_in_edges(
     [financial_analyst, risk_analyst,
      market_analyst, compliance_analyst],
     analysis_aggregator)
  .add_edge(analysis_aggregator, debate_executor)
  .add_edge(debate_executor, summary_report_generator)
  .build()
Full file: investment_workflow.py
```

## Slide 38

![Slide 38](slide_images/slide_38.png)

```
What-if workflow with fan-in/fan-out




workflow = WorkflowBuilder()
  .set_start_executor(planner_agent)
  .add_fan_out_edges(planner_agent,
     [financial_analyst_agent, risk_analyst_agent,
      market_analyst_agent, compliance_analyst_agent])
  .add_fan_in_edges(
     [financial_analyst_agent, risk_analyst_agent,
      market_analyst_agent, compliance_analyst_agent],
     summarizer_agent)
  .build()
Full file: what_if_workflow.py
```

## Slide 39

![Slide 39](slide_images/slide_39.png)

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
