<template>
  <v-list>
    <v-list-item-group active-class="nav-selected">
      <template v-for="option in options">
        <v-divider v-if="option.divider" :key="option.label + '-div'" />
        <v-list-item
          :key="option.label"
          :to="option.path"
          :data-cy="'button-nav-' + option.label"
        >
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
import { appStore, projectStore, sessionStore } from "@/hooks";
import { QueryParams, Routes } from "@/router";
import { Typography } from "@/components/common";

/**
 * Renders the navigation drawer.
 */
export default Vue.extend({
  name: "NavOptions",
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
      return !projectStore.isProjectDefined;
    },
    /**
     * @return The navigation bar options.
     */
    options(): NavOption[] {
      const query = {
        [QueryParams.VERSION]: projectStore.versionId,
      };

      const items: NavOption[] = [
        {
          label: "Home",
          icon: "mdi-home",
          path: Routes.HOME,
        },
        {
          label: "Create Project",
          icon: "mdi-folder-plus",
          path: Routes.PROJECT_CREATOR,
        },
        {
          label: "Open Project",
          icon: "mdi-list-box",
          path: Routes.MY_PROJECTS,
        },
        {
          label: "Project Uploads",
          icon: "mdi-folder-upload",
          path: Routes.UPLOAD_STATUS,
        },
        {
          label: "Artifact View",
          icon: "mdi-family-tree",
          disabled: this.hideProjectOptions,
          divider: true,
          path: { path: Routes.ARTIFACT, query },
        },
        {
          label: "Trace Prediction",
          icon: "mdi-link-box",
          disabled:
            this.hideProjectOptions ||
            !sessionStore.isEditor(projectStore.project),
          path: { path: Routes.TRACE_LINK, query },
        },
        {
          label: "Settings",
          icon: "mdi-cog-box",
          disabled: this.hideProjectOptions,
          path: { path: Routes.PROJECT_SETTINGS, query },
        },
      ];

      return items.filter(({ disabled }) => !disabled);
    },
  },
});
</script>

<style scoped lang="scss"></style>
