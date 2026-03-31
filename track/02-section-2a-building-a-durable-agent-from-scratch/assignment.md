---
slug: section-2a-building-a-durable-agent-from-scratch
id: ozeo1k8wjr2z
type: challenge
title: 'Section 2a: Building a Durable Agent from Scratch'
teaser: Implement the agentic loop inside a Temporal workflow. LLM calls and tool
  calls are activities.
notes:
- type: text
  contents: |-
    ## Structure of a Durable Agent

    ```
    WeatherAgentWorkflow   (the loop, the state, the decisions)
      └── call_llm          activity — LLM call, retries intentionally disabled
      └── get_weather_alerts activity — tool call, retried automatically on failure
    ```

    **The workflow is the brain. Activities are the hands.**

    Everything that can fail or be slow goes in an activity.
    The workflow orchestrates — it never does I/O directly.
- type: text
  contents: |-
    ## Why Put LLM Calls in Activities?

    Two reasons:

    **1. Non-determinism.** Temporal workflows must be deterministic — given the same
    event history, they must produce the same decisions. An LLM call is non-deterministic
    by nature. Putting it in an activity keeps the workflow deterministic.

    **2. Retries.** LLM API calls can fail transiently. Activity retry policies let
    you configure exactly how to handle that — independently of your workflow logic.

    Note: for LLM calls, you usually want `maximum_attempts=1`. Retrying a failed LLM
    call blindly gives you a different response. Handle LLM errors in your own logic.
- type: text
  contents: |-
    ## Loose Coupling

    Activities don't know they're part of an agent. They're just functions that do
    one thing. This matters when you add new tools:

    1. Write a new activity
    2. Add it to the tool definitions list
    3. Add a dispatch branch in the workflow

    The agentic loop itself — the `while True`, the LLM call, the message accumulation
    — **does not change**. You'll see this directly in the next challenge.
tabs:
- id: xc6cqfzezlar
  title: Terminal 1 - Worker
  type: terminal
  hostname: workshop-host
  workdir: /workspace/exercise
- id: yavbh8jrbh6t
  title: Terminal 2 - Starter
  type: terminal
  hostname: workshop-host
  workdir: /workspace/exercise
- id: budww5krwtsc
  title: VS Code
  type: service
  hostname: workshop-host
  path: ?folder=/workspace/exercise&openFile=/workspace/exercise/workflow.py
  port: 8443
- id: lelwxqpvfhpu
  title: Temporal UI
  type: service
  hostname: workshop-host
  path: /
  port: 8080
difficulty: basic
timelimit: 2400
enhanced_loading: null
---

## Section 2a: Building a Durable Agent from Scratch

The code for this section is in `/workspace/exercise/`. Open **VS Code** to explore it.

***

### Walk the Code

Open `workflow.py`. Notice:

1. **`@workflow.defn`** — this class is a Temporal workflow
2. **The agentic loop** — `while True:` with a break when there are no tool calls
3. **`workflow.execute_activity(call_llm, ...)`** — the LLM call happens in an activity
4. **`RetryPolicy(maximum_attempts=1)`** — LLM calls are not retried automatically
5. **`workflow.execute_activity(get_weather_alerts, ...)`** — each tool call is also an activity

Open `activities.py`. Notice:

1. **`@activity.defn`** decorates every activity
2. `call_llm` just calls the OpenAI API — no workflow logic here
3. `get_weather_alerts` calls the NWS API — a real external call
4. Neither activity knows about the loop — **loose coupling**

***

### Run It

Start the worker in **Terminal 1**:

```bash
python run_worker.py
```

Start a workflow in **Terminal 2**:

```bash
python run_starter.py "What are the active weather alerts in California?"
```

Switch to the **Temporal UI** tab and find your workflow. Click into it and look at the
**Event History** — every activity call is a discrete, durable event. If the worker
restarted right now, Temporal would replay this history and pick up exactly where it
left off without re-executing completed activities.

***

### Try Breaking It

While a workflow is running, kill the worker with **Ctrl+C** in Terminal 1. Watch the
workflow in the Temporal UI — it shows as running but blocked. Restart the worker:

```bash
python run_worker.py
```

Watch the workflow resume automatically from where it stopped.

***

Click **Check** when you've successfully run the agent and explored the event history.
