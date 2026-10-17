export interface FaceLayoutItem {
  x: number;
  y: number;
  width: number;
  height: number;
}

export const faceLayout: Record<string, FaceLayoutItem> = {
  "ojo-izquierdo": {
    x: 0,
    y: 0,
    width: 50,
    height: 95,
  },
  "ojo-derecho": {
    x: 50,
    y: 0,
    width: 50,
    height: 95,
  },
  nariz: {
    x: 42,
    y: 22,
    width: 16,
    height: 28,
  },
  boca: {
    x: 39,
    y: 75,
    width: 22,
    height: 8,
  },
};