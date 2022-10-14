<template>
  <generic-modal
    :is-open="isOpen"
    :title="modelTitle"
    size="m"
    :is-loading="isLoading"
    data-cy="modal-project-edit"
    :actions-height="0"
    @close="handleClose"
  >
    <template v-slot:body>
      <project-files-uploader
        v-if="doShowUpload"
        v-bind:name.sync="identifier.name"
        v-bind:description.sync="identifier.description"
        data-cy-name="input-project-name-modal"
        data-cy-description="input-project-description-modal"
      />
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { IdentifierModel } from "@/types";
import { identifierSaveStore } from "@/hooks";
import { GenericModal } from "@/components/common";
import ProjectFilesUploader from "./ProjectFilesUploader.vue";

/**
 * A modal for creating or editing a project.
 *
 * @emits-1 `close` - On close.
 * @emits-2 `save` - On project save.
 */
export default Vue.extend({
  name: "ProjectIdentifierModal",
  components: {
    GenericModal,
    ProjectFilesUploader,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    isLoading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    /**
     * @return  The identifier being updated.
     */
    identifier(): IdentifierModel {
      return identifierSaveStore.editedIdentifier;
    },
    /**
     * @return Whether an existing identifier is being updated.
     */
    isUpdate(): boolean {
      return identifierSaveStore.isUpdate;
    },
    modelTitle(): string {
      return this.isUpdate ? "Edit Project" : "Create Project";
    },
    /**
     * @return Whether to show the file upload.
     */
    doShowUpload(): boolean {
      return !this.isUpdate;
    },
  },
  methods: {
    /**
     * Emits a request to close.
     */
    handleClose() {
      this.$emit("close");
    },
    /**
     * Emits a request to save a project.
     */
    handleSave() {
      this.$emit("save");
    },
  },
  watch: {
    /**
     * Resets identifier data when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      identifierSaveStore.resetIdentifier();
    },
  },
});
</script>
