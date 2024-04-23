import { defineStore } from "pinia";

import { computed } from "vue";
import { ChatApiHook, ChatMessageSchema } from "@/types";
import { useApi } from "@/hooks";
import { pinia } from "@/plugins";

/**
 * This store manages interactions with the chat api for a project.
 */
export const useChatApi = defineStore("chatApi", (): ChatApiHook => {
  const chatApi = useApi("chatApi");

  const loading = computed(() => chatApi.loading);

  async function handleGetProjectChats() {}

  async function handleGetProjectChat(chatId: string) {}

  async function handleCreateProjectChat() {}

  async function handleDeleteProjectChat() {}

  async function handleSendChatMessage(message: ChatMessageSchema) {}

  return {
    loading,
    handleGetProjectChats,
    handleGetProjectChat,
    handleCreateProjectChat,
    handleDeleteProjectChat,
    handleSendChatMessage,
  };
});

export default useChatApi(pinia);
