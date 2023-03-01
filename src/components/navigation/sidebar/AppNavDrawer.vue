<template>
  <q-drawer
    persistent
    model-value
    elevated
    breakpoint="0"
    width="280"
    :mini="!sidebarOpen"
  >
    <flex-box
      v-if="sidebarOpen"
      full-width
      justify="between"
      align="center"
      x="3"
      y="3"
      style="height: 40px; padding-left: 5px; padding-right: 5px"
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
    <flex-box
      v-else
      justify="center"
      align="center"
      full-width
      y="3"
      style="height: 40px"
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
import { useQuasar } from "quasar";
import { appStore, useTheme } from "@/hooks";
import { FlexBox, IconButton, SafaIcon } from "@/components/common";
import NavOptions from "./NavOptions.vue";
import NavAccount from "./NavAccount.vue";

const { darkMode } = useTheme();
const $q = useQuasar();

const sidebarOpen = computed({
  get(): boolean {
    return appStore.isAppPanelOpen;
  },
  set() {
    appStore.toggleAppPanel();
  },
});

onMounted(() => {
  if ($q.screen.lt.md) {
    appStore.toggleAppPanel();
  }
});
</script>
