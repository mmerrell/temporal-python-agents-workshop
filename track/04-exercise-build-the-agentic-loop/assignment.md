---
slug: exercise-build-the-agentic-loop
id: ytq0mywlhapb
type: challenge
title: 'Exercise: Build the Agentic Loop'
teaser: Wire up the workflow so the agentic loop runs durably. Four TODOs to complete.
notes:
- type: text
  contents: |-
    ## Your Task

    `workflow.py` has four TODOs. Complete them in order:

    1. Add `@workflow.defn` to the class
    2. Add `@workflow.run` to the method
    3. Call `call_llm` as an activity (replace `response = None`)
    4. Call each tool activity in the dispatch section (replace each `result = None`)

    The activities in `activities.py` are fully implemented — don't touch them.
    The run scripts are ready to go.
- type: text
  contents: |-
    ## Hints

    **TODO 3 — calling call_llm:**
    ```python
    response = await workflow.execute_activity(
        call_llm,
        args=[messages, TOOLS],
        start_to_close_timeout=timedelta(seconds=30),
        retry_policy=RetryPolicy(maximum_attempts=1),
    )
    ```

    **TODO 4 — calling a tool activity:**
    ```python
    result = await workflow.execute_activity(
        get_weather_alerts,
        args=[tool_args["state"]],
        start_to_close_timeout=timedelta(seconds=10),
    )
    ```

    For `get_coordinates`, pass `tool_args["location"]`.
    For `get_distance_km`, pass four floats: lat1, lon1, lat2, lon2 — and wrap the result in `json.dumps()`.
tabs:
- id: 9orzlyto2dfd
  title: Terminal 1 - Worker
  type: terminal
  hostname: workshop-host
  workdir: /workspace/exercise
- id: tdulj4xh0jhr
  title: Terminal 2 - Starter
  type: terminal
  hostname: workshop-host
  workdir: /workspace/exercise
- id: ss7vndgsbamf
  title: VS Code
  type: service
  hostname: workshop-host
  path: ?folder=/workspace/exercise&openFile=/workspace/exercise/workflow.py
  port: 8443
- id: papnl2k1lzjv
  title: Temporal UI
  type: service
  hostname: workshop-host
  path: /
  port: 8080
difficulty: basic
timelimit: 3600
enhanced_loading: null
---

## Exercise: Build the Agentic Loop

Open `workflow.py` in VS Code and work through the four TODOs.

***

### When You're Ready to Test

Start the worker in **Terminal 1**:

```bash
python run_worker.py
```

Run the agent in **Terminal 2**:

```bash
python run_starter.py "What are the weather alerts in California?"
```

If it works, try a multi-tool query:

```bash
python run_starter.py "How far is it from New York to Boston?"
```

Check the **Temporal UI** — you should see your workflow completed with activity
calls visible in the event history.

***

### Stuck?

The complete solution is in `/workspace/exercises/02-building-from-scratch/solution/workflow.py`.

***

Click **Check** when you have a completed workflow in the Temporal UI.
