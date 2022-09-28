<template>
  <generic-modal :is-open="!!isOpen" title="Share Model" @close="handleClose">
    <template v-slot:body>
      <flex-box column t="4">
        <project-input v-model="projectId" exclude-current-project />
        <v-select
          filled
          hide-details
          label="Share Method"
          v-model="shareMethod"
          :items="shareMethods"
          item-value="id"
          item-text="name"
        />
      </flex-box>
    </template>
    <template v-slot:actions>
      <v-spacer />
      <v-btn :disabled="!canSave" color="primary" @click="handleSave">
        Share
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { IdentifierModel, ModelShareType, TrainedModel } from "@/types";
import { modelShareOptions } from "@/util";
import { projectStore } from "@/hooks";
import { handleShareModel } from "@/api";
import { FlexBox, GenericModal } from "@/components/common";
import ProjectInput from "@/components/common/input/ProjectInput.vue";

/**
 * A modal for sharing models.
 *
 * @emits-1 `close` - On close.
 */
export default Vue.extend({
  name: "ModelShareModal",
  components: {
    ProjectInput,
    GenericModal,
    FlexBox,
  },
  props: {
    isOpen: Boolean,
    model: Object as PropType<TrainedModel | undefined>,
  },
  data() {
    return {
      projectId: "",
      shareMethod: ModelShareType.CLONE,
      shareMethods: modelShareOptions(),
    };
  },
  computed: {
    /**
     * @return All unloaded projects for the current user.
     */
    projects(): IdentifierModel[] {
      return projectStore.unloadedProjects;
    },
    /**
     * @return Whether the model can be shared.
     */
    canSave(): boolean {
      return this.projectId !== "" && !!this.model;
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
      if (!this.model || !this.projectId) return;

      handleShareModel(this.projectId, this.model, this.shareMethod);

      this.handleClose();
    },
  },
  watch: {
    /**
     * Resets the modal when opened.
     */
    isOpen(open: boolean) {
      if (!open) return;

      this.projectId = "";
      this.shareMethod = ModelShareType.CLONE;
    },
  },
});
</script>
