import { ChatMessageSchema, ProjectChatSchema } from "@/types";
import { ENABLED_FEATURES } from "@/util";
import { buildRequest } from "@/api";

const EXAMPLE_SAFA_MESSAGE: ChatMessageSchema = {
  id: "1",
  userMessage: false,
  message: "Hello! How can I help you?",
  artifactIds: [],
};

const EXAMPLE_PROJECT_CHAT: ProjectChatSchema = {
  id: "1",
  title: "Mockup Chat",
  permission: "owner",
  messages: [EXAMPLE_SAFA_MESSAGE],
};

const EXAMPLE_NASA_CHAT: ProjectChatSchema = {
  id: "2",
  title: "GLM Coverage",
  permission: "owner",
  messages: [
    {
      id: "1",
      userMessage: true,
      message: "How is the GLM coverage ensured?",
      artifactIds: [],
    },
    {
      id: "2",
      userMessage: false,
      message:
        "LIRD137 established the first coverage specification for the GLM.\n\n" +
        "A change request (CCR01543) was issued to update the level two requirement, MRD222.\n\n" +
        "MRD222 contains three children further refining the coverage requirements:\n" +
        "MRD1256, MRD1262, MRD1254.",
      artifactIds: [
        "LIRD137",
        "CCR1543",
        "MRD222",
        "MRD1256",
        "MRD1262",
        "MRD1264",
      ],
    },
  ],
};

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
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return {
      ...EXAMPLE_PROJECT_CHAT,
      id: Math.random().toString(),
      messages: [message],
    };
  }
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
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return;
  }
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
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return [EXAMPLE_NASA_CHAT, EXAMPLE_PROJECT_CHAT];
  }
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
): Promise<ChatMessageSchema> {
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return EXAMPLE_SAFA_MESSAGE;
  }
  return buildRequest<
    ChatMessageSchema,
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
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return EXAMPLE_PROJECT_CHAT;
  }
  return buildRequest<ProjectChatSchema, "versionId" | "chatId">("getChats", {
    versionId,
    chatId,
  }).get();
}
