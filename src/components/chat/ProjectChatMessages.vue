<template>
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
        class="overflow-auto q-pa-md chat-wrapper chat-messages"
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
            <div class="q-pa-md bg-neutral rounded overflow-auto">
              <typography variant="subtitle" :value="message.userName" />
              <typography variant="markdown" :value="message.message" />
              <flex-box v-if="message.artifacts.length > 0" wrap>
                <artifact-chip
                  v-for="relatedArtifact in message.artifacts"
                  :key="relatedArtifact.id"
                  :artifact="relatedArtifact"
                />
              </flex-box>
            </div>
          </flex-box>
        </list-item>

        <div :id="scrollId" />
      </div>

      <div class="full-width q-px-md chat-wrapper chat-input">
        <q-input
          v-model="currentMessage"
          outlined
          :loading="chatApiStore.loading || chatApiStore.loadingResponse"
          :disable="chatApiStore.loading || chatApiStore.loadingResponse"
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
</template>

<script lang="ts">
/**
 * Displays chat messages between a member and SAFA AI.
 */
export default {
  name: "ProjectChatMessages",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { chatApiStore, chatStore } from "@/hooks";
import {
  IconButton,
  ListItem,
  Typography,
  Icon,
  FlexBox,
  PopupEditInput,
} from "@/components/common";
import { ArtifactChip } from "@/components/artifact";

const scrollId = "chat-bottom";

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
 * Scrolls to the bottom of the chat when a new message is added.
 */
watch(
  () => messages.value,
  () => {
    setTimeout(() => {
      document.getElementById(scrollId)?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  }
);
</script>
