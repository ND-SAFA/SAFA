<template>
  <flex-box>
    <search-mode-input />
    <search-prompt-input />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays a searchbar for generating searches
 * to trace to related artifacts within a project.
 */
export default {
  name: "ProjectSearchbar",
};
</script>

<script setup lang="ts">
import { FlexBox } from "@/components/common";
import SearchModeInput from "./SearchModeInput.vue";
import SearchPromptInput from "./SearchPromptInput.vue";
</script>
