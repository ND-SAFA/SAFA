<template>
  <v-container style="max-width: 40em">
    <typography
      el="p"
      value="Upload any technical documents that would train the model to understand this domain."
    />
    <generic-file-selector />
    <v-btn block color="primary"> Start Model Pre-Training </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import { Typography, GenericFileSelector } from "@/components/common";

/**
 * A step for training a model on documents.
 */
export default Vue.extend({
  name: "ModelDocumentStep",
  components: { Typography, GenericFileSelector },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
});
</script>
