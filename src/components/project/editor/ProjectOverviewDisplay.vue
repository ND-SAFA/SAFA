<template>
  <panel-card title="Project Overview">
    <typography variant="caption" value="Description" />
    <typography
      ep="p"
      variant="expandable"
      :value="description"
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

const project = computed(() => projectStore.project);

const description = computed(
  () => project.value.description || "No Description."
);
</script>
