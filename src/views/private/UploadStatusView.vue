<template>
  <private-page>
    <template v-slot:page>
      <typography t="4" el="h1" variant="title" value="Project Uploads" />
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
import { PrivatePage, Typography, JobTable } from "@/components";

/**
 * Displays project uploads.
 */
export default Vue.extend({
  name: "UploadStatusView",
  components: {
    JobTable,
    Typography,
    PrivatePage,
  },
});
</script>
