export interface FaceLayoutItem {
  x: number;
  y: number;
  width: number;
  height: number;
}

export const faceLayout: Record<string, FaceLayoutItem> = {
  "ojo-izquierdo": {
    x: -15,
    y: -10,
    width: 75,
    height: 100,
  },
  "ojo-derecho": {
    x: 35,
    y: -10,
    width: 75,
    height: 100,
  },
  nariz: {
    x: 41,
    y: 28,
    width: 16,
    height: 28,
  },
boca: {
    x: 24,
    y: 72,
    width: 50,
    height: 34,
  },
};