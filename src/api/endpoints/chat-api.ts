import { ChatMessageSchema, ProjectChatSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Create a chat dialogue for a project.
 * @param versionId - The unique identifier of the version.
 * @param message - The chat message to create.
 * @returns The chat dialogue created.
 */
export async function createProjectChat(
  versionId: string,
  message: ChatMessageSchema
): Promise<ProjectChatSchema> {
  return buildRequest<ProjectChatSchema, "versionId", ChatMessageSchema>(
    "createChat",
    { versionId }
  ).post(message);
}

/**
 * Delete a chat dialogue for a project.
 * @param versionId - The unique identifier of the version.
 * @param chatId - The unique identifier of the chat dialogue.
 */
export async function deleteProjectChat(
  versionId: string,
  chatId: string
): Promise<void> {
  return buildRequest<void, "versionId" | "chatId">("deleteChat", {
    versionId,
    chatId,
  }).delete();
}

/**
 * Get all chat dialogues for a project.
 * @param versionId - The unique identifier of the version.
 * @returns All chat dialogues for the project.
 */
export async function getProjectChats(
  versionId: string
): Promise<ProjectChatSchema[]> {
  return buildRequest<ProjectChatSchema[], "versionId", ChatMessageSchema>(
    "getChats",
    { versionId }
  ).get();
}

/**
 * Create a new message in a chat dialogue.
 * @param versionId - The unique identifier of the version.
 * @param chatId - The unique identifier of the chat dialogue.
 * @param message - The chat message to create.
 * @returns The chat dialogues with the new message.
 */
export async function createProjectChatMessage(
  versionId: string,
  chatId: string,
  message: ChatMessageSchema
): Promise<ProjectChatSchema> {
  return buildRequest<
    ProjectChatSchema,
    "versionId" | "chatId",
    ChatMessageSchema
  >("getChats", { versionId, chatId }).post(message);
}

/**
 * Get all messages in a chat dialogue.
 * @param versionId - The unique identifier of the version.
 * @param chatId - The unique identifier of the chat dialogue.
 * @returns The chat dialogue.
 */
export async function getProjectChatMessages(
  versionId: string,
  chatId: string
): Promise<ProjectChatSchema> {
  return buildRequest<ProjectChatSchema, "versionId" | "chatId">("getChats", {
    versionId,
    chatId,
  }).get();
}
