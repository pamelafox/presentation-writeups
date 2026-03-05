# Python + Agents: Orchestrating advanced multi-agent workflows

- **Date:** 2026-03-04
- **Video:** https://www.youtube.com/watch?v=WtZbDrd-RJg
- **Slides:** PythonAgents-AdvancedWorkflows.pdf

## Format

Use the format used in #python-agents-session4/outputs/writeup.md which is slightly different than the usual format.
The session description should be past tense and updated if there are any significant differences between the abstract and what was actually covered in the session.

## Notes

This is the abstract for the session:

In Session 5 of our Python + Agents series, we’ll go beyond workflow fundamentals and explore how to orchestrate advanced, multi‑agent workflows using the Microsoft Agent Framework.

This session focuses on patterns that coordinate multiple steps or multiple agents at once, enabling more powerful and flexible AI‑driven systems. We’ll begin by comparing sequential vs. concurrent execution, then dive into techniques for running workflow steps in parallel.

You’ll learn how fan‑out and fan‑in edges enable multiple branches to run at the same time, how to aggregate their results, and how concurrency allows workflows to scale across tasks efficiently.

From there, we’ll introduce two multi‑agent orchestration approaches that are built into the framework. We’ll start with handoff, where control moves entirely from one agent to another based on workflow logic, which is useful for routing tasks to the right agent as the workflow progresses.

We’ll then look at Magentic, a planning‑oriented supervisor that generates a high‑level plan for completing a task and delegates portions of that plan to other agents.

Finally, we'll wrap up with a demo of an E2E application that showcases a concurrent multi-agent workflow in action.

