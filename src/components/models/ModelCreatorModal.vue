<template>
  <generic-modal
    :is-open="!!isOpen"
    :is-loading="isLoading"
    :title="creatorTitle"
    @close="handleClose"
  >
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
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TrainedModel } from "@/types";
import { createModel } from "@/util";
import { GenericModal, GenMethodInput, FlexBox } from "@/components/common";

/**
 * A modal for creating and editing models.
 *
 * @emits-1 `close` - On close.
 */
export default Vue.extend({
  name: "ModelCreatorModal",
  components: {
    GenericModal,
    GenMethodInput,
    FlexBox,
  },
  props: {
    isOpen: Boolean,
    model: Object as PropType<TrainedModel | undefined>,
  },
  data() {
    return {
      isLoading: false,
      canSave: false,
      editedModel: createModel(this.model),
    };
  },
  computed: {
    /**
     * @return The name of the modal.
     */
    creatorTitle(): string {
      return this.model ? "Edit Model" : "Create Model";
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
    handleSave() {},
  },
  watch: {
    /**
     * Resets the modal when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.editedModel = createModel(this.model);
      this.canSave = this.editedModel.name !== "";
    },
    /**
     * Checks whether the model is valid when it changes.
     */
    editedModel: {
      handler(): void {
        this.canSave = this.editedModel.name !== "";
      },
      deep: true,
    },
  },
});
</script>
