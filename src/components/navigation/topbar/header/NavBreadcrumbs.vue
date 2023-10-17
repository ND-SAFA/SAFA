<template>
  <q-breadcrumbs gutter="xs" class="nav-breadcrumb-list" separator-color="grey">
    <q-breadcrumbs-el v-if="displayOrgOptions">
      <organization-selector />
    </q-breadcrumbs-el>

    <q-breadcrumbs-el>
      <project-selector />
    </q-breadcrumbs-el>

    <q-breadcrumbs-el v-if="displayProjectOptions">
      <version-selector />
    </q-breadcrumbs-el>
    <q-breadcrumbs-el v-if="displayProjectOptions">
      <document-selector />
    </q-breadcrumbs-el>
  </q-breadcrumbs>
  <icon-button
    v-if="smallWindow"
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
import { projectStore, useScreen } from "@/hooks";
import { ProjectSelector, VersionSelector } from "@/components/project";
import { DocumentSelector } from "@/components/document";
import { IconButton } from "@/components/common";
import { OrganizationSelector } from "@/components/organization";

const { smallWindow } = useScreen();

const collapsed = ref(true);

const displayOptions = computed(() => !smallWindow.value || !collapsed.value);

const displayOrgOptions = computed(() => !projectStore.isProjectDefined);

const displayProjectOptions = computed(
  () => displayOptions.value && projectStore.isProjectDefined
);
</script>
