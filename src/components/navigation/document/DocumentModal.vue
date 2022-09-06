<template>
  <generic-modal
    :title="title"
    size="sm"
    :is-open="isOpen"
    data-cy="modal-document-save"
    @close="resetModalData"
  >
    <template v-slot:body>
      <v-text-field
        filled
        label="Name"
        class="mt-4"
        v-model="editingDocument.name"
        :error-messages="nameErrors"
        data-cy="input-document-name"
      />
      <v-select
        filled
        label="Type"
        v-model="editingDocument.type"
        :items="types"
        item-text="name"
        item-value="id"
        data-cy="input-document-type"
      />
      <artifact-type-input
        multiple
        label="Include Artifact Types"
        v-model="includedTypes"
        @blur="handleSaveTypes"
        data-cy="input-document-include-types"
      />
      <artifact-input
        label="Artifacts"
        v-model="editingDocument.artifactIds"
        data-cy="input-document-artifacts"
      />
      <v-switch
        label="Include artifact children"
        v-model="includeChildren"
        data-cy="button-document-include-children"
      />
      <artifact-type-input
        v-if="includeChildren"
        multiple
        label="Include Child Types"
        v-model="includedChildTypes"
        @blur="handleSaveChildren"
        data-cy="input-document-include-child-types"
      />
      <artifact-input
        v-if="includeChildren"
        label="Child Artifacts"
        v-model="childIds"
        data-cy="input-document-child-artifacts"
      />
    </template>
    <template v-slot:actions>
      <v-btn
        v-if="isEditMode"
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
        :disabled="!isValid"
        data-cy="button-document-save"
        @click="handleSubmit"
      >
        Confirm
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DocumentModel } from "@/types";
import { createDocument, documentTypeOptions } from "@/util";
import { artifactStore, documentStore, subtreeStore } from "@/hooks";
import { handleDeleteDocument, handleSaveDocument } from "@/api";
import {
  ArtifactInput,
  GenericModal,
  ArtifactTypeInput,
} from "@/components/common";

/**
 * A modal for adding or editing documents.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "DocumentModal",
  components: { ArtifactTypeInput, GenericModal, ArtifactInput },
  props: {
    isOpen: Boolean,
    document: {
      type: Object as PropType<DocumentModel>,
      required: false,
    },
  },
  data() {
    return {
      editingDocument: createDocument(this.document),
      confirmDelete: false,
      isValid: false,
      types: documentTypeOptions(),
      includedTypes: [] as string[],
      includeChildren: false,
      includedChildTypes: [] as string[],
      childIds: [] as string[],
    };
  },
  computed: {
    /**
     * @return Whether the document is in edit mode.
     */
    isEditMode(): boolean {
      return !!this.document;
    },
    /**
     * @return The modal title.
     */
    title(): string {
      return this.isEditMode ? "Edit View" : "Add View";
    },
    /**
     * @return Whether the current document name is valid.
     */
    isNameValid(): boolean {
      return (
        !documentStore.doesDocumentExist(this.editingDocument?.name) ||
        this.editingDocument.name === this.document?.name
      );
    },
    /**
     * @return Whether the current document is valid.
     */
    isDocumentValid(): boolean {
      return !!this.editingDocument.name && this.isNameValid;
    },
    /**
     * @return Document name errors to display.
     */
    nameErrors(): string[] {
      return this.isNameValid ? [] : ["This name already exists"];
    },
    /**
     * @return The text to display on the delete button.
     */
    deleteButtonText(): string {
      return this.confirmDelete ? "Delete" : "Delete Document";
    },
  },
  methods: {
    /**
     * Resets all modal data.
     */
    resetModalData() {
      this.includeChildren = false;
      this.includedChildTypes = [];
      this.childIds = [];
      this.editingDocument = createDocument(this.document);
      this.confirmDelete = false;
      this.$emit("close");
    },
    /**
     * Generates children to save on this document.
     */
    handleSaveTypes() {
      const baseArtifacts = this.document?.artifactIds || [];

      this.editingDocument.artifactIds =
        this.includedTypes.length > 0
          ? artifactStore.allArtifacts
              .filter(
                ({ id, type }) =>
                  this.includedTypes.includes(type) ||
                  baseArtifacts.includes(id)
              )
              .map(({ id }) => id)
          : baseArtifacts;
    },
    /**
     * Generates children to save on this document.
     */
    handleSaveChildren() {
      this.childIds = subtreeStore.getMatchingChildren(
        this.editingDocument.artifactIds,
        this.includedChildTypes
      );
    },
    /**
     * Attempts to save the document.
     */
    handleSubmit() {
      const artifactIds = this.includeChildren
        ? [...this.editingDocument.artifactIds, ...this.childIds]
        : this.editingDocument.artifactIds;

      handleSaveDocument(
        {
          ...this.editingDocument,
          artifactIds,
        },
        this.isEditMode,
        {
          onSuccess: () => this.resetModalData(),
        }
      );
    },
    /**
     * Attempts to delete the document, after confirming.
     */
    handleDelete() {
      if (!this.confirmDelete) {
        this.confirmDelete = true;
      } else if (this.editingDocument) {
        handleDeleteDocument(this.editingDocument, {
          onSuccess: () => this.resetModalData(),
        });
      }
    },
  },
  watch: {
    /**
     * Whenever any document field changes, check whether the document is valid.
     */
    editingDocument: {
      handler() {
        this.isValid = this.isDocumentValid;
      },
      deep: true,
    },
    /**
     * Reset the document when the modal is opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.editingDocument = createDocument(this.document);
    },
  },
});
</script>
