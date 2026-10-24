import React, { useState, useRef, useEffect } from "react";
import { interpretChat } from "../controllers/chatController";
import type { BlinkAnimation } from "../models/chatModel";
import "../styles/chat.css";

interface Message {
  id: string;
  role: "user" | "bot";
  text: string;
}

interface Props {
  onBlink: (animation: BlinkAnimation) => void;
}

export function ChatCentral({ onBlink }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || loading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      text,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setError(null);

    try {
      const result = await interpretChat(text);
      if (result.intent === "blink") {
        onBlink({
          frames: result.response.frames,
          count: result.response.count,
        });
      }

      const botMessage: Message = {
        id: `bot-${Date.now()}`,
        role: "bot",
        text: result.response.content,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <span className="chat-title">WORSHIP Chat</span>
      </div>
      <div className="chat-messages" aria-live="polite" aria-relevant="additions">
        {messages.length === 0 && (
          <div className="chat-static-message">
            <h2 className="chat-static-title">
              Parpadea <span className="chat-static-highlight">2 veces</span>.
            </h2>
            <p className="chat-static-subtitle">Pide que parpadee y no serás el mismo.</p>
            <p className="chat-static-subtitle">Próximamente podré verte y entender tu entorno.</p>
          </div>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`chat-bubble ${msg.role === "user" ? "user" : "bot"}`}
            role="article"
            aria-label={msg.role === "user" ? "Tu mensaje" : "Respuesta del robot"}
          >
            {msg.text}
          </div>
        ))}
        {loading && (
          <div className="chat-bubble bot" aria-label="El robot está escribiendo">
            <span className="chat-typing">...</span>
          </div>
        )}
        {error && <div className="chat-error" role="alert">{error}</div>}
        <div ref={messagesEndRef} />
      </div>
      <p className="chat-vision-message" aria-hidden="true">
        Próximamente podré verte y entender tu entorno.
      </p>
      <div className="chat-input-area">
        <textarea
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Escribe un mensaje..."
          rows={1}
          disabled={loading}
          aria-label="Escribe tu mensaje para WORSHIP"
        />
        <button
          className="chat-send"
          onClick={handleSend}
          disabled={loading || !input.trim()}
          aria-label="Enviar mensaje"
        >
          Enviar
        </button>
      </div>
    </div>
  );
}