import React, { useEffect, useState } from "react";
import { loadFace } from "../controllers/faceController";
import type { FaceResponse } from "../models/faceModel";
import type { BlinkAnimation } from "../models/chatModel";
import { FaceRenderer } from "../components/FaceRenderer";
import { ChatCentral } from "../components/ChatCentral";
import "../styles/face.css";
import "../styles/chat.css";

export function FaceView() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<FaceResponse | null>(null);
  const [animation, setAnimation] = useState<BlinkAnimation | null>(null);

  const handleBlink = (blink: BlinkAnimation) => {
    setAnimation(blink);
  };

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await loadFace();
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let mounted = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const result = await loadFace();
        if (mounted) setData(result);
      } catch (e) {
        if (mounted) setError(e instanceof Error ? e.message : "Unknown error");
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div className="face-page">
      <div className="face-stage">
        {loading && <p style={{ color: "#94A3B8" }}>Loading...</p>}
        {error && (
          <div>
            <p style={{ color: "#ff8a8a" }}>{error}</p>
            <button onClick={load}>Retry</button>
          </div>
        )}
        {!loading && !error && data && (
          <>
            <FaceRenderer components={data.components} animation={animation} />
            <div className="face-message">
              <h2 className="face-message-title">
                Tu rostro, <span className="face-message-highlight">tu señal</span>.
              </h2>
              <p className="face-message-subtitle">WORSHIP ya puede verte y dejar su marca.</p>
            </div>
          </>
        )}
      </div>
      <ChatCentral onBlink={handleBlink} />
    </div>
  );
}