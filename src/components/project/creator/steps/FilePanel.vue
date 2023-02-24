<template>
  <expansion-item
    v-model="panel.open"
    :label="panel.name || newLabel"
    :caption="props.label"
    :icon="iconId"
    :header-class="headerClass"
  >
    <div class="q-mx-md">
      <slot name="panel" :panel="panel" />
      <text-input
        v-if="props.variant === 'artifact'"
        v-model="panel.type"
        label="Artifact Type"
        hint="Required"
      />
      <file-input
        v-model="panel.file"
        :multiple="false"
        data-cy="input-files-panel"
      />
      <flex-box full-width justify="between">
        <switch-input
          v-model="panel.ignoreErrors"
          label="Ignore Errors"
          color="grey"
          data-cy="button-ignore-errors"
        />
        <typography v-if="!isValid" :value="errorMessage" color="negative" />
      </flex-box>
      <flex-box justify="end">
        <text-button icon="delete" label="Delete" @click="handleDeletePanel" />
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
  if (props.panel.ignoreErrors) {
    return undefined;
  } else if (!props.panel.name) {
    return "The file requires an artifact type";
  } else if (!props.panel.file) {
    return "No file has been uploaded";
  } else {
    return props.panel.errorMessage;
  }
});

const isValid = computed(() => !errorMessage.value);

const headerClass = computed(() =>
  isValid.value ? "text-positive" : "text-negative"
);

const iconId = computed(() =>
  isValid.value ? getIcon("success") : getIcon("error")
);

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

    props.panel.name = `${fromType} to ${toType}`;
  }
);

watch(
  () => props.panel.file,
  () => parseFilePanel(props.panel, projectSaveStore.artifactMap)
);
</script>
