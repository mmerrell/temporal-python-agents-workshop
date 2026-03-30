---
slug: exercise-sdk
id: ""
type: challenge
title: "Exercise: Make the SDK Agent Durable"
teaser: Wire up the Temporal workflow around the OpenAI Agents SDK. Four TODOs.
notes:
- type: text
  contents: |-
    ## Your Task

    `workflow.py` has four TODOs:

    1. Add `@workflow.defn` to the class
    2. Add `@workflow.run` to the method
    3. Define the `Agent` using `openai_agents.workflow.activity_as_tool()` for each activity
    4. Run the agent with `Runner.run()` and return `result.final_output`

    `activities.py` and the run scripts are complete — don't touch them.
- type: text
  contents: |-
    ## Hints

    **Wrapping an activity as a tool:**
    ```python
    openai_agents.workflow.activity_as_tool(
        get_weather_alerts,
        start_to_close_timeout=timedelta(seconds=10),
    )
    ```

    **Running the agent:**
    ```python
    result = await Runner.run(agent, query)
    return result.final_output
    ```

    The `OpenAIAgentsPlugin` is already configured in `run_worker.py` and
    `run_starter.py` — you don't need to touch those.
tabs:
- title: Terminal 1 - Worker
  type: terminal
  hostname: workshop-host
  workdir: /workspace/exercise
- title: Terminal 2 - Starter
  type: terminal
  hostname: workshop-host
  workdir: /workspace/exercise
- title: VS Code
  type: service
  hostname: workshop-host
  path: ?folder=/workspace/exercise&openFile=/workspace/exercise/workflow.py
  port: 8443
- title: Temporal UI
  type: service
  hostname: workshop-host
  path: /
  port: 8080
difficulty: basic
timelimit: 3600
---

## Exercise: Make the SDK Agent Durable

Open `workflow.py` in VS Code and work through the four TODOs.

***

### When You're Ready to Test

Start the worker in **Terminal 1**:

```bash
python run_worker.py
```

Run the agent in **Terminal 2**:

```bash
python run_starter.py "What are the weather alerts in Texas?"
```

Check the **Temporal UI** — you should see a completed `WeatherAgentWorkflow`
with activity calls in the event history.

***

### Stuck?

The complete solution is in `/workspace/exercises/03-agent-sdks/solution/workflow.py`.

***

Click **Check** when you have a completed workflow in the Temporal UI.
