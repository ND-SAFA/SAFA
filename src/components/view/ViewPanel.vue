<template>
  <details-panel panel="document" @open="handleReset">
    <panel-card title="Save View" borderless>
      <text-input
        v-model="editedDocument.name"
        label="Name"
        :error-message="nameError"
        data-cy="input-document-name"
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
 * Allows for creating and editing views.
 */
export default {
  name: "ViewPanel",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { appStore, viewApiStore, documentSaveStore } from "@/hooks";
import {
  ArtifactInput,
  ArtifactTypeInput,
  FlexBox,
  SwitchInput,
  TextButton,
  PanelCard,
  TextInput,
  DetailsPanel,
} from "@/components/common";

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
  appStore.close("detailsPanel");
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
  viewApiStore.handleSave({
    onSuccess: () => handleClose(),
  });
}

/**
 * Attempts to delete the document after confirming.
 */
function handleDelete() {
  viewApiStore.handleDelete({
    onSuccess: () => handleClose(),
  });
}

watch(() => documentSaveStore.baseDocument, handleReset);
</script>
