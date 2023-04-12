<template>
  <expansion-item
    v-model="props.panel.open"
    :label="props.panel.name || newLabel"
    :caption="props.label"
    :icon="iconId"
    :header-class="headerClass"
    data-cy="panel-files"
  >
    <div class="q-mx-md">
      <slot name="panel" :panel="props.panel" />

      <flex-box
        v-if="props.variant === 'trace'"
        full-width
        align="center"
        y="2"
      >
        <select-input
          v-model="props.panel.type"
          label="Source Type"
          :options="artifactTypes"
          hint="Required"
          class="full-width"
          data-cy="input-source-type"
        />
        <icon class="q-mx-md" variant="trace" size="md" />
        <select-input
          v-model="props.panel.toType"
          label="Target Type"
          :options="artifactTypes"
          hint="Required"
          class="full-width"
          data-cy="input-target-type"
        />
      </flex-box>
      <text-input
        v-if="props.variant === 'artifact'"
        v-model="props.panel.type"
        label="Artifact Type"
        hint="Required"
        data-cy="input-artifact-type"
      />

      <file-input
        v-if="!isGenerated"
        v-model="props.panel.file"
        :multiple="false"
        data-cy="input-files-panel"
      />

      <flex-box
        v-if="props.variant === 'trace'"
        full-width
        justify="between"
        align="center"
        y="2"
      >
        <switch-input
          v-model="props.panel.isGenerated"
          label="Generate Trace Links"
        />
        <gen-method-input
          v-if="isGenerated"
          v-model="props.panel.generateMethod"
        />
      </flex-box>

      <flex-box full-width justify="between" y="2">
        <switch-input
          v-model="props.panel.ignoreErrors"
          label="Ignore Errors"
          color="grey"
          class="q-mr-sm"
          data-cy="button-ignore-errors"
        />
        <typography v-if="!valid" :value="errorMessage" color="negative" />
      </flex-box>

      <list v-if="props.panel.itemNames.length > 0" class="q-mb-md">
        <expansion-item label="Parsed Entities">
          <div class="q-mx-md">
            <attribute-chip
              v-for="itemName of props.panel.itemNames"
              :key="itemName"
              :value="itemName"
              :icon="props.variant"
              data-cy="button-file-entities"
            />
          </div>
        </expansion-item>
      </list>

      <flex-box justify="end">
        <text-button
          icon="delete"
          label="Delete"
          data-cy="button-delete-panel"
          @click="handleDeletePanel"
        />
      </flex-box>
    </div>
  </expansion-item>
</template>

<script lang="ts">
/**
 * Provides inputs for uploading a file.
 */
export default {
  name: "FilePanel",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { CreatorFilePanel } from "@/types";
import { getIcon } from "@/util";
import { projectSaveStore } from "@/hooks";
import { parseFilePanel } from "@/api";
import {
  ExpansionItem,
  FileInput,
  SwitchInput,
  TextButton,
  FlexBox,
  Typography,
  TextInput,
  GenMethodInput,
  Icon,
  SelectInput,
  List,
  AttributeChip,
} from "@/components/common";

const props = defineProps<{
  panel: CreatorFilePanel;
  index: number;
  variant: "artifact" | "trace";
  label: string;
  newLabel: string;
}>();

// const emit = defineEmits<{}>();

const errorMessage = computed(() => {
  if (!props.panel.name) {
    return "The file requires an artifact type";
  } else if (!props.panel.file && !props.panel.isGenerated) {
    return "No file has been uploaded";
  } else if (props.panel.ignoreErrors) {
    return undefined;
  } else {
    return props.panel.errorMessage;
  }
});

const valid = computed(() => !errorMessage.value);

const headerClass = computed(() =>
  valid.value ? "text-positive" : "text-negative"
);

const iconId = computed(() =>
  valid.value ? getIcon("success") : getIcon("error")
);

const artifactTypes = computed(() => projectSaveStore.artifactTypes);

const isGenerated = computed(() => props.panel.isGenerated);

/**
 * Deletes the current file panel.
 */
function handleDeletePanel() {
  projectSaveStore.removePanel(props.variant, props.index);
}

watch(
  () => props.panel.type,
  (type) => {
    if (props.panel.variant === "trace") return;

    props.panel.name = type;
  }
);

watch(
  () => [props.panel.type, props.panel.toType],
  ([fromType, toType]) => {
    if (props.panel.variant === "artifact") return;

    props.panel.name =
      !props.panel.type || !props.panel.toType
        ? ""
        : `${fromType} to ${toType}`;
  }
);

watch(
  () => props.panel.file,
  (file) => {
    if (file) {
      parseFilePanel(props.panel, projectSaveStore.artifactMap);
    } else {
      props.panel.artifacts = [];
      props.panel.traces = [];
      props.panel.itemNames = [];
      props.panel.errorMessage = undefined;
    }
  }
);

watch(
  () => [valid.value, props.panel.loading],
  () => {
    props.panel.valid = valid.value;

    if (!valid.value || props.panel.loading) return;

    props.panel.open = false;
  }
);
</script>
