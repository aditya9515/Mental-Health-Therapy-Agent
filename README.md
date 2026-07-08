# Mental Health Therapy Agent

A prototype backend for a mental-health support assistant built with FastAPI,
LangGraph, LangChain, Ollama, Chroma, and Twilio. The agent routes each user
message through triage, safety screening, emotion classification, retrieval of
therapy techniques, and a therapist-style response generator.

> Safety note: this project is not a licensed mental-health provider and should
> not be used as the only source of support in a crisis. If someone may harm
> themselves or others, contact local emergency services or a trusted crisis
> hotline immediately. The Twilio escalation path in this repository is prototype
> code and should be reviewed, tested, and legally/clinically approved before
> any real-world use.

## What It Does

- Accepts user messages through a FastAPI backend.
- Uses a first-layer LLM classifier to separate normal conversation from
  messages that need mental-health support.
- Runs a safety classifier for crisis or self-harm risk.
- Can trigger an emergency contact flow through Twilio for high-risk messages.
- Classifies user emotions from the latest message and conversation history.
- Retrieves relevant therapy techniques from a local Chroma vector database.
- Generates empathetic, therapist-style responses with local Ollama models.

## Tech Stack

- Python 3.12
- FastAPI and Uvicorn
- LangGraph and LangChain
- Ollama chat and embedding models
- ChromaDB for local retrieval
- Pydantic for request validation
- Twilio for optional emergency-call escalation

## Agent Flow

```text
User message
  -> first_layer_agent
  -> safety_check
  -> safety_defy
  -> emotion_classification_agent
  -> Chroma retriever
  -> therapist
  -> responce_to_user
```

The main graph is defined in `backend/agent_graph.py`. Shared graph state is
defined in `backend/state.py`.

## Project Structure

```text
backend/
  backendapi.py                         FastAPI app with / and /run-agent
  agent_graph.py                        LangGraph workflow definition
  state.py                              Shared TypedDict state
  fisrt_layer/agent.py                  First-layer routing classifier
  safety_check/safety.py                Mental-health safety classifier
  emotion_classification/
    emotion_classification.py           Emotion classification node
  final_model/ai_agent.py               Therapist response generation
  tools/
    rag.py                              Chroma retriever setup
    emergency_call.py                   Twilio emergency-call hook
db/
  chroma_db/                            Local Chroma persistence directory
pyproject.toml                          Python project dependencies
uv.lock                                 Locked dependency graph for uv
requirements.txt                        Minimal legacy requirements file
```

Note: the directory name `fisrt_layer` and the state key `responce` are kept as
they currently exist in the source code.

## Prerequisites

Install and run Ollama, then pull the models used by the agent:

```powershell
ollama pull qwen2.5:3b
ollama pull qwen2.5:7b-instruct
ollama pull qwen3:8b
ollama pull nomic-embed-text
```

The Chroma retriever expects the local database at:

```text
db/chroma_db
```

## Setup

Using `uv`:

```powershell
uv sync
```

Or using a standard virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Create `backend/.env` for Twilio and local configuration:

```env
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
EMERGENCY_CONTACT_NUMBER=
DB_LOCATION=db/chroma_db
```

Do not commit real credentials or phone numbers.

## Run The API

Start the FastAPI server from the repository root:

```powershell
uvicorn backend.backendapi:app --reload --host 127.0.0.1 --port 8000
```

Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
```

Example agent request:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/run-agent `
  -ContentType "application/json" `
  -Body '{"query":"I have been feeling anxious lately.","emotions":[]}'
```

## Development Notes

- `backend.backendapi:app` is the API entry point that matches the current file
  layout.
- `backend/main.py` appears to reference an older module path and may need to be
  updated before it can be used as an entry point.
- `backend/final_model/ai_agent.py` currently prompts for terminal input inside
  `responce_to_user`. For a pure HTTP API, that node should return a final
  response instead of calling `input()`.
- The emergency-call function has the Twilio call creation commented out. Review
  and test that path carefully before enabling real calls.
- The project currently does not include an automated test suite.

## Verification

Run a basic syntax check:

```powershell
python -m compileall backend
```

Recommended manual checks:

1. Confirm Ollama is running.
2. Confirm all required models are pulled.
3. Start the FastAPI server.
4. Open `/docs`.
5. Call `/run-agent` with a low-risk message.
6. Test crisis-routing behavior only in a safe development environment with
   Twilio calls disabled or pointed at a verified test number.

## Current Limitations

- The project is a prototype and should not be used as a production clinical
  system.
- Safety, escalation, and therapeutic responses depend on local LLM behavior and
  must be evaluated before any real deployment.
- The Chroma database is expected to already exist locally; this repository does
  not currently include a database-building script.
- API conversation persistence is represented in state but is not backed by a
  durable user/session store yet.
