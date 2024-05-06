<template>
  <q-layout
    v-if="layoutStore.isChatMode"
    container
    view="lHh Lpr lff"
    style="min-height: inherit"
    class="bg-background"
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

<script setup lang="ts">
import { onMounted } from "vue";
import { chatApiStore, layoutStore } from "@/hooks";
import ProjectChatMessages from "./ProjectChatMessages.vue";
import ProjectChatList from "./ProjectChatList.vue";

/**
 * Fetches the project chats when opened.
 */
onMounted(() => {
  chatApiStore.handleGetProjectChats();
});
</script>
