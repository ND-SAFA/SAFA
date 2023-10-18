<template>
  <flex-box v-if="layoutStore.mode !== 'tim'" align="center">
    <separator vertical inset nav x="1" />
    <icon-button
      :disabled="!documentStore.hasPreviousHistory"
      tooltip="Previous View"
      icon="back"
      color="text"
      @click="documentStore.switchDocumentHistory('previous')"
    />
    <icon-button
      :disabled="!documentStore.hasNextHistory"
      tooltip="Next View"
      icon="forward"
      color="text"
      @click="documentStore.switchDocumentHistory('next')"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays buttons for going back and forward in the document history.
 */
export default {
  name: "DocumentHistory",
};
</script>

<script setup lang="ts">
import { documentStore, layoutStore } from "@/hooks";
import { FlexBox, IconButton, Separator } from "@/components";
</script>
