import { defineStore } from "pinia";

import {
  ArtifactSchema,
  ChatMessageSchema,
  DisplayChatMessageSchema,
  IconVariant,
  ProjectChatSchema,
} from "@/types";
import { buildProjectChat } from "@/util";
import { artifactStore, projectStore, sessionStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * This store manages the chat data for a project.
 */
export const useChat = defineStore("useChat", {
  state: () => ({
    chats: [] as ProjectChatSchema[],
    currentChat: buildProjectChat(),
  }),
  getters: {
    /**
     * @returns The current chat messages.
     */
    currentMessages(): ChatMessageSchema[] {
      return this.currentChat.messages;
    },
    /**
     * @returns The current chat messages with additional display data.
     */
    currentMessagesDisplay(): DisplayChatMessageSchema[] {
      return this.currentChat.messages.map((message) => ({
        ...message,
        iconClass: message.isUser ? undefined : "bg-gradient",
        iconColor: message.isUser ? "primary" : undefined,
        iconVariant: (message.isUser ? "account" : "generate") as IconVariant,
        userName: message.isUser ? sessionStore.userEmail : "SAFA",
        referenceLabel:
          message.artifactIds.length === 1
            ? `1 Reference`
            : `${message.artifactIds.length} References`,
        artifacts: message.artifactIds
          .map(
            (artifactId) =>
              artifactStore.getArtifactById(artifactId) ||
              artifactStore.getArtifactByName(artifactId) // TODO: remove after mockup
          )
          .filter((artifact) => !!artifact) as ArtifactSchema[],
      }));
    },
  },
  actions: {
    initializeChats(chats: ProjectChatSchema[]): void {
      this.chats = chats;
      this.currentChat = chats[0] || buildProjectChat();
    },
    /**
     * Switch the current chat.
     * @param chat - The chat to switch to.
     */
    switchChat(chat: ProjectChatSchema): void {
      this.currentChat = chat;
    },
    /**
     * Add a chat to the store, and sets it as the current.
     * No-operation is performed if current chat does not have ID set.
     * @param chat
     */
    addChat(chat: Partial<ProjectChatSchema> = {}): void {
      if (chat.id === undefined && this.chats.map((c) => c.id).includes("")) {
        return; // blocks spamming the `create` button
      }
      const newChat = buildProjectChat({
        versionId: projectStore.versionId,
        ...chat,
      });
      this.chats = [newChat, ...this.chats];
      this.currentChat = newChat;
    },
    /**
     * Delete a chat from the store.
     * If the chat is the current chat, the current chat will be set to the next most recent.
     * @param chatId - The chat to delete.
     */
    deleteChat(chatId: string): void {
      this.chats = this.chats.filter((chat) => chat.id !== chatId);

      if (this.currentChat.id === chatId) {
        // Sets first chat or new empty chat if none left.
        this.currentChat = this.chats[0] || buildProjectChat();
      }
    },
    /**
     * Update a chat with new data, retaining order of chats.
     * @param chat - The chat data to update.
     */
    updateChat(
      chat: Pick<ProjectChatSchema, "id"> & Partial<ProjectChatSchema>
    ): void {
      const index = this.chats.findIndex((c) => c.id === chat.id);

      if (index === -1) return;

      const fullChat = { ...this.chats[index], ...chat };

      this.chats[index] = fullChat;

      if (chat.id === this.currentChat.id) {
        this.currentChat = fullChat;
      }
    },
  },
});

export default useChat(pinia);
