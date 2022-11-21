<template>
  <v-container>
    <typography
      el="p"
      value="Train the model on trace links in the current project. Both links that exist and those that do not will inform the model."
    />
    <trace-matrix-creator v-model="matrices" />
    <v-btn
      block
      color="primary"
      class="mt-4"
      :disabled="!areMatricesValid"
      :loading="isLoading"
      @click="handleTrainModel"
    >
      Start Model Training
    </v-btn>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ArtifactLevelModel, GenerationModel } from "@/types";
import { handleTrainModel } from "@/api";
import { Typography } from "@/components/common";
import { TraceMatrixCreator } from "@/components/traceLink";

/**
 * A step for training a model with artifacts and trace links from the current project.
 *
 * @emits-1 `submit` - On submit.
 */
export default Vue.extend({
  name: "ModelProjectStep",
  components: { Typography, TraceMatrixCreator },
  props: {
    model: {
      type: Object as PropType<GenerationModel>,
      required: true,
    },
  },
  data() {
    return {
      isLoading: false,
      matrices: [{ source: "", target: "" }] as ArtifactLevelModel[],
    };
  },
  computed: {
    /**
     * @return Whether the current matrices are valid.
     */
    areMatricesValid(): boolean {
      return this.matrices
        .map((matrix) => !!matrix.source && !!matrix.target)
        .reduce((acc, cur) => acc && cur, true);
    },
  },
  methods: {
    /**
     * Trains the current model on selected trace links within the current project.
     */
    async handleTrainModel(): Promise<void> {
      this.isLoading = true;
      await handleTrainModel(this.model, this.matrices, {
        onComplete: () => (this.isLoading = false),
        onSuccess: () => {
          this.matrices = [{ source: "", target: "" }];
          this.$emit("submit");
        },
      });
    },
  },
});
</script>
