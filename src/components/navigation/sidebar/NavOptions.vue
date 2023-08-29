<template>
  <list :items="options">
    <template v-for="item in options" :key="item.label">
      <separator v-if="item.divider" />
      <list-item
        :to="item.path"
        :data-cy="'button-nav-' + item.label"
        :icon="item.icon"
        :title="item.label"
        :icon-title="item.iconTitle"
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
import { appStore, projectStore } from "@/hooks";
import { QueryParams, Routes } from "@/router";
import { List, ListItem, Separator } from "@/components/common";

const sidebarOpen = computed(() => appStore.isAppPanelOpen);
const hideProjectOptions = computed(() => !projectStore.isProjectDefined);

const options = computed(() => {
  const query = {
    [QueryParams.VERSION]: projectStore.versionId,
  };

  const items: NavOption[] = [
    {
      label: "Create Project",
      iconTitle: !sidebarOpen.value ? "Create" : undefined,
      icon: "nav-create",
      path: Routes.PROJECT_CREATOR,
    },
    {
      label: "Open Project",
      iconTitle: !sidebarOpen.value ? "Projects" : undefined,
      icon: "nav-open",
      path: Routes.MY_PROJECTS,
    },
    {
      label: "Project View",
      iconTitle: !sidebarOpen.value ? "View" : undefined,
      icon: "nav-artifact",
      disabled: hideProjectOptions.value,
      divider: true,
      path: { path: Routes.ARTIFACT, query },
    },
    {
      label: "Settings",
      iconTitle: !sidebarOpen.value ? "Settings" : undefined,
      icon: "nav-settings",
      disabled: hideProjectOptions.value,
      path: { path: Routes.PROJECT_SETTINGS, query },
    },
  ];

  return items.filter(({ disabled }) => !disabled);
});
</script>
