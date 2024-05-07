import { ArtifactSchema, IconVariant } from "@/types";

/**
 * Represents a chat message between SAFA and a user.
 */
export interface ChatMessageSchema {
  /**
   * Unique identifier for the message.
   */
  id: string;
  /**
   * Whether this is a user created message.
   */
  isUser: boolean;
  /**
   * The message content.
   */
  message: string;
  /**
   * Artifact IDs referenced in the message.
   */
  artifactIds: string[];
  /**
   * ISO timestamp of when the message was created.
   */
  createdAt: string;
}

/**
 * Represents a new chat message to be sent by a user.
 */
export type SendChatMessageSchema = Pick<ChatMessageSchema, "message">;

/**
 * Represents response for a successful send of a user message.
 */
export interface ChatMessageSendResponseSchema {
  /**
   * Saved user message containing persistent properties (e.g ID and timestamp)
   */
  userMessage: ChatMessageSchema;
  /**
   * Saved assistant response.
   */
  responseMessage: ChatMessageSchema;
}

/**
 * Represents a chat message between SAFA and a user, with additional display information.
 */
export interface DisplayChatMessageSchema extends ChatMessageSchema {
  /**
   * The icon class for the message.
   */
  iconClass: string | undefined;
  /**
   * The icon color for the message.
   */
  iconColor: string | undefined;
  /**
   * The icon variant for the message.
   */
  iconVariant: IconVariant;
  /**
   * The user name of the message sender.
   */
  userName: string;
  /**
   * The label for the references.
   */
  referenceLabel: string;
  /**
   * The artifacts referenced in the message.
   */
  artifacts: ArtifactSchema[];
}

/**
 * Represents the permissions for a chat.
 */
export type ChatPermissionType = "owner" | "reader" | "editor";

/**
 * Represents a chat dialogue between SAFA and a user.
 */
export interface ProjectChatSchema {
  /**
   * Unique identifier for the chat.
   */
  id: string;
  /**
   * Title of chat.
   */
  title: string;
  /**
   * Version ID of the project for this chat.
   */
  versionId: string;
  /**
   * Restricts available actions on chat.
   */
  permission: ChatPermissionType;
  /**
   * All chat messages.
   */
  messages: ChatMessageSchema[];
}

/**
 * Represents a new chat dialogue for a project.
 */
export type CreateProjectChatSchema = Pick<
  ProjectChatSchema,
  "versionId" | "title"
>;

/**
 * Represents an edit to a project chat.
 */
export type EditProjectChatSchema = Pick<ProjectChatSchema, "title">;
