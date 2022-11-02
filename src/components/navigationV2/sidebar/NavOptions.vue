<template>
  <v-list>
    <v-list-item-group active-class="nav-selected">
      <template v-for="option in options">
        <v-divider v-if="option.divider" :key="option.label + '-div'" />
        <v-list-item link :key="option.label" :to="option.path">
          <v-list-item-icon>
            <v-icon>{{ option.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            <typography bold :value="option.label" />
          </v-list-item-title>
        </v-list-item>
        <v-list dense v-if="option.subOptions" :key="option.label + '-options'">
          <v-list-item
            link
            v-for="subOption in option.subOptions"
            :key="subOption.label"
            @click="subOption.onClick"
            class="ml-4"
          >
            <v-list-item-icon>
              <v-icon>{{ subOption.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              <typography :value="subOption.label" />
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </template>
    </v-list-item-group>
  </v-list>
</template>

<script lang="ts">
import Vue from "vue";
import { NavOption } from "@/types";
import { appStore, projectStore } from "@/hooks";
import { Routes } from "@/router";
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
          label: "My Projects",
          icon: "mdi-list-box",
          path: Routes.MY_PROJECTS,
        },
        {
          label: "My Uploads",
          icon: "mdi-folder-upload",
          path: Routes.UPLOAD_STATUS,
        },
        {
          label: "Artifact View",
          icon: "mdi-family-tree",
          disabled: this.hideProjectOptions,
          divider: true,
          path: Routes.ARTIFACT,
          // subOptions: [
          //   {
          //     label: "Table View",
          //     icon: "mdi-table-multiple",
          //     onClick: () => undefined,
          //   },
          //   {
          //     label: "Delta View",
          //     icon: "mdi-file-compare",
          //     onClick: () => undefined,
          //   },
          // ],
        },
        {
          label: "Trace Models",
          icon: "mdi-link-box",
          disabled: this.hideProjectOptions,
          path: Routes.PROJECT_MODELS,
        },
        {
          label: "Trace Approval",
          icon: "mdi-link-plus",
          disabled: this.hideProjectOptions,
          path: Routes.TRACE_LINK,
        },
        {
          label: "Settings",
          icon: "mdi-cog-box",
          disabled: this.hideProjectOptions,
          path: Routes.PROJECT_SETTINGS,
        },
      ];

      return items.filter(({ disabled }) => !disabled);
    },
  },
});
</script>

<style scoped lang="scss"></style>
