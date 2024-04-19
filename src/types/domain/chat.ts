/**
 * Represents a chat message between SAFA and a user.
 */
export interface ChatMessageSchema {
  /**
   * Unique identifier for the message.
   */
  id: string;
  /**
   * The user's message.
   */
  userMessage: boolean;
  /**
   * SAFA AI's response.
   */
  message: string;
  /**
   * Artifact IDs referenced in the message.
   */
  artifactIds: string[];
}

/**
 * Represents a chat dialogue between SAFA and a user.
 */
export interface ProjectChatSchema {
  /**
   * Unique identifier for the chat.
   */
  id: string;
  /**
   * All chat messages.
   */
  messages: ChatMessageSchema[];
}
