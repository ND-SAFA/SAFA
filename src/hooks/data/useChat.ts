import { defineStore } from "pinia";

import { ProjectChatSchema } from "@/types";
import { pinia } from "@/plugins";

/**
 * This store manages the chat data for a project.
 */
export const useChat = defineStore("useChat", {
  state: () => ({
    chats: [] as ProjectChatSchema[],
    currentChat: undefined as ProjectChatSchema | undefined,
  }),
  actions: {
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
    updateCurrentChat(chat: Partial<ProjectChatSchema>): void {
      if (!this.currentChat) return;

      this.currentChat = { ...this.currentChat, ...chat };
    },
  },
});

export default useChat(pinia);
