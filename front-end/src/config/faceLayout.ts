export interface FaceLayoutItem {
  x: number;
  y: number;
  width: number;
  height: number;
}

export const faceLayout: Record<string, FaceLayoutItem> = {
  "ojo-izquierdo": {
    x: -17,
    y: 12,
    width: 72,
    height: 62,
  },
  "ojo-derecho": {
    x: 44,
    y: 12,
    width: 72,
    height: 62,
  },
  nariz: {
    x: 40,
    y: 32,
    width: 19,
    height: 28,
  },
  boca: {
    x: 29,
    y: 68,
    width: 42,
    height: 20,
  },
};