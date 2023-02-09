<template>
  <div v-if="isOpen">
    <v-text-field
      v-model="store.editedDocument.name"
      filled
      label="Name"
      class="mt-4"
      :error-messages="nameErrors"
      data-cy="input-document-name"
    />
    <v-select
      v-model="store.editedDocument.type"
      filled
      label="Type"
      :items="types"
      item-text="name"
      item-value="id"
      data-cy="input-document-type"
    />
    <artifact-type-input
      v-model="store.includedTypes"
      multiple
      label="Include Artifact Types"
      data-cy="input-document-include-types"
      @blur="handleSaveTypes"
    />
    <artifact-input
      v-model="store.editedDocument.artifactIds"
      label="Artifacts"
      data-cy="input-document-artifacts"
    />
    <switch-input
      v-model="store.includeChildren"
      class="ml-1"
      label="Include artifact children"
      data-cy="button-document-include-children"
    />
    <artifact-type-input
      v-if="store.includeChildren"
      v-model="store.includedChildTypes"
      multiple
      label="Include Child Types"
      data-cy="input-document-include-child-types"
      @blur="handleSaveChildren"
    />
    <artifact-input
      v-if="store.includeChildren"
      v-model="store.childIds"
      label="Child Artifacts"
      data-cy="input-document-child-artifacts"
    />

    <v-divider class="my-4" />
    <flex-box justify="space-between">
      <text-button
        v-if="isUpdate"
        text
        variant="delete"
        data-cy="button-document-delete"
        @click="handleDelete"
      >
        Delete
      </text-button>
      <v-spacer />
      <text-button
        :disabled="!canSave"
        variant="save"
        data-cy="button-document-save"
        @click="handleSubmit"
      >
        Save
      </text-button>
    </flex-box>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { DocumentSchema } from "@/types";
import { documentTypeOptions } from "@/util";
import { appStore, documentSaveStore } from "@/hooks";
import { handleDeleteDocument, handleSaveDocument } from "@/api";
import {
  FlexBox,
  ArtifactInput,
  ArtifactTypeInput,
  SwitchInput,
  TextButton,
} from "@/components/common";

/**
 * Allows for creating and editing documents.
 */
export default Vue.extend({
  name: "DocumentPanel",
  components: {
    TextButton,
    FlexBox,
    SwitchInput,
    ArtifactTypeInput,
    ArtifactInput,
  },
  data() {
    return {
      types: documentTypeOptions(),
    };
  },
  computed: {
    /**
     * @return Whether this panel is open.
     */
    isOpen(): boolean {
      return appStore.isDetailsPanelOpen === "document";
    },
    /**
     * @return Whether an existing document is being updated.
     */
    isUpdate(): boolean {
      return documentSaveStore.isUpdate;
    },
    /**
     * @return Whether the current document name is valid.
     */
    isNameValid(): boolean {
      return documentSaveStore.isNameValid;
    },
    /**
     * @return Whether the current document is valid.
     */
    canSave(): boolean {
      return documentSaveStore.canSave;
    },
    /**
     * @return Document name errors to display.
     */
    nameErrors(): string[] {
      return documentSaveStore.editedDocument.name === ""
        ? []
        : documentSaveStore.nameErrors;
    },
    /**
     * @return The store for saving documents.
     */
    store(): typeof documentSaveStore {
      return documentSaveStore;
    },
    /**
     * @return The base document being edited.
     */
    baseDocument(): DocumentSchema | undefined {
      return documentSaveStore.baseDocument;
    },
  },
  watch: {
    /**
     * Reset the document when the modal is opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      documentSaveStore.resetDocument();
    },
    /**
     * Reset the document when the base document changes.
     */
    baseDocument() {
      documentSaveStore.resetDocument();
    },
  },
  methods: {
    /**
     * Emits a request to close the modal.
     */
    handleClose() {
      this.$emit("close");
    },
    /**
     * Generates artifacts to save on this document.
     */
    handleSaveTypes() {
      documentSaveStore.updateArtifacts();
    },
    /**
     * Generates child artifacts to save on this document.
     */
    handleSaveChildren() {
      documentSaveStore.updateChildArtifacts();
    },
    /**
     * Attempts to save the document.
     */
    handleSubmit() {
      handleSaveDocument({
        onSuccess: () => this.handleClose(),
      });
    },
    /**
     * Attempts to delete the document, after confirming.
     */
    handleDelete() {
      handleDeleteDocument({
        onSuccess: () => this.handleClose(),
      });
    },
  },
});
</script>
