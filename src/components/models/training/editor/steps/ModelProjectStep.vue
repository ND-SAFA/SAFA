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
      :disabled="!isValid"
      :loading="isLoading"
      @click="handleSubmit"
    >
      Start Model Training
    </v-btn>
  </v-container>
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
import { defineProps, defineEmits, computed, ref } from "vue";
import { ArtifactLevelSchema, GenerationModelSchema } from "@/types";
import { handleTrainModel } from "@/api";
import { Typography } from "@/components/common";
import { TraceMatrixCreator } from "@/components/traceLink";

const props = defineProps<{
  model: GenerationModelSchema;
}>();

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const isLoading = ref(false);
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
  isLoading.value = true;

  await handleTrainModel(props.model, matrices.value, {
    onComplete: () => (isLoading.value = false),
    onSuccess: () => {
      matrices.value = [{ source: "", target: "" }];
      emit("submit");
    },
  });
}
</script>
