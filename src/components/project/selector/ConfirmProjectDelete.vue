<template>
  <generic-modal
    size="md"
    :is-open="isOpen"
    :title="title"
    data-cy="modal-project-delete"
    @close="handleCancel"
  >
    <template v-slot:body>
      <v-text-field
        v-model="confirmText"
        :label="textboxLabel"
        class="ma-3"
        filled
        data-cy="input-project-delete-name"
      />
    </template>
    <template v-slot:actions>
      <v-btn
        :disabled="!validated"
        color="error"
        @click="handleConfirm"
        class="ml-auto"
        data-cy="button-project-delete"
      >
        Delete
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import { IdentifierModel } from "@/types";
import Vue, { PropType } from "vue";
import { GenericModal } from "@/components/common";

/**
 * A modal for confirming project deletion.
 *
 * @emits-1 `confirm` (string) - On delete confirm.
 * @emits-2 `cancel` - On delete cancel.
 */
export default Vue.extend({
  name: "ConfirmProjectDelete",
  components: { GenericModal },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    project: {
      type: Object as PropType<IdentifierModel>,
      required: false,
    },
  },
  data() {
    return {
      confirmText: "",
      textboxLabel: "",
      title: "",
      validated: false,
    };
  },
  methods: {
    /**
     * Clears modal data.
     */
    clearData(): void {
      this.confirmText = "";
      this.validated = false;
    },
    /**
     * Emits a request to confirm deleting this project.
     */
    handleConfirm() {
      if (this.validated) {
        this.$emit("confirm", this.project);
      }
    },
    /**
     * Emits a request to cancel deleting this project.
     */
    handleCancel() {
      this.$emit("cancel");
    },
  },
  watch: {
    /**
     * Updates the modal text when the project changes.
     */
    project(project: IdentifierModel | undefined) {
      if (!project) return;

      this.textboxLabel = `Type "${project.name}"`;
      this.title = `Deleting: ${project.name}`;
    },
    /**
     * Updates the validated status when the text changes.
     */
    confirmText() {
      this.validated = this.project && this.confirmText === this.project.name;
    },
    /**
     * Clears the modal data when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.clearData();
    },
  },
});
</script>
