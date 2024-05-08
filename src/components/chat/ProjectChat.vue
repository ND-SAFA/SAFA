<template>
  <q-layout
    v-if="layoutStore.isChatMode"
    class="bg-background"
    container
    style="min-height: inherit"
    view="lHh Lpr lff"
  >
    <project-chat-list />
    <project-chat-messages />
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

<script lang="ts" setup>
import { watch } from "vue";
import { chatApiStore, layoutStore, projectStore } from "@/hooks";
import ProjectChatMessages from "./ProjectChatMessages.vue";
import ProjectChatList from "./ProjectChatList.vue";

// Watch the projectId for changes.
watch(
  () => projectStore.projectId,
  (newProjectId) => {
    if (newProjectId !== "") {
      chatApiStore.handleGetProjectChats();
    }
  },
  {
    immediate: true, // This option triggers the handler immediately with the current value on mount.
  }
);
</script>
