import React, { useEffect, useState } from "react";
import type { FaceComponent } from "../models/faceModel";
import type { BlinkAnimation, BlinkFrame } from "../models/chatModel";
import { faceLayout } from "../config/faceLayout";
import "../styles/face.css";

interface Props {
  components: FaceComponent[];
  animation: BlinkAnimation | null;
}

const FRAME_DURATION_MS = 250;
const CLOSED_FRAME_HOLD_MS = 2000;

export function FaceRenderer({ components, animation }: Props) {
  const [activeFrame, setActiveFrame] = useState<BlinkFrame | null>(null);

  useEffect(() => {
    if (!animation) {
      setActiveFrame(null);
      return;
    }

    let frameIndex = 0;
    let completedCycles = 0;
    let timeoutId: number | undefined;

    const showNextFrame = () => {
      setActiveFrame(animation.frames[frameIndex]);
      frameIndex += 1;

      if (frameIndex === animation.frames.length) {
        frameIndex = 0;
        completedCycles += 1;
      }

      if (completedCycles === animation.count) {
        timeoutId = window.setTimeout(
          () => setActiveFrame(null),
          FRAME_DURATION_MS + CLOSED_FRAME_HOLD_MS,
        );
        return;
      }

      timeoutId = window.setTimeout(showNextFrame, FRAME_DURATION_MS);
    };

    showNextFrame();
    return () => {
      if (timeoutId !== undefined) window.clearTimeout(timeoutId);
    };
  }, [animation]);

  const find = (name: string) => components.find((c) => c.name === name);

  const boca = find("boca");
  const nariz = find("nariz");
  const ojoDerecho = find("ojo-derecho");
  const ojoIzquierdo = find("ojo-izquierdo");

  const imageSource = (component: FaceComponent | undefined) => {
    if (!component) return undefined;
    if (activeFrame) return `data:image/png;base64,${activeFrame.data}`;
    return `data:${component.type};base64,${component.data}`;
  };

  const eyeClassName = activeFrame?.name === "3.png"
    ? "face-iframe face-eye face-eye-closed"
    : "face-iframe face-eye";

  const buildStyle = (name: string) => {
    const layout = faceLayout[name];
    if (!layout) return undefined;
    return {
      left: `${layout.x}%`,
      top: `${layout.y}%`,
      width: `${layout.width}%`,
      height: `${layout.height}%`,
    };
  };

  return (
    <div className="face-container" role="img" aria-label="Rostro de la mascota WORSHIP compuesto por ojos, nariz y boca">
      {ojoIzquierdo && (
        <img
          className={eyeClassName}
          src={imageSource(ojoIzquierdo)}
          alt=""
          aria-hidden="true"
          style={buildStyle("ojo-izquierdo")}
        />
      )}
      {ojoDerecho && (
        <img
          className={eyeClassName}
          src={imageSource(ojoDerecho)}
          alt=""
          aria-hidden="true"
          style={buildStyle("ojo-derecho")}
        />
      )}
      {activeFrame?.name === "3.png" && (
        <div className="blink-message-bubble" role="status">
          YA ERES PARTE DE WORSHIP
        </div>
      )}
      {nariz && (
        <img
          className="face-iframe"
          src={`data:${nariz.type};base64,${nariz.data}`}
          alt=""
          aria-hidden="true"
          style={buildStyle("nariz")}
        />
      )}
      {boca && (
        <img
          className="face-iframe"
          src={`data:${boca.type};base64,${boca.data}`}
          alt=""
          aria-hidden="true"
          style={buildStyle("boca")}
        />
      )}
    </div>
  );
}