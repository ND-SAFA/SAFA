<template>
  <div>
    <q-breadcrumbs gutter="none" class="nav-breadcrumb-list">
      <q-breadcrumbs-el :to="Routes.ORG">
        <q-select
          dense
          standout
          label="Organization"
          :model-value="orgName"
          class="nav-breadcrumb"
        />
      </q-breadcrumbs-el>
      <q-breadcrumbs-el v-if="orgName !== teamName" :to="Routes.TEAM">
        <q-select
          dense
          standout
          label="Team"
          :model-value="orgName"
          class="nav-breadcrumb"
        />
      </q-breadcrumbs-el>
    </q-breadcrumbs>
    <q-breadcrumbs
      v-if="projectStore.isProjectDefined"
      gutter="none"
      class="nav-breadcrumb-list"
    >
      <q-breadcrumbs-el :to="Routes.PROJECT_SETTINGS">
        <q-select
          dense
          standout
          label="Project"
          :model-value="projectName"
          class="nav-breadcrumb"
        />
      </q-breadcrumbs-el>
      <q-breadcrumbs-el :to="Routes.ARTIFACT">
        <q-select
          dense
          standout
          label="Version"
          :model-value="versionName"
          class="nav-breadcrumb"
        />
      </q-breadcrumbs-el>
      <q-breadcrumbs-el :to="Routes.ARTIFACT">
        <q-select
          dense
          standout
          label="View"
          :model-value="viewName"
          style="min-width: 100px"
        />
      </q-breadcrumbs-el>
    </q-breadcrumbs>
  </div>
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
import { documentStore, orgStore, projectStore, teamStore } from "@/hooks";
import { Routes } from "@/router";

const orgName = computed(() => orgStore.org.name || "Organization");
const teamName = computed(() => teamStore.team.name || "Team");
const projectName = computed(() => projectStore.project.name || "Project");
const versionName = computed(() => versionToString(projectStore.version));
const viewName = computed(() => documentStore.currentDocument.name);

// const props = defineProps<{}>();
</script>
