<template>
  <onboarding-callout />
  <list :items="options">
    <template v-for="item in options" :key="item.label">
      <separator v-if="item.divider" />
      <list-item
        :to="item.path"
        :data-cy="'button-nav-' + item.label"
        :icon="item.icon"
        :title="item.label"
        :icon-title="item.iconTitle"
        :color="item.color"
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
import { useRoute } from "vue-router";
import { NavOption } from "@/types";
import { appStore, projectStore } from "@/hooks";
import { QueryParams, Routes } from "@/router";
import { List, ListItem, Separator } from "@/components/common";
import { OnboardingCallout } from "@/components/onboarding";

const currentRoute = useRoute();

const sidebarOpen = computed(() => appStore.popups.navPanel);
const hideProjectOptions = computed(() => !projectStore.isProjectDefined);

const options = computed(() => {
  const query = {
    [QueryParams.VERSION]: projectStore.versionId,
  };

  const items: NavOption[] = [
    {
      label: "Create Project",
      iconTitle: !sidebarOpen.value ? "Create" : undefined,
      icon: "project-add",
      path: Routes.PROJECT_CREATOR,
      color: Routes.PROJECT_CREATOR === currentRoute.path ? "primary" : "text",
    },
    {
      label: "Open Project",
      iconTitle: !sidebarOpen.value ? "Projects" : undefined,
      icon: "nav-open",
      path: Routes.MY_PROJECTS,
      color: Routes.MY_PROJECTS === currentRoute.path ? "primary" : "text",
    },
    {
      label: "Project View",
      iconTitle: !sidebarOpen.value ? "View" : undefined,
      icon: "nav-artifact",
      disabled: hideProjectOptions.value,
      path: { path: Routes.ARTIFACT, query },
      color: Routes.ARTIFACT === currentRoute.path ? "primary" : "text",
    },
    {
      label: "Settings",
      iconTitle: !sidebarOpen.value ? "Settings" : undefined,
      icon: "nav-settings",
      disabled: hideProjectOptions.value,
      path: { path: Routes.PROJECT_SETTINGS, query },
      color: Routes.PROJECT_SETTINGS === currentRoute.path ? "primary" : "text",
    },
  ];

  return items.filter(({ disabled }) => !disabled);
});
</script>
