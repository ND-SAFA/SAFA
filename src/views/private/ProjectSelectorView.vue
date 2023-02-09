<template>
  <private-page>
    <template #page>
      <project-version-stepper />
    </template>
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
