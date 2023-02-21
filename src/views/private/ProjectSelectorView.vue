<template>
  <private-page
    title="Open Project"
    subtitle="Select a project and version to load."
  >
    <project-version-stepper />
  </private-page>
</template>

<script lang="ts">
/**
 * Displays the steps for creating a project.
 */
export default {
  name: "ProjectCreatorView",
};
</script>

<script setup lang="ts">
import { PrivatePage, ProjectVersionStepper } from "@/components";
</script>
