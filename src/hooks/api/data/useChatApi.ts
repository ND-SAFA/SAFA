import { defineStore } from "pinia";

import { computed } from "vue";
import { ChatApiHook, ChatMessageSchema } from "@/types";
import { chatStore, projectStore, useApi } from "@/hooks";
import {
  createProjectChat,
  createProjectChatMessage,
  deleteProjectChat,
  getProjectChatMessages,
  getProjectChats,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * This store manages interactions with the chat api for a project.
 */
export const useChatApi = defineStore("chatApi", (): ChatApiHook => {
  const chatApi = useApi("chatApi");

  const loading = computed(() => chatApi.loading);

  async function handleGetProjectChats() {
    await chatApi.handleRequest(async () => {
      chatStore.initializeChats(await getProjectChats(projectStore.versionId));
    }, {});
  }

  async function handleGetProjectChat(chatId: string) {
    await chatApi.handleRequest(async () => {
      chatStore.updateChat(
        await getProjectChatMessages(projectStore.versionId, chatId)
      );
    }, {});
  }

  async function handleCreateProjectChat(message: ChatMessageSchema) {
    await chatApi.handleRequest(async () => {
      chatStore.addChat(
        await createProjectChat(projectStore.versionId, message)
      );
    }, {});
  }

  async function handleDeleteProjectChat() {
    await chatApi.handleRequest(async () => {
      const chatId = chatStore.currentChat?.id;
      if (!chatId) return;

      await deleteProjectChat(projectStore.versionId, chatId);

      chatStore.deleteChat(chatId);
    }, {});
  }

  async function handleSendChatMessage(message: ChatMessageSchema) {
    await chatApi.handleRequest(async () => {
      if (!chatStore.currentChat) return;

      const createdMessage = await createProjectChatMessage(
        projectStore.versionId,
        chatStore.currentChat.id,
        message
      );

      chatStore.updateChat({
        ...chatStore.currentChat,
        messages: [...chatStore.currentChat.messages, createdMessage],
      });
    }, {});
  }

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
