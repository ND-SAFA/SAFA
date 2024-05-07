import { defineStore } from "pinia";

import { computed } from "vue";
import { ChatApiHook, ChatMessageSchema, ProjectChatSchema } from "@/types";
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
      const newMessage: ChatMessageSchema = {
        id: "",
        isUser: true,
        message,
        artifactIds: [],
      };

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

      const messagesWithNewMessage = [...chat.messages, newMessage];
      chatStore.updateChat({
        ...chat,
        messages: messagesWithNewMessage,
      });

      const messagesCreated = await createProjectChatMessage(
        chat.id,
        newMessage
      );

      const chatMessages = [
        ...messagesWithNewMessage.slice(0, -1), // everything but last user message
        messagesCreated.userMessage,
        messagesCreated.responseMessage,
      ];

      console.log("New Messages:", chatMessages);
      chat = { ...chat, messages: chatMessages };
      chatStore.updateChat(chat);

      if (chatMessages.length == 2) {
        // if first chat response then generate title
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
