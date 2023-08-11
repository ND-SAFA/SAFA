<template>
  <list :items="options">
    <template v-for="item in options" :key="item.label">
      <separator v-if="item.divider" />
      <list-item
        :to="item.path"
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
import { projectStore } from "@/hooks";
import { QueryParams, Routes } from "@/router";
import { List, ListItem, Separator } from "@/components/common";

const hideProjectOptions = computed(() => !projectStore.isProjectDefined);

const options = computed(() => {
  const query = {
    [QueryParams.VERSION]: projectStore.versionId,
  };

  const items: NavOption[] = [
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
      label: "Project View",
      icon: "nav-artifact",
      disabled: hideProjectOptions.value,
      divider: true,
      path: { path: Routes.ARTIFACT, query },
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
