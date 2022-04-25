<template>
  <private-page>
    <template v-slot:page>
      <v-btn text @click="handleGoBack">
        <v-icon left> mdi-arrow-left </v-icon>
        Back To Tree View
      </v-btn>
      <v-container> </v-container>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { navigateBack } from "@/router";
import { PrivatePage } from "@/components";

/**
 * Displays project settings.
 */
export default Vue.extend({
  name: "UploadStatusView",
  components: {
    PrivatePage,
  },
  methods: {
    /**
     * Goes back to the artifact page.
     */
    handleGoBack() {
      navigateBack();
    },
  },
});
</script>
