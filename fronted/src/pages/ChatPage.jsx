import { useState, useEffect, useRef } from "react";
import { chatApi } from "../services/api";

function ThinkingBubble() {
  return (
    <div className="message assistant">
      <div className="thinking">
        <span /><span /><span />
      </div>
    </div>
  );
}

function Message({ msg }) {
  return (
    <div className={`message ${msg.role}`}>
      <div className="message-bubble">{msg.content}</div>
      {msg.sources?.length > 0 && (
        <div className="message-sources">
          Sources:&nbsp;
          {msg.sources.map((s) => (
            <span key={s.document_id} className="source-tag">{s.title}</span>
          ))}
        </div>
      )}
    </div>
  );
}

export default function ChatPage() {
  const [conversations, setConversations] = useState([]);
  const [activeConvId, setActiveConvId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    chatApi.listConversations().then((r) => setConversations(r.data)).catch(() => {});
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const loadConversation = async (id) => {
    setActiveConvId(id);
    try {
      const { data } = await chatApi.getConversation(id);
      setMessages(data.messages);
    } catch {
      setMessages([]);
    }
  };

  const startNewChat = () => {
    setActiveConvId(null);
    setMessages([]);
  };

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setLoading(true);
    try {
      const { data } = await chatApi.query({ message: text, conversation_id: activeConvId });
      setActiveConvId(data.conversation_id);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer, sources: data.sources },
      ]);
      setConversations((prev) => {
        const exists = prev.find((c) => c.id === data.conversation_id);
        if (!exists) {
          return [{ id: data.conversation_id, last_message: text, created_at: new Date() }, ...prev];
        }
        return prev;
      });
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error: " + (err.response?.data?.detail || "Failed to get response.") },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-page">
      <div className="chat-history-panel">
        <h3>Conversations</h3>
        <button className="new-chat-btn" onClick={startNewChat}>+ New Chat</button>
        {conversations.map((c) => (
          <button
            key={c.id}
            className={`conv-item ${activeConvId === c.id ? "active" : ""}`}
            onClick={() => loadConversation(c.id)}
          >
            {c.last_message || "Conversation"}
          </button>
        ))}
      </div>

      <div className="chat-main">
        <div className="chat-messages">
          {messages.length === 0 && !loading ? (
            <div className="chat-empty">
              <h2>Ask anything about your documents</h2>
              <p>Type a question below to get started</p>
            </div>
          ) : (
            <>
              {messages.map((m, i) => <Message key={i} msg={m} />)}
              {loading && <ThinkingBubble />}
            </>
          )}
          <div ref={bottomRef} />
        </div>
        <div className="chat-input-area">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question... (Enter to send, Shift+Enter for newline)"
            rows={1}
          />
          <button onClick={sendMessage} disabled={loading || !input.trim()}>Send</button>
        </div>
      </div>
    </div>
  );
}
