import React from "react";
import type { FaceComponent } from "../models/faceModel";

interface Props {
  components: FaceComponent[];
}

export function FaceRenderer({ components }: Props) {
  const find = (name: string) => components.find((c) => c.name === name);

  const boca = find("boca");
  const nariz = find("nariz");
  const ojoDerecho = find("ojo-derecho");
  const ojoIzquierdo = find("ojo-izquierdo");

  const style: React.CSSProperties = { position: "absolute", objectFit: "contain" };

  return (
    <div style={{ position: "relative", width: 300, height: 300 }}>
      {ojoIzquierdo && (
        <img
          src={`data:${ojoIzquierdo.type};base64,${ojoIzquierdo.data}`}
          alt="ojo-izquierdo"
          style={{ ...style, left: 40, top: 80, width: 80, height: 80 }}
        />
      )}
      {ojoDerecho && (
        <img
          src={`data:${ojoDerecho.type};base64,${ojoDerecho.data}`}
          alt="ojo-derecho"
          style={{ ...style, right: 40, top: 80, width: 80, height: 80 }}
        />
      )}
      {nariz && (
        <img
          src={`data:${nariz.type};base64,${nariz.data}`}
          alt="nariz"
          style={{ ...style, left: 125, top: 150, width: 50, height: 50 }}
        />
      )}
      {boca && (
        <img
          src={`data:${boca.type};base64,${boca.data}`}
          alt="boca"
          style={{ ...style, left: 75, top: 200, width: 150, height: 60 }}
        />
      )}
    </div>
  );
}
