<template>
  <v-container>
    <typography
      el="p"
      value="Train the model on trace links in the current project. Both links that exist and those that do not will inform the model."
    />
    <trace-matrix-creator v-model="matrices" />
    <v-btn block color="primary" class="mt-4"> Train Model </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactLevelModel, GenerationModel } from "@/types";
import { Typography } from "@/components/common";
import { TraceMatrixCreator } from "@/components/trace-link";

/**
 * A step for training a model with artifacts and trace links from the current project.
 */
export default Vue.extend({
  name: "ModelKeywordsStep",
  components: { Typography, TraceMatrixCreator },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
  data() {
    return {
      matrices: [{ source: "", target: "" }] as ArtifactLevelModel[],
    };
  },
});
</script>
