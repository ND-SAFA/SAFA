<template>
  <modal :is-open="!!isOpen" title="Share Model" @close="handleClose">
    <template #body>
      <flex-box column t="4">
        <project-input v-model="projectId" exclude-current-project />
        <v-select
          v-model="shareMethod"
          filled
          hide-details
          label="Share Method"
          :items="shareMethods"
          item-value="id"
          item-text="name"
        />
      </flex-box>
    </template>
    <template #actions>
      <v-spacer />
      <v-btn :disabled="!canSave" color="primary" @click="handleSave">
        Share
      </v-btn>
    </template>
  </modal>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import {
  IdentifierSchema,
  ModelShareType,
  GenerationModelSchema,
} from "@/types";
import { modelShareOptions } from "@/util";
import { projectStore } from "@/hooks";
import { handleShareModel } from "@/api";
import { FlexBox, Modal, ProjectInput } from "@/components/common";

/**
 * A modal for sharing models.
 *
 * @emits-1 `close` - On close.
 */
export default defineComponent({
  name: "ModelShareModal",
  components: {
    ProjectInput,
    Modal,
    FlexBox,
  },
  props: {
    isOpen: Boolean,
    model: Object as PropType<GenerationModelSchema | undefined>,
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
    projects(): IdentifierSchema[] {
      return projectStore.unloadedProjects;
    },
    /**
     * @return Whether the model can be shared.
     */
    canSave(): boolean {
      return this.projectId !== "" && !!this.model;
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
});
</script>
