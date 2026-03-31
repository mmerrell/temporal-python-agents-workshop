---
slug: section-2b-adding-tools-without-changing-the-loop
id: vnk44giwc6gx
type: challenge
title: 'Section 2b: Adding Tools Without Changing the Loop'
teaser: Add geolocation tools to the agent. The loop stays identical.
notes:
- type: text
  contents: |-
    ## Loose Coupling in Practice

    The agentic loop doesn't know which tools exist.
    It passes tool definitions to the LLM and dispatches whatever comes back.

    Adding a new tool means:
    1. Write a new activity
    2. Add it to the `TOOLS` list
    3. Add a dispatch branch in the workflow

    **The `while True` loop, the LLM call, the message accumulation — none of it changes.**
- type: text
  contents: |-
    ## What Was Added

    Two new activities in `activities.py`:
    - `get_coordinates(location)` — geocodes a place name to lat/lon
    - `get_distance_km(lat1, lon1, lat2, lon2)` — calculates straight-line distance

    Two new entries in `TOOLS`. Two new `elif` branches in the workflow dispatch.

    Compare the workflow from 2a to this one — the loop is identical.
tabs:
- id: 1mtph8oebw0t
  title: Terminal 1 - Worker
  type: terminal
  hostname: workshop-host
  workdir: /workspace/exercise
- id: vsdes7xykssm
  title: Terminal 2 - Starter
  type: terminal
  hostname: workshop-host
  workdir: /workspace/exercise
- id: 4jrxc5qfbyuw
  title: VS Code
  type: service
  hostname: workshop-host
  path: ?folder=/workspace/exercise
  port: 8443
- id: gh47bzz7ya3a
  title: Temporal UI
  type: service
  hostname: workshop-host
  path: /
  port: 8080
difficulty: basic
timelimit: 1800
enhanced_loading: null
---

## Section 2b: Adding Tools Without Changing the Loop

This challenge is a **code walk and demo**. The setup script loaded the complete
solution — all three tools are already wired up.

***

### What Changed Since 2a

Open `activities.py` in VS Code. Scroll to the bottom — `get_coordinates` and
`get_distance_km` are there after `get_weather_alerts`. Each is a plain
`@activity.defn` function. Neither knows about the other or the workflow.

Open `workflow.py`. Find the tool dispatch section — two new `elif` branches.
Now scroll back up to the `while True` loop. **Nothing changed.**

***

### Run a Multi-Tool Query

Start the worker in **Terminal 1**:

```bash
python run_worker.py
```

Run a query that requires chaining tools in **Terminal 2**:

```bash
python run_starter.py "How far is it from San Francisco to Los Angeles?"
```

Watch the **Temporal UI** — the LLM chains `get_coordinates` twice then
`get_distance_km`, in sequence, automatically. It figured out the plan
from the tool descriptions alone.

***

Click **Check** when you've run a multi-tool query and seen the chaining in the UI.
