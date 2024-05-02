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
}

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

export type CreateProjectChatSchema = Pick<
  ProjectChatSchema,
  "versionId" | "title"
>;
