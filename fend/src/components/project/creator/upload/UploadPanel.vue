<template>
  <expansion-item
    v-model="props.panel.open"
    :label="props.panel.name || newLabel"
    :caption="label"
    :icon="iconId"
    :header-class="headerClass"
    data-cy="panel-files"
  >
    <div class="q-mx-md">
      <slot name="panel" :panel="props.panel" />

      <select-input
        v-if="!props.hideUploadType"
        v-model="props.panel.variant"
        label="Upload Type"
        :options="variantOptions"
        hint="Required"
        class="full-width q-mb-sm"
        option-to-value
        option-label="name"
        option-value="id"
        data-cy="input-upload-type"
      />

      <upload-panel-name v-bind="props" />

      <file-input
        v-if="hasSingleFile"
        v-model="props.panel.file"
        :multiple="false"
        data-cy="input-files-panel"
      />
      <project-files-input
        v-if="hasBulkFiles"
        v-model="props.panel.bulkFiles"
        v-model:tim="props.panel.tim"
        data-cy="input-files-bulk"
      />

      <git-hub-project-input v-if="props.panel.variant === 'github'" />
      <jira-project-input v-if="props.panel.variant === 'jira'" />

      <switch-input
        v-if="props.panel.variant === 'bulk'"
        v-model="props.panel.emptyFiles"
        label="Create an empty project"
        data-cy="toggle-create-empty-project"
      />

      <expansion-item v-if="!props.hideUploadType" label="Advanced Settings">
        <flex-box column>
          <switch-input
            v-if="hasBulkFiles"
            v-model="props.panel.summarize"
            label="Generate artifact summaries"
            data-cy="toggle-create-summarize"
          />
          <switch-input
            v-if="props.panel.variant === 'trace'"
            v-model="props.panel.isGenerated"
            label="Generate Trace Links"
          />
        </flex-box>

        <upload-panel-errors v-bind="props" />

        <list
          v-if="hasSingleFile && props.panel.itemNames.length > 0"
          class="q-mb-md"
        >
          <expansion-item label="Parsed Entities">
            <div class="q-mx-md">
              <attribute-chip
                v-for="itemName of props.panel.itemNames"
                :key="itemName"
                :value="itemName"
                :icon="
                  props.panel.variant === 'artifact' ? 'artifact' : 'trace'
                "
                data-cy="button-file-entities"
              />
            </div>
          </expansion-item>
        </list>
      </expansion-item>

      <flex-box justify="end" t="2">
        <text-button
          v-if="!props.hideUploadType"
          text
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
  name: "UploadPanel",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { FilePanelProps } from "@/types";
import { getIcon, uploadPanelOptions } from "@/util";
import { parseApiStore, projectSaveStore } from "@/hooks";
import {
  ExpansionItem,
  FileInput,
  SwitchInput,
  TextButton,
  FlexBox,
  SelectInput,
  List,
  AttributeChip,
} from "@/components/common";
import { ProjectFilesInput } from "@/components/project/save";
import {
  GitHubProjectInput,
  JiraProjectInput,
} from "@/components/integrations";
import UploadPanelErrors from "./UploadPanelErrors.vue";
import UploadPanelName from "./UploadPanelName.vue";

const props = defineProps<FilePanelProps>();

const variantOptions = computed(() =>
  props.index === 0 ? uploadPanelOptions() : uploadPanelOptions().slice(0, 2)
);

const label = computed(
  () =>
    ({
      artifact: "Artifact Type",
      trace: "Trace Matrix",
      bulk: "Bulk Upload",
      github: "GitHub Import",
      jira: "Jira Import",
    })[props.panel.variant]
);
const newLabel = computed(() => `New ${label.value}`);

const valid = computed(() => !props.panel.errorMessage);

const headerClass = computed(() =>
  valid.value ? "text-positive" : "text-negative"
);

const iconId = computed(() =>
  valid.value ? getIcon("success") : getIcon("error")
);

const hasSingleFile = computed(
  () =>
    (props.panel.variant === "artifact" || props.panel.variant === "trace") &&
    !props.panel.isGenerated
);
const hasBulkFiles = computed(
  () => props.panel.variant === "bulk" && !props.panel.emptyFiles
);

/**
 * Deletes the current file panel.
 */
function handleDeletePanel() {
  projectSaveStore.removePanel(props.panel.variant, props.index);
}

// Clear the name when the variant changes.
watch(
  () => props.panel.variant,
  () => {
    props.panel.name = "";
  }
);

// For artifact upload, set the name to the artifact type when the type changes.
watch(
  () => props.panel.type,
  (type) => {
    if (props.panel.variant === "artifact") {
      props.panel.name = type;
    }
  }
);

// For trace upload, set the name to the artifact types when the type changes.
watch(
  () => [props.panel.type, props.panel.toType],
  ([fromType, toType]) => {
    if (props.panel.variant === "trace") {
      props.panel.name =
        !props.panel.type || !props.panel.toType
          ? ""
          : `${fromType} to ${toType}`;
    }
  }
);

// For file upload, parse uploaded files and store the parse state.
watch(
  () => props.panel.file,
  (file) => {
    if (file) {
      parseApiStore.handleParseProjectFile(
        props.panel,
        projectSaveStore.artifactMap
      );
    } else {
      props.panel.artifacts = [];
      props.panel.traces = [];
      props.panel.itemNames = [];
      props.panel.errorMessage = undefined;
    }
  }
);

// For file upload, close the panel after successful upload.
watch(
  () => props.panel.loading,
  () => {
    if (props.panel.loading || !valid.value) return;

    props.panel.open = false;
  }
);
</script>
