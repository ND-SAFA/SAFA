import { defineStore } from "pinia";

import { computed } from "vue";
import { ChatApiHook, ProjectChatSchema } from "@/types";
import { buildProjectChatMessage } from "@/util";
import { chatStore, projectStore, useApi } from "@/hooks";
import {
  createProjectChat,
  createProjectChatMessage,
  deleteProjectChat,
  editProjectChat,
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
      await handleLoadProjectChatMessages(chatStore.currentChat.id);
    }, {});
  }

  async function handleLoadProjectChatMessages(chatId: string) {
    if (!chatId) {
      return; // on mounted might have default chat with no id
    }
    await chatApi.handleRequest(async () => {
      chatStore.updateChat(await getProjectChatMessages(chatId));
    }, {});
  }

  async function handleCreateProjectChat(
    title?: string
  ): Promise<ProjectChatSchema | undefined> {
    let chatCreated; // Define the variable to store the chat creation result
    await chatApi.handleRequest(async () => {
      chatCreated = await createProjectChat(projectStore.versionId, title);
      chatStore.addChat(chatCreated); // Use the chatCreated variable
    }, {});
    return chatCreated; // Return the chatCreated variable
  }

  async function handleEditProjectChat(title: string) {
    await chatApi.handleRequest(async () => {
      const chatId = chatStore.currentChat.id;

      if (!chatId) return;

      chatStore.currentChat.title = title;

      await editProjectChat(chatStore.currentChat);
    }, {});
  }

  async function handleDeleteProjectChat() {
    await chatApi.handleRequest(async () => {
      const chatId = chatStore.currentChat.id;
      if (chatId) {
        await deleteProjectChat(chatId);
      }
      chatStore.deleteChat(chatId);
    }, {});
  }

  async function handleSendChatMessage(
    chat: ProjectChatSchema,
    message: string
  ) {
    await chatDialogApi.handleRequest(async () => {
      const newMessage = buildProjectChatMessage({ message });

      if (!chat) return;

      /**
       * BUG
       * Slight problem here, currentChat could be switched at anytime
       * which is why this now accepts the chat to send the message in.
       * However, handleCreateProjectChat will create the currentChat
       * and set the new response there. So, there is a chance that the user
       * sends their first message, jumps to another chat and sends another message,
       * and so when the first chat is done creating currentChat could have switched.
       */
      if (!chat.id) {
        chatStore.deleteChat(""); // todo: better way to delete empty current chat?
        const chatCreated = await handleCreateProjectChat(chat.title); // sets chat with id in store.
        if (chatCreated) {
          chat = chatCreated;
        } else {
          return; //error occurred while saving chat.
        }
      }

      chatStore.updateChat({
        ...chat,
        messages: [...chat.messages, newMessage],
      });

      const messagesCreated = await createProjectChatMessage(
        chat.id,
        newMessage
      );

      chatStore.updateChat({
        ...chat,
        messages: [
          ...chat.messages, // Chat object not mutated, so the user message is not in this list
          messagesCreated.userMessage,
          messagesCreated.responseMessage,
        ],
      });
    }, {});
  }

  return {
    loading,
    loadingResponse,
    handleGetProjectChats,
    handleLoadProjectChatMessages,
    handleCreateProjectChat,
    handleEditProjectChat,
    handleDeleteProjectChat,
    handleSendChatMessage,
  };
});

export default useChatApi(pinia);
