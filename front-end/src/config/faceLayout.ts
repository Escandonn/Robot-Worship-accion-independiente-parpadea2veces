export interface FaceLayoutItem {
  x: number;
  y: number;
  width: number;
  height: number;
}

export const faceLayout: Record<string, FaceLayoutItem> = {
  "ojo-izquierdo": {
    x: 8,
    y: 12,
    width: 32,
    height: 52,
  },
  "ojo-derecho": {
    x: 60,
    y: 12,
    width: 32,
    height: 52,
  },
  nariz: {
    x: 42,
    y: 22,
    width: 16,
    height: 28,
  },
  boca: {
    x: 39,
    y: 68,
    width: 22,
    height: 10,
  },
};