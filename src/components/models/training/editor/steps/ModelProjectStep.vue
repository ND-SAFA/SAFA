<template>
  <div>
    <typography
      el="p"
      value="Train the model on trace links in the current project. Both links that exist and those that do not will inform the model."
    />
    <trace-matrix-creator v-model="matrices" />
    <text-button
      block
      label="Start Model Training"
      color="primary"
      class="q-mt-sm"
      :disabled="!isValid"
      :loading="traceGenerationApiStore.loading"
      @click="handleSubmit"
    />
  </div>
</template>

<script lang="ts">
/**
 * A step for training a model with artifacts and trace links from the current project.
 */
export default {
  name: "ModelProjectStep",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { ArtifactLevelSchema, GenerationModelSchema } from "@/types";
import { traceGenerationApiStore } from "@/hooks";
import { Typography, TextButton } from "@/components/common";
import { TraceMatrixCreator } from "@/components/traceLink";

const props = defineProps<{
  model: GenerationModelSchema;
}>();

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const matrices = ref<ArtifactLevelSchema[]>([{ source: "", target: "" }]);

const isValid = computed(() =>
  matrices.value
    .map((matrix) => !!matrix.source && !!matrix.target)
    .reduce((acc, cur) => acc && cur, true)
);

/**
 * Trains the current model on selected trace links within the current project.
 */
async function handleSubmit(): Promise<void> {
  await traceGenerationApiStore.handleTrain(props.model, matrices.value, {
    onSuccess: () => {
      matrices.value = [{ source: "", target: "" }];
      emit("submit");
    },
  });
}
</script>
