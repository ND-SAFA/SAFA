<template>
  <div v-if="isOpen">
    <v-text-field
      filled
      label="Name"
      class="mt-4"
      v-model="store.editedDocument.name"
      :error-messages="nameErrors"
      data-cy="input-document-name"
    />
    <v-select
      filled
      label="Type"
      v-model="store.editedDocument.type"
      :items="types"
      item-text="name"
      item-value="id"
      data-cy="input-document-type"
    />
    <artifact-type-input
      multiple
      label="Include Artifact Types"
      v-model="store.includedTypes"
      @blur="handleSaveTypes"
      data-cy="input-document-include-types"
    />
    <artifact-input
      label="Artifacts"
      v-model="store.editedDocument.artifactIds"
      data-cy="input-document-artifacts"
    />
    <switch-input
      class="ml-1"
      label="Include artifact children"
      v-model="store.includeChildren"
      data-cy="button-document-include-children"
    />
    <artifact-type-input
      v-if="store.includeChildren"
      multiple
      label="Include Child Types"
      v-model="store.includedChildTypes"
      @blur="handleSaveChildren"
      data-cy="input-document-include-child-types"
    />
    <artifact-input
      v-if="store.includeChildren"
      label="Child Artifacts"
      v-model="store.childIds"
      data-cy="input-document-child-artifacts"
    />

    <v-divider class="my-4" />
    <flex-box justify="space-between">
      <v-btn
        text
        v-if="isUpdate"
        color="error"
        @click="handleDelete"
        data-cy="button-document-delete"
      >
        <v-icon class="mr-1">mdi-delete</v-icon>
        Delete
      </v-btn>
      <v-spacer />
      <v-btn
        color="primary"
        :disabled="!canSave"
        data-cy="button-document-save"
        @click="handleSubmit"
      >
        <v-icon class="mr-1">mdi-content-save</v-icon>
        Save
      </v-btn>
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
} from "@/components/common";

/**
 * Allows for creating and editing documents.
 */
export default Vue.extend({
  name: "DocumentPanel",
  components: {
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
});
</script>
