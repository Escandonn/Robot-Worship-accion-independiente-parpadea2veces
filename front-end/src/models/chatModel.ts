export interface ChatMessage {
  id: string;
  role: "user" | "bot";
  text: string;
  timestamp: number;
}

export interface ChatResponse {
  success: boolean;
  intent: string;
  response: {
    type: string;
    content: string;
    resource?: Record<string, unknown> | null;
  };
}