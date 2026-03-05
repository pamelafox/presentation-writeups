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
       Building your first AI-driven workflows
aka.ms/pythonagents/slides/workflows
Pamela Fox
Python Cloud Advocate
www.pamelafox.org
```

## Slide 3

![Slide 3](slide_images/slide_3.png)

```
Today we'll cover...
• Workflows: executors, edges, messages, and outputs
• Building a basic sequential workflow
• Using agents as workflow executors
• Visualizing workflow runs with DevUI
• Branching with conditional edges and switch-case routing
• Structured outputs for more reliable workflow routing
• Workflow state management
• Full-stack web application with an agentic workflow
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




   LLM
                  Tools



   Goal
```

## Slide 6

![Slide 6](slide_images/slide_6.png)

```
Workflows
```

## Slide 7

![Slide 7](slide_images/slide_7.png)

```
What's a workflow?
An agentic workflow is any flow that involves an agent at some point,
typically to handle decision making or answer synthesis.


               Processing                           Processing
 Input              or               Agent               or             Output
               Data Lookup                          Data Lookup
                                  Tool       Tool




 Not all calls in our systems should be agentic!
 Every call to an LLM increases the non-determinism of a system and
 possibility of failure or safety risk.
```

## Slide 8

![Slide 8](slide_images/slide_8.png)

```
agent-framework

Anatomy of a workflow
A workflow is a graph with Executor nodes and edges between them:

               Executor    edge   Executor    edge    Executor
   Input                                                             Output


Each executor subclass defines handler methods that receive messages
and may send messages to next executor and/or yield outputs:
class SampleExecutor(Executor):
  @handler
  async def sample_handler(self, text: str, ctx: WorkflowContext[str]):
    await ctx.send_message(text.upper())

class OutputExecutor(Executor):
  @handler
  async def sample_handler(self, text: str, ctx: WorkflowContext[Never, str]):
    await ctx.yield_output(text)
```

## Slide 9

![Slide 9](slide_images/slide_9.png)

```
agent-framework

Building a workflow
Use WorkflowBuilder() to connect instances of Executor() subclasses:

from agent_framework import WorkflowBuilder                 Input
extract = ExtractExecutor(id="extract")
chunk = ChunkExecutor(id="chunk")                       ExtractExecutor
embed = EmbedExecutor(id="embed")

workflow = WorkflowBuilder(start_executor=extract)      ChunkExecutor
  .add_edge(extract, chunk)
  .add_edge(chunk, embed).build()

events = await workflow.run(pdf_path)                   EmbedExecutor
outputs = events.get_outputs()
Full example: workflow_rag_ingest.py                       Output
```

## Slide 10

![Slide 10](slide_images/slide_10.png)

```
agent-framework

Visualize workflows with DevUI
Install the devui package:
agent-framework-devui

Point devui to the workflow:
from agent_framework.devui import serve
serve(entities=[workflow], auto_open=True)

Run the workflow and see the progress through each node:
```

## Slide 11

![Slide 11](slide_images/slide_11.png)

```
agent-framework

Workflows with Agent executors
Every Agent instance can also be used as an Executor in a workflow:




writer = Agent(client=client,
  name="Writer",
  instructions="You are a concise content writer.")
reviewer = Agent(client=client,
  name="Reviewer",
  instructions="Review content based on clarity, accuracy, and structure.")

workflow = WorkflowBuilder(start_executor=writer)
             .add_edge(writer, reviewer)
             .build()
Full example: workflow_agents.py
```

## Slide 12

![Slide 12](slide_images/slide_12.png)

```
agent-framework

Streaming events from workflows
Emit events from workflows by specifying stream=True:
async for event in workflow.run(prompt, stream=True):
  if event.type == "started":
    print(f"[started] for workflow {workflow.name}")
  elif event.type == "executor_invoked":
    print(f"[executor_invoked] from executor {event.executor_id}")
  elif event.type == "output" and isinstance(event.data, AgentResponseUpdate):
    print(event.data.text, end="", flush=True)
  elif event.type == "executor_completed":
    print(f"[executor_completed] from executor {event.executor_id}")
  elif event.type == "executor_failed":
    print(f"[executor_failed] from executor {event.executor_id}:   {event.data}")
  elif event.type == "error":
    print(f"[error] {event.data}")

Full example: workflow_agents_streaming.py
```

## Slide 13

![Slide 13](slide_images/slide_13.png)

```
agent-framework

Built-in workflow builder: SequentialBuilder
If you're building a linear conversation pipeline, you can use SequentialBuilder:

from agent_framework.orchestrations import SequentialBuilder

workflow = SequentialBuilder(participants=[writer, reviewer])
             .build()




The workflow assumes that participants accept and emit conversation-shaped data,
so executors must be Agents or custom Executors that process conversations.
The extra start/end nodes normalize input and output to list[Message].
Full example: workflow_agents_sequential.py
```

## Slide 14

![Slide 14](slide_images/slide_14.png)

```
Branching workflows
```

## Slide 15

![Slide 15](slide_images/slide_15.png)

```
agent-framework

Workflow with conditional branching
                                                Each edge in a graph
                                                can have a condition
                                                (function that
                                                returns True/False).
def needs_revision(message) -> bool:
  return message.agent_response.text.upper().startswith("REVISION NEEDED")
def is_approved(message) -> bool:
  return message.agent_response.text.upper().startswith("APPROVED")

workflow = (WorkflowBuilder(start_executor=writer)
  .add_edge(writer, reviewer)
  .add_edge(reviewer, publisher, condition=is_approved)
  .add_edge(reviewer, editor, condition=needs_revision)
  .build())

Full example: workflow_conditional.py
```

## Slide 16

![Slide 16](slide_images/slide_16.png)

```
Text output is fragile for workflow control
System prompt for the Reviewer agent:
Your response MUST begin with exactly one of these two tokens:
APPROVED — if the draft is clear, accurate, and well-structured.
REVISION NEEDED — if it requires improvement.

Condition functions that route based on Reviewer response:
def needs_revision(message) -> bool:
  return message.agent_response.text.upper().startswith("REVISION NEEDED")
def is_approved(message) -> bool:
  return message.agent_response.text.upper().startswith("APPROVED")

What can go wrong?                                                        Result:
Leading whitespace/newline/prefix   Review result: APPROVED                  No condition matched
Localization                        APROBADO                                 No condition matched
False positive approval             APPROVED, but major issues remain..      Routes to wrong path
Mixed output                        APPROVED....REVISION REQUIRED...         Unclear intent
```

## Slide 17

![Slide 17](slide_images/slide_17.png)

```
Unstructured text vs. structured output
 The default output for an       If an LLM supports structured outputs, you
 LLM is free text:               can force output to conform to schema:




 REVISION NEEDED                      {
                                       "decision": "REVISION NEEDED",
 Problems to fix                       "feedback": "Problems to fix: Rem
 - Remove em dashes. Replace e        ove em dashes. Replace each "—" wi
 ach "—" with a comma, semicol        th a comma, semicolon, or parenthe
 on, or parentheses.".                ses."
                                      }
```

## Slide 18

![Slide 18](slide_images/slide_18.png)

```
agent-framework

Using structured outputs for workflow decisions
Specify response_format for Agent and convert response to that model:
class ReviewDecision(BaseModel):
  decision: Literal["APPROVED", "REVISION_NEEDED"]
  feedback: str
  final_post: str | None = None

reviewer = Agent(client=client,
  name="Reviewer",
  instructions=("You are a strict content reviewer."
  "If draft is ready, set decision=APPROVED and include final post in final_post. "
  "If it needs changes, set decision=REVISION_NEEDED and provide feedback." ),
  response_format=ReviewDecision)

def is_approved(message: Any) -> bool:
  result = ReviewDecision.model_validate_json(message.agent_response.text)
  return result.decision == "APPROVED"

Full example: workflow_conditional_structured.py
```

## Slide 19

![Slide 19](slide_images/slide_19.png)

```
agent-framework

Category-based routing with structured outputs
                              category=="Question":




      how do I reset my
        password?

                              category=="Complaint":




 {                            Default:
   "category": "Question",
   "reasoning": "The input
 is asking a question."
 }
```

## Slide 20

![Slide 20](slide_images/slide_20.png)

```
agent-framework

Using switch-case edges in workflows
Add a switch-case edge group with an executor that categorizes output:
classifier = Agent(..., response_format=ClassifyResult)

@executor(id="extract_category")
async def extract_category(response, ctx):
  result = ClassifyResult.model_validate_json(response.agent_response.text)
  await ctx.send_message(result)

workflow = (WorkflowBuilder(start_executor=classifier)
  .add_edge(classifier, extract_category)
  .add_switch_case_edge_group(extract_category,
   [Case(condition=is_question, target=handle_question),
    Case(condition=is_complaint, target=handle_complaint),
    Default(target=handle_feedback)])
  .build())
Full example: workflow_switch_case.py
```

## Slide 21

![Slide 21](slide_images/slide_21.png)

```
State management
```

## Slide 22

![Slide 22](slide_images/slide_22.png)

```
When do we need workflow state?
Without state:                                        With state:



"These are 5 reasons why..."

                                                                                              state:
                                                                                              key         value

                                                                                              post_text   "These are 5
{                                                       {                                                 reasons why..."
 "decision": "APPROVED",                                    "decision": "APPROVED"
 "post_text": "These are 5.."                           }
}




Reviewer must carry content that it didn't produce,   Reviewer only decides. Draft is stored once and
just to pass it downstream.                           read by any step that needs it.
```

## Slide 23

![Slide 23](slide_images/slide_23.png)

```
agent-framework

Storing and accessing state in workflows
 @executor(id="store_post_text")
 async def store_post_text(response, ctx):                              store state
   ctx.set_state("post_text", response.agent_response.text.strip())
   await ctx.send_message(response)
 @executor(id="publisher")
 async def publisher(response, ctx):                                    access state
   content = str(ctx.get_state("post_text", "")).strip()
   await ctx.yield_output(f"    Published:\n\n{content}")

 workflow = (WorkflowBuilder(start_executor=writer, max_iterations=8)
    .add_edge(writer, store_post_text)
    .add_edge(store_post_text, reviewer)
    .add_edge(reviewer, publisher, condition=is_approved)
    .add_edge(reviewer, editor, condition=needs_revision)
    .add_edge(editor, store_post_text)
    .build())
Full example: workflow_conditional_state.py
```

## Slide 24

![Slide 24](slide_images/slide_24.png)

```
Shared workflow state leaks between requests
 Be careful about using a shared Workflow instance across multiple runs:
 workflow = WorkflowBuilder(start_executor=writer, ...).build()




                                             state:
                                             key         value

                                             post_text   "These are 5
                                                         reasons why..."




If two runs execute in parallel, they can run into a race condition!
```

## Slide 25

![Slide 25](slide_images/slide_25.png)

```
Shared agents accumulate conversation history
Be careful about using a module-level Agent instance shared across workflow runs:
writer = Agent(...)
workflow = WorkflowBuilder(start_executor=writer, ...).build()

   Run 1: "Write a post about AI jobs"
                                user: "Write a post about AI jobs"
                     history:
                                assistant: "AI agents are transforming..."

       Published: "AI agents are transforming..."

   Run 2: "Write a post about remote work"
                                                                                   R1
                                user: "Write a post about AI jobs"
                                                                                   R1
                                assistant: "AI agents are transforming..."
                                user: "Write a post about remote work"
                                assistant: "Remote jobs are at risk due to AI.."
       Published: "Remote jobs are at risk due to AI..."
```

## Slide 26

![Slide 26](slide_images/slide_26.png)

```
agent-framework

State isolation via factory functions
Use a factory function to create Agent instances and build the Workflow:
def create_workflow():
  writer = Agent(name="Writer", ...)
  reviewer = Agent(name="Reviewer", ...)
  editor = Agent(name="Editor", ...)

   return (WorkflowBuilder(start_executor=writer, max_iterations=8)
       .add_edge(writer, store_post_text)
       .add_edge(store_post_text, reviewer)
       .add_edge(reviewer, publisher, condition=is_approved)
       .add_edge(reviewer, editor, condition=needs_revision)
       .add_edge(editor, store_post_text)
       .build())
workflow = create_workflow(client)
events = await workflow.run(prompt)
Full example: workflow_conditional_state_isolated.py
```

## Slide 27

![Slide 27](slide_images/slide_27.png)

```
Using workflows in applications
```

## Slide 28

![Slide 28](slide_images/slide_28.png)

```
Retail shop with agentic workflows
```

## Slide 29

![Slide 29](slide_images/slide_29.png)

```
Sequential workflow: Restocking inventory
                            Inventory MCP


[Item A, Item B, Item D]



                     Prioritization


[Item B, Item D, Item A]




                     Summarization

"Based on my analysis..."
```

## Slide 30

![Slide 30](slide_images/slide_30.png)

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

## Slide 31

![Slide 31](slide_images/slide_31.png)

```
Appendix
```

## Slide 32

![Slide 32](slide_images/slide_32.png)

```
agent-framework

Building a workflow
                                                            Or use the built-in
                                                            workflow builder subclasses
                                                            for common scenarios:

                                                             ConcurrentBuilder()
                                                             SequentialBuilder()
                                                             GroupChatBuilder()
                                                             HandoffBuilder()
                                                             MagenticBuilder()

                                                            Join us tomorrow to learn more!


https://learn.microsoft.com/agent-framework/user-guide/workflows
```

## Slide 33

![Slide 33](slide_images/slide_33.png)

```
agent-framework

Visualize workflows with diagrams
from agent_framework import WorkflowViz                        viz.export(format="svg")

viz = WorkflowViz(workflow)


 print(viz.to_mermaid())

flowchart TD
  writer_agent["writer_agent (Start)"];
  final_editor_agent["final_editor_agent"];
  coordinator["coordinator"];
  internal_writer_agent --> writer_agent;
  internal_final_editor_agent --> final_editor_agent;
  internal_coordinator --> coordinator;
  writer_agent --> coordinator;
  coordinator --> writer_agent;
  final_editor_agent --> coordinator;
  coordinator --> final_editor_agent;


https://learn.microsoft.com/agent-framework/user-guide/workflows/visualization
```

## Slide 34

![Slide 34](slide_images/slide_34.png)

```
Sequential workflow: Restocking inventory
                            Inventory MCP


[Item A, Item B, Item D]



                     Prioritization


[Item B, Item D, Item A]




                     Summarization

"Based on my analysis..."
```
