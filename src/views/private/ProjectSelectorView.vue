<template>
  <private-page>
    <project-loader />
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
import { PrivatePage, ProjectLoader } from "@/components";
</script>
