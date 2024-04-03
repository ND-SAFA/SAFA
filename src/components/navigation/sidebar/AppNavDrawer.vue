<template>
  <q-drawer
    :breakpoint="0"
    :mini="!sidebarOpen"
    :mini-width="65"
    :width="260"
    model-value
    persistent
    bordered
  >
    <flex-box
      v-if="sidebarOpen"
      align="center"
      class="nav-sidebar-header-open"
      full-width
      justify="between"
      y="2"
    >
      <safa-icon :hidden="!sidebarOpen" clickable @click="handleLogoClick" />
      <icon-button
        color="primary"
        data-cy="button-sidebar-close"
        icon="nav-toggle"
        tooltip="Close sidebar"
        @click="sidebarOpen = false"
      />
    </flex-box>
    <flex-box
      v-else
      align="center"
      class="nav-sidebar-header"
      full-width
      justify="center"
      y="3"
    >
      <icon-button
        data-cy="button-sidebar-open"
        icon="safa"
        tooltip="Open sidebar"
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

<script lang="ts" setup>
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
