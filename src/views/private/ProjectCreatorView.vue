<template>
  <private-page :full-window="ENABLED_FEATURES.PROJECT_CREATOR_WORKFLOW">
    <project-builder v-if="ENABLED_FEATURES.PROJECT_CREATOR_WORKFLOW" />
    <project-creator v-else />
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
import { ENABLED_FEATURES } from "@/util";
import { PrivatePage, ProjectCreator, ProjectBuilder } from "@/components";
</script>
