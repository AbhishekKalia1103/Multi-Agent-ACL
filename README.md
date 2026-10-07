# Multi-Agent Wedding Planner

A multi-agent wedding planner built with [LangChain](https://python.langchain.com/) agents, OpenAI and [Tavily](https://tavily.com/) web search. A main **planner agent** reads the couple's requirements and hands research off to two specialist **subagents**. Each subagent searches the live web and reports back, and the planner combines their findings into one wedding plan.

It runs either as a command-line app ([main.py](main.py)) or as a Streamlit web UI ([app.py](app.py)).

## How it works

```
                    ┌──────────────────────────────┐
  requirements ───▶ │   Main Wedding Planner Agent │ ───▶ final wedding plan
                    └──────────────┬───────────────┘
                 delegate_to_      │       delegate_to_
                 subagent1         │       subagent2
              ┌────────────────────┴────────────────────┐
              ▼                                         ▼
   ┌─────────────────────┐                  ┌─────────────────────┐
   │      SubAgent1      │                  │      SubAgent2      │
   │  venues & catering  │                  │ photographers, decor│
   │                     │                  │   attire & music    │
   └──────────┬──────────┘                  └──────────┬──────────┘
              └──────────── search_web (Tavily) ───────┘
```

1. **Main planner agent.** Its system prompt includes the user's requirements and tells it to gather information through its two delegation tools before writing the plan.
2. **SubAgent1, venues and catering.** Finds venues and caterers that fit the location, budget, guest count and date.
3. **SubAgent2, vendors.** Finds photographers, decorators, attire and music, with prices.
4. **`search_web` tool.** Both subagents use it. It wraps the Tavily search API.

Each subagent works in its own conversation and returns only a short summary with sources. This keeps the planner's context small.

## Project structure

| File | Purpose |
| --- | --- |
| [model.py](model.py) | Sets up the chat model (`gpt-5-mini`) |
| [tools.py](tools.py) | `search_web` tool backed by the Tavily API |
| [agents.py](agents.py) | The two subagents and the `delegate_to_subagent1/2` tools the planner calls |
| [prompt.py](prompt.py) | System prompt for the main planner agent |
| [main.py](main.py) | Terminal app: asks for requirements and prints the plan |
| [app.py](app.py) | Streamlit UI: requirements form, live run status, saved plans and downloads |

## Requirements

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- An [OpenAI API key](https://platform.openai.com/api-keys)
- A [Tavily API key](https://app.tavily.com/) (the free tier is enough to try it out)

## Setup

```bash
git clone https://github.com/AbhishekKalia1103/Multi-Agent-ACL.git
cd Multi-Agent-ACL
uv sync
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-key
```

`.env` is git-ignored, so your keys are never committed. In the Streamlit UI you can also enter the keys in the sidebar or set them in Streamlit secrets.

## Usage

### Web UI

```bash
uv run streamlit run app.py
```

Fill in the wedding brief: location, date, guest count, budget, style, priorities, must-haves and constraints. Then click generate. The status panel shows the agents running, and the finished plan is saved in the session, where you can download it.

### Terminal

```bash
uv run python main.py
```

Enter your requirements on one line, for example:

```
Wedding in Jaipur, India on 15 February 2027, 250 guests, total budget 40 lakh INR. Want a heritage palace venue with Rajasthani vegetarian catering. Also need a candid photographer, marigold decor, a designer lehenga and sherwani, and a live folk music band.
```

The logs show the delegation as it happens:

```
INFO | Delegating query to SubAgent1: wedding venues in Jaipur ...
INFO | Searching the web for topic: ...
INFO | Delegating query to SubAgent2: wedding photographers decorators Jaipur ...
```

Give specific details (city, date, guest count, budget). The planner builds its subagent queries from them, so specific input gives more relevant research.

## Configuration

- **Model:** change the model name in [model.py](model.py). Smaller models such as `gpt-5-nano` are cheaper but sometimes skip the delegation tools and answer from their own knowledge. `gpt-5-mini` uses the tools more reliably.
- **Subagent roles:** edit the `system_prompt` and docstring of each subagent and delegate tool in [agents.py](agents.py). The planner chooses a subagent based on the tool docstrings, so keep them specific.
- **Planner behavior:** edit `WEDDING_PLANNER_AGENT_PROMPT` in [prompt.py](prompt.py).

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `command not found: python` on macOS | Use `uv run python ...`, or activate the venv with `source .venv/bin/activate` |
| `No module named 'langchain.messages'` | You're on LangChain 0.3 or Python 3.9. Use Python 3.12 and run `uv sync` |
| Subagents never get called | Use a larger model, and make sure your requirements include concrete details |
| UI says the planner could not complete the run | Open "Technical details". This is usually a missing or invalid API key, or a used-up quota |
