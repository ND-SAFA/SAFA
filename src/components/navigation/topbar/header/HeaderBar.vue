<template>
  <div class="full-width">
    <flex-box full-width :wrap="false" justify="between" align="center">
      <project-searchbar v-if="graphVisible" />
      <q-space />
      <flex-box align="center">
        <update-button />
        <saving-icon />
        <version-selector />
      </flex-box>
    </flex-box>
    <separator v-if="graphVisible" nav />
  </div>
</template>

<script lang="ts">
/**
 * Renders the top navigation bar header.
 */
export default {
  name: "HeaderBar",
};
</script>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { Routes } from "@/router";
import { FlexBox, Separator } from "@/components/common";
import { VersionSelector } from "@/components/project";
import ProjectSearchbar from "./ProjectSearchbar.vue";
import SavingIcon from "./SavingIcon.vue";
import UpdateButton from "./UpdateButton.vue";

const currentRoute = useRoute();
const graphVisible = ref(currentRoute.path === Routes.ARTIFACT);

watch(
  () => currentRoute.path,
  () => (graphVisible.value = currentRoute.path === Routes.ARTIFACT)
);
</script>
