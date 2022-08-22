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
      <v-autocomplete
        filled
        multiple
        label="Include Artifact Types"
        v-model="includedTypes"
        :items="artifactTypes"
        @blur="handleSaveTypes"
      />
      <artifact-input label="Artifacts" v-model="editingDocument.artifactIds" />
      <v-switch label="Include artifact children" v-model="includeChildren" />
      <v-autocomplete
        v-if="includeChildren"
        filled
        multiple
        label="Include Child Types"
        v-model="includedChildTypes"
        :items="artifactTypes"
        @blur="handleSaveChildren"
      />
      <artifact-input
        v-if="includeChildren"
        label="Child Artifacts"
        v-model="childIds"
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
import { documentModule, subtreeModule } from "@/store";
import { artifactStore } from "@/hooks";
import { typeOptionsStore } from "@/hooks";
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
      return typeOptionsStore.artifactTypes;
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
      this.editingDocument.artifactIds = artifactStore.allArtifacts
        .filter(({ type }) => this.includedTypes.includes(type))
        .map(({ id }) => id);
    },
    /**
     * Generates children to save on this document.
     */
    handleSaveChildren() {
      this.childIds = subtreeModule.getMatchingChildren(
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
      this.includeChildren = false;
      this.includedChildTypes = [];
    },
  },
});
</script>
