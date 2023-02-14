<template>
  <modal
    size="md"
    :is-open="isOpen"
    title="Delete Project"
    data-cy="modal-project-delete"
    @close="handleCancel"
  >
    <template #body>
      <typography
        t="2"
        el="p"
        value="Are you sure you want to delete this project? Type in the project's name to confirm deletion."
      />
      <v-text-field
        v-model="confirmText"
        hide-details
        :label="label"
        class="mt-4"
        filled
        data-cy="input-project-delete-name"
      />
    </template>
    <template #actions>
      <v-btn
        :disabled="!canDelete"
        color="error"
        class="ml-auto"
        data-cy="button-project-delete"
        @click="handleConfirm"
      >
        Delete
      </v-btn>
    </template>
  </modal>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { identifierSaveStore } from "@/hooks";
import { Modal, Typography } from "@/components/common";

/**
 * A modal for confirming project deletion.
 *
 * @emits-1 `confirm` - On delete confirm.
 * @emits-2 `cancel` - On delete cancel.
 */
export default defineComponent({
  name: "ConfirmProjectDelete",
  components: { Typography, Modal },
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
  watch: {
    /**
     * Clears the modal data when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.clearData();
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
});
</script>
