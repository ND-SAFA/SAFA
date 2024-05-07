import { ComputedRef } from "vue";
import { ProjectChatSchema } from "@/types";

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
   * Switches to the given chat, then retrieves messages and updates the store.
   * @param chat - The chat to load messages for.
   */
  handleLoadProjectChatMessages(chat: ProjectChatSchema): Promise<void>;

  /**
   * Creates a new chat for the current project, and sets it as the current chat.
   * @param title - Optional title to creat chat with.
   */
  handleCreateProjectChat(
    title?: string
  ): Promise<ProjectChatSchema | undefined>;

  /**
   * Saves edits to the title of the current chat.
   */
  handleEditProjectChat(title: string): Promise<void>;

  /**
   * Deletes a chat for the current project.
   * If the chat is the current chat, the current chat will be set to the next most recent.
   * @param chatId - The chat to delete.
   */
  handleDeleteProjectChat(chatId: string): Promise<void>;

  /**
   * Sends a chat message to the current chat.
   * @param chat - The chat to send the message in.
   * @param message - The message to send.
   */
  handleSendChatMessage(
    chat: ProjectChatSchema,
    message: string
  ): Promise<void>;
}
