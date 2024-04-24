<template>
  <div
    v-if="layoutStore.isChatMode"
    class="q-pa-sm bg-background"
    style="min-height: inherit"
  >
    <div style="width: 60vw; position: absolute; top: 12px; left: 20%">
      <list-item v-for="message in messages" :key="message.id">
        <flex-box b="1" full-width>
          <div :class="message.userMessage ? undefined : 'bg-gradient'">
            <icon
              :color="message.userMessage ? 'primary' : undefined"
              :variant="message.userMessage ? 'account' : 'generate'"
              size="md"
              class="q-mr-md"
            />
          </div>
          <div class="full-width">
            <typography
              variant="subtitle"
              :value="message.userMessage ? 'Tim' : 'SAFA'"
            />
            <typography
              variant="expandable"
              :value="message.message"
              default-expanded
            />
            <flex-box>
              <q-chip
                v-for="artifactId in message.artifactIds"
                :key="artifactId"
                :label="artifactId"
                class="q-mr-xs"
                color="primary"
                clickable
                outline
                icon="mdi-clipboard-text"
              />
            </flex-box>
          </div>
        </flex-box>
      </list-item>
    </div>
    <div style="width: 60vw; position: absolute; bottom: 12px; left: 20%">
      <q-input
        v-model="currentMessage"
        outlined
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
import { ref } from "vue";
import { ProjectChatSchema } from "@/types";
import { layoutStore } from "@/hooks";
import {
  IconButton,
  ListItem,
  Typography,
  Icon,
  FlexBox,
} from "@/components/common";

const EXAMPLE_CHAT: ProjectChatSchema = {
  id: "1",
  title: "GLM Coverage",
  permission: "owner",
  messages: [
    {
      id: "1",
      userMessage: true,
      message: "How is the GLM coverage ensured?",
      artifactIds: [],
    },
    {
      id: "2",
      userMessage: false,
      message:
        "LIRD137 established the first coverage specification for the GLM.\n\n" +
        "A change request (CCR01543) was issued to update the level two requirement, MRD222.\n\n" +
        "MRD222 contains three children further refining the coverage requirements:\n" +
        "MRD1256, MRD1262, MRD1254.",
      artifactIds: [
        "LIRD137",
        "CCR1543",
        "MRD222",
        "MRD1256",
        "MRD1262",
        "MRD1264",
      ],
    },
  ],
};

const messages = ref(EXAMPLE_CHAT.messages);
const currentMessage = ref("");

function handleSendMessage() {
  // TODO
}

/**
 * Emits an event when enter is clicked.
 */
function handleKeydown(e?: { key: string }) {
  if (e?.key === "Enter") {
    handleSendMessage();
  }
}
</script>
