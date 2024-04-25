<template>
  <div
    v-if="layoutStore.isChatMode"
    class="q-pa-sm bg-background"
    style="min-height: inherit"
  >
    <div
      style="
        width: 50vw;
        position: absolute;
        top: 12px;
        left: 25%;
        max-height: 70vh;
      "
      class="overflow-auto"
    >
      <div v-if="!chatApiStore.loading">
        <list-item v-for="message in formattedMessages" :key="message.id">
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
              <expansion-item
                v-if="message.artifactIds.length > 0"
                :label="message.referenceLabel"
              >
                <artifact-list-display
                  :artifacts="message.artifacts"
                  @click="
                    (artifact) => selectionStore.selectArtifact(artifact.id)
                  "
                />
              </expansion-item>
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
    </div>
    <div style="width: 50vw; position: absolute; bottom: 12px; left: 25%">
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
  </div>
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
import { computed, onMounted, ref } from "vue";
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
} from "@/components/common";
import { ArtifactListDisplay } from "@/components/artifact";

const currentMessage = ref("");

const messages = computed(() => chatStore.currentMessages);

const formattedMessages = computed(() =>
  messages.value.map((message) => ({
    ...message,
    iconClass: message.userMessage ? undefined : "bg-gradient",
    iconColor: message.userMessage ? "primary" : undefined,
    iconVariant: (message.userMessage ? "account" : "generate") as IconVariant,
    userName: message.userMessage ? sessionStore.userEmail : "SAFA",
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
</script>
