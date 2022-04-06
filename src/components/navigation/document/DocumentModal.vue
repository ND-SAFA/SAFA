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
    </template>
    <template v-slot:actions>
      <v-btn
        v-if="isEditMode"
        color="error"
        :text="!confirmDelete"
        :outlined="confirmDelete"
        @click="handleDelete"
      >
        {{ confirmDelete ? "Delete" : "Delete Document" }}
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
import { ProjectDocument } from "@/types";
import { createDocument, documentTypeOptions } from "@/util";
import { addNewDocument, deleteAndSwitchDocuments, editDocument } from "@/api";
import { documentModule, logModule } from "@/store";
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
      type: Object as PropType<ProjectDocument>,
      required: false,
    },
  },
  data() {
    return {
      editingDocument: createDocument(this.document),
      confirmDelete: false,
      isValid: false,
    };
  },
  computed: {
    isEditMode(): boolean {
      return !!this.document;
    },
    title(): string {
      return this.isEditMode ? "Edit Document" : "Add Document";
    },
    types: documentTypeOptions,

    isNameValid(): boolean {
      return (
        !documentModule.doesDocumentExist(this.document?.name) ||
        this.editingDocument.name === this.document?.name
      );
    },
    isDocumentValid(): boolean {
      return !!this.editingDocument.name && this.isNameValid;
    },
    nameErrors(): string[] {
      return this.isNameValid ? [] : ["This name already exists"];
    },
  },
  methods: {
    resetModalData() {
      this.editingDocument = createDocument(this.document);
      this.confirmDelete = false;
      this.$emit("close");
    },
    handleSubmit() {
      if (this.isEditMode) {
        editDocument(this.editingDocument)
          .then(() => {
            logModule.onSuccess(
              `Document edited: ${this.editingDocument.name}`
            );
            this.resetModalData();
          })
          .catch(() => {
            logModule.onError(
              `Unable to edit document: ${this.editingDocument.name}`
            );
          });
      } else {
        const { name, type, artifactIds } = this.editingDocument;

        addNewDocument(name, type, artifactIds)
          .then(() => {
            logModule.onSuccess(`Document created: ${name}`);
            this.resetModalData();
          })
          .catch(() => {
            logModule.onError(`Unable to create document: ${name}`);
          });
      }
    },
    handleDelete() {
      if (!this.confirmDelete) {
        this.confirmDelete = true;
      } else if (this.editingDocument) {
        deleteAndSwitchDocuments(this.editingDocument)
          .then(() => {
            logModule.onSuccess(
              `Document Deleted: ${this.editingDocument.name}`
            );
            this.resetModalData();
          })
          .catch(() => {
            logModule.onError(
              `Unable to delete document: ${this.editingDocument.name}`
            );
          });
      }
    },
  },
  watch: {
    editingDocument: {
      handler() {
        this.isValid = this.isDocumentValid;
      },
      deep: true,
    },
    isOpen(open: boolean) {
      if (!open) return;

      this.editingDocument = createDocument(this.document);
    },
  },
});
</script>
