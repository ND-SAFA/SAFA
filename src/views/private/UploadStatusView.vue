<template>
  <private-page>
    <template v-slot:page>
      <job-display />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, JobDisplay } from "@/components";

/**
 * Displays project uploads.
 */
export default Vue.extend({
  name: "UploadStatusView",
  components: {
    JobDisplay,
    PrivatePage,
  },
});
</script>
