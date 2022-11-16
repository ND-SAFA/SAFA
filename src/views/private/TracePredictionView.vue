<template>
  <private-page full-window>
    <template v-slot:page>
      <trace-prediction-tabs />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, TracePredictionTabs } from "@/components";

export default Vue.extend({
  name: "ApproveLinksView",
  components: {
    TracePredictionTabs,
    PrivatePage,
  },
});
</script>
