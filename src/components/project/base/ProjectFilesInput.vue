<template>
  <div>
    <file-format-alert />
    <file-input
      v-model="selectedFiles"
      :data-cy="dataCy"
      :errors="errors"
      @clear="handleClear"
    />
    <v-expansion-panels v-if="selectedFiles.length > 0" class="mb-4">
      <v-expansion-panel data-cy="toggle-tim-manage">
        <v-expansion-panel-title> Manage Project TIM </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-autocomplete
            v-model="artifactTypes"
            filled
            chips
            deletable-chips
            multiple
            label="Artifact Files"
            :items="typeOptions"
            hint="Select the artifact files. Reads the file name <type>.csv"
            persistent-hint
            data-cy="input-tim-artifacts"
            @change="handleTypesChange"
          />
          <v-autocomplete
            v-model="traceMatrices"
            filled
            multiple
            chips
            deletable-chips
            return-object
            label="Trace Matrix Files"
            :items="matrixOptions"
            :item-text="(item) => `${item.source} To ${item.target}`"
            hint="Select the trace matrix files. Reads the file name <source>2<target>.csv"
            persistent-hint
            data-cy="input-tim-traces"
            @change="handleTimChange"
          />
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
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
import { ref, computed, defineProps, defineEmits, watch } from "vue";
import { ArtifactLevelSchema, TimJsonSchema } from "@/types";
import { FileInput, FileFormatAlert } from "@/components/common";

const props = defineProps<{
  dataCy?: string;
}>();

const emit = defineEmits<{
  (e: "input", files: File[]): void;
}>();

const selectedFiles = ref<File[]>([]);
const tim = ref<TimJsonSchema | undefined>(undefined);
const artifactTypes = ref<string[]>([]);
const traceMatrices = ref<ArtifactLevelSchema[]>([]);

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
const errors = computed(() =>
  selectedFiles.value.length === 0 ||
  selectedFiles.value.find(({ name }) => name === "tim.json")
    ? []
    : ["Missing project TIM. Please create one below."]
);

/**
 * Clears the current tim file data.
 */
function handleClear(): void {
  tim.value = undefined;
  artifactTypes.value = [];
  traceMatrices.value = [];
}

/**
 * Creates a new tim file when the inputs change.
 */
function handleTimChange(): void {
  tim.value = {
    DataFiles: artifactTypes.value
      .map((type) => ({ [type]: { File: `${type}.csv` } }))
      .reduce((acc, cur) => ({ ...acc, ...cur }), {}),
    ...traceMatrices.value
      .map(({ source, target }) => ({
        [`${source}2${target}`]: {
          Source: source,
          Target: target,
          File: `${source}2${target}.csv`,
        },
      }))
      .reduce((acc, cur) => ({ ...acc, ...cur }), {}),
  } as TimJsonSchema;

  selectedFiles.value = [
    ...selectedFiles.value.filter(({ name }) => name !== "tim.json"),
    new File([JSON.stringify(tim.value)], "tim.json", {
      type: "application/json",
    }),
  ];
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
 * Emits changes to selected files.
 * If a tim file is loaded, it is parsed so that it can be edited.
 */
watch(
  () => selectedFiles.value,
  (files: File[]) => {
    emit("input", files);

    const timFile = files.find(({ name }) => name === "tim.json");

    if (!timFile) return;

    const reader = new FileReader();

    reader.addEventListener("load", (event) => {
      tim.value = JSON.parse(String(event.target?.result));

      artifactTypes.value = Object.values(tim.value?.DataFiles || {}).map(
        ({ File }) => File.split(".")[0]
      );

      traceMatrices.value = Object.values(tim.value || {})
        .filter(({ Source, Target }) => Source && Target)
        .map(({ Source, Target }) => ({
          source: String(Source),
          target: String(Target),
        }));
    });

    reader.readAsText(timFile);
  }
);
</script>
