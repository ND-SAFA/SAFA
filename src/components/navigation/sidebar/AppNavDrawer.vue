<template>
  <q-drawer show-if-above :mini="!sidebarOpen">
    <flex-box
      v-if="sidebarOpen"
      full-width
      justify="center"
      align="center"
      t="3"
      b="3"
    >
      <safa-icon style="width: 180px !important" />
      <icon-button
        large
        icon-variant="nav-toggle"
        tooltip="Close sidebar"
        :color="darkMode ? 'secondary' : 'primary'"
        data-cy="button-sidebar-close"
        @click="sidebarOpen = false"
      />
    </flex-box>
    <flex-box v-else justify="center" full-width t="2">
      <icon-button
        large
        icon-variant="nav-toggle"
        tooltip="Open sidebar"
        color="primary"
        data-cy="button-sidebar-open"
        rotate="180"
        @click="sidebarOpen = true"
      />
    </flex-box>

    <q-scroll-area class="fit">
      <nav-options />
      <nav-account />
    </q-scroll-area>
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
