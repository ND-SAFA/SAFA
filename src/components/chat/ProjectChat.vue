<template>
  <div v-if="layoutStore.isChatMode">hi</div>
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
import { layoutStore } from "@/hooks";
</script>
