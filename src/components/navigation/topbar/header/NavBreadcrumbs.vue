<template>
  <q-breadcrumbs
    v-if="projectStore.isProjectDefined"
    gutter="xs"
    class="nav-breadcrumb-list"
    separator-color="primary"
  >
    <q-breadcrumbs-el>
      <q-select
        standout
        label="Project"
        label-color="primary"
        bg-color="transparent"
        :model-value="projectName"
        class="nav-breadcrumb"
        hide-dropdown-icon
      />
    </q-breadcrumbs-el>
    <q-breadcrumbs-el>
      <q-select
        standout
        label="Version"
        label-color="primary"
        bg-color="transparent"
        :model-value="versionName"
        class="nav-breadcrumb"
        hide-dropdown-icon
      />
    </q-breadcrumbs-el>
    <q-breadcrumbs-el>
      <q-select
        standout
        label="View"
        label-color="primary"
        bg-color="transparent"
        :model-value="viewName"
        class="nav-breadcrumb"
        hide-dropdown-icon
      />
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
import { versionToString } from "@/util";
import { documentStore, projectStore } from "@/hooks";

const projectName = computed(() => projectStore.project.name || "Project");
const versionName = computed(() => versionToString(projectStore.version));
const viewName = computed(() => documentStore.currentDocument.name);
</script>
