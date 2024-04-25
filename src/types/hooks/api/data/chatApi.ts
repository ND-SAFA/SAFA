import { ComputedRef } from "vue";
import { ChatMessageSchema } from "@/types";

/**
 * Represents actions that can be performed on the chat API.
 */
export interface ChatApiHook {
  /**
   * Whether the chat api is currently loading.
   */
  loading: ComputedRef<boolean>;
  /**
   * Whether the chat api is currently loading a response message.
   */
  loadingResponse: ComputedRef<boolean>;
  /**
   * Gets all chats for the current project.
   */
  handleGetProjectChats(): Promise<void>;
  /**
   * Loads a chat for the project.
   * @param chatId - The chat to load.
   */
  handleGetProjectChat(chatId: string): Promise<void>;
  /**
   * Creates a new chat for the current project, and sets it as the current chat.
   */
  handleCreateProjectChat(message: ChatMessageSchema): Promise<void>;
  /**
   * Deletes a chat for the current project.
   * If the chat is the current chat, the current chat will be set to the next most recent.
   * @param chatId - The chat to delete.
   */
  handleDeleteProjectChat(chatId: string): Promise<void>;
  /**
   * Sends a chat message to the current chat.
   * @param message - The message to send.
   */
  handleSendChatMessage(message: string): Promise<void>;
}
