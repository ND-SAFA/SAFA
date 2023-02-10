<template>
  <v-navigation-drawer
    permanent
    :rail="!sidebarOpen"
    height="100%"
    elevation="1"
  >
    <flex-box
      v-if="sidebarOpen"
      full-width
      justify="center"
      align="center"
      t="3"
      b="3"
    >
      <safa-icon style="width: 180px" />
      <icon-button
        large
        icon-id="mdi-menu-open"
        tooltip="Close sidebar"
        :color="darkMode ? 'secondary' : 'primary'"
        data-cy="button-sidebar-close"
        @click="sidebarOpen = false"
      />
    </flex-box>
    <flex-box v-else justify="center" full-width t="2">
      <icon-button
        large
        icon-id="mdi-menu-open"
        tooltip="Open sidebar"
        color="primary"
        data-cy="button-sidebar-open"
        icon-style="transform: rotate(180deg)"
        @click="sidebarOpen = true"
      />
    </flex-box>

    <nav-options />
    <nav-account />
  </v-navigation-drawer>
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
import { useTheme } from "vuetify";
import { appStore } from "@/hooks";
import { FlexBox, IconButton, SafaIcon } from "@/components/common";
import NavOptions from "./NavOptions.vue";
import NavAccount from "./NavAccount.vue";

const theme = useTheme();
const darkMode = computed(() => theme.global.current.value.dark);

const sidebarOpen = computed({
  get(): boolean {
    return appStore.isAppPanelOpen;
  },
  set() {
    appStore.toggleAppPanel();
  },
});
</script>
