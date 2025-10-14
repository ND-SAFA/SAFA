<template>
  <flex-box v-if="layoutStore.mode !== 'tim' && !smallWindow" align="center">
    <icon-button
      v-if="documentStore.hasPreviousHistory"
      small
      tooltip="Previous View"
      icon="back"
      color="text"
      @click="documentStore.switchDocumentHistory('previous')"
    />
    <icon-button
      v-if="documentStore.hasNextHistory"
      small
      tooltip="Next View"
      icon="forward"
      color="text"
      @click="documentStore.switchDocumentHistory('next')"
    />
    <separator
      v-if="documentStore.hasPreviousHistory || documentStore.hasNextHistory"
      vertical
      inset
      nav
      x="1"
    />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays buttons for going back and forward in the view history.
 */
export default {
  name: "ViewHistory",
};
</script>

<script setup lang="ts">
import { documentStore, layoutStore, useScreen } from "@/hooks";
import { FlexBox, IconButton, Separator } from "@/components/common";

const { smallWindow } = useScreen();
</script>
