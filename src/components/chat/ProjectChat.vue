<template>
  <div
    v-if="layoutStore.isChatMode"
    class="q-pa-sm bg-background"
    style="min-height: inherit"
  >
    <div style="width: 60vw; position: absolute; top: 12px; left: 20%">
      <list-item
        icon="account"
        title="Tim"
        color="primary"
        subtitle="Tell me about my project"
      />
      <list-item
        icon="generate"
        title="SAFA"
        class="bg-gradient"
        subtitle="This project..."
      />
      <list-item
        icon="account"
        title="Tim"
        color="primary"
        subtitle="Oh cool, how does X work"
      />
      <list-item
        icon="generate"
        title="SAFA"
        class="bg-gradient"
        subtitle="X works by..."
      />
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
import { layoutStore } from "@/hooks";
import { PanelCard, IconButton } from "@/components/common";
import ListItem from "@/components/common/display/list/ListItem.vue";

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
