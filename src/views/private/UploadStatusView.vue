<template>
  <private-page>
    <template #page>
      <job-display />
    </template>
  </private-page>
</template>

<script lang="ts">
/**
 * Displays project uploads.
 */
export default {
  name: "UploadStatusView",
};
</script>

<script setup lang="ts">
import { PrivatePage, JobDisplay } from "@/components";
</script>
