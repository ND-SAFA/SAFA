import { defineStore } from "pinia";

import {
  ArtifactSchema,
  ChatMessageSchema,
  DisplayChatMessageSchema,
  IconVariant,
  ProjectChatSchema,
} from "@/types";
import { removeMatches } from "@/util";
import { artifactStore, sessionStore } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * This store manages the chat data for a project.
 */
export const useChat = defineStore("useChat", {
  state: () => ({
    chats: [] as ProjectChatSchema[],
    currentChat: undefined as ProjectChatSchema | undefined,
  }),
  getters: {
    /**
     * @returns The current chat messages.
     */
    currentMessages(): ChatMessageSchema[] {
      return this.currentChat?.messages || [];
    },
    /**
     * @returns The current chat messages with additional display data.
     */
    currentMessagesDisplay(): DisplayChatMessageSchema[] {
      return (this.currentChat?.messages || []).map((message) => ({
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
      this.currentChat = chats[0];
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
     * @param chat
     */
    addChat(chat: ProjectChatSchema): void {
      this.chats.push(chat);
      this.currentChat = chat;
    },
    /**
     * Delete a chat from the store.
     * If the chat is the current chat, the current chat will be set to the next most recent.
     * @param chatId - The chat to delete.
     */
    deleteChat(chatId: string): void {
      this.chats = this.chats.filter((chat) => chat.id !== chatId);

      if (this.currentChat?.id === chatId) {
        this.currentChat = this.chats[0] || this.chats[0];
      }
    },
    /**
     * Update the current chat with new data.
     * @param chat - The chat data to update.
     */
    updateChat(chat: ProjectChatSchema): void {
      this.chats = [...removeMatches(this.chats, "id", [chat.id]), chat];

      if (chat.id === this.currentChat?.id) {
        this.currentChat = chat;
      }
    },
  },
});

export default useChat(pinia);
