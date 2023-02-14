<template>
  <modal :is-open="!!isOpen" :title="modalTitle" @close="handleClose">
    <template #body>
      <flex-box t="4">
        <v-text-field
          v-model="editedModel.name"
          filled
          label="Model Name"
          class="mr-1"
          hide-details
        />
        <gen-method-input
          v-if="!isUpdate"
          v-model="editedModel.baseModel"
          only-trainable
          style="max-width: 200px"
        />
      </flex-box>
    </template>
    <template #actions>
      <v-spacer />
      <v-btn :disabled="!canSave" color="primary" @click="handleSave">
        Save
      </v-btn>
    </template>
  </modal>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { GenerationModelSchema } from "@/types";
import { modelSaveStore } from "@/hooks";
import { handleSaveModel } from "@/api";
import { Modal, GenMethodInput, FlexBox } from "@/components/common";

/**
 * A modal for creating and editing models.
 *
 * @emits-1 `close` - On close.
 */
export default defineComponent({
  name: "ModelCreatorModal",
  components: {
    Modal,
    GenMethodInput,
    FlexBox,
  },
  props: {
    isOpen: Boolean,
  },
  computed: {
    /**
     * @return Whether an existing model is being updated.
     */
    isUpdate(): boolean {
      return modelSaveStore.isUpdate;
    },
    /**
     * @return The model being edited.
     */
    editedModel(): GenerationModelSchema {
      return modelSaveStore.editedModel;
    },
    /**
     * @return The name of the modal.
     */
    modalTitle(): string {
      return this.isUpdate ? "Edit Model" : "Create Model";
    },
    /**
     * @return Whether the model can be saved.
     */
    canSave(): boolean {
      return modelSaveStore.canSave;
    },
  },
  watch: {
    /**
     * Resets the modal when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      modelSaveStore.resetModel();
    },
  },
  methods: {
    /**
     * Emits an event to close the modal.
     */
    handleClose() {
      this.$emit("close");
    },
    /**
     * Saves the current model.
     */
    handleSave() {
      handleSaveModel({});
      this.handleClose();
    },
  },
});
</script>
