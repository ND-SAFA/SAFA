import {
  ChatMessageSchema,
  ChatMessageSendResponseSchema,
  CreateProjectChatSchema,
  EditProjectChatSchema,
  ProjectChatSchema,
  SendChatMessageSchema,
} from "@/types";
import { ENABLED_FEATURES } from "@/util";
import { buildRequest } from "@/api";

const EXAMPLE_SAFA_MESSAGE: ChatMessageSchema = {
  id: "3",
  isUser: false,
  message: "Hello! How can I help you?",
  artifactIds: [],
  createdAt: new Date().toISOString(),
};

const EXAMPLE_SAFA_MESSAGE_RESPONSE = {
  userMessage: EXAMPLE_SAFA_MESSAGE,
  responseMessage: EXAMPLE_SAFA_MESSAGE,
};

const EXAMPLE_PROJECT_CHAT: ProjectChatSchema = {
  id: "1",
  versionId: "1",
  title: "Mockup Chat",
  permission: "owner",
  messages: [EXAMPLE_SAFA_MESSAGE],
};

const EXAMPLE_NASA_CHAT: ProjectChatSchema = {
  id: "2",
  title: "GLM Coverage",
  versionId: "1",
  permission: "owner",
  messages: [
    {
      id: "1",
      isUser: true,
      message: "How is the GLM coverage ensured?",
      artifactIds: [],
      createdAt: new Date().toISOString(),
    },
    {
      id: "2",
      isUser: false,
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
        "[Feature56] Kernel Profiling and Optimization",
        "[FR231] Collect RCU Diagnostics and Statistics",
        "kernel/rcu/tree_exp.h",
        "kernel/rcu/tree.h",
        "kernel/rcu/update.c",
      ],
      createdAt: new Date().toISOString(),
    },
  ],
};

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
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return {
      ...EXAMPLE_PROJECT_CHAT,
      title: title || "New Chat",
      id: Math.random().toString(),
      versionId,
    };
  }

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
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return chat;
  }

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
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return;
  }
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
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return [EXAMPLE_NASA_CHAT, EXAMPLE_PROJECT_CHAT];
  }

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
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return {
      ...EXAMPLE_SAFA_MESSAGE_RESPONSE,
      userMessage: { ...EXAMPLE_SAFA_MESSAGE, ...message },
    };
  }

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
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return EXAMPLE_PROJECT_CHAT;
  }

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
  if (ENABLED_FEATURES.NASA_PROJECT_CHAT_MOCKUP) {
    return EXAMPLE_PROJECT_CHAT;
  }

  return buildRequest<ProjectChatSchema, "chatId">("chatTitle", {
    chatId,
  }).post();
}
