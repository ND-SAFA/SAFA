<template>
  <v-navigation-drawer
    app
    permanent
    :mini-variant="!sidebarOpen"
    height="100%"
    class="elevation-1"
  >
    <flex-box full-width justify="center" y="2" v-if="sidebarOpen">
      <safa-icon variant="primary" style="width: 230px" />
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

    <app-nav-drawer-options />
    <app-nav-drawer-account />
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from "vue";
import { NavOption } from "@/types";
import { appStore } from "@/hooks";
import { navigateTo, router, Routes } from "@/router";
import { handleLogout } from "@/api";
import { FlexBox, GenericIconButton, SafaIcon } from "@/components/common";
import AppNavDrawerOptions from "./AppNavDrawerOptions.vue";
import AppNavDrawerAccount from "./AppNavDrawerAccount.vue";

/**
 * Renders the navigation drawer.
 */
export default Vue.extend({
  name: "AppNavDrawer",
  components: {
    AppNavDrawerAccount,
    AppNavDrawerOptions,
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
    /**
     * @return Whether to hide project-specific nav options.
     */
    hideProjectOptions(): boolean {
      return false;
    },
    /**
     * @return The navigation bar options.
     */
    options(): NavOption[] {
      const items = [
        {
          label: "Home",
          icon: "mdi-home",
          path: Routes.HOME,
          onClick: () => navigateTo(Routes.HOME),
        },
        {
          label: "Create Project",
          icon: "mdi-folder-plus",
          path: Routes.PROJECT_CREATOR,
          onClick: () => navigateTo(Routes.PROJECT_CREATOR),
        },
        {
          label: "My Projects",
          icon: "mdi-list-box",
          path: Routes.MY_PROJECTS,
          onClick: () => navigateTo(Routes.MY_PROJECTS),
        },
        {
          label: "My Uploads",
          icon: "mdi-folder-upload",
          path: Routes.UPLOAD_STATUS,
          onClick: () => navigateTo(Routes.UPLOAD_STATUS),
        },
        {
          label: "Artifact View",
          icon: "mdi-family-tree",
          disabled: this.hideProjectOptions,
          divider: true,
          path: Routes.ARTIFACT,
          onClick: () => navigateTo(Routes.ARTIFACT),
        },
        {
          label: "Trace Models",
          icon: "mdi-link-box",
          disabled: this.hideProjectOptions,
          path: Routes.PROJECT_MODELS,
          onClick: () => navigateTo(Routes.PROJECT_MODELS),
        },
        {
          label: "Trace Approval",
          icon: "mdi-link-plus",
          disabled: this.hideProjectOptions,
          path: Routes.TRACE_LINK,
          onClick: () => navigateTo(Routes.TRACE_LINK),
        },
        {
          label: "Settings",
          icon: "mdi-cog-box",
          disabled: this.hideProjectOptions,
          path: Routes.PROJECT_SETTINGS,
          onClick: () => navigateTo(Routes.PROJECT_SETTINGS),
        },
      ];

      return items.filter(({ disabled }) => !disabled);
    },
    selectedOption(): number {
      const path = router.currentRoute.path;

      return this.options.findIndex((option) => option.path === path);
    },
  },
  methods: {
    /**
     * Routes the user to the feedback page.
     */
    handleFeedback(): void {
      window.open(
        "https://www.notion.so/nd-safa/b73d1a8bfe0345f8b4d72daa1ceaf934?v=6e5d2439907a428fa1db2671a5eaa0b6"
      );
    },
    /**
     * Routes the user to the walkthrough page.
     */
    handleWalkthrough(): void {
      window.open(
        "https://www.notion.so/nd-safa/8dc14ae706074b099928afe13df39448?v=5b5e744919f84178bac1c96f5a5a92ba"
      );
    },
    /**
     * Routes the user to the walkthrough page.
     */
    handleChangelog(): void {
      window.open(
        "https://www.notion.so/nd-safa/5155dc357f534eb49f8071a03ce3ae32?v=74f671825a1b4d048909843740c003f1"
      );
    },
    /**
     * Logs the user out.
     */
    handleLogout(): void {
      handleLogout();
    },
    /**
     * Navigates to the account editing page.
     */
    handleEditAccount(): void {
      navigateTo(Routes.ACCOUNT);
    },
  },
});
</script>

<style scoped lang="scss"></style>
