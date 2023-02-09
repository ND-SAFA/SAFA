<template>
  <private-page>
    <template #page>
      <project-creator />
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
import { PrivatePage, ProjectCreator } from "@/components";
</script>
