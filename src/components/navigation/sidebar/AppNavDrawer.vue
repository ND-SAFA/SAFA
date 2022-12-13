<template>
  <v-navigation-drawer
    app
    permanent
    :mini-variant="!sidebarOpen"
    height="100%"
    class="elevation-1"
  >
    <flex-box v-if="sidebarOpen" full-width justify="center" t="3" b="3">
      <safa-icon style="width: 180px" />
      <icon-button
        large
        icon-id="mdi-menu-open"
        tooltip="Close sidebar"
        :color="$vuetify.theme.dark ? 'secondary' : 'primary'"
        data-cy="button-sidebar-close"
        @click="sidebarOpen = false"
      />
    </flex-box>
    <flex-box justify="center" full-width v-else t="2">
      <icon-button
        large
        icon-id="mdi-menu-open"
        tooltip="Open sidebar"
        @click="sidebarOpen = true"
        color="primary"
        data-cy="button-sidebar-open"
        icon-style="transform: rotate(180deg)"
      />
    </flex-box>

    <nav-options />
    <nav-account />
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from "vue";
import { appStore } from "@/hooks";
import { FlexBox, IconButton, SafaIcon } from "@/components/common";
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
    IconButton,
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
