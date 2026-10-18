import { sendChatMessage } from "../services/chatService";
import type { ChatResponse } from "../models/chatModel";

export async function interpretChat(text: string): Promise<ChatResponse> {
  return sendChatMessage(text);
}