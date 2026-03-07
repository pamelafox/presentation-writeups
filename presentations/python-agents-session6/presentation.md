# Python + Agents: Adding a human in the loop to your agent workflows

- **Date:** 2026-03-05
- **Video:** https://www.youtube.com/watch?v=7pGqASn-LEY
- **Slides:** PythonAgents-HITL-ForSharing.pdf

## Format

Use the format used in #python-agents-session4/outputs/writeup.md which is slightly different than the usual format.
The session description should be past tense and updated if there are any significant differences between the abstract and what was actually covered in the session.

## Notes

This is the abstract for the session:
In the final session of our Python + Agents series, we’ll explore how to incorporate human‑in‑the‑loop (HITL) interactions into agentic workflows using the Microsoft Agent Framework.

This session focuses on adding points where a workflow can pause, request input or approval from a user, and then resume once the human has responded. HITL is especially important because LLMs can produce uncertain or inconsistent outputs, and human checkpoints provide an added layer of accuracy and oversight.

We’ll begin with the framework’s requests‑and‑responses model, which provides a structured way for workflows to ask questions, collect human input, and continue execution with that data.

We'll move onto tool approval, one of the most frequent reasons an agent requests input from a human, and see how workflows can surface pending tool calls for approval or rejection.

Next, we’ll cover checkpoints and resuming, which allow workflows to pause and be restarted later. This is especially important for HITL scenarios where the human may not be available immediately.

We’ll walk through examples that demonstrate how checkpoints store progress, how resuming picks up the workflow state, and how this mechanism supports longer‑running or multi‑step review cycles.

This session brings together everything from the series—agents, workflows, branching, orchestration—and shows how to integrate humans thoughtfully into AI‑driven processes, especially when reliability and judgment matter most.