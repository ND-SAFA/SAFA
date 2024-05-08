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
  generateChatTitle,
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
      chatStore.initializeChats(await getProjectChats(projectStore.projectId));
      await handleLoadProjectChatMessages(chatStore.currentChat);
    }, {});
  }

  async function handleLoadProjectChatMessages(chat: ProjectChatSchema) {
    // Skip loading messages if the chat has yet to be created.
    if (!chat.id) return;

    await chatApi.handleRequest(async () => {
      chatStore.switchChat(chat);
      chatStore.updateChat(await getProjectChatMessages(chat.id));
    }, {});
  }

  async function handleCreateProjectChat(
    title?: string
  ): Promise<ProjectChatSchema | undefined> {
    let chatCreated: ProjectChatSchema | undefined; // Define the variable to store the chat creation result

    await chatApi.handleRequest(async () => {
      chatCreated = await createProjectChat(projectStore.versionId, title);
      chatStore.deleteChat(""); // Delete the unsaved chat to replace.
      chatStore.addChat(chatCreated); // Add the newly created chat and switch to it.
    }, {});

    return chatCreated; // Return the chatCreated variable
  }

  async function handleEditProjectChat(title: string) {
    await chatApi.handleRequest(
      async () => {
        const chatId = chatStore.currentChat.id;

        if (!chatId) return;

        chatStore.currentChat.title = title;

        await editProjectChat(chatStore.currentChat);
      },
      {
        success: "Chat title has been updated: " + title,
        error: "Unable to update chat title: " + title,
      }
    );
  }

  async function handleDeleteProjectChat() {
    const title = chatStore.currentChat.title;

    await chatApi.handleRequest(
      async () => {
        const chatId = chatStore.currentChat.id;
        if (chatId) {
          await deleteProjectChat(chatId);
        }
        chatStore.deleteChat(chatId);
      },
      {
        success: "Chat has been deleted: " + title,
        error: "Unable to delete chat: " + title,
      }
    );
  }

  async function handleSendChatMessage(
    chat: ProjectChatSchema,
    message: string
  ) {
    await chatDialogApi.handleRequest(async () => {
      const newMessage = buildProjectChatMessage({ message });

      if (!chat.id) {
        const chatCreated = await handleCreateProjectChat(chat.title); // sets chat with id in store.
        if (chatCreated) {
          chat = chatCreated;
        } else {
          return; //error occurred while saving chat.
        }
      }

      const messagesWithNewMessage = [...chat.messages, newMessage];
      chatStore.updateChat({
        ...chat,
        messages: messagesWithNewMessage,
      });

      const messagesCreated = await createProjectChatMessage(
        chat.id,
        newMessage
      );

      chat.messages = [
        ...chat.messages, // Chat object not mutated, so the user message is not in this list
        messagesCreated.userMessage,
        messagesCreated.responseMessage,
      ];
      chatStore.updateChat(chat);

      if (chat.messages.length == 2) {
        const chatWithTitle = await generateChatTitle(chat.id);
        chat = { ...chat, title: chatWithTitle.title };
        chatStore.updateChat(chat);
      }
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
