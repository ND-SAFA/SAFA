<template>
  <q-drawer
    persistent
    model-value
    elevated
    :breakpoint="0"
    :width="260"
    :mini="!sidebarOpen"
  >
    <flex-box
      v-if="sidebarOpen"
      full-width
      justify="between"
      align="center"
      y="2"
      class="nav-sidebar-header-open"
    >
      <safa-icon clickable :hidden="!sidebarOpen" @click="handleLogoClick" />
      <icon-button
        icon="nav-toggle"
        tooltip="Close sidebar"
        color="primary"
        data-cy="button-sidebar-close"
        @click="sidebarOpen = false"
      />
    </flex-box>
    <flex-box
      v-else
      justify="center"
      align="center"
      full-width
      y="3"
      class="nav-sidebar-header"
    >
      <icon-button
        icon="nav-toggle"
        tooltip="Open sidebar"
        color="primary"
        data-cy="button-sidebar-open"
        :rotate="180"
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
import { computed, onMounted } from "vue";
import { appStore, useScreen } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import { FlexBox, IconButton, SafaIcon } from "@/components/common";
import NavOptions from "./NavOptions.vue";
import NavAccount from "./NavAccount.vue";

const { smallWindow } = useScreen();

const sidebarOpen = computed({
  get(): boolean {
    return appStore.isAppPanelOpen;
  },
  set() {
    appStore.toggleAppPanel();
  },
});

/**
 * Navigates to the home page when the logo is clicked.
 */
function handleLogoClick(): void {
  navigateTo(Routes.HOME);
}

onMounted(() => {
  if (!smallWindow) return;

  appStore.toggleAppPanel();
});
</script>
