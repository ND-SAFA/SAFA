<template>
  <v-app-bar app color="primary">
    <generic-icon-button
      v-if="sidebarOpen"
      icon-id="mdi-chevron-left"
      tooltip="Close sidebar"
      @click="sidebarOpen = false"
      color="secondary"
    />
  </v-app-bar>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";
import { GenericIconButton } from "@/components/common";

/**
 * Renders the top navigation bar.
 */
export default Vue.extend({
  name: "AppNavBar",
  components: { GenericIconButton },
  computed: {
    /**
     * Manages changes to the panel open state.
     */
    sidebarOpen: {
      get(): boolean {
        return appStore.isAppPanelOpen;
      },
      set() {
        appStore.toggleAppPanel();
      },
    },
  },
});
</script>

<style scoped lang="scss"></style>
