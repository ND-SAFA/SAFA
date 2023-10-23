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

      <flex-box
        v-if="props.panel.variant === 'trace'"
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
        v-if="props.panel.variant === 'artifact'"
        v-model="props.panel.type"
        label="Artifact Type"
        hint="Required"
        data-cy="input-artifact-type"
      />

      <file-input
        v-if="!isGenerated && hasSingleFile"
        v-model="props.panel.file"
        :multiple="false"
        data-cy="input-files-panel"
      />
      <project-files-input
        v-if="props.panel.variant === 'bulk'"
        v-model="props.panel.bulkFiles"
        v-model:tim="props.panel.tim"
        data-cy="input-files-bulk"
      />

      <git-hub-project-input v-if="props.panel.variant === 'github'" />
      <jira-project-input v-if="props.panel.variant === 'jira'" />

      <switch-input
        v-if="hasArtifactFile"
        v-model="props.panel.summarize"
        label="Generate artifact summaries"
        data-cy="toggle-create-summarize"
      />
      <switch-input
        v-if="props.panel.variant === 'trace'"
        v-model="props.panel.isGenerated"
        label="Generate Trace Links"
      />

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
              :icon="props.panel.variant"
              data-cy="button-file-entities"
            />
          </div>
        </expansion-item>
      </list>

      <flex-box justify="end" t="2">
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
import { FilePanelProps } from "@/types";
import { getIcon, uploadPanelOptions } from "@/util";
import { integrationsStore, parseApiStore, projectSaveStore } from "@/hooks";
import {
  ExpansionItem,
  FileInput,
  SwitchInput,
  TextButton,
  FlexBox,
  Typography,
  TextInput,
  Icon,
  SelectInput,
  List,
  AttributeChip,
} from "@/components/common";
import { ProjectFilesInput } from "@/components/project/save";
import {
  GitHubProjectInput,
  JiraProjectInput,
} from "@/components/integrations";

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

const errorMessage = computed(() => {
  if (!props.panel.name) {
    return "Requires a name";
  } else if (props.panel.ignoreErrors) {
    return undefined;
  } else if (
    (props.panel.variant === "artifact" || props.panel.variant === "trace") &&
    !props.panel.file &&
    !props.panel.isGenerated
  ) {
    return "No files have been uploaded.";
  } else if (
    (props.panel.variant === "jira" || props.panel.variant === "github") &&
    !integrationsStore.gitHubProject &&
    !integrationsStore.jiraProject
  ) {
    return "Select a project to import.";
  } else if (
    props.panel.variant === "bulk" &&
    (props.panel.bulkFiles.length === 0 ||
      !props.panel.bulkFiles.find(({ name }) => name === "tim.json"))
  ) {
    return "Requires a tim.json configuration file.";
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

const hasSingleFile = computed(
  () => props.panel.variant === "artifact" || props.panel.variant === "trace"
);
const hasArtifactFile = computed(
  () =>
    props.panel.variant === "artifact" ||
    props.panel.variant === "bulk" ||
    props.panel.variant === "github"
);

/**
 * Deletes the current file panel.
 */
function handleDeletePanel() {
  projectSaveStore.removePanel(props.panel.variant, props.index);
}

watch(
  () => props.panel.variant,
  () => {
    props.panel.name = "";
  }
);

watch(
  () => props.panel.type,
  (type) => {
    if (props.panel.variant === "artifact") {
      props.panel.name = type;
    }
  }
);

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

watch(
  () => valid.value,
  () => {
    props.panel.valid = valid.value;
  }
);

watch(
  () => props.panel.loading,
  () => {
    if (props.panel.loading || !valid.value) return;

    props.panel.open = false;
  }
);
</script>
