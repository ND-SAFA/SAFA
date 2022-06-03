<template>
  <private-page>
    <template v-slot:page>
      <v-btn text @click="handleGoBack">
        <v-icon left> mdi-arrow-left </v-icon>
        Back To Project Creator
      </v-btn>
      <v-container>
        <h1 class="text-h4">Current Uploads</h1>
        <v-divider />
        <p class="text-body-1 mt-2 mb-3">
          Select a project below to see more detailed updates on the import
          status.
        </p>
        <job-list />
      </v-container>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { navigateTo, Routes } from "@/router";
import { JobList, PrivatePage } from "@/components";

/**
 * Displays project uploads.
 */
export default Vue.extend({
  name: "UploadStatusView",
  components: {
    JobList,
    PrivatePage,
  },
  methods: {
    /**
     * Goes back to the artifact page.
     */
    handleGoBack() {
      navigateTo(Routes.PROJECT_CREATOR);
    },
  },
});
</script>
