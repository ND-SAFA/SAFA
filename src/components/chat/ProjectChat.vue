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
import { layoutStore } from "@/hooks";
import ProjectChatMessages from "./ProjectChatMessages.vue";
import ProjectChatList from "./ProjectChatList.vue";
</script>
