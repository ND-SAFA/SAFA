<template>
  <list :items="options">
    <template #item="{ item }">
      <separator v-if="item.divider" />
      <list-item
        :to="item.path"
        color="primary"
        :data-cy="'button-nav-' + item.label"
        :icon="item.icon"
        :title="item.label"
      />
    </template>
  </list>
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
import { List, ListItem, Separator } from "@/components/common";

const hideProjectOptions = computed(() => !projectStore.isProjectDefined);

const options = computed(() => {
  const query = {
    [QueryParams.VERSION]: projectStore.versionId,
  };

  const items: NavOption[] = [
    {
      label: "Home",
      icon: "nav-home",
      path: Routes.HOME,
    },
    {
      label: "Create Project",
      icon: "nav-create",
      path: Routes.PROJECT_CREATOR,
    },
    {
      label: "Open Project",
      icon: "nav-open",
      path: Routes.MY_PROJECTS,
    },
    {
      label: "Project Uploads",
      icon: "nav-uploads",
      path: Routes.UPLOAD_STATUS,
    },
    {
      label: "Artifact View",
      icon: "nav-artifact",
      disabled: hideProjectOptions.value,
      divider: true,
      path: { path: Routes.ARTIFACT, query },
    },
    {
      label: "Trace Prediction",
      icon: "nav-trace",
      disabled:
        hideProjectOptions.value ||
        !sessionStore.isEditor(projectStore.project),
      path: { path: Routes.TRACE_LINK, query },
    },
    {
      label: "Settings",
      icon: "nav-settings",
      disabled: hideProjectOptions.value,
      path: { path: Routes.PROJECT_SETTINGS, query },
    },
  ];

  return items.filter(({ disabled }) => !disabled);
});
</script>
