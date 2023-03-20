<template>
  <q-drawer
    persistent
    model-value
    elevated
    :breakpoint="0"
    :width="260"
    :mini="!sidebarOpen"
    :style="style"
  >
    <flex-box
      v-if="sidebarOpen"
      full-width
      justify="between"
      align="center"
      y="3"
      class="nav-sidebar-header-open"
    >
      <safa-icon />
      <icon-button
        icon="nav-toggle"
        tooltip="Close sidebar"
        :color="darkMode ? 'secondary' : 'primary'"
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
import { computed, onMounted } from "vue";
import { ThemeColors } from "@/util";
import { appStore, useScreen, useTheme } from "@/hooks";
import { FlexBox, IconButton, SafaIcon } from "@/components/common";
import NavOptions from "./NavOptions.vue";
import NavAccount from "./NavAccount.vue";

const { darkMode } = useTheme();
const { smallWindow } = useScreen();

const style = computed(() =>
  darkMode.value ? `background-color: ${ThemeColors.darkGrey}` : ""
);

const sidebarOpen = computed({
  get(): boolean {
    return appStore.isAppPanelOpen;
  },
  set() {
    appStore.toggleAppPanel();
  },
});

onMounted(() => {
  if (!smallWindow) return;

  appStore.toggleAppPanel();
});
</script>
