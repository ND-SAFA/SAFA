<template>
  <details-panel panel="document" @open="handleReset">
    <panel-card>
      <text-input
        v-model="editedDocument.name"
        label="Name"
        :error-message="nameError"
        data-cy="input-document-name"
      />
      <select-input
        v-model="editedDocument.type"
        label="Type"
        :options="typeOptions"
        option-label="name"
        option-value="id"
        option-to-value
        class="q-mb-md"
        data-cy="input-document-type"
      />
      <artifact-type-input
        v-model="store.includedTypes"
        multiple
        label="Include Artifact Types"
        class="q-mb-md"
        data-cy="input-document-include-types"
        @blur="handleSaveTypes"
      />
      <artifact-input
        v-model="editedDocument.artifactIds"
        multiple
        label="Artifacts"
        class="q-mb-md"
        data-cy="input-document-artifacts"
      />
      <switch-input
        v-model="store.includeChildren"
        label="Include artifact children"
        class="q-mb-md"
        data-cy="button-document-include-children"
      />
      <artifact-type-input
        v-if="includeChildren"
        v-model="store.includedChildTypes"
        multiple
        label="Include Child Types"
        class="q-mb-md"
        data-cy="input-document-include-child-types"
        @blur="handleSaveChildren"
      />
      <artifact-input
        v-if="includeChildren"
        v-model="store.childIds"
        multiple
        label="Child Artifacts"
        class="q-mb-md"
        data-cy="input-document-child-artifacts"
      />

      <template #actions>
        <flex-box full-width justify="between">
          <text-button
            v-if="isUpdate"
            text
            label="Delete"
            icon="delete"
            data-cy="button-document-delete"
            @click="handleDelete"
          />
          <q-space />
          <text-button
            :disabled="!canSave"
            label="Save"
            icon="save"
            data-cy="button-document-save"
            @click="handleSubmit"
          />
        </flex-box>
      </template>
    </panel-card>
  </details-panel>
</template>

<script lang="ts">
/**
 * Allows for creating and editing documents.
 */
export default {
  name: "DocumentPanel",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { PanelType } from "@/types";
import { documentTypeOptions } from "@/util";
import { appStore, documentSaveStore } from "@/hooks";
import { handleDeleteDocument, handleSaveDocument } from "@/api";
import {
  ArtifactInput,
  ArtifactTypeInput,
  FlexBox,
  SwitchInput,
  TextButton,
  PanelCard,
  TextInput,
  SelectInput,
  DetailsPanel,
} from "@/components/common";

const typeOptions = documentTypeOptions();

const store = computed(() => documentSaveStore);
const isUpdate = computed(() => documentSaveStore.isUpdate);
const canSave = computed(() => documentSaveStore.canSave);
const nameError = computed(() => documentSaveStore.nameError);
const editedDocument = computed(() => documentSaveStore.editedDocument);
const includeChildren = computed(() => documentSaveStore.includeChildren);

/**
 * Resets the document fields when opened.
 */
function handleReset(): void {
  documentSaveStore.resetDocument();
}

/**
 * Closes the document panel.
 */
function handleClose() {
  appStore.closePanel(PanelType.detailsPanel);
}

/**
 * Generates artifacts to save on this document.
 */
function handleSaveTypes() {
  documentSaveStore.updateArtifacts();
}

/**
 * Generates child artifacts to save on this document.
 */
function handleSaveChildren() {
  documentSaveStore.updateChildArtifacts();
}

/**
 * Attempts to save the document.
 */
function handleSubmit() {
  handleSaveDocument({
    onSuccess: () => handleClose(),
  });
}

/**
 * Attempts to delete the document after confirming.
 */
function handleDelete() {
  handleDeleteDocument({
    onSuccess: () => handleClose(),
  });
}

watch(() => documentSaveStore.baseDocument, handleReset);
</script>
