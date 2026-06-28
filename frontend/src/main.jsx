import React, { useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Activity,
  Bot,
  BrainCircuit,
  Code2,
  Cpu,
  FlaskConical,
  Layers3,
  Menu,
  MessageSquarePlus,
  Network,
  PanelRightOpen,
  Rocket,
  Search,
  Send,
  Sparkles,
  TerminalSquare,
  X,
} from "lucide-react";
import { fetchAgents, fetchHealth, sendMessage } from "./api";
import "./styles.css";

const samplePrompts = [
  "AI roadmap",
  "Review RAG prompt",
  "Debug code",
];

const samplePromptMap = {
  "AI roadmap": "Make a roadmap for my AI engineering portfolio project",
  "Review RAG prompt": "Review this prompt for a RAG chatbot",
  "Debug code": "Debug this Python function and explain the error",
};

const iconMap = {
  router: Network,
  ai_engineer: BrainCircuit,
  research: Search,
  code: Code2,
  product: Rocket,
  prompt_eval: FlaskConical,
  synthesizer: Sparkles,
};

function App() {
  const [agents, setAgents] = useState([]);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      type: "system",
      content:
        "Ask anything. I route it to the right AI agent.",
    },
  ]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [activeResult, setActiveResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [isMobileSidebarVisible, setIsMobileSidebarVisible] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    fetchAgents()
      .then((data) => setAgents(data.agents))
      .catch((err) => setError(err.message));
    fetchHealth()
      .then(() => {})
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const visibleAgents = useMemo(
    () => agents.filter((agent) => agent.key !== "synthesizer"),
    [agents],
  );

  async function handleSubmit(event) {
    event?.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;
    await runPrompt(trimmed);
  }

  async function runPrompt(prompt) {
    setError("");
    setInput("");
    setIsLoading(true);
    setMessages((current) => [...current, { role: "user", content: prompt }]);

    try {
      const result = await sendMessage(prompt, sessionId);
      setSessionId(result.session_id);
      setActiveResult(result);
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: result.answer,
          result,
        },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  function resetConversation() {
    setSessionId(null);
    setActiveResult(null);
    setError("");
    setMessages([
      {
        role: "assistant",
        type: "system",
        content:
          "Conversation reset. Send a task and I will dispatch the agent team.",
      },
    ]);
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${isMobileSidebarVisible ? "open" : ""}`}>
        <div className="sidebar-brand-row">
          <div className="brand">
            <div className="brand-mark">
              <Bot size={22} />
            </div>
            <div>
              <strong>Agent Studio</strong>
              <span>AI agents</span>
            </div>
          </div>
          <button className="sidebar-close" onClick={() => setIsMobileSidebarVisible(false)}>
            <X size={20} />
          </button>
        </div>

        <button className="new-chat" onClick={resetConversation}>
          <MessageSquarePlus size={18} />
          New chat
        </button>

        <section className="side-section">
          <div className="section-label">Agent Swarm</div>
          <div className="agent-list">
            {visibleAgents.map((agent) => {
              const AgentIcon = iconMap[agent.key] || Cpu;
              const isActive = activeResult?.routing?.agent_key === agent.key;
              return (
                <div className={`agent-card ${isActive ? "active" : ""}`} key={agent.key}>
                  <div className="agent-card-icon-container">
                    <AgentIcon size={16} />
                  </div>
                  <div className="agent-card-details">
                    <strong>{agent.name.replace(" Agent", "")}</strong>
                    <span>{agent.role}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        <section className="side-section">
          <div className="section-label">Status</div>
          <div className="status-grid">
            <div>
              <strong>{agents.length || "-"}</strong>
              <span>agents</span>
            </div>
            <div>
              <strong>{messages.filter((m) => m.role === "user").length}</strong>
              <span>tasks</span>
            </div>
          </div>
        </section>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div className="topbar-left">
            <button className="menu-toggle" onClick={() => setIsMobileSidebarVisible(true)}>
              <Menu size={22} />
            </button>
            <div>
              <p className="eyebrow">Multi-agent AI</p>
              <h1>Agent Studio</h1>
            </div>
          </div>
          <div className="top-actions">
            <span className="status-dot" />
            Online
          </div>
        </header>

        <section className="command-strip">
          <div className="hero-copy">
            <h2>Ask. Route. Answer.</h2>
            <p>Agents for AI engineering, code, prompts, and product thinking.</p>
          </div>
          <div className="insight-panel">
            <div className="insight-header">
              <Activity size={16} />
              Routing Engine
            </div>
            {activeResult ? (
              <div className="insight-data">
                <div className="insight-main">
                  <strong>{activeResult.routing.agent_name}</strong>
                  <div className="confidence-meter-container">
                    <div className="confidence-meter-bar" style={{ width: `${activeResult.routing.confidence * 100}%` }}></div>
                    <span className="confidence-text">{Math.round(activeResult.routing.confidence * 100)}% Match</span>
                  </div>
                </div>
                {activeResult.routing.reason && (
                  <p className="insight-reason">{activeResult.routing.reason}</p>
                )}
                {activeResult.routing.matched_signals && activeResult.routing.matched_signals.length > 0 && (
                  <div className="insight-signals">
                    {activeResult.routing.matched_signals.map((sig, i) => (
                      <span key={i} className="signal-pill">{sig}</span>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="insight-data empty">
                <strong>Awaiting Request...</strong>
                <span>System operational</span>
              </div>
            )}
          </div>
        </section>

        <section className="content-grid">
          <div className="chat-panel">
            <div className="panel-title">
              <TerminalSquare size={18} />
              Chat
            </div>

            <div className="samples">
              {samplePrompts.map((label) => (
                <button key={label} onClick={() => runPrompt(samplePromptMap[label])} disabled={isLoading}>
                  {label}
                </button>
              ))}
            </div>

            <div className="messages">
              {messages.map((message, index) => (
                <MessageBubble key={`${message.role}-${index}`} message={message} />
              ))}
              {isLoading && (
                <div className="message assistant">
                  <div className="avatar"><Bot size={18} /></div>
                  <div className="bubble loading">Routing...</div>
                </div>
              )}
              <div ref={scrollRef} />
            </div>

            {error && <div className="error-banner">{error}</div>}

            <form className="composer" onSubmit={handleSubmit}>
              <input
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="Ask your agents..."
              />
              <button type="submit" disabled={isLoading || !input.trim()}>
                <Send size={18} />
              </button>
            </form>
          </div>

          <aside className="trace-panel">
            <div className="panel-title">
              <PanelRightOpen size={18} />
              Trace
            </div>
            {activeResult ? (
              <div className="trace-list">
                {activeResult.trace.map((item, index) => {
                  const TraceIcon = iconMap[item.agent_key] || Layers3;
                  return (
                    <div className="trace-step" key={`${item.agent_key}-${index}`}>
                      <div className="trace-index">{index + 1}</div>
                      <div className="trace-body">
                        <div className="trace-name">
                          <TraceIcon size={16} />
                          <strong>{item.agent_name}</strong>
                        </div>
                        <span>{item.role}</span>
                        <p>{shortTrace(item)}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="empty-trace">
                <Layers3 size={28} />
                <strong>No trace yet</strong>
                <span>Send a message.</span>
              </div>
            )}
          </aside>
        </section>
      </main>
      {isMobileSidebarVisible && (
        <div className="sidebar-backdrop" onClick={() => setIsMobileSidebarVisible(false)} />
      )}
    </div>
  );
}

function shortTrace(item) {
  if (item.agent_key === "router") {
    const selected = item.bullets?.find((bullet) => bullet.startsWith("Selected:"));
    return selected ? selected.replace("Selected: ", "Picked ") : item.content;
  }
  if (item.agent_key === "synthesizer") {
    return "Final answer prepared.";
  }
  return item.content;
}

function renderInlineContent(text) {
  if (!text) return "";
  const regex = /(\*\*.*?\*\*|`.*?`)/g;
  const tokens = text.split(regex);
  return tokens.map((token, index) => {
    if (token.startsWith("**") && token.endsWith("**")) {
      return <strong key={index}>{token.slice(2, -2)}</strong>;
    }
    if (token.startsWith("`") && token.endsWith("`")) {
      return <code key={index} className="inline-code">{token.slice(1, -1)}</code>;
    }
    return token;
  });
}

function CodeBlock({ language, code }) {
  const [copied, setCopied] = useState(false);

  function handleCopy() {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="code-block-container">
      <div className="code-block-header">
        <span className="code-block-lang">{language || "code"}</span>
        <button onClick={handleCopy} className="code-copy-btn">
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre className="code-block-pre">
        <code>{code}</code>
      </pre>
    </div>
  );
}

function MessageBubble({ message }) {
  const isUser = message.role === "user";
  const blocks = formatMessage(message.content);
  return (
    <div className={`message ${isUser ? "user" : "assistant"}`}>
      <div className="avatar">{isUser ? "You" : <Bot size={18} />}</div>
      <div className="bubble">
        {message.result && (
          <div className="route-pill">
            <span className="route-dot"></span>
            Routed to <strong>{message.result.routing.agent_name}</strong>
          </div>
        )}
        <div className="bubble-content">
          {blocks.map((block, index) => {
            if (block.type === "code") {
              return <CodeBlock key={index} language={block.language} code={block.text} />;
            }
            if (block.type === "heading") {
              const HeadingTag = `h${Math.min(block.level || 3, 6)}`;
              return <HeadingTag key={index}>{renderInlineContent(block.text)}</HeadingTag>;
            }
            if (block.type === "item") {
              return <li key={index}>{renderInlineContent(block.text)}</li>;
            }
            return <p key={index}>{renderInlineContent(block.text)}</p>;
          })}
        </div>
      </div>
    </div>
  );
}

function formatMessage(content) {
  if (!content) return [];
  const blocks = [];
  const lines = content.split("\n");
  let inCodeBlock = false;
  let codeContent = [];
  let codeLanguage = "";

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (line.trim().startsWith("```")) {
      if (inCodeBlock) {
        blocks.push({
          type: "code",
          language: codeLanguage || "text",
          text: codeContent.join("\n"),
        });
        codeContent = [];
        codeLanguage = "";
        inCodeBlock = false;
      } else {
        inCodeBlock = true;
        codeLanguage = line.trim().slice(3).trim();
      }
      continue;
    }

    if (inCodeBlock) {
      codeContent.push(line);
      continue;
    }

    const trimmed = line.trim();
    if (!trimmed && line === "") continue; // keep empty paragraphs out, but let spaces pass

    if (trimmed.startsWith("#")) {
      const level = (trimmed.match(/^#+/) || ["#"])[0].length;
      const text = trimmed.replace(/^#+\s+/, "");
      blocks.push({ type: "heading", level, text });
      continue;
    }

    if (/^[-*+]\s+/.test(trimmed)) {
      const text = trimmed.replace(/^[-*+]\s+/, "");
      blocks.push({ type: "item", text });
      continue;
    }

    if (/^\d+\.\s+/.test(trimmed)) {
      const text = trimmed.replace(/^\d+\.\s+/, "");
      blocks.push({ type: "item", text });
      continue;
    }

    blocks.push({ type: "paragraph", text: line }); // preserve full line styling
  }

  if (inCodeBlock && codeContent.length > 0) {
    blocks.push({
      type: "code",
      language: codeLanguage || "text",
      text: codeContent.join("\n"),
    });
  }

  return blocks;
}

createRoot(document.getElementById("root")).render(<App />);
