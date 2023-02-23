<template>
  <private-page
    title="Create Project"
    subtitle="Create a project using one of the following methods."
  >
    <project-creator />
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
import { PrivatePage, ProjectCreator } from "@/components";
</script>
