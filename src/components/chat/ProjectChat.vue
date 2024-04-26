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
        @click="chatStore.switchChat(chat)"
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
                  class="q-mr-md"
                />
              </div>
              <div class="full-width">
                <typography variant="subtitle" :value="message.userName" />
                <typography
                  variant="expandable"
                  :value="message.message"
                  default-expanded
                />
                <q-card flat bordered class="width-fit">
                  <expansion-item
                    v-if="message.artifactIds.length > 0"
                    :label="message.referenceLabel"
                    class="width-fit"
                  >
                    <artifact-list-display
                      :artifacts="message.artifacts"
                      @click="
                        (artifact) => selectionStore.selectArtifact(artifact.id)
                      "
                    />
                  </expansion-item>
                </q-card>
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
import { ArtifactSchema, IconVariant } from "@/types";
import {
  artifactStore,
  chatApiStore,
  chatStore,
  layoutStore,
  selectionStore,
  sessionStore,
} from "@/hooks";
import {
  IconButton,
  ListItem,
  Typography,
  Icon,
  FlexBox,
  ExpansionItem,
  TextButton,
} from "@/components/common";
import { ArtifactListDisplay } from "@/components/artifact";

const currentMessage = ref("");

const messages = computed(() => chatStore.currentMessages);

const formattedMessages = computed(() =>
  messages.value.map((message) => ({
    ...message,
    iconClass: message.isUser ? undefined : "bg-gradient",
    iconColor: message.isUser ? "primary" : undefined,
    iconVariant: (message.isUser ? "account" : "generate") as IconVariant,
    userName: message.isUser ? sessionStore.userEmail : "SAFA",
    referenceLabel:
      message.artifactIds.length === 1
        ? `1 Reference`
        : `${message.artifactIds.length} References`,
    artifacts: message.artifactIds
      .map(
        (artifactId) =>
          artifactStore.getArtifactById(artifactId) ||
          artifactStore.getArtifactByName(artifactId) // TODO: remove after mockup
      )
      .filter((artifact) => !!artifact) as ArtifactSchema[],
  }))
);

/**
 * Sends a chat message to the server.
 */
function handleSendMessage() {
  chatApiStore.handleSendChatMessage(currentMessage.value);
  currentMessage.value = "";
}

function handleCreateChat() {
  chatStore.currentChat = undefined;
}

/**
 * Emits an event when enter is clicked.
 */
function handleKeydown(e?: { key: string }) {
  if (e?.key === "Enter") {
    handleSendMessage();
  }
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
