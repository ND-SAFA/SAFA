<template>
  <private-page>
    <job-display />
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
