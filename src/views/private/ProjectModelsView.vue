<template>
  <private-page>
    <template v-slot:page>
      <back-button />
      <typography el="h1" variant="title" value="Project Models" />
      <v-divider />
      <model-table />
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { BackButton, PrivatePage, Typography, ModelTable } from "@/components";

/**
 * Displays project models.
 */
export default Vue.extend({
  name: "ProjectModelsView",
  components: {
    ModelTable,
    Typography,
    BackButton,
    PrivatePage,
  },
});
</script>
