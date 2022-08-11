<template>
  <private-page>
    <template v-slot:page>
      <back-button text="Back To Project Creator" />
      <typography el="h1" variant="title" value="Current Uploads" />
      <v-divider />
      <typography
        el="p"
        y="2"
        value="Select a project below to see more detailed updates on the import
        status."
      />
      <job-list />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { JobList, PrivatePage, BackButton, Typography } from "@/components";

/**
 * Displays project uploads.
 */
export default Vue.extend({
  name: "UploadStatusView",
  components: {
    Typography,
    BackButton,
    JobList,
    PrivatePage,
  },
});
</script>
