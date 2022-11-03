<template>
  <v-navigation-drawer
    app
    permanent
    :mini-variant="!sidebarOpen"
    height="100%"
    class="elevation-1"
  >
    <flex-box v-if="sidebarOpen" full-width justify="center" t="3" b="3">
      <safa-icon variant="primary" style="width: 180px" />
      <generic-icon-button
        large
        icon-id="mdi-chevron-left"
        tooltip="Close sidebar"
        @click="sidebarOpen = false"
        color="primary"
      />
    </flex-box>
    <flex-box justify="center" full-width v-else t="2">
      <generic-icon-button
        large
        icon-id="mdi-chevron-right"
        tooltip="Open sidebar"
        @click="sidebarOpen = true"
        color="primary"
      />
    </flex-box>

    <nav-options />
    <nav-account />
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";
import { FlexBox, GenericIconButton, SafaIcon } from "@/components/common";
import NavOptions from "./NavOptions.vue";
import NavAccount from "./NavAccount.vue";

/**
 * Renders the navigation drawer.
 */
export default Vue.extend({
  name: "AppNavDrawer",
  components: {
    NavOptions,
    NavAccount,
    FlexBox,
    GenericIconButton,
    SafaIcon,
  },
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
