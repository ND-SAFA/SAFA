<template>
  <div>
    <back-button text="Back To Tree View" to-project />
    <typography t="2" el="h1" variant="title" value="Trace Prediction" />
    <v-divider class="mb-2" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { Typography, BackButton } from "@/components/common";

/**
 * Displays the header of the trace prediction page.
 */
export default defineComponent({
  name: "TracePredictionHeader",
  components: {
    BackButton,
    Typography,
  },
});
</script>
