import type { FaceResponse } from "../models/faceModel";

const API_BASE_URL =
  import.meta.env.PUBLIC_API_BASE_URL ??
  "https://robot-worship-accion-independiente.vercel.app";
const MAX_IMAGE_SIZE = 5 * 1024 * 1024;
const ACCEPTED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"];

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

export function validateFaceImageFile(file: File): void {
  if (!ACCEPTED_IMAGE_TYPES.includes(file.type)) {
    throw new Error("Selecciona una imagen JPEG, PNG o WebP.");
  }

  if (file.size === 0) {
    throw new Error("El archivo está vacío.");
  }

  if (file.size > MAX_IMAGE_SIZE) {
    throw new Error("La imagen no debe superar los 5 MiB.");
  }
}

export async function annotateFaceImage(file: File): Promise<Blob> {
  validateFaceImageFile(file);

  const formData = new FormData();
  formData.append("file", file);

  let response: Response;
  try {
    response = await fetch("/api/v1/face/annotate", {
      method: "POST",
      body: formData,
    });
  } catch {
    throw new Error(
      "No se pudo conectar con la API. Comprueba tu conexión e inténtalo de nuevo.",
    );
  }

  if (!response.ok) {
    let message: string | null = null;
    try {
      const body: unknown = await response.json();
      if (
        isRecord(body) &&
        isRecord(body.error) &&
        typeof body.error.message === "string"
      ) {
        message = body.error.message;
      }
    } catch {
      // Some proxies return a non-JSON error body.
    }

    throw new Error(
      message ?? `La API respondió con el estado ${response.status}.`,
    );
  }

  const contentType = response.headers.get("content-type") ?? "";
  if (!contentType.toLowerCase().includes("image/png")) {
    throw new Error("La API respondió, pero no devolvió una imagen PNG.");
  }

  const image = await response.blob();
  if (image.size === 0) {
    throw new Error("La API devolvió una imagen vacía.");
  }

  return image;
}

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
