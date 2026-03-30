---
slug: foundations
id: 0u0lph8avfns
type: challenge
title: 'Section 1: Foundations of Agentic Systems'
teaser: What is an AI agent? Agency, decision-making, the OODA loop, and why durability
  matters.
notes:
- type: text
  contents: |-
    ## What Is an AI Agent?

    An **agent** is a system where the LLM is in control of the flow — it has *agency*.
    The LLM doesn't just answer a question; it decides what to do next, which tools to call,
    whether to loop, and when it's done.

    This is fundamentally different from a chatbot or a prompt-response system.
    The LLM drives the control flow.
- type: text
  contents: |-
    ## The Agentic Loop and the OODA Model

    Every agent runs a loop. A useful mental model is the **OODA loop**:

    - **Observe** — receive input, tool results, or context
    - **Orient** — the LLM reasons about what it knows
    - **Decide** — choose the next action: call a tool, respond, or ask for more info
    - **Act** — execute the decision, then loop back

    Tools are how the LLM reaches outside itself — querying APIs, reading data,
    triggering workflows. **System boundaries** define where your agent ends and
    the rest of your system begins. That boundary is a critical design decision.
- type: text
  contents: |-
    ## Why Durability Matters

    Most agent implementations are fragile in ways that only surface in production:

    - **Non-determinism** — the same input can produce different tool call sequences.
      How do you reproduce a failure?
    - **Long-running processes** — agents may run for minutes, hours, or days.
      What happens when your server restarts?
    - **Tool failures** — external APIs fail. How many retries? What backoff?
    - **Human interaction** — what if the agent needs to pause and wait for a human?
    - **Observability** — when something goes wrong, what was the LLM doing?

    **Temporal solves all of these.** An agentic loop is a workflow. LLM calls and
    tool calls are activities. State lives in the workflow. Durability, retries,
    and observability come for free.
tabs:
- id: uq0crdsuzp2x
  title: Terminal
  type: terminal
  hostname: workshop-host
- id: y5xw5f5tpouv
  title: Temporal UI
  type: service
  hostname: workshop-host
  path: /
  port: 8080
difficulty: basic
timelimit: 1800
enhanced_loading: null
---

## Section 1: Foundations of Agentic Systems

This is a **facilitated discussion** — your instructor will walk through the concepts in the notes above. Use the arrows to navigate between them.

***

### What makes something an agent?

The LLM has *agency* — it controls the flow. It decides what to do next, which tools to call, and when it's done. This is not a chatbot. It's not a pipeline. The LLM is the orchestrator.

***

### The agentic loop

Every agent runs some version of this:

1. Call the LLM with the current context
2. Parse the response — is it a final answer, or a tool call?
3. If a tool call: execute it, add the result to context, go to step 1
4. If a final answer: done

This loop is simple. Making it *reliable* is where Temporal comes in.

***

### Tools and system boundaries

Tools are how the LLM reaches outside itself — calling APIs, reading data, triggering workflows. Where your agent ends and the rest of your system begins is a design decision. Temporal helps you draw that boundary cleanly: the workflow owns the loop and the state; activities own the I/O.

***

### Why Temporal?

Consider what happens to a raw agentic loop when:
- Your worker restarts mid-loop
- A tool API returns a 503
- The agent needs to wait hours for a human response
- You need to debug why the agent took the wrong path two days ago

Temporal turns these hard problems into solved ones. You'll see exactly how in the next section.

***

### Discussion Questions

Your instructor will ask the room:

1. What's the longest-running process in your current agent implementation?
2. Where have you had failures that were hard to debug or reproduce?
3. What does "human-in-the-loop" mean for your use case?

***

Click **Check** when the discussion is complete and you're ready to move on.
