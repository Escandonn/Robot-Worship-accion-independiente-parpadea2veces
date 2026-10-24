import type { FaceResponse } from "../models/faceModel";

const API_BASE_URL =
  import.meta.env.PUBLIC_API_BASE_URL ??
  "https://robot-worship-accion-independiente.vercel.app";

export async function fetchFaceInitial(): Promise<FaceResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/face/initial`, {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  let json: unknown;
  try {
    json = await response.json();
  } catch {
    throw new Error("Invalid JSON response");
  }

  if (typeof json !== "object" || json === null) {
    throw new Error("Invalid response");
  }

  const data = json as FaceResponse;

  if (data.success !== true) {
    throw new Error("Request not successful");
  }

  if (!Array.isArray(data.components) || data.components.length !== 4) {
    throw new Error("Missing components");
  }

  for (const component of data.components) {
    if (
      typeof component?.name !== "string" ||
      !component.name ||
      typeof component?.type !== "string" ||
      !component.type ||
      typeof component?.data !== "string" ||
      !component.data
    ) {
      throw new Error("Invalid component data");
    }
  }

  return data;
}
