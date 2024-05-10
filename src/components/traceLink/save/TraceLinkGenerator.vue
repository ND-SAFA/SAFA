<template>
  <div>
    <typography
      el="p"
      b="4"
      value="Select which sets of artifact types that you would like to generate links between."
    />
    <trace-matrix-creator v-model="matrices" />
    <text-button
      block
      label="Generate Trace Links"
      :disabled="!isValid"
      :loading="traceGenerationApiStore.loading"
      color="primary"
      data-cy="button-trace-generate"
      class="q-mt-md"
      @click="handleSubmit"
    />
  </div>
</template>

<script lang="ts">
/**
 * Displays inputs for generating trace links.
 */
export default {
  name: "TraceLinkGenerator",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { MatrixSchema, OpenableProps } from "@/types";
import { traceGenerationApiStore } from "@/hooks";
import { Typography, TextButton } from "@/components/common";
import { TraceMatrixCreator } from "@/components/traceLink/save";

const props = defineProps<OpenableProps>();

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const createEmptyArtifactLevel = (): MatrixSchema[] => [
  { source: "", target: "" },
];

const isValid = ref(false);
const matrices = ref(createEmptyArtifactLevel());

const areMatricesValid = computed(() =>
  matrices.value
    .map((matrix: MatrixSchema) => !!matrix.source && !!matrix.target)
    .reduce((acc: boolean, cur: boolean) => acc && cur, true)
);

/**
 * Resets this component's data.
 */
function handleReset(): void {
  isValid.value = false;
  matrices.value = createEmptyArtifactLevel();
}

/**
 * Attempts to generate the selected trace links.
 */
function handleSubmit(): void {
  traceGenerationApiStore.handleGenerate(matrices.value, {
    onComplete: () => {
      emit("submit");
      handleReset();
    },
  });
}

watch(
  () => props.open,
  (open) => {
    if (!open) return;

    handleReset();
  }
);

watch(
  () => matrices.value,
  () => {
    isValid.value = areMatricesValid.value;
  },
  { deep: true }
);
</script>
