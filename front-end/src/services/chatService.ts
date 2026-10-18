import type { ChatResponse } from "../models/chatModel";

const API_BASE_URL = import.meta.env.PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function sendChatMessage(text: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/robot/interpret`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
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

  const data = json as ChatResponse;

  if (data.success !== true) {
    throw new Error("Request not successful");
  }

  return data;
}