<template>
  <v-container style="max-width: 40em">
    <under-construction-alert />
    <typography
      el="p"
      value="Upload any technical documents that would train the model to understand this domain."
    />
    <file-input />
    <v-btn disabled block color="primary"> Start Model Pre-Training </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { GenerationModel } from "@/types";
import {
  Typography,
  FileInput,
  UnderConstructionAlert,
} from "@/components/common";

/**
 * A step for training a model on documents.
 */
export default Vue.extend({
  name: "ModelDocumentStep",
  components: {
    Typography,
    FileInput,
    UnderConstructionAlert,
  },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
});
</script>
