<template>
  <v-container style="max-width: 40em">
    <typography
      el="p"
      value="Enter keywords for the domain that this model should be trained on. Press enter to save a keyword."
    />
    <v-combobox filled multiple chips deletable-chips label="Keywords" />
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
 * A step for pre-training a model with keywords and documents.
 */
export default Vue.extend({
  name: "ModelKeywordsStep",
  components: { Typography, GenericFileSelector },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
});
</script>
