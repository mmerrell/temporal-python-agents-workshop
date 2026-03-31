---
slug: section-3b-making-the-sdk-agent-durable
id: w0pt4uiy0gki
type: challenge
title: 'Section 3b: Making the SDK Agent Durable'
teaser: Wrap the SDK agent in a Temporal workflow. Then look at the UI — it's identical
  to Section 2.
notes:
- type: text
  contents: |-
    ## The Integration Pattern

    `temporalio.contrib.openai_agents` provides the bridge between the SDK and Temporal.

    Activities become tools via `openai_agents.workflow.activity_as_tool()`.
    The SDK still manages the agentic loop.
    Temporal manages durability, retries, and observability.

    The agent definition is **identical** to the raw version.
    The only change is where it runs: inside a `@workflow.defn` class.
- type: text
  contents: |-
    ## The Big Reveal

    After you run the durable agent, open the Temporal UI.

    The event history looks exactly like Section 2 — the hand-rolled version.
    Same workflow structure. Same activity trace. Same observability.

    The SDK is doing the agentic loop.
    Temporal is doing the durability.
    You get both.
tabs:
- id: ib4igdysrliq
  title: Terminal 1 - Worker
  type: terminal
  hostname: workshop-host
  workdir: /workspace/exercise
- id: vw3obubzoxmo
  title: Terminal 2 - Starter
  type: terminal
  hostname: workshop-host
  workdir: /workspace/exercise
- id: b6h0rvgkfn2k
  title: VS Code
  type: service
  hostname: workshop-host
  path: ?folder=/workspace/exercise&openFile=/workspace/exercise/workflow.py
  port: 8443
- id: fjlkwhgxiqnu
  title: Temporal UI
  type: service
  hostname: workshop-host
  path: /
  port: 8080
difficulty: basic
timelimit: 1800
enhanced_loading: null
---

## Section 3b: Making the SDK Agent Durable

Open `workflow.py` in VS Code.

***

### Walk the Code

Compare this workflow to the one in Section 2. The structure is the same:
`@workflow.defn`, `@workflow.run`, a single `run()` method.

The difference is inside `run()`. Instead of a hand-rolled `while True` loop,
there's an `Agent` definition and `Runner.run()`. The tools are activities
wrapped with `openai_agents.workflow.activity_as_tool()`.

Open `activities.py` — identical to the raw SDK version, just `@activity.defn`
instead of `@function_tool`.

***

### Run It

Start the worker in **Terminal 1**:

```bash
python run_worker.py
```

Run a workflow in **Terminal 2**:

```bash
python run_starter.py "How far is it from Seattle to Portland?"
```

Now open the **Temporal UI** and find your workflow. Look at the event history.
Compare it to what you saw in Section 2.

***

### What You're Seeing

Every tool call the SDK made is a discrete activity in the event history.
Retries, timeouts, and observability come for free — the SDK didn't know
anything about Temporal. The integration handled the translation.

***

Click **Check** when you've run the durable agent and compared the UI to Section 2.
