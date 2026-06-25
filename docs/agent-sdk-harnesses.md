# Agent SDK Harnesses

Checked on 2026-06-25.

This page is a public reference for how the current Claude, OpenAI, and Google
agent SDK harnesses work. It is meant to be maintained as the packages evolve.
It separates documented behavior from source-inspection findings.

## Version Snapshot

| Vendor | Package | Latest version checked | How checked | Harness role |
|---|---|---:|---|---|
| Anthropic | `claude-agent-sdk` | `0.2.110` | PyPI | Python SDK for Claude Code as an agent harness |
| Anthropic | `@anthropic-ai/claude-agent-sdk` | `0.3.191` | npm | TypeScript SDK for Claude Code as an agent harness |
| OpenAI | `openai-agents` | `0.17.7` | PyPI | Python runner for agents, tools, handoffs, guardrails, sessions, and tracing |
| OpenAI | `@openai/agents` | `0.12.0` | npm | TypeScript runner for agents, tools, handoffs, sessions, and tracing |
| Google | `google-adk` | `2.3.0` | PyPI | Python Agent Development Kit |
| Google | `@google/adk` | `1.3.0` | npm | TypeScript Agent Development Kit |

Refresh versions with:

```bash
npm view @anthropic-ai/claude-agent-sdk version
npm view @openai/agents version
npm view @google/adk version
python3 -m pip index versions claude-agent-sdk
python3 -m pip index versions openai-agents
python3 -m pip index versions google-adk
```

Refresh this repo's live inventory with:

```bash
uvx --with claude-agent-sdk --with openai-agents --with google-adk \
  python scripts/sdk_surface_inventory.py \
  > evals/results/sdk_surface_inventory_$(date +%F).json
```

## Harness Boundary

An agent harness is the layer that owns the loop around a model:

1. Build the model request from instructions, memory, tool schemas, and prior
   messages.
2. Inspect the model response for final output, tool calls, handoffs, or
   interruptions.
3. Execute tools or route tool requests to another runtime.
4. Feed tool results back into the model.
5. Persist, stream, trace, limit, or resume the run.

The current SDK families put that boundary in different places.

| Surface | Loop owner | Tool execution boundary | State model |
|---|---|---|---|
| Claude Agent SDK | Claude Code agent process invoked by the SDK | Claude Code process handles built-in tools. SDK handles custom tools, MCP, hooks, and approvals | Claude Code session plus SDK session stores |
| Claude Managed Agents | Anthropic-hosted runtime or self-hosted worker | Managed environment executes tools and streams events | Server-side sessions, environments, and event stream |
| OpenAI Agents SDK | Native Python or TypeScript `Runner` | Host process runs function tools. OpenAI API runs hosted tools | Run history, sessions, Conversations API, previous response ids |
| Google ADK | ADK `Runner`, `App`, `SessionService`, and flow runtime | ADK tool layer, MCP, Google tools, app functions, workflow nodes | Event sessions, memory services, artifact services |

## Claude Agent SDK

### What It Is

Documented: Claude Agent SDK lets applications build agents with Claude Code as
a library. The SDK exposes Claude Code's tools, agent loop, and context
management in Python and TypeScript. The docs cover built-in tools, custom
tools, hooks, sessions, skills, subagents, MCP, permissions, streaming, and
structured output.

Source-inspection finding: the Python SDK launches the Claude Code executable
as a subprocess. It starts the process with stream JSON input and output, then
speaks a control protocol for permissions, hooks, SDK MCP messages, and result
streaming. The TypeScript npm package bundles platform-specific Claude Code
binaries through optional packages and exposes the same `query()` surface.

The design point is that Claude Agent SDK embeds the Claude Code harness. It is
not a thin Messages API wrapper.

### Loop

Documented loop:

```text
prompt plus context
-> Claude response
-> optional tool call
-> tool execution
-> tool result returned to Claude
-> repeat until final answer, turn limit, or budget limit
```

Tool-use round trips count as turns. Budget controls include `max_turns` or
`maxTurns` and `max_budget_usd` or `maxBudgetUsd`.

### Built-in Tools

Documented built-in tools include:

- File operations: `Read`, `Write`, `Edit`
- Search: `Glob`, `Grep`
- Execution: `Bash`
- Web: `WebSearch`, `WebFetch`
- Discovery: `ToolSearch`
- Orchestration: `Agent`, `Skill`, `AskUserQuestion`, `TaskCreate`, `TaskUpdate`

Read-only tools and read-only MCP tools can run at the same time. Tools that
change state run in sequence. Custom tools default to sequence unless they are
declared read-only.

### Permissions

`allowed_tools` means tools are auto-approved. It does not mean every other
tool is removed from the agent. Tools outside `allowed_tools` can still be
available but require permission unless they are blocked by `disallowed_tools`.

Documented permission modes include:

- `default`
- `acceptEdits`
- `plan`
- `dontAsk`
- `bypassPermissions`
- TypeScript-only `auto`

Use `disallowed_tools` for hard blocks. Use `allowed_tools` for auto-approval
policy.

### Context

The active context can include:

- System prompt
- `CLAUDE.md`
- Tool definitions
- Conversation history
- Tool calls and tool results
- Skill metadata and loaded skill instructions
- MCP tool metadata

Claude Code can compact context and emit a compaction boundary. Subagents get
fresh context and return a summary to the parent rather than copying their full
internal history back into the parent context.

### Extension Points

Claude Agent SDK can be extended with:

- Custom SDK tools
- MCP servers
- Hooks such as `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`,
  `SessionEnd`, and `UserPromptSubmit`
- Permission callbacks
- Subagents
- Skills
- Plugins
- Session stores
- Structured output schemas

### Source-Inspection Notes

The Python SDK source shows:

- It looks for a bundled Claude Code executable, then `claude` on `PATH`, then
  common install paths.
- It sets `CLAUDE_CODE_ENTRYPOINT=sdk-py`.
- It sets `CLAUDE_AGENT_SDK_VERSION`.
- It builds a `claude --output-format stream-json --verbose` command.
- It passes flags for tools, MCP config, permissions, hooks, sessions, sandbox,
  skills, plugins, structured output, and streaming.
- It sends input as `--input-format stream-json`.
- It routes control requests such as permission checks, hook callbacks, and SDK
  MCP calls through the SDK.

The TypeScript package source is minified in the npm tarball. The exposed types
and package behavior show the same main shape: `query()`, `startup()`, session
store helpers, bundled binary handling, hooks, MCP, skills, plugins, sandbox
options, and session mirroring.

### Claude Python Example

```python
import anyio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)


async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are a careful file assistant.",
        allowed_tools=["Read", "Write", "Edit"],
        max_turns=4,
        max_budget_usd=1.00,
    )

    async for message in query(
        prompt="Create notes.md with a 5-line summary of this repo.",
        options=options,
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)

        if isinstance(message, ResultMessage):
            print(f"total cost: {message.total_cost_usd}")


if __name__ == "__main__":
    anyio.run(main)
```

What this shows:

- The app does not implement the loop.
- The SDK invokes Claude Code's loop.
- `allowed_tools` auto-approves the listed tools.
- The result stream contains assistant content and a final result message.

### Claude TypeScript Example

```ts
import { query } from '@anthropic-ai/claude-agent-sdk'

for await (const message of query({
  prompt: 'Inspect this repo and list the top 3 files to read first.',
  options: {
    allowedTools: ['Read', 'Glob', 'Grep'],
    maxTurns: 4,
    systemPrompt: 'Answer with file paths and one-line reasons.'
  }
})) {
  if (message.type === 'assistant') {
    console.log(message)
  }
}
```

### Claude Permission Callback Pattern

Use a callback when policy depends on tool input.

```python
from claude_agent_sdk import ClaudeAgentOptions


async def can_use_tool(tool_name, tool_input, context):
    if tool_name == "Bash" and "rm " in str(tool_input):
        return {"behavior": "deny", "message": "File deletion is not allowed."}

    return {"behavior": "allow"}


options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep"],
    permission_prompt_tool=can_use_tool,
)
```

The exact callback return types vary by SDK version. Treat this as the pattern:
approve, deny, or edit tool input at the permission boundary.

## Claude Managed Agents

Managed Agents are Anthropic's hosted stateful harness. They are different from
Claude Agent SDK.

### What It Is

Documented: Managed Agents provide a prebuilt agent harness and managed
infrastructure. The app creates an agent, creates an environment, starts a
session, sends events, streams responses over SSE, and steers or interrupts the
running session.

Core objects:

- Agent: model, system prompt, tools, MCP, skills
- Environment: cloud sandbox or self-hosted runtime
- Session: running instance of an agent
- Events: user, agent, session, span, and system events

### Event Surface

Documented event examples include:

- User events: `user.message`, `user.interrupt`,
  `user.custom_tool_result`, `user.tool_confirmation`,
  `user.define_outcome`, `user.tool_result`
- Agent events: `agent.message`, `agent.thinking`, `agent.tool_use`,
  `agent.tool_result`, `agent.mcp_tool_use`, `agent.mcp_tool_result`,
  `agent.custom_tool_use`, `agent.thread_context_compacted`
- Session events: running, idle, rescheduled, terminated, deleted, updated,
  error, and thread events
- Span events: model request start and end, usage, outcome evaluation
- System events: `system.message` on supported models

### Managed Agents Example Shape

```python
from anthropic import Anthropic

client = Anthropic(
    default_headers={"anthropic-beta": "managed-agents-2026-04-01"}
)

# Pseudocode. Resource names and fields should be checked against the current
# beta SDK reference before use.
agent = client.beta.managed_agents.agents.create(
    name="repo-review-agent",
    model="claude-opus-4-8",
    system_prompt="Review source changes and return risks first.",
    tools=["bash", "file_editor", "web_search"],
)

environment = client.beta.managed_agents.environments.create(
    agent_id=agent.id,
    type="cloud",
)

session = client.beta.managed_agents.sessions.create(
    agent_id=agent.id,
    environment_id=environment.id,
)

stream = client.beta.managed_agents.sessions.events.stream(
    session_id=session.id,
    event={"type": "user.message", "content": "Review the current branch."},
)

for event in stream:
    print(event)
```

Use this shape for long-running server-side work. Use Claude Agent SDK when the
app should own the local runtime and process boundary.

### Managed Agents Caveats

Managed Agents are beta and require the `managed-agents-2026-04-01` beta
header. The docs say this surface is not currently eligible for zero data
retention or HIPAA BAA because stateful sessions store history, state, and
outputs server-side.

## OpenAI Agents SDK

### What It Is

The OpenAI Agents SDK is a native Python and TypeScript agent runner. It owns
the loop in the host language instead of launching a separate CLI process.

The core objects are:

- `Agent`
- `Runner` or `run()`
- Tools
- Handoffs
- Guardrails
- Sessions
- Tracing
- Model providers
- Sandbox Agents
- Realtime or voice agents

### Loop

Documented runner loop:

```text
call current agent model
-> if final output, return
-> if handoff, switch active agent and keep history
-> if tool calls, execute tools and append tool results
-> repeat
-> throw max-turns error when limit is reached
```

OpenAI's runner has an app-level design. The host process owns local function
tools, guardrails, handoffs, and tracing. Hosted tools run through OpenAI APIs.

### Tool Types

Common tool categories:

- Hosted tools from OpenAI APIs
- Function tools in the host process
- Custom tools
- MCP tools
- Agents as tools
- Computer, shell, local shell, and apply-patch style tools in supported SDK
  surfaces
- Sandbox capability tools for Sandbox Agents

### Handoffs vs Agents As Tools

Handoffs transfer the conversation to another agent. The new agent becomes the
active agent and receives the accumulated history according to the handoff
configuration.

Agents as tools do not transfer control. The parent agent calls another agent
like a function. The child agent receives generated input and returns final
output as the tool result.

This difference matters for support bots, coding agents, and analyst agents:
handoff is conversation routing. Agent-as-tool is task delegation.

### State Options

OpenAI exposes several state patterns:

- `result.history`: app-managed history
- `session`: SDK-managed persistent memory interface
- `conversationId`: OpenAI Conversations API state
- `previousResponseId`: continuation through the previous Responses API call
- Sandbox session or snapshot: filesystem and workspace state for Sandbox
  Agents

Pick one conversation history strategy per thread unless the app deliberately
reconciles multiple state layers.

### OpenAI Python Example

```python
import asyncio
from typing import Annotated

from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field


class Weather(BaseModel):
    city: str = Field(description="The city name")
    temperature_range: str = Field(description="The Celsius range")
    conditions: str = Field(description="The weather conditions")


@function_tool
def get_weather(city: Annotated[str, "The city to check"]) -> Weather:
    return Weather(
        city=city,
        temperature_range="14-20C",
        conditions="Sunny with wind.",
    )


agent = Agent(
    name="weather_agent",
    instructions="Answer weather questions by calling the tool.",
    tools=[get_weather],
)


async def main():
    result = await Runner.run(agent, "What is the weather in Tokyo?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
```

What this shows:

- The Python process runs `get_weather`.
- The runner feeds the tool result back into the model.
- The final answer is `result.final_output`.

### OpenAI TypeScript Example

```ts
import { Agent, run, tool } from '@openai/agents'
import { z } from 'zod'

const getWeather = tool({
  name: 'get_weather',
  description: 'Get the weather for a city.',
  parameters: z.object({ city: z.string() }),
  execute: async ({ city }) => {
    return {
      city,
      temperatureRange: '14-20C',
      conditions: 'Sunny with wind.'
    }
  }
})

const agent = new Agent({
  name: 'weather_agent',
  instructions: 'Answer weather questions by calling the tool.',
  tools: [getWeather]
})

const result = await run(agent, 'What is the weather in Tokyo?')
console.log(result.finalOutput)
```

### OpenAI Agent-As-Tool Example

```python
import asyncio

from agents import Agent, Runner


summarizer = Agent(
    name="summarizer",
    instructions="Summarize the input in 3 bullets.",
)

writer = Agent(
    name="writer",
    instructions="Write a short brief. Use the summarizer tool first.",
    tools=[
        summarizer.as_tool(
            tool_name="summarize_text",
            tool_description="Summarize source text before writing.",
        )
    ],
)


async def main():
    result = await Runner.run(
        writer,
        "Source: The SDK owns the loop, calls tools, and returns final output.",
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
```

The parent remains active. The summarizer only returns a tool result.

## Google ADK

### What It Is

Google ADK is the Agent Development Kit. It is Gemini-first but not only a
Gemini wrapper. The docs describe it as an open-source framework for building,
debugging, evaluating, and deploying agents. Current docs list Python,
TypeScript, Go, Java, and Kotlin.

ADK's harness is event and service oriented:

```text
App
-> Runner
-> SessionService
-> InvocationContext
-> Agent or Workflow node
-> Events
-> Tools, Memory, Artifacts, Plugins
```

### Loop

Source-inspection finding: Python ADK's `Runner` creates or loads a session,
builds an invocation context, runs the selected agent or workflow node, emits
events, and persists state. The LLM flow runs one model step, processes model
output, handles function calls, emits function response events, and continues
until the agent finishes, pauses, or transfers.

Simplified LLM flow:

```text
preprocess request
-> call model
-> emit model response event
-> detect function calls
-> execute tools or request input
-> emit tool result event
-> continue, pause, transfer, or finish
```

### Core Objects

- `LlmAgent`: model-backed agent
- `Runner`: execution engine
- `InMemoryRunner`: testing and local runner
- `SessionService`: session and event storage
- `MemoryService`: memory backends
- `ArtifactService`: file and artifact storage
- `Workflow`: graph node orchestration
- `NodeRunner`: workflow node execution
- `Event`: execution log and state transition unit
- `FunctionTool`: app function as tool
- `McpToolset`: MCP tools over stdio, SSE, or streamable HTTP

### Agent Modes

ADK exposes different agent modes:

- `chat`: root conversational agent mode
- `single_turn`: isolated task node or subagent, often used in workflows
- `task`: runs until completion with a `finish_task` tool and optional schemas

Task-mode agents are invoked as tools. Current ADK docs say task-mode
`LlmAgent` instances cannot be used as static workflow graph nodes.

### Workflows

ADK 2.0 adds graph workflows. A workflow is a DAG of nodes and edges. Nodes can
be functions, tools, `LlmAgent` instances, or nested workflows. The runner can
resume paused workflows by reading the session history and reconstructing
state.

This gives ADK a stronger built-in scheduling layer than the base OpenAI runner
or Claude Agent SDK.

### Google ADK Python Example

```python
from google.adk.agents import LlmAgent


root_agent = LlmAgent(
    name="research_agent",
    model="gemini-3.1-pro-preview-customtools",
    instruction="Answer with concise bullets and cite sources when available.",
    tools=[],
)
```

This is only the agent definition. ADK agents are normally run by the ADK
runner, CLI, dev UI, API server, or deployment target.

### Google ADK TypeScript Example

```ts
import { GOOGLE_SEARCH, LlmAgent } from '@google/adk'

export const rootAgent = new LlmAgent({
  model: 'gemini-3.1-pro-preview-customtools',
  name: 'search_agent',
  description: 'Searches Google and answers from the results.',
  instruction: 'Use search when the answer depends on current information.',
  tools: [GOOGLE_SEARCH]
})
```

### Google ADK Function Tool Example

```ts
import { FunctionTool, LlmAgent } from '@google/adk'
import { z } from 'zod'

async function getWeather({ city }: { city: string }) {
  return {
    status: 'success',
    report: `Weather for ${city}: 14-20C and windy.`
  }
}

const getWeatherTool = new FunctionTool({
  name: 'get_weather',
  description: 'Get the weather for a city.',
  parameters: z.object({
    city: z.string().describe('The city name')
  }),
  execute: getWeather
})

export const rootAgent = new LlmAgent({
  model: 'gemini-3.1-pro-preview-customtools',
  name: 'weather_agent',
  instruction: 'Answer weather questions with the weather tool.',
  tools: [getWeatherTool]
})
```

### Google ADK Task-Agent Example

```python
from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


class ResearchInput(BaseModel):
    topic: str = Field(description="The topic to research")
    depth: str = Field(default="brief", description="brief or detailed")


class ResearchOutput(BaseModel):
    summary: str = Field(description="Summary of findings")
    sources: list[str] = Field(description="Sources used")


researcher = LlmAgent(
    name="researcher",
    instruction="Research the topic and return structured output.",
    mode="task",
    input_schema=ResearchInput,
    output_schema=ResearchOutput,
    tools=[],
)

writer = LlmAgent(
    name="writer",
    instruction="Write a short memo. Use the researcher when facts are needed.",
    sub_agents=[researcher],
)
```

The parent calls the task agent as a tool. The task agent can run its own loop
and finish with structured output.

## Claude Developer Platform Surface

This section lists the Claude platform areas that matter when designing an
agent harness.

### Model Capabilities

Documented platform capabilities include:

- Context windows up to 1M tokens
- Extended thinking
- Adaptive thinking
- Batch processing
- Citations
- PDF support
- Search result content blocks
- Structured outputs
- Data residency
- Effort controls
- Server-side fallback beta
- Fallback credit beta

### Tools

Server-side tools:

- Web search
- Web fetch
- Code execution
- Advisor tool beta

Client-side tools:

- Bash
- Text editor
- Computer use
- Memory

### Tool Infrastructure

- Agent Skills beta
- Fine-grained tool streaming
- MCP connector beta
- Programmatic tool calling
- Tool search

### Context Management

- Automatic prompt caching
- Prompt caching with 5-minute and 1-hour durations
- Compaction beta
- Context editing beta
- Token counting

### Files, Assets, Admin

- Files API beta for PDFs, images, and text
- Admin API
- Usage and Cost API
- Compliance API

### Agent Skills

Skills package instructions, metadata, scripts, templates, and other resources.
The loading model is progressive:

1. Metadata is available first.
2. `SKILL.md` loads when the skill matches the task.
3. Referenced resources and scripts load only when needed.

The Claude API docs list beta headers for Skills use with code execution and
the Files API. Skills are not zero-data-retention eligible according to the
Skills docs.

## Main Differences

| Question | Claude Agent SDK | Claude Managed Agents | OpenAI Agents SDK | Google ADK |
|---|---|---|---|---|
| Who owns the loop? | Claude Code process | Anthropic hosted runtime | SDK runner in Python or TS | ADK Runner and LLM flow |
| Is it a subprocess harness? | Yes for local Claude Code SDK use | No, hosted or worker model | No | No |
| Best fit | Local coding agents and Claude Code-like automation | Long-running hosted agents | App workflows around OpenAI Responses | Graph workflows and Google Cloud oriented agents |
| Tool policy | Claude Code permissions and SDK callbacks | Managed environment policy | Host functions, hosted tools, approvals, guardrails | Toolsets, workflow nodes, services |
| Subagent model | Subagents via `Agent` tool | Multiagent thread events | Handoffs or agents as tools | Subagents, task agents, workflow nodes |
| State | Claude Code sessions and stores | Server-side sessions | History, sessions, conversation ids, previous response ids | Event sessions, memory, artifacts |
| Distinct edge | Claude Code harness as a library | Hosted stateful runtime | Clean handoff and guardrail model | Graph workflows and event services |

## What This Repo Should Test Next

This reference should drive live cases in `evals/live_harnesses/`:

| SDK | Next live cases |
|---|---|
| Claude Agent SDK | permissions, hooks, skills, subagents, session resume, checkpoints, cost and usage |
| OpenAI Agents SDK | handoffs, guardrails, sessions, MCP servers, tracing export, hosted tools, local shell tool |
| Google ADK | callbacks, tool error recovery, multi-agent transfer, evaluation, deployment and tracing |
| Claude Managed Agents | session events, tool confirmations, interruptions, environment lifecycle, self-hosted worker |

## Harness Patterns Worth Testing

- Event-sourced runs: every model output, tool call, tool result, interruption,
  and compaction boundary should be a durable event.
- Permission gates: put approval policy between model intent and tool
  execution.
- Read-only hints: let safe tools run at the same time.
- Tool schema lazy loading: expose names and descriptions first, then load
  detail when needed.
- Session stores: separate conversation state from process memory.
- Sandbox adapters: make local, Docker, cloud, and hosted workspaces swappable.
- Subagent isolation: child agents should not dump full private context back
  into the parent.
- Handoff semantics: distinguish task delegation from conversation transfer.
- Compaction boundaries: make context reduction explicit in the transcript.
- Tracing spans: record model calls, tool calls, costs, and errors.
- Workflow graphs: use DAG execution when work is scheduled, resumable, or
  parallel.

## Maintenance Procedure

When a package or docs surface changes:

1. Refresh the package versions with the npm and PyPI commands above.
2. Refresh the live SDK smoke in `docs/sdk-harness-coverage.md`.
3. Refresh `scripts/sdk_surface_inventory.py` output.
4. Update this page's version table and any changed feature claims.
5. Update `docs/source-map.md` with any new primary source.
6. Add or update a live case in `evals/live_harnesses/` for any new harness
   feature.
7. Run `python scripts/deslop_check.py`.

## Sources

Claude:

- [Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Claude Agent SDK agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop)
- [Claude Agent SDK docs index](https://code.claude.com/docs/llms.txt)
- [Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview)
- [Claude Managed Agents reference](https://platform.claude.com/docs/en/managed-agents/reference)
- [Claude platform overview](https://platform.claude.com/docs/en/build-with-claude/overview)
- [Claude tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Claude Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Claude Agent SDK Python source](https://github.com/anthropics/claude-agent-sdk-python)
- [Claude Agent SDK TypeScript source](https://github.com/anthropics/claude-agent-sdk-typescript)

OpenAI:

- [OpenAI Agents Python docs](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents JS docs](https://openai.github.io/openai-agents-js/)
- [OpenAI Agents Python source](https://github.com/openai/openai-agents-python)
- [OpenAI Agents JS source](https://github.com/openai/openai-agents-js)

Google:

- [Google ADK docs](https://adk.dev/)
- [Google ADK runtime](https://adk.dev/runtime/)
- [Google ADK event loop](https://adk.dev/runtime/event-loop/)
- [Google ADK Python source](https://github.com/google/adk-python)
- [Google ADK JS source](https://github.com/google/adk-js)
