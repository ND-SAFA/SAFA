import {
  ChatMessageSendResponseSchema,
  CreateProjectChatSchema,
  EditProjectChatSchema,
  ProjectChatSchema,
  SendChatMessageSchema,
} from "@/types";
import { buildRequest } from "@/api";

/**
 * Create a chat dialogue for a project.
 * @param versionId - The unique identifier of the version.
 * @param title - The title of the chat dialogue.
 * @returns The chat dialogue created.
 */
export async function createProjectChat(
  versionId: string,
  title = ""
): Promise<ProjectChatSchema> {
  return buildRequest<ProjectChatSchema, string, CreateProjectChatSchema>(
    "chatCollection"
  ).post({ versionId, title });
}

/**
 * Edits the title of a project chat.
 * @param chat - The chat dialogue to edit.
 * @returns The chat dialogue with the new title.
 */
export async function editProjectChat(
  chat: ProjectChatSchema
): Promise<ProjectChatSchema> {
  return buildRequest<ProjectChatSchema, "chatId", EditProjectChatSchema>(
    "chat",
    {
      chatId: chat.id,
    }
  ).put({ title: chat.title });
}

/**
 * Delete a chat dialogue for a project.
 * @param chatId - The unique identifier of the chat dialogue.
 */
export async function deleteProjectChat(chatId: string): Promise<void> {
  return buildRequest<void, "chatId">("chat", {
    chatId,
  }).delete();
}

/**
 * Get all chat dialogues for a project.
 * @param projectId - The unique identifier of the project.
 * @returns All chat dialogues for the project.
 */
export async function getProjectChats(
  projectId: string
): Promise<ProjectChatSchema[]> {
  return buildRequest<ProjectChatSchema[]>("chatProject", { projectId }).get();
}

/**
 * Create a new message in a chat dialogue.
 * @param chatId - The unique identifier of the chat dialogue.
 * @param message - The chat message to create.
 * @returns The chat dialogues with the new message.
 */
export async function createProjectChatMessage(
  chatId: string,
  message: SendChatMessageSchema
): Promise<ChatMessageSendResponseSchema> {
  return buildRequest<
    ChatMessageSendResponseSchema,
    "chatId",
    SendChatMessageSchema
  >("chatMessages", { chatId }).post(message);
}

/**
 * Get all messages in a chat dialogue.
 * @param chatId - The unique identifier of the chat dialogue.
 * @returns The chat dialogue.
 */
export async function getProjectChatMessages(
  chatId: string
): Promise<ProjectChatSchema> {
  return buildRequest<ProjectChatSchema, "chatId">("chatMessages", {
    chatId,
  }).get();
}

/**
 * Generates title for chat.
 * @param chatId - ID of chat to generate title for.
 */
export async function generateChatTitle(
  chatId: string
): Promise<ProjectChatSchema> {
  return buildRequest<ProjectChatSchema, "chatId">("chatTitle", {
    chatId,
  }).post();
}
