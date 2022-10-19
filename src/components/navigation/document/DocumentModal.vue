<template>
  <generic-modal
    :title="modalTitle"
    size="sm"
    :is-open="isOpen"
    data-cy="modal-document-save"
    @close="handleClose"
  >
    <template v-slot:body>
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
      <generic-switch
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
    </template>
    <template v-slot:actions>
      <v-btn
        v-if="isUpdate"
        color="error"
        :text="!confirmDelete"
        :outlined="confirmDelete"
        @click="handleDelete"
        data-cy="button-document-delete"
      >
        {{ deleteButtonText }}
      </v-btn>
      <v-btn outlined v-if="confirmDelete" @click="confirmDelete = false">
        Cancel
      </v-btn>
      <v-spacer />
      <v-btn
        color="primary"
        :disabled="!canSave"
        data-cy="button-document-save"
        @click="handleSubmit"
      >
        Confirm
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { documentTypeOptions } from "@/util";
import { documentSaveStore } from "@/hooks";
import { handleDeleteDocument, handleSaveDocument } from "@/api";
import {
  ArtifactInput,
  GenericModal,
  ArtifactTypeInput,
  GenericSwitch,
} from "@/components/common";

/**
 * A modal for adding or editing documents.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "DocumentModal",
  components: { GenericSwitch, ArtifactTypeInput, GenericModal, ArtifactInput },
  props: {
    isOpen: Boolean,
  },
  data() {
    return {
      confirmDelete: false,
      types: documentTypeOptions(),
    };
  },
  computed: {
    /**
     * @return Whether an existing document is being updated.
     */
    isUpdate(): boolean {
      return documentSaveStore.isUpdate;
    },
    /**
     * @return The modal title.
     */
    modalTitle(): string {
      return this.isUpdate ? "Edit View" : "Add View";
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
     * @return The text to display on the delete button.
     */
    deleteButtonText(): string {
      return this.confirmDelete ? "Delete" : "Delete Document";
    },
    /**
     * @return The store for saving documents.
     */
    store(): typeof documentSaveStore {
      return documentSaveStore;
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
      if (!this.confirmDelete) {
        this.confirmDelete = true;
      } else {
        handleDeleteDocument({
          onSuccess: () => this.handleClose(),
        });
      }
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
  },
});
</script>
