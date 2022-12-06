<template>
  <modal :is-open="!!isOpen" :title="modalTitle" @close="handleClose">
    <template v-slot:body>
      <flex-box t="4">
        <v-text-field
          filled
          v-model="editedModel.name"
          label="Model Name"
          class="mr-1"
          hide-details
        />
        <gen-method-input
          v-if="!isUpdate"
          only-trainable
          v-model="editedModel.baseModel"
          style="max-width: 200px"
        />
      </flex-box>
    </template>
    <template v-slot:actions>
      <v-spacer />
      <v-btn :disabled="!canSave" color="primary" @click="handleSave">
        Save
      </v-btn>
    </template>
  </modal>
</template>

<script lang="ts">
import Vue from "vue";
import { GenerationModelSchema } from "@/types";
import { modelSaveStore } from "@/hooks";
import { handleSaveModel } from "@/api";
import { Modal, GenMethodInput, FlexBox } from "@/components/common";

/**
 * A modal for creating and editing models.
 *
 * @emits-1 `close` - On close.
 */
export default Vue.extend({
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
  watch: {
    /**
     * Resets the modal when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      modelSaveStore.resetModel();
    },
  },
});
</script>
