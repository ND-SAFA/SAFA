<template>
  <private-page
    title="Project Uploads"
    subtitle="Select an upload below to see more details on its status."
  >
    <jobs-table :display-project-jobs="false" />
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
import { PrivatePage, JobsTable } from "@/components";
</script>
