---
slug: section-3a-the-openai-agents-sdk-raw
id: hsw2frzkkah1
type: challenge
title: 'Section 3a: The OpenAI Agents SDK - Raw'
teaser: Rebuild the weather agent with the OpenAI Agents SDK. Much less code, same
  capability.
notes:
- type: text
  contents: |-
    ## What Agent SDKs Give You

    When you built the agent from scratch, you wrote:
    - The `while True` loop
    - Tool call parsing
    - Message accumulation
    - Context management

    The OpenAI Agents SDK handles all of that for you.
    You define an agent with instructions and tools. You call `Runner.run()`. Done.
- type: text
  contents: |-
    ## The Tradeoff

    The raw SDK agent is clean and fast to write.

    But it runs in a single process. If that process dies mid-execution:
    - The agentic loop state is gone
    - Tool calls in progress are lost
    - There's no way to resume

    There's also no event history, no retry policy on tool calls,
    and no visibility into what the LLM was doing when it failed.

    **That changes in 3b.**
tabs:
- id: xj4cdptr3e74
  title: Terminal
  type: terminal
  hostname: workshop-host
  workdir: /workspace/exercise
- id: coc8quj6wmlj
  title: VS Code
  type: service
  hostname: workshop-host
  path: ?folder=/workspace/exercise&openFile=/workspace/exercise/agent_raw.py
  port: 8443
- id: jlocgjwtl7cd
  title: Temporal UI
  type: service
  hostname: workshop-host
  path: /
  port: 8080
difficulty: basic
timelimit: 1800
enhanced_loading: null
---

## Section 3a: The OpenAI Agents SDK — Raw

Open `agent_raw.py` in VS Code.

***

### Walk the Code

Notice what's gone compared to `workflow.py` from Section 2:
- No `while True` loop
- No message list management
- No tool call parsing
- No `@workflow.defn`, no `@activity.defn`

You define tools with `@function_tool`. The SDK extracts the name, docstring,
and parameter schema automatically. You define an agent with instructions and
a tool list. `Runner.run()` handles the rest.

***

### Run It

```bash
python agent_raw.py "What are the weather alerts in California?"
```

Try a multi-tool query:

```bash
python agent_raw.py "How far is it from Chicago to Detroit?"
```

It works — but notice: there's nothing in the **Temporal UI**. No event history,
no activity trace. If this process died mid-run, you'd have no idea what happened.

***

Click **Check** when you've run the raw agent successfully.
