import React, { useState, useRef, useEffect } from "react";
import { interpretChat } from "../controllers/chatController";
import type { BlinkAnimation } from "../models/chatModel";
import {
  annotateFaceImage,
  validateFaceImageFile,
} from "../services/faceService";
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
  const [photoUrl, setPhotoUrl] = useState<string | null>(null);
  const [annotatedPhotoUrl, setAnnotatedPhotoUrl] = useState<string | null>(
    null,
  );
  const [photoLoading, setPhotoLoading] = useState(false);
  const [photoError, setPhotoError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const galleryInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    return () => {
      if (photoUrl) URL.revokeObjectURL(photoUrl);
    };
  }, [photoUrl]);

  useEffect(() => {
    return () => {
      if (annotatedPhotoUrl) URL.revokeObjectURL(annotatedPhotoUrl);
    };
  }, [annotatedPhotoUrl]);

  const handlePhotoChange = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;

    setPhotoError(null);
    try {
      validateFaceImageFile(file);
    } catch (caught) {
      setPhotoError(
        caught instanceof Error
          ? caught.message
          : "No se pudo validar la imagen.",
      );
      return;
    }

    setPhotoUrl(URL.createObjectURL(file));
    setAnnotatedPhotoUrl(null);
    setPhotoLoading(true);

    try {
      const annotatedImage = await annotateFaceImage(file);
      setAnnotatedPhotoUrl(URL.createObjectURL(annotatedImage));
      setMessages((prev) => [
        ...prev,
        {
          id: `bot-photo-${Date.now()}`,
          role: "bot",
          text: "El conjuro está completo. La marca de WORSHIP ha aparecido en tu retrato.",
        },
      ]);
    } catch (caught) {
      setPhotoError(
        caught instanceof Error
          ? caught.message
          : "No se pudo procesar la imagen.",
      );
    } finally {
      setPhotoLoading(false);
    }
  };

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

  const previewUrl =
    annotatedPhotoUrl ?? photoUrl ?? "/referencia.png";

  return (
    <div className="chat-container">
      <div className="chat-header">
        <span className="chat-title">WORSHIP Chat</span>
      </div>
      <aside className="photo-actions" aria-label="Añadir una foto">
        <button
          className="photo-action"
          type="button"
          disabled={photoLoading}
          aria-busy={photoLoading}
          onClick={() => galleryInputRef.current?.click()}
        >
          <span className="photo-action-icon" aria-hidden="true">
            <svg viewBox="0 0 32 32">
              <rect x="5" y="7" width="18" height="17" rx="2" />
              <path d="m7 21 5-5 4 4 2-2 4 4M22 12h5v14H10v-2" />
              <circle cx="17.5" cy="12" r="1.5" />
            </svg>
          </span>
          <span>{photoLoading ? "Procesando..." : "Subir foto"}</span>
        </button>
        <input
          ref={galleryInputRef}
          className="photo-file-input"
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={handlePhotoChange}
          aria-label="Subir una foto"
        />
        <p className="photo-privacy-note">
          Ofrece tu retrato al grimorio y la sombra revelará su antiguo sello.
        </p>
      </aside>
      <div
        className="chat-messages"
        aria-live="polite"
        aria-relevant="additions"
        aria-busy={photoLoading}
      >
        {photoUrl && (
          <div
            className="chat-photo-display"
            aria-label={
              annotatedPhotoUrl
                ? "Foto procesada por WORSHIP"
                : "Foto seleccionada para procesar"
            }
          >
            <img
              className={annotatedPhotoUrl ? "annotated" : "original"}
              src={annotatedPhotoUrl ?? photoUrl}
              alt={
                annotatedPhotoUrl
                  ? "Tu foto procesada con la marca WORSHIP"
                  : "Tu foto seleccionada para procesar"
              }
            />
          </div>
        )}
        {photoLoading && (
          <p className="photo-processing" role="status">
            Enviando y procesando tu foto...
          </p>
        )}
        {messages.length === 0 && !photoUrl && (
          <div className="chat-static-message">
            <h2 className="chat-static-title">
              El grimorio te observa:{" "}
              <span className="chat-static-highlight">tu señal</span>.
            </h2>
            <p className="chat-static-subtitle">
              WORSHIP ya puede verte. Entrega tu retrato y revela la marca que
              la sombra guarda para ti.
            </p>
            <p className="chat-static-whisper">
              La niebla se mueve. El antiguo sello aguarda tu rostro.
            </p>
            <p className="chat-static-whisper">
              Sube una imagen y deja que el conjuro trace su señal.
            </p>
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
        {photoError && <div className="chat-error" role="alert">{photoError}</div>}
        <div ref={messagesEndRef} />
      </div>
      <aside className="photo-preview" aria-label="Vista previa de tu foto">
        <h2>Vista previa de tu marca</h2>
        <div className={`photo-preview-frame${photoUrl ? " has-photo" : ""}`}>
          {photoUrl ? (
            <img
              className={annotatedPhotoUrl ? "annotated" : "original"}
              src={annotatedPhotoUrl ?? photoUrl}
              alt={
                annotatedPhotoUrl
                  ? "Foto marcada por WORSHIP"
                  : "Foto seleccionada para WORSHIP"
              }
            />
          ) : (
            <div className="photo-placeholder" role="img" aria-label="Rostro de ejemplo con la marca WORSHIP">
              <img
                className="placeholder-portrait"
                src="/referencia.png"
                alt=""
                aria-hidden="true"
              />
            </div>
          )}
        </div>
        <p>
          {annotatedPhotoUrl
            ? "El sello ya vive en tu retrato."
            : "Aquí quedarás marcado."}
        </p>
        <div className="photo-preview-links">
          <a href={previewUrl} target="_blank" rel="noreferrer">
            Abrir completa
          </a>
          <a
            href={previewUrl}
            download={
              annotatedPhotoUrl
                ? "worship-foto-anotada.png"
                : photoUrl
                  ? "worship-foto"
                  : "referencia.png"
            }
          >
            Descargar
          </a>
        </div>
      </aside>
      <div className="chat-input-area">
        <textarea
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Escribe un mensaje para WORSHIP..."
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