<template>
  <panel-card title="Project Overview">
    <typography
      v-if="displayDescription"
      variant="caption"
      value="Description"
    />
    <typography
      v-if="displayDescription"
      ep="p"
      variant="expandable"
      :value="description"
      default-expanded
      :collapse-length="0"
    />
    <typography
      v-if="!!specification"
      variant="caption"
      value="Specification"
    />
    <typography
      v-if="!!specification"
      ep="p"
      variant="expandable"
      :value="specification"
      default-expanded
      :collapse-length="0"
    />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the project description.
 */
export default {
  name: "ProjectOverviewDisplay",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { projectStore } from "@/hooks";
import { PanelCard, Typography } from "@/components/common";

// Hide the description if it is just a copy of the generated specification.
const displayDescription = computed(
  () =>
    projectStore.project.description.length !==
    projectStore.project.specification?.length
);

const description = computed(
  () => projectStore.project.description || "No Description."
);

const specification = computed(() => projectStore.project.specification);
</script>
