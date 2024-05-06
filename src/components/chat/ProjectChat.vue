<template>
  <q-layout
    v-if="layoutStore.isChatMode"
    container
    view="lHh Lpr lff"
    style="min-height: inherit"
    class="bg-background"
  >
    <q-drawer
      model-value
      persistent
      bordered
      :breakpoint="0"
      :width="260"
      class="bg-background"
    >
      <flex-box
        full-width
        justify="between"
        align="center"
        t="1"
        class="q-pa-sm"
      >
        <typography variant="subtitle" value="Chats" />
        <text-button
          text
          label="Create"
          icon="add"
          data-cy="button-add-attribute"
          @click="handleCreateChat"
        />
      </flex-box>
      <list-item
        v-for="chat in chatStore.chats"
        :key="chat.id"
        :title="chat.title"
        clickable
        :focused="chatStore.currentChat?.id === chat.id"
        :action-cols="1"
        @click="handleSwitchChat(chat)"
      >
        <template #actions>
          <icon-button
            small
            icon="delete"
            tooltip="Delete chat"
            @click="chatApiStore.handleDeleteProjectChat(chat.id)"
          />
        </template>
      </list-item>
    </q-drawer>
    <q-page-container>
      <q-page>
        <popup-edit-input
          :value="chatStore.currentChat.title"
          :editing="editing"
          @close="editing = false"
          @open="editing = true"
          @save="handleSaveEdit"
        >
          <typography
            variant="subtitle"
            :value="chatStore.currentChat.title"
            el="h2"
            class="q-py-sm q-pl-md"
          />
        </popup-edit-input>

        <div
          v-if="!chatApiStore.loading"
          style="max-width: 60vw; max-height: 70vh"
          class="overflow-auto q-pa-md"
        >
          <list-item
            v-for="(message, idx) in formattedMessages"
            :id="`message-${idx}`"
            :key="message.id"
          >
            <flex-box b="1" full-width>
              <div :class="message.iconClass">
                <icon
                  :color="message.iconColor"
                  :variant="message.iconVariant"
                  size="md"
                  class="q-mr-md q-mt-md"
                />
              </div>
              <div class="q-pa-md bg-neutral rounded">
                <typography variant="subtitle" :value="message.userName" />
                <typography variant="markdown" :value="message.message" />
                <flex-box v-if="message.artifacts.length > 0">
                  <artifact-chip
                    v-for="relatedArtifact in message.artifacts"
                    :key="relatedArtifact.id"
                    :artifact="relatedArtifact"
                  />
                </flex-box>
              </div>
            </flex-box>
          </list-item>
        </div>
        <flex-box
          v-if="chatApiStore.loading || chatApiStore.loadingResponse"
          justify="center"
          t="4"
          style="height: 40px"
        >
          <q-circular-progress color="primary" indeterminate size="md" />
        </flex-box>
        <div
          style="max-width: 60vw; width: 100%; position: absolute; bottom: 20px"
          class="full-width q-px-md"
        >
          <q-input
            v-model="currentMessage"
            outlined
            :disable="chatApiStore.loading"
            placeholder="Ask a question"
            class="full-width bg-neutral"
            clearable
            @keydown="handleKeydown"
          >
            <template #append>
              <icon-button
                icon="forward"
                tooltip="Send message"
                @click="handleSendMessage"
              />
            </template>
          </q-input>
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
/**
 * Displays a project chat exchange between a member and SAFA AI.
 */
export default {
  name: "ProjectChat",
};
</script>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { ProjectChatSchema } from "@/types";
import { chatApiStore, chatStore, layoutStore } from "@/hooks";
import {
  IconButton,
  ListItem,
  Typography,
  Icon,
  FlexBox,
  TextButton,
} from "@/components/common";
import { ArtifactChip } from "@/components/artifact";
import PopupEditInput from "@/components/common/input/PopupEditInput.vue";

const currentMessage = ref("");
const editing = ref(false);

const messages = computed(() => chatStore.currentMessages);

const formattedMessages = computed(() => chatStore.currentMessagesDisplay);

/**
 * Sends a chat message to the server.
 */
function handleSendMessage() {
  chatApiStore.handleSendChatMessage(
    chatStore.currentChat,
    currentMessage.value
  );
  currentMessage.value = "";
}

function handleCreateChat() {
  chatStore.addChat();
}

/**
 * Switches chat and loads its messages afterwards.
 * @param chat The chat to switch to.
 */
function handleSwitchChat(chat: ProjectChatSchema) {
  chatStore.switchChat(chat);
  chatApiStore.handleLoadProjectChatMessages(chat.id);
}

/**
 * Emits an event when enter is clicked and sends the message associated with the specific chat.
 * @param e - The keyboard event.
 */
function handleKeydown(e: KeyboardEvent) {
  if (e.key === "Enter") {
    handleSendMessage();
    e.preventDefault(); // To prevent form submission or other default actions
  }
}

/**
 * Saves an edit to the chat title.
 * @param title - The new chat title.
 */
function handleSaveEdit(title: string) {
  chatApiStore.handleEditProjectChat(title);

  editing.value = false;
}

/**
 * Fetches the project chats when opened.
 */
onMounted(() => {
  chatApiStore.handleGetProjectChats();
});

/**
 * Scrolls to the bottom of the chat when a new message is added.
 */
watch(
  () => messages.value,
  () => {
    setTimeout(() => {
      const chat = document.getElementById(
        "message-" + (messages.value.length - 1)
      );
      if (chat) {
        chat.scrollIntoView({ behavior: "smooth" });
      }
    }, 100);
  }
);
</script>
