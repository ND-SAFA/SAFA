<template>
  <q-breadcrumbs
    gutter="xs"
    class="nav-breadcrumb-list"
    separator-color="primary"
  >
    <q-breadcrumbs-el v-if="!projectStore.isProjectDefined">
      <q-select
        standout
        label="Organization"
        label-color="primary"
        bg-color="transparent"
        :model-value="orgName"
        class="nav-breadcrumb"
      />
    </q-breadcrumbs-el>

    <q-breadcrumbs-el>
      <project-selector />
    </q-breadcrumbs-el>

    <q-breadcrumbs-el v-if="projectStore.isProjectDefined">
      <version-selector />
    </q-breadcrumbs-el>
    <q-breadcrumbs-el v-if="projectStore.isProjectDefined">
      <document-selector />
    </q-breadcrumbs-el>
  </q-breadcrumbs>
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
import { computed } from "vue";
import { orgStore, projectStore } from "@/hooks";
import { ProjectSelector, VersionSelector } from "@/components/project";
import { DocumentSelector } from "@/components/document";

const orgName = computed(() => orgStore.org.name);
</script>
