<template>
  <details-panel panel="displayProject" data-cy="panel-artifact-type">
    <project-overview-display borderless />
  </details-panel>
</template>

<script lang="ts">
/**
 * Displays the project overview panel.
 */
export default {
  name: "ProjectOverviewPanel",
};
</script>

<script setup lang="ts">
import { DetailsPanel } from "@/components/common";
import { ProjectOverviewDisplay } from "@/components/project/editor";
</script>
