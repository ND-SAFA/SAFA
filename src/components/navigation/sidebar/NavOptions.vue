<template>
  <v-list>
    <v-item-group selected-class="nav-selected">
      <template v-for="option in options" :key="option.label">
        <v-divider v-if="option.divider" />
        <v-list-item :to="option.path" :data-cy="'button-nav-' + option.label">
          <template #prepend>
            <v-icon :icon="option.icon" />
          </template>
          <v-list-item-title class="ml-4">
            <typography bold :value="option.label" />
          </v-list-item-title>
        </v-list-item>
      </template>
    </v-item-group>
  </v-list>
</template>

<script lang="ts">
/**
 * Renders the navigation drawer.
 */
export default {
  name: "NavOptions",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { NavOption } from "@/types";
import { projectStore, sessionStore } from "@/hooks";
import { QueryParams, Routes } from "@/router";
import { Typography } from "@/components/common";

const hideProjectOptions = computed(() => !projectStore.isProjectDefined);

const options = computed(() => {
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
      disabled: hideProjectOptions.value,
      divider: true,
      path: { path: Routes.ARTIFACT, query },
    },
    {
      label: "Trace Prediction",
      icon: "mdi-link-box",
      disabled:
        hideProjectOptions.value ||
        !sessionStore.isEditor(projectStore.project),
      path: { path: Routes.TRACE_LINK, query },
    },
    {
      label: "Settings",
      icon: "mdi-cog-box",
      disabled: hideProjectOptions.value,
      path: { path: Routes.PROJECT_SETTINGS, query },
    },
  ];

  return items.filter(({ disabled }) => !disabled);
});
</script>
