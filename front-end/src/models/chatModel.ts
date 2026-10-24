export interface ChatMessage {
  id: string;
  role: "user" | "bot";
  text: string;
  timestamp: number;
}

export interface BlinkFrame {
  name: "1.png" | "2.png" | "3.png";
  format: "png";
  data: string;
}

export interface BlinkAnimation {
  frames: BlinkFrame[];
  count: number;
}

interface TextChatResponse {
  success: true;
  intent: "text";
  response: {
    type: "text";
    content: string;
    frames: [];
  };
}

interface BlinkChatResponse {
  success: true;
  intent: "blink";
  response: {
    type: "animation";
    content: string;
    frames: BlinkFrame[];
    count: number;
  };
}

export type ChatResponse = TextChatResponse | BlinkChatResponse;