# 🌌 Multi-Agent AI Engineering Studio

> A high-fidelity, full-stack collaborative environment demonstrating intelligent swarm orchestration and real-time routing for complex software engineering workflows.

---

## 🚀 The Mission

**Multi-Agent AI Engineering Studio** solves the bottleneck of single-LLM chats by dispatching a highly specialized swarm of AI agents. Each request is mathematically evaluated, routed to a dedicated domain expert, and polished by a synthesizer into a singular, clean, and structured deliverable.

Developed with a cutting-edge **Navy Blue & Amber Glassmorphic UI**, this project displays live telemetry data, confidence metrics, and raw multi-agent execution traces behind the scenes.

```
       [ 💬 User Request ]
                │
                ▼
      [ 🧭 Routing Engine ] ──(Categorizes & Scores)
                │
         ┌──────┼──────┬──────┐
         ▼      ▼      ▼      ▼
        [🧠]   [🔍]   [💻]   [🚀] ... (Specialist Swarm)
         │      │      │      │
         └──────┼──────┴──────┘
                ▼
      [ ✍️ Synthesizer Agent ] ──(Refines & Polishes)
                │
                ▼
       [ 💎 Premium Feed ]
```

---

## 🛠️ The Agent Swarm

The studio orchestrates **7 specialized AI specialists**, each with a dedicated role in the engineering lifecycle:

| Agent | Avatar | Role | Description |
| :--- | :---: | :--- | :--- |
| **Router** | 🧭 | Traffic Controller | Analyzes incoming queries, detects signals, and dispatches the most capable agent with a confidence rating. |
| **AI Engineer** | 🧠 | Architect & Mentor | Handles high-level system architecture, technology selections, and AI learning pathways. |
| **Research** | 🔍 | Ground Truth Explorer | Dissects factual questions, identifies assumptions, and flags when external lookups are required. |
| **Code Expert** | 💻 | Syntax & Optimization | Reviews code snippets, provides debugging instructions, and advises on engineering trade-offs. |
| **Product Strategist** | 🚀 | Roadmap Builder | Turns raw product ideas into prioritized feature backlogs, roadmaps, and business plans. |
| **Prompt & Eval** | 🧪 | LLM Quality Assurance | Optimizes context window limits, designs prompts, and builds RAG metric tests. |
| **Synthesizer** | ✍️ | Response Editor | Collates specialist outputs, cleans markdown, and publishes the final polished layout. |

---

## ✨ Premium Features

- **⚡ Live Routing Telemetry**: A real-time HUD showcasing route match confidence progress, reasoning details, and glowing matched keyword tags.
- **🕵️ Swarm Execution Traces**: An interactive vertical timeline connecting each agent's internal reasoning logs.
- **🎨 Glassmorphic Interface**: Sleek radial gradient backdrops, interactive hover states, glowing pulses, and custom styled scrollbars.
- **💻 Terminal Code Frames**: Preformatted code rendering with language tags and an interactive **Copy to Clipboard** utility.
- **🛡️ Resilient Failbacks**: Fully functional out-of-the-box using local rules if no API key is present—meaning zero crashes during live demos.

---

## ⚙️ Running Locally

### 1. Backend Setup (FastAPI)

Ensure you have Python 3.10+ installed.

```bash
# Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment keys
cp .env.example .env
```

To configure Gemini's model, add your key inside `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

```bash
# Run server
uvicorn backend.main:app --reload --port 8000
```

---

### 2. Frontend Setup (React 19 + Vite)

In a separate terminal tab:

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧪 Testing

Verify the routing engine logic and API integrity using pytest:

```bash
# Run tests inside the virtual environment
PYTHONPATH=. ./.venv/bin/pytest tests -v
```

---

## 📦 Technology Stack

- **Frontend**: React 19, Vite, Lucide Icons, Custom CSS3 Grid/Flexbox
- **Backend**: FastAPI, Pydantic, Uvicorn, Python Dotenv
- **AI Engine**: Google Gemini API SDK / Local fallback rules
