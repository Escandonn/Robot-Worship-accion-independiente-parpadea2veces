import type { ChatResponse } from "../models/chatModel";

const API_BASE_URL = import.meta.env.PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";
const BLINK_FRAME_NAMES = ["1.png", "2.png", "3.png"] as const;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

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

  if (!isRecord(json)) {
    throw new Error("Invalid response");
  }

  if (json.success !== true) {
    throw new Error("Request not successful");
  }

  if (!isRecord(json.response) || typeof json.response.content !== "string") {
    throw new Error("Invalid response");
  }

  const responseData = json.response;
  if (!Array.isArray(responseData.frames)) {
    throw new Error("Invalid response frames");
  }

  if (
    json.intent === "text" &&
    responseData.type === "text" &&
    responseData.frames.length === 0
  ) {
    return {
      success: true,
      intent: "text",
      response: {
        type: "text",
        content: responseData.content,
        frames: [],
      },
    };
  }

  if (
    json.intent === "blink" &&
    responseData.type === "animation" &&
    Number.isInteger(responseData.count) &&
    typeof responseData.count === "number" &&
    responseData.count >= 1 &&
    responseData.count <= 10 &&
    responseData.frames.length === BLINK_FRAME_NAMES.length
  ) {
    const frames = responseData.frames.map((frame, index) => {
      if (
        !isRecord(frame) ||
        frame.name !== BLINK_FRAME_NAMES[index] ||
        frame.format !== "png" ||
        typeof frame.data !== "string" ||
        frame.data.length === 0
      ) {
        throw new Error("Invalid animation frame");
      }

      return {
        name: frame.name,
        format: "png" as const,
        data: frame.data,
      };
    });

    return {
      success: true,
      intent: "blink",
      response: {
        type: "animation",
        content: responseData.content,
        frames,
        count: responseData.count,
      },
    };
  }

  throw new Error("Invalid response intent");
}