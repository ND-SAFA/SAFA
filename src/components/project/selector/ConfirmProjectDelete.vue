<template>
  <generic-modal
    size="md"
    :is-open="isOpen"
    title="Delete Project"
    data-cy="modal-project-delete"
    @close="handleCancel"
  >
    <template v-slot:body>
      <v-text-field
        hide-details
        v-model="confirmText"
        :label="label"
        class="mt-4"
        filled
        data-cy="input-project-delete-name"
      />
    </template>
    <template v-slot:actions>
      <v-btn
        :disabled="!canDelete"
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
import Vue from "vue";
import { identifierSaveStore } from "@/hooks";
import { GenericModal } from "@/components/common";

/**
 * A modal for confirming project deletion.
 *
 * @emits-1 `confirm` - On delete confirm.
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
  },
  data() {
    return {
      confirmText: "",
    };
  },
  computed: {
    /**
     * @return The name of the project being deleted.
     */
    projectName(): string {
      return identifierSaveStore.baseIdentifier?.name || "";
    },
    /**
     * @return The project name input label.
     */
    label(): string {
      return `Type "${this.projectName}"`;
    },
    /**
     * @return Whether the project can be deleted.
     */
    canDelete(): boolean {
      return this.confirmText === this.projectName;
    },
  },
  methods: {
    /**
     * Clears modal data.
     */
    clearData(): void {
      this.confirmText = "";
    },
    /**
     * Emits a request to confirm deleting this project.
     */
    handleConfirm() {
      this.$emit("confirm");
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
     * Clears the modal data when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.clearData();
    },
  },
});
</script>
