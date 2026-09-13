# Checkpoint Project — Local MCP Study Tools Server

[![M8ven Score](https://m8ven.ai/badge/mcp/elmachhoune/checkpoint-project-local-mcp-study-tools-server)](https://m8ven.ai/mcp/elmachhoune/checkpoint-project-local-mcp-study-tools-server)

A local **Model Context Protocol (MCP) server** built with **Python** and **FastMCP**, providing AI-powered study tools for explaining technical topics, creating personalized study plans, and generating revision checklists.

Built as a checkpoint project to explore **MCP server development, tool design, structured inputs/outputs, input validation, and AI-assisted learning workflows**.

---

## ✨ Features

The server exposes three study-focused MCP tools:

* 📚 **Explain Topic** — `explain_topic` — Generate a clear explanation of a technical or academic topic.
* 🗓️ **Create Study Plan** — `create_study_plan` — Generate a structured study plan based on a topic and a number of days (1–14).
* ✅ **Generate Revision Checklist** — `generate_revision_checklist` — Create a practical checklist for reviewing and preparing a topic.

Plus two read-only MCP **resources**:

* 📄 `project://course-outline` — Course curriculum with modules and topics (JSON).
* ℹ️ `project://status` — Server status, available tools and resources (JSON).

The server runs locally over **stdio** and can be connected to MCP-compatible AI clients.

---

## 🧰 Available Tools

### 1. `explain_topic`

Provides a structured explanation of a given topic.

**Parameters:**

| Name    | Type   | Required | Description            |
| ------- | ------ | -------- | ---------------------- |
| `topic` | string | Yes      | The topic to explain   |

**Typical input:**

```json
{
  "topic": "python"
}
```

**Example output:**

```json
{
  "topic": "python",
  "explanation": "Python is a high-level, interpreted programming language known for its readability and simplicity. It uses indentation to define code blocks and supports multiple programming paradigms.",
  "related_topics": ["machine learning", "mcp", "fastapi"]
}
```

---

### 2. `create_study_plan`

Creates a structured study plan for a specific subject over a number of days.

**Parameters:**

| Name    | Type | Required | Description                                           |
| ------- | ---- | -------- | ----------------------------------------------------- |
| `topic` | str  | Yes      | The topic for the study plan                          |
| `days`  | int  | Yes      | Number of study days (1–14, out-of-range is clamped)  |

**Typical input:**

```json
{
  "topic": "machine learning",
  "days": 5
}
```

**Example output structure:**

```json
{
  "topic": "machine learning",
  "days": 5,
  "study_plan": [
    { "day": 1, "focus": "Day 1: machine learning fundamentals", "estimated_hours": 2, "activities": ["Read machine learning documentation"] },
    { "day": 2, "focus": "Day 2: machine learning fundamentals", "estimated_hours": 2, "activities": ["Read machine learning documentation", "Complete machine learning exercises"] },
    { "day": 3, "focus": "Day 3: machine learning fundamentals", "estimated_hours": 2, "activities": ["Read machine learning documentation", "Complete machine learning exercises", "Build a small machine learning project"] },
    { "day": 4, "focus": "Day 4: machine learning practice & review", "estimated_hours": 3, "activities": ["Read machine learning documentation", "Complete machine learning exercises", "Build a small machine learning project"] },
    { "day": 5, "focus": "Day 5: machine learning practice & review", "estimated_hours": 3, "activities": ["Read machine learning documentation", "Complete machine learning exercises", "Build a small machine learning project"] }
  ]
}
```

> ⚠️ If `days` is outside the 1–14 range, the value is **clamped** and the response includes both a `DAYS_CLAMPED` error object and the adjusted plan.

---

### 3. `generate_revision_checklist`

Generates a checklist for reviewing a subject before an assessment, project, or exam.

**Parameters:**

| Name    | Type   | Required | Description                       |
| ------- | ------ | -------- | --------------------------------- |
| `topic` | string | Yes      | The topic for the revision checklist |

**Typical input:**

```json
{
  "topic": "fastapi"
}
```

**Example output:**

```json
{
  "topic": "fastapi",
  "checklist": [
    "Understand core concepts of fastapi",
    "Explain fastapi to someone else in simple terms",
    "Solve 3 practice problems related to fastapi",
    "Review common fastapi pitfalls and best practices",
    "Create a mind map of fastapi connections",
    "Complete a mini-project using fastapi",
    "Teach fastapi basics to a peer"
  ],
  "total_items": 7,
  "completion_status": {
    "Understand core concepts of fastapi": false
  }
}
```

---

## 🏗️ Architecture

The project follows a simple MCP server architecture over the **stdio** transport:

```text
┌──────────────────────────────┐
│       MCP Client             │
│                              │
│  Claude / Cursor / Other     │
│  MCP-compatible applications │
└──────────────┬───────────────┘
               │
               │ JSON-RPC 2.0 over stdio
               ▼
┌──────────────────────────────┐
│     Local MCP Server         │
│        (FastMCP)             │
│                              │
│  ┌────────────────────────┐  │
│  │ explain_topic          │  │
│  ├────────────────────────┤  │
│  │ create_study_plan      │  │
│  ├────────────────────────┤  │
│  │ generate_revision_     │  │
│  │ checklist              │  │
│  └────────────────────────┘  │
│                              │
│  Resources:                  │
│  ┌────────────────────────┐  │
│  │ project://course-outline│ │
│  ├────────────────────────┤  │
│  │ project://status       │  │
│  └────────────────────────┘  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Study Workflow         │
│                              │
│ Explanation → Planning       │
│ → Revision → Assessment      │
└──────────────────────────────┘
```

---

## 🛠️ Technology Stack

* **Python 3.11+**
* **Model Context Protocol (MCP)** — official Python SDK (`mcp` package)
* **FastMCP** — high-level MCP server framework
* **Pydantic** — input model definitions and validation
* **stdio transport** — JSON-RPC 2.0 over standard input/output

---

## 🚀 Getting Started

### Prerequisites

* **Python 3.11+**
* **pip**
* An MCP-compatible client

You can verify your Python installation with:

```bash
python --version
```

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/ELMACHHOUNE/Checkpoint-Project-Local-MCP-Study-Tools-Server.git
```

Navigate to the project:

```bash
cd Checkpoint-Project-Local-MCP-Study-Tools-Server/mcp-study-tools
```

Install dependencies:

```bash
pip install "mcp<2"
```

---

## ▶️ Running the Server

Run the server in standalone mode:

```bash
python server.py
```

Since the server communicates over **stdio**, it is designed to be launched by an MCP client rather than run interactively in a terminal. See [MCP Client Configuration](#-mcp-client-configuration) below.

### Test scripts

Once the server is running, you can exercise it with the included client test:

```bash
python client_test.py
```

Or with the agent-style demonstration:

```bash
python agent_demo.py
```

`client_test.py` connects to the server, lists tools and resources, reads both resources, calls all three tools, and verifies the error-handling and clamping behaviors.

`agent_demo.py` demonstrates a lightweight agent that parses natural-language requests (e.g. *"Explain what is Python"*, *"Create a study plan for machine learning for 10 days"*, *"Generate a revision checklist for FastAPI"*), validates the selected tool and its arguments, and executes it over MCP.

---

## 🔌 MCP Client Configuration

Add the server to an MCP-compatible client by spawning it like any stdio server. A typical configuration follows this structure:

```json
{
  "mcpServers": {
    "study-tools": {
      "command": "python",
      "args": [
        "C:\\path\\to\\mcp-study-tools\\server.py"
      ]
    }
  }
}
```

Replace the path with the actual location of `server.py` on your machine.

---

## 🔐 Security & Privacy

This project is designed as a **local MCP server**.

The study tools are focused on educational content and do not require access to:

* Passwords
* Authentication credentials
* Private keys
* Financial information
* Personal files
* Sensitive system information

The project does not intentionally implement credential collection or sensitive file access.

**Server-side protections (see `docs/mcp-checkpoint-report.md`):**

* ✅ **Empty-input protection** — every tool rejects empty `topic` values with a structured `EMPTY_TOPIC` error.
* ✅ **Range limiting** — `create_study_plan.days` is validated and clamped to 1–14.
* ✅ **Structured errors** — consistent `{error, code, details}` response format.
* ✅ **No arbitrary code execution** — tools return predefined/structured data only.
* ✅ **Read-only resources** — resources expose static data only.
* ✅ **Tool annotations** — every tool declares explicit `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` hints so hosts can inform users before invocation.

> ⚠️ **No authentication** — this is a local development/education server, not intended for production or network-exposed deployment.

---

## 📊 M8ven Verification

[![M8ven Score](https://m8ven.ai/badge/mcp/elmachhoune/checkpoint-project-local-mcp-study-tools-server)](https://m8ven.ai/mcp/elmachhoune/checkpoint-project-local-mcp-study-tools-server)

This project is listed and verified on the **M8ven Trust Index**.

Current reported status:

* **Code Verified** — no credential exfiltration, no sensitive file access, no obfuscation
* **No concerning findings**

Per the latest quality suggestions, the following were addressed:

* ✅ `README` describing the server and its tools
* ✅ `LICENSE` (MIT)
* ✅ Explicit tool annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) on all tools

[View the M8ven Trust Index listing](https://m8ven.ai/mcp/elmachhoune/checkpoint-project-local-mcp-study-tools-server)

> The M8ven score is an external assessment and may change as the project evolves. New projects cap at grade C until they build reputation through adoption.

---

## 📁 Project Structure

```text
Checkpoint-Project-Local-MCP-Study-Tools-Server/
│
├── LICENSE                        # MIT License
├── README.md                      # This file
│
└── mcp-study-tools/
    ├── server.py                  # FastMCP server: 3 tools + 2 resources
    ├── client_test.py             # MCP client test suite
    ├── agent_demo.py              # Agent-style natural-language demonstration
    └── docs/
        └── mcp-checkpoint-report.md  # Full architecture / security writeup
```

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. **Fork** the repository (or clone it directly).
2. Create a branch: `git checkout -b feature/your-feature`.
3. Make your changes.
4. Commit your changes: `git add . && git commit -m "feat: add new study tool"`.
5. Push your branch: `git push origin feature/your-feature`.
6. Open a **Pull Request** describing your changes and why they are useful.

---

## 📄 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Mohamed EL MACHHOUNE**

Software Engineer • AI Developer • Graphic Designer • Technical Instructor

* GitHub: https://github.com/ELMACHHOUNE
* Portfolio: https://elmachhoune.me
* LinkedIn: https://www.linkedin.com/in/mohamed-el-machhoune/

---

## 📚 Related Resources

* [Model Context Protocol](https://modelcontextprotocol.io/)
* [FastMCP — MCP SDK for Python](https://github.com/modelcontextprotocol/python-sdk)
* [M8ven Trust Index](https://m8ven.ai/)
* [M8ven MCP Listing](https://m8ven.ai/mcp/elmachhoune/checkpoint-project-local-mcp-study-tools-server)

---

## 📌 Project Status

**Status:** Active / Educational Project

This project was created as a practical exploration of MCP server development and AI-powered educational tooling. The implementation may evolve as MCP standards, SDKs, and AI client integrations continue to develop.