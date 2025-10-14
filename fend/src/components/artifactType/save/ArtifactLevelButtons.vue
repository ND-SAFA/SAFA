<template>
  <flex-box v-if="permissionStore.isAllowed('project.edit_data')">
    <text-button
      text
      label="Edit Type"
      icon="edit"
      @click="appStore.openDetailsPanel('saveArtifactLevel')"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays artifact level action buttons.
 */
export default {
  name: "ArtifactLevelButtons",
};
</script>

<script setup lang="ts">
import { appStore, permissionStore } from "@/hooks";
import { FlexBox, TextButton } from "@/components/common";
</script>
