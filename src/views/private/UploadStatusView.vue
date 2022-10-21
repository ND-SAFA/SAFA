<template>
  <private-page>
    <template v-slot:page>
      <back-button />
      <typography el="h1" variant="title" value="Current Uploads" />
      <v-divider />
      <typography
        el="p"
        y="2"
        value="Select an upload below to see more details on its status."
      />
      <job-table />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, BackButton, Typography, JobTable } from "@/components";

/**
 * Displays project uploads.
 */
export default Vue.extend({
  name: "UploadStatusView",
  components: {
    JobTable,
    Typography,
    BackButton,
    PrivatePage,
  },
});
</script>
