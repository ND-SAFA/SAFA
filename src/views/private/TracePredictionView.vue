<template>
  <private-page>
    <template v-slot:page>
      <back-button text="Back To Tree View" to-project />
      <trace-prediction-tabs />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, BackButton, TracePredictionTabs } from "@/components";

export default Vue.extend({
  name: "ApproveLinksView",
  components: {
    TracePredictionTabs,
    BackButton,
    PrivatePage,
  },
});
</script>
