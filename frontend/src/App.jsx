import React, { useEffect, useRef, useState } from "react";

// Use environment variable for API URL, fallback to local development
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";
const API_URL = `${API_BASE_URL}/api/chat`;
const LS_KEY = "chatgpt_like_chats_v1";

function nowTs() {
  return Date.now();
}

function makeEmptyChat() {
  return {
    id: `chat_${nowTs()}`,
    title: "New chat",
    messages: [{ id: `b-${nowTs()}`, role: "bot", text: "Hello — ask me anything.", ts: nowTs() }],
    updatedAt: nowTs(),
  };
}

export default function App() {
  const [chats, setChats] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const endRef = useRef(null);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(LS_KEY);
      const parsed = raw ? JSON.parse(raw) : null;
      if (parsed && Array.isArray(parsed) && parsed.length) {
        setChats(parsed);
        setActiveId(parsed[0].id);
      } else {
        const first = makeEmptyChat();
        setChats([first]);
        setActiveId(first.id);
      }
    } catch {
      const first = makeEmptyChat();
      setChats([first]);
      setActiveId(first.id);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(LS_KEY, JSON.stringify(chats));
  }, [chats]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [activeId, chats, loading]);

  const activeChat = chats.find((c) => c.id === activeId) || null;

  const updateChat = (id, patchFn) =>
    setChats((prev) => prev.map((c) => (c.id === id ? { ...c, ...patchFn(c) } : c)));

  const createNewChat = () => {
    const chat = makeEmptyChat();
    setChats((prev) => [chat, ...prev]);
    setActiveId(chat.id);
  };

  const deleteChat = (id) => {
    setChats((prev) => {
      const next = prev.filter((c) => c.id !== id);
      if (next.length === 0) {
        const n = makeEmptyChat();
        setActiveId(n.id);
        return [n];
      }
      if (id === activeId) setActiveId(next[0].id);
      return next;
    });
  };

  const renameChat = (id, title) => {
    updateChat(id, () => ({ title, updatedAt: nowTs() }));
  };

  const sendToBackend = async (userText) => {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userText }),
    });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt || "Network error");
    }
    const payload = await res.json();
    return (payload && (payload.reply || payload.message || payload.text)) || JSON.stringify(payload);
  };

  const handleSend = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading || !activeChat) return;

    const userMsg = { id: `u-${nowTs()}`, role: "user", text: trimmed, ts: nowTs() };
    const waitingId = `wait-${nowTs()}`;
    const waitingMsg = { id: waitingId, role: "bot", text: "…", ts: nowTs() };

    updateChat(activeChat.id, (c) => ({
      messages: [...c.messages, userMsg, waitingMsg],
      title: c.title === "New chat" ? trimmed.slice(0, 40) : c.title,
      updatedAt: nowTs(),
    }));
    setInput("");
    setLoading(true);

    try {
      const botText = await sendToBackend(trimmed);
      updateChat(activeChat.id, (c) => ({
        messages: c.messages.map((m) => (m.id === waitingId ? { ...m, text: botText, ts: nowTs() } : m)),
        updatedAt: nowTs(),
      }));
    } catch (err) {
      updateChat(activeChat.id, (c) => ({
        messages: c.messages.map((m) =>
          m.id === waitingId ? { ...m, text: "Error: failed to get response from server." } : m
        ),
        updatedAt: nowTs(),
      }));
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formattedTime = (ts) => new Date(ts).toLocaleTimeString();

  return (
    <>
      {/* 🌊 Top Global Header */}
      <div className="global-header">FloatChat</div>

      <div className="app-shell">
        <aside className="sidebar">
          <div className="sidebar-header">
            <button className="new-chat-btn" onClick={createNewChat}>
              + New chat
            </button>
          </div>

          <div className="chat-list">
            {chats.map((c) => {
              const last = c.messages[c.messages.length - 1];
              return (
                <div
                  key={c.id}
                  className={`chat-item ${c.id === activeId ? "active" : ""}`}
                  onClick={() => setActiveId(c.id)}
                >
                  <div className="chat-item-main">
                    <div className="chat-title">{c.title || "Untitled"}</div>
                    <div className="chat-snippet">
                      {last ? (last.role === "user" ? "You: " : "") + last.text.slice(0, 60) : ""}
                    </div>
                  </div>
                  <div className="chat-meta">
                    <div className="chat-time">{formattedTime(c.updatedAt)}</div>
                    <button
                      className="del-btn"
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteChat(c.id);
                      }}
                    >
                      ✕
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="sidebar-footer">
            <small>Local chats — stored in browser</small>
          </div>
        </aside>

        <main className="main-area">
          <header className="main-header">
            <input
              className="title-input"
              value={(activeChat && activeChat.title) || ""}
              onChange={(e) => activeChat && renameChat(activeChat.id, e.target.value)}
            />
            <div className="header-right">{activeChat ? formattedTime(activeChat.updatedAt) : ""}</div>
          </header>

          <section className="chat-window">
            {/* ✨ Intro Text Before First Message */}
            {activeChat && activeChat.messages.length === 1 && (
              <div className="intro-text">
                <h2>Welcome to FloatChat 🌊</h2>
                <p>An AI-powered conversational interface for exploring ARGO Ocean Data.</p>
                <p className="hint">Type your query below to begin.</p>
              </div>
            )}

            {activeChat &&
              activeChat.messages.map((m) => (
                <div key={m.id} className={`message-row ${m.role === "user" ? "user" : "bot"}`}>
                  <div className="bubble">
                    <div className="text">{m.text}</div>
                    <div className="meta">{new Date(m.ts).toLocaleTimeString()}</div>
                  </div>
                </div>
              ))}
            <div ref={endRef} />
          </section>

          <footer className="composer">
            <textarea
              className="input"
              placeholder="Type a message. Enter to send, Shift+Enter for newline"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={onKeyDown}
              rows={1}
              disabled={loading}
            />
            <button className="send-btn" onClick={handleSend} disabled={loading || !input.trim()}>
              {loading ? "Sending..." : "Send"}
            </button>
          </footer>
        </main>
      </div>
    </>
  );
}
