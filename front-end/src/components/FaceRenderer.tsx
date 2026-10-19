import React from "react";
import type { FaceComponent } from "../models/faceModel";
import { faceLayout } from "../config/faceLayout";
import "../styles/face.css";

interface Props {
  components: FaceComponent[];
}

export function FaceRenderer({ components }: Props) {
  const find = (name: string) => components.find((c) => c.name === name);

  const boca = find("boca");
  const nariz = find("nariz");
  const ojoDerecho = find("ojo-derecho");
  const ojoIzquierdo = find("ojo-izquierdo");

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
          className="face-iframe"
          src={`data:${ojoIzquierdo.type};base64,${ojoIzquierdo.data}`}
          alt=""
          aria-hidden="true"
          style={buildStyle("ojo-izquierdo")}
        />
      )}
      {ojoDerecho && (
        <img
          className="face-iframe"
          src={`data:${ojoDerecho.type};base64,${ojoDerecho.data}`}
          alt=""
          aria-hidden="true"
          style={buildStyle("ojo-derecho")}
        />
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