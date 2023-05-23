<template>
  <tab-list v-model="tab" :tabs="tabs">
    <template #load>
      <project-version-stepper />
    </template>
    <template #uploads>
      <jobs-table />
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

<script setup lang="ts">
import { ref } from "vue";
import { loaderTabOptions } from "@/util";
import { TabList } from "@/components/common";
import { JobsTable } from "@/components/jobs";
import ProjectVersionStepper from "./ProjectVersionStepper.vue";

const tabs = loaderTabOptions();
const tab = ref(tabs[0].id);
</script>
