---
slug: environment-setup
id: ""
type: challenge
title: Environment Setup
teaser: Verify your sandbox and confirm Temporal is running before writing any agent code.
notes:
- type: text
  contents: |-
    ## Welcome to Building Durable AI Agents with Temporal

    This workshop will take you from first principles to a production-ready multi-agent system.

    **What's already running in this sandbox:**
    - A Temporal dev server (running as a systemd service on this VM)
    - The Temporal Web UI — available in the **Temporal UI** tab above

    Click **Start** when you're ready.
tabs:
- title: Terminal
  type: terminal
  hostname: workshop-host
- title: Temporal UI
  type: service
  hostname: workshop-host
  path: /
  port: 8080
difficulty: basic
timelimit: 600
---

## Verify Your Environment

### 1. Check the Temporal server

In the **Terminal** tab:

```bash
temporal operator cluster health
```

You should see `SERVING`.

### 2. Open the Temporal Web UI

Click the **Temporal UI** tab. You should see the Temporal Web UI showing the `default` namespace.

***

Click **Check** when both pass.
