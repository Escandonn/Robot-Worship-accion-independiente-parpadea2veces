import { fetchFaceInitial } from "../services/faceService";
import type { FaceResponse } from "../models/faceModel";

export interface FaceControllerState {
  loading: boolean;
  error: string | null;
  data: FaceResponse | null;
}

export async function loadFace(): Promise<FaceResponse> {
  return fetchFaceInitial();
}
