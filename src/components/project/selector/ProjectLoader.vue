<template>
  <tab-list v-model="tab" :tabs="tabs">
    <template #load>
      <project-version-stepper />
    </template>
    <template v-if="hasProject" #project>
      <jobs-table :display-project-jobs="true" />
    </template>
    <template #user>
      <jobs-table :display-project-jobs="false" />
    </template>
  </tab-list>
</template>

<script lang="ts">
/**
 * Allows for loading created projects and versions, as well as viewing past project uploads.
 */
export default {
  name: "ProjectLoader",
};
</script>

<script lang="ts" setup>
import { computed, ref } from "vue";
import { loaderTabOptions } from "@/util";
import { projectStore } from "@/hooks";
import { TabList } from "@/components/common";
import { JobsTable } from "@/components/jobs";
import ProjectVersionStepper from "./ProjectVersionStepper.vue";

const hasProject = computed(() => projectStore.projectId !== "");
const allTabs = loaderTabOptions();
const tabs = computed(() => (hasProject.value ? allTabs : allTabs.slice(0, 2)));
const tab = ref(tabs.value[0].id);
</script>
