<template>
  <q-breadcrumbs gutter="xs" class="nav-breadcrumb-list" separator-color="grey">
    <q-breadcrumbs-el v-if="displayOrgOptions">
      <organization-selector />
    </q-breadcrumbs-el>

    <q-breadcrumbs-el v-if="!displayOrgOptions">
      <project-selector />
    </q-breadcrumbs-el>
    <q-breadcrumbs-el v-if="displayProjectOptions">
      <version-selector />
    </q-breadcrumbs-el>
    <q-breadcrumbs-el v-if="displayProjectOptions">
      <view-selector />
    </q-breadcrumbs-el>

    <q-breadcrumbs-el v-if="displayPageTitle">
      <flex-box align="center">
        <typography
          variant="subtitle"
          el="h1"
          :value="pageTitle"
          x="2"
          color="text"
        />
        <icon-button
          v-if="pageDescription"
          :tooltip="pageDescription"
          icon="info"
          color="grey"
          small
        />
      </flex-box>
    </q-breadcrumbs-el>
  </q-breadcrumbs>
  <icon-button
    v-if="displayMore"
    tooltip="Toggle more options"
    class="q-mx-sm"
    color="text"
    :icon="collapsed ? 'down' : 'up'"
    @click="collapsed = !collapsed"
  />
</template>

<script lang="ts">
/**
 * Displays breadcrumbs for navigating between the current org, team, project, and version.
 */
export default {
  name: "NavBreadcrumbs",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute } from "vue-router";
import { projectStore, useScreen } from "@/hooks";
import { Routes } from "@/router";
import { ProjectSelector, VersionSelector } from "@/components/project";
import { ViewSelector } from "@/components/view";
import { IconButton, Typography } from "@/components/common";
import { OrganizationSelector } from "@/components/organization";
import FlexBox from "@/components/common/display/content/FlexBox.vue";

const { smallWindow } = useScreen();
const currentRoute = useRoute();

const collapsed = ref(true);

const displayMore = computed(
  () => smallWindow.value && currentRoute.path === Routes.ARTIFACT
);

const displayOptions = computed(() => !smallWindow.value || !collapsed.value);

const displayOrgOptions = computed(
  () => currentRoute.path === Routes.ORG || currentRoute.path === Routes.TEAM
);

const displayProjectOptions = computed(
  () =>
    displayOptions.value &&
    projectStore.isProjectDefined &&
    currentRoute.path === Routes.ARTIFACT
);

const pageTitle = computed(() =>
  currentRoute.name ? String(currentRoute.name) : undefined
);
const pageDescription = computed(
  () => currentRoute.meta.description as string | undefined
);

const displayPageTitle = computed(
  () => !displayProjectOptions.value && !!pageTitle.value && !collapsed.value
);
</script>
