<template>
  <v-list>
    <v-list-item-group :value="selectedOption" active-class="nav-selected">
      <template v-for="option in options">
        <v-divider v-if="option.divider" :key="option.label + '-div'" />
        <v-list-item link :key="option.label" @click="option.onClick()">
          <v-list-item-icon>
            <v-icon>{{ option.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            <typography bold :value="option.label" />
          </v-list-item-title>
        </v-list-item>
      </template>
    </v-list-item-group>
  </v-list>
</template>

<script lang="ts">
import Vue from "vue";
import { NavOption } from "@/types";
import { appStore } from "@/hooks";
import { navigateTo, router, Routes } from "@/router";
import { Typography } from "@/components/common";

/**
 * Renders the navigation drawer.
 */
export default Vue.extend({
  name: "AppNavDrawerOptions",
  components: { Typography },
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
    /**
     * @return The index of the nav option representing the current page.
     */
    selectedOption(): number {
      const path = router.currentRoute.path;

      return this.options.findIndex((option) => option.path === path);
    },
  },
});
</script>

<style scoped lang="scss"></style>
