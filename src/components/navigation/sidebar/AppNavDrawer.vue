<template>
  <q-drawer
    persistent
    :model-value="true"
    elevated
    breakpoint="0"
    :mini="!sidebarOpen"
  >
    <flex-box
      v-if="sidebarOpen"
      full-width
      justify="between"
      align="center"
      x="3"
      y="3"
    >
      <safa-icon style="width: 200px !important" />
      <icon-button
        icon="nav-toggle"
        tooltip="Close sidebar"
        :color="darkMode ? 'secondary' : 'primary'"
        data-cy="button-sidebar-close"
        @click="sidebarOpen = false"
      />
    </flex-box>
    <flex-box v-else justify="center" full-width t="2">
      <icon-button
        icon="nav-toggle"
        tooltip="Open sidebar"
        :color="darkMode ? 'secondary' : 'primary'"
        data-cy="button-sidebar-open"
        rotate="180"
        @click="sidebarOpen = true"
      />
    </flex-box>

    <nav-options />
    <nav-account />
  </q-drawer>
</template>

<script lang="ts">
/**
 * Renders the navigation drawer.
 */
export default {
  name: "AppNavDrawer",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { appStore, useTheme } from "@/hooks";
import { FlexBox, IconButton, SafaIcon } from "@/components/common";
import NavOptions from "./NavOptions.vue";
import NavAccount from "./NavAccount.vue";

const { darkMode } = useTheme();

const sidebarOpen = computed({
  get(): boolean {
    return appStore.isAppPanelOpen;
  },
  set() {
    appStore.toggleAppPanel();
  },
});
</script>
