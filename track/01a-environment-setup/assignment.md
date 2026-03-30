---
slug: environment-setup
id: xvrlngdahtej
type: challenge
title: Environment Setup
teaser: Verify your sandbox and confirm Temporal is running before writing any agent
  code.
notes:
- type: text
  contents: |-
    ## Welcome to Building Durable AI Agents with Temporal

    This workshop will take you from first principles to a production-ready multi-agent system.

    **What's already running in this sandbox:**
    - Python 3.11 with the Temporal SDK and OpenAI Agents SDK installed
    - A Temporal dev server (running as a systemd service on this VM)
    - The Temporal Web UI — available in the **Temporal UI** tab above

    Click **Start** when you're ready.
tabs:
- id: tc6aeeuevhsd
  title: Terminal
  type: terminal
  hostname: workshop-host
- id: aizygwacbrti
  title: VS Code
  type: service
  hostname: workshop-host
  path: ?folder=/workspace/exercise
  port: 8443
- id: emsp5sl51fxi
  title: Temporal UI
  type: service
  hostname: workshop-host
  path: /
  port: 8080
difficulty: basic
timelimit: 600
enhanced_loading: null
---

## Verify Your Environment

### 1. Check Python and the SDKs

In the **Terminal** tab:

```bash
python --version
python -c "import temporalio; print('Temporal SDK:', temporalio.__version__)"
python -c "import agents; print('OpenAI Agents SDK: OK')"
```

You should see Python 3.11.x and both SDKs confirmed.

### 2. Verify the Temporal server

```bash
temporal operator cluster health
```

You should see `SERVING`.

### 3. Open the Temporal Web UI

Click the **Temporal UI** tab. You should see the Temporal Web UI showing the `default` namespace with no workflows yet. Keep this tab open throughout the workshop.

### 4. Check the exercise directories

```bash
ls /workspace/exercises/
```

You should see four directories:

```
01-scratch-agent/   02-sdk-agent/   03-hitl-agent/   04-multi-agent/
```

Each has a `practice/` (you write the code) and `solution/` (reference implementation).

***

Click **Check** when all four checks pass.
