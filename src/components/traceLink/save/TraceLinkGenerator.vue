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
      :loading="loading"
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
import { ArtifactLevelSchema, ModelType } from "@/types";
import { handleGenerateLinks } from "@/api";
import { Typography, TextButton } from "@/components/common";
import { TraceMatrixCreator } from "../save";

const props = defineProps<{
  open: boolean;
}>();

const emit = defineEmits<{
  (e: "submit"): void;
}>();

const createEmptyArtifactLevel = (): ArtifactLevelSchema[] => [
  { source: "", target: "" },
];

const loading = ref(false);
const isValid = ref(false);
const method = ref<ModelType | undefined>();
const matrices = ref(createEmptyArtifactLevel());

const areMatricesValid = computed(() =>
  matrices.value
    .map((matrix: ArtifactLevelSchema) => !!matrix.source && !!matrix.target)
    .reduce((acc: boolean, cur: boolean) => acc && cur, true)
);

/**
 * Resets this component's data.
 */
function handleReset(): void {
  loading.value = false;
  isValid.value = false;
  method.value = undefined;
  matrices.value = createEmptyArtifactLevel();
}

/**
 * Attempts to generate the selected trace links.
 */
function handleSubmit(): void {
  loading.value = true;

  handleGenerateLinks(undefined, matrices.value, {
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
