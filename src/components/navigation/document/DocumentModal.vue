<template>
  <generic-modal
    :title="title"
    size="sm"
    :is-open="isOpen"
    @close="resetModalData"
  >
    <template v-slot:body>
      <v-text-field
        filled
        label="Name"
        class="mt-4"
        v-model="editingDocument.name"
        :error-messages="nameErrors"
      />
      <v-select
        filled
        label="Type"
        v-model="editingDocument.type"
        :items="types"
        item-text="name"
        item-value="id"
      />
      <artifact-input v-model="editingDocument.artifactIds" />
      <v-switch
        class="my-0 py-0"
        label="Include artifact children"
        v-model="includeChildren"
      />
      <v-autocomplete
        v-if="includeChildren"
        filled
        multiple
        label="Included Child Types"
        v-model="includedChildTypes"
        :items="artifactTypes"
      />
    </template>
    <template v-slot:actions>
      <v-btn
        v-if="isEditMode"
        color="error"
        :text="!confirmDelete"
        :outlined="confirmDelete"
        @click="handleDelete"
      >
        {{ deleteButtonText }}
      </v-btn>
      <v-btn outlined v-if="confirmDelete" @click="confirmDelete = false">
        Cancel
      </v-btn>
      <v-spacer />
      <v-btn color="primary" :disabled="!isValid" @click="handleSubmit">
        Confirm
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { DocumentModel } from "@/types";
import { createDocument, documentTypeOptions } from "@/util";
import { documentModule, typeOptionsModule } from "@/store";
import { handleDeleteDocument, handleSaveDocument } from "@/api";
import { ArtifactInput, GenericModal } from "@/components/common";

/**
 * A modal for adding or editing documents.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "DocumentModal",
  components: { GenericModal, ArtifactInput },
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
      includeChildren: false,
      includedChildTypes: [] as string[],
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
      return this.isEditMode ? "Edit Document" : "Add Document";
    },
    /**
     * @return Whether the current document name is valid.
     */
    isNameValid(): boolean {
      return (
        !documentModule.doesDocumentExist(this.editingDocument?.name) ||
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
    /**
     * @return All types of artifacts
     */
    artifactTypes(): string[] {
      return typeOptionsModule.artifactTypes;
    },
  },
  methods: {
    /**
     * Resets all modal data.
     */
    resetModalData() {
      this.editingDocument = createDocument(this.document);
      this.confirmDelete = false;
      this.$emit("close");
    },
    /**
     * Attempts to save the document.
     */
    handleSubmit() {
      handleSaveDocument(
        this.editingDocument,
        this.isEditMode,
        this.includeChildren ? this.includedChildTypes : [],
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
      this.includeChildren = false;
      this.includedChildTypes = [];
    },
  },
});
</script>
