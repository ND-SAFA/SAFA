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
      if (!chat.id) {
        const chatCreated = await handleCreateProjectChat(chat.title); // sets chat with id in store.
        if (chatCreated) {
          chat = chatCreated;
        } else {
          return; //error occurred while saving chat.
        }
      }

      const { messages: priorMessages, id } = chat;
      const newMessage = buildProjectChatMessage({ message });

      chatStore.updateChat({
        id,
        messages: [...priorMessages, newMessage],
      });

      const messagesCreated = await createProjectChatMessage(id, newMessage);

      chatStore.updateChat({
        id,
        messages: [
          ...priorMessages,
          messagesCreated.userMessage,
          messagesCreated.responseMessage,
        ],
      });

      if (chat.messages.length == 2) {
        const { title } = await generateChatTitle(id);

        chatStore.updateChat({ id, title });
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
