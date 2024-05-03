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
  const chatDialogApi = useApi("chatDialogApi");

  const loading = computed(() => chatApi.loading);
  const loadingResponse = computed(() => chatDialogApi.loading);

  async function handleGetProjectChats() {
    await chatApi.handleRequest(async () => {
      chatStore.initializeChats(await getProjectChats());
    }, {});
  }

  async function handleGetProjectChat(chatId: string) {
    await chatApi.handleRequest(async () => {
      chatStore.updateChat(await getProjectChatMessages(chatId));
    }, {});
  }

  async function handleCreateProjectChat() {
    await chatApi.handleRequest(async () => {
      chatStore.addChat(await createProjectChat(projectStore.versionId));
    }, {});
  }

  async function handleDeleteProjectChat() {
    await chatApi.handleRequest(async () => {
      const chatId = chatStore.currentChat?.id;

      if (!chatId) return;

      await deleteProjectChat(chatId);

      chatStore.deleteChat(chatId);
    }, {});
  }

  async function handleSendChatMessage(message: string) {
    await chatDialogApi.handleRequest(async () => {
      const fullMessage: ChatMessageSchema = {
        id: "",
        isUser: true,
        message,
        artifactIds: [],
      };

      if (!chatStore.currentChat) {
        await handleCreateProjectChat();
      }

      if (!chatStore.currentChat) return;

      chatStore.updateChat({
        ...chatStore.currentChat,
        messages: [...chatStore.currentChat.messages, fullMessage],
      });

      const responseMessage = await createProjectChatMessage(
        chatStore.currentChat.id,
        fullMessage
      );

      chatStore.updateChat({
        ...chatStore.currentChat,
        messages: [...chatStore.currentChat.messages, responseMessage],
      });
    }, {});
  }

  return {
    loading,
    loadingResponse,
    handleGetProjectChats,
    handleGetProjectChat,
    handleCreateProjectChat,
    handleDeleteProjectChat,
    handleSendChatMessage,
  };
});

export default useChatApi(pinia);
