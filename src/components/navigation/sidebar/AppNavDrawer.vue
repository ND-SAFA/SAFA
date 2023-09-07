<template>
  <q-drawer
    persistent
    model-value
    elevated
    :breakpoint="0"
    :width="260"
    :mini-width="65"
    :mini="!sidebarOpen"
  >
    <flex-box
      v-show="sidebarOpen"
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
      v-show="!sidebarOpen"
      justify="center"
      align="center"
      full-width
      y="3"
      class="nav-sidebar-header"
    >
      <icon-button
        icon="safa"
        tooltip="Open sidebar"
        color="primary"
        data-cy="button-sidebar-open"
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
    return appStore.popups.navPanel;
  },
  set() {
    appStore.toggle("navPanel");
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

  appStore.close("navPanel");
});
</script>
