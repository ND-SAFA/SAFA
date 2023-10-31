<template>
  <div>
    <file-input
      v-model="selectedFiles"
      multiple
      :data-cy="props.dataCy"
      :error-message="errorMessage"
      @clear="handleClear"
    />
    <expansion-item
      v-if="selectedFiles.length > 0"
      class="q-mb-md"
      label="Manage Project TIM"
      data-cy="toggle-tim-manage"
    >
      <multiselect-input
        v-model="artifactTypes"
        label="Artifact Files"
        :options="typeOptions"
        hint="Select the artifact files. Reads the file name <type>.csv"
        data-cy="input-tim-artifacts"
        b="1"
      />
      <multiselect-input
        v-model="traceMatrices"
        label="Trace Matrix Files"
        :options="matrixOptions"
        hint="Select the trace matrix files. Reads the file name <source>2<target>.csv"
        data-cy="input-tim-traces"
        :option-label="getMatrixName"
        b="1"
      />
    </expansion-item>
  </div>
</template>

<script lang="ts">
/**
 * An input for project files.
 */
export default {
  name: "ProjectFilesInput",
};
</script>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { MatrixSchema, ProjectFilesInputProps, TimJsonSchema } from "@/types";
import { useVModel } from "@/hooks";
import {
  FileInput,
  MultiselectInput,
  ExpansionItem,
} from "@/components/common";

const props = defineProps<ProjectFilesInputProps>();

const emit = defineEmits<{
  (e: "update:modelValue", files: File[]): void;
  (e: "update:tim", tim: TimJsonSchema | undefined): void;
}>();

const selectedFiles = useVModel(props, "modelValue");
const tim = ref<TimJsonSchema | undefined>(undefined);
const artifactTypes = ref<string[]>([]);
const traceMatrices = ref<MatrixSchema[]>([]);

/**
 * @return Generated artifact types based on file names.
 */
const typeOptions = computed(() =>
  selectedFiles.value
    .map(({ name }) => name.split(".")[0])
    .filter((name) => name !== "tim")
);

/**
 * @return Generated trace matrices based on file names.
 */
const matrixOptions = computed(() =>
  artifactTypes.value
    .map((source) => artifactTypes.value.map((target) => ({ source, target })))
    .reduce((acc, cur) => [...acc, ...cur], [])
);

/**
 * @return Any errors on uploaded files.
 */
const errorMessage = computed(() =>
  selectedFiles.value.length === 0 ||
  selectedFiles.value.find(({ name }) => name === "tim.json")
    ? undefined
    : "Missing project TIM. Please create one below."
);

/**
 * Returns the display name of a trace matrix.
 * @param matrix - The matrix to name.
 * @return The display name.
 */
function getMatrixName(matrix: MatrixSchema): string {
  return `${matrix.source} to ${matrix.target}`;
}

/**
 * Clears the current tim file data.
 */
function handleClear(): void {
  tim.value = undefined;
  selectedFiles.value = [];
  artifactTypes.value = [];
  traceMatrices.value = [];
  emit("update:tim", undefined);
}

/**
 * Creates a new tim file when the inputs change.
 * Only creates a new file if there is no existing TIM file.
 */
function handleTimChange(): void {
  if (
    selectedFiles.value.length === 0 ||
    selectedFiles.value.find(({ name }) => name == "tim.json")
  )
    return;

  tim.value = {
    artifacts: artifactTypes.value.map((type) => ({
      type,
      fileName: `${type}.csv`,
    })),
    traces: traceMatrices.value.map(({ source, target }) => ({
      sourceType: source,
      targetType: target,
      fileName: `${source}2${target}.csv`,
    })),
  };

  selectedFiles.value = [
    ...selectedFiles.value.filter(({ name }) => name !== "tim.json"),
    new File([JSON.stringify(tim.value)], "tim.json", {
      type: "application/json",
    }),
  ];

  emit("update:tim", tim.value);
}

/**
 * Selects relevant trace matrices when the types change, and updates the tim file.
 */
function handleTypesChange(): void {
  traceMatrices.value = matrixOptions.value.filter(({ source, target }) =>
    selectedFiles.value.find(({ name }) => name === `${source}2${target}.csv`)
  );

  handleTimChange();
}

/**
 * If a tim file is loaded, it is parsed so that it can be edited.
 */
watch(
  () => selectedFiles.value,
  (files: File[]) => {
    const timFile = files.find(({ name }) => name === "tim.json");

    if (!timFile || artifactTypes.value.length > 0) return;

    const reader = new FileReader();

    reader.addEventListener("load", (event) => {
      tim.value = JSON.parse(String(event.target?.result));

      artifactTypes.value = (tim.value?.artifacts || []).map(
        ({ fileName }) => fileName.split(".")[0]
      );

      traceMatrices.value = (tim.value?.traces || [])
        .filter(({ sourceType, targetType }) => sourceType && targetType)
        .map(({ sourceType, targetType }) => ({
          source: sourceType,
          target: targetType,
        }));

      emit("update:tim", tim.value);
    });

    reader.readAsText(timFile);
  }
);

watch(
  () => artifactTypes.value,
  () => handleTypesChange()
);

watch(
  () => traceMatrices.value,
  () => handleTimChange()
);
</script>
