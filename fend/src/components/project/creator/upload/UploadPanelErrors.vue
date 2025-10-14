<template>
  <flex-box full-width justify="between" align="center" y="2">
    <switch-input
      v-model="props.panel.ignoreErrors"
      label="Ignore Errors"
      color="grey"
      class="q-mr-sm"
      data-cy="button-ignore-errors"
    />
    <typography v-if="!!errorMessage" :value="errorMessage" color="negative" />
  </flex-box>
</template>

<script lang="ts">
/**
 * Displays any errors for this panel.
 */
export default {
  name: "UploadPanelErrors",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { FilePanelProps } from "@/types";
import { integrationsStore } from "@/hooks";
import { SwitchInput, FlexBox, Typography } from "@/components/common";

const props = defineProps<FilePanelProps>();

const errorMessage = computed(() => {
  if (
    (props.panel.variant === "artifact" || props.panel.variant === "trace") &&
    !props.panel.name
  ) {
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
      !props.panel.bulkFiles.find(({ name }) => name === "tim.json")) &&
    !props.panel.emptyFiles
  ) {
    return "Requires a tim.json configuration file.";
  } else {
    return props.panel.parseErrorMessage;
  }
});

// Update the panel validity and error when the error check updates.
watch(
  () => errorMessage.value,
  (message) => {
    props.panel.errorMessage = message;
    props.panel.valid = !message;
  }
);
</script>
