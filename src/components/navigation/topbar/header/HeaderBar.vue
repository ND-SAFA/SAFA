<template>
  <div class="full-width">
    <flex-box full-width justify="space-between">
      <flex-box align="center">
        <searchbar v-if="graphVisible" />
      </flex-box>
      <flex-box align="center">
        <update-button />
        <saving-icon />
        <app-version />
      </flex-box>
    </flex-box>
    <v-divider v-if="graphVisible" class="accent faded mt-2" />
    <loading-bar />
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
import { FlexBox } from "@/components/common";
import Searchbar from "./Searchbar.vue";
import AppVersion from "./AppVersion.vue";
import SavingIcon from "./SavingIcon.vue";
import UpdateButton from "./UpdateButton.vue";
import LoadingBar from "./LoadingBar.vue";

const currentRoute = useRoute();
const graphVisible = ref(currentRoute.path === Routes.ARTIFACT);

watch(
  () => currentRoute.path,
  () => (graphVisible.value = currentRoute.path === Routes.ARTIFACT)
);
</script>
