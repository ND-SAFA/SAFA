<template>
  <generic-selector
    is-open
    :has-select="false"
    :has-edit="false"
    :headers="headers"
    :items="items"
    item-key="id"
    class="model-table mt-5"
    @item:add="handleAdd"
    @item:edit="handleEdit"
    @item:delete="handleDelete"
    @refresh="handleRefresh"
  >
    <template v-slot:addItemDialogue>
      <model-creator-modal :is-open="isSaveOpen" @close="handleClose" />
      <model-share-modal
        :model="currentItem"
        :is-open="isShareOpen"
        @close="handleClose"
      />
    </template>
    <template v-slot:expanded-item="{ item }">
      <div class="my-2">
        <typography
          el="h2"
          variant="subtitle"
          value="Default Trace Directions"
        />
        <flex-box
          v-for="(direction, idx) in item.defaultTraceDirections"
          :key="idx"
        >
          <attribute-chip artifact-type :value="direction.source" />
          <v-icon>mdi-arrow-right</v-icon>
          <attribute-chip artifact-type :value="direction.target" />
        </flex-box>
        <typography t="2" el="h2" variant="subtitle" value="Training Runs" />
        <typography secondary value="There are no training runs." />
        <typography t="2" el="h2" variant="subtitle" value="Evaluation Runs" />
        <typography secondary value="There are no evaluation runs." />
      </div>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <generic-icon-button
        icon-id="mdi-share-variant"
        tooltip="Share Model"
        @click="handleShare(item)"
      />
    </template>
  </generic-selector>
</template>

<script lang="ts">
import Vue from "vue";
import { TrainedModel } from "@/types";
import { modelSaveStore, projectStore } from "@/hooks";
import { handleDeleteModel, handleLoadModels } from "@/api";
import {
  AttributeChip,
  FlexBox,
  GenericSelector,
  Typography,
  GenericIconButton,
} from "@/components/common";
import ModelShareModal from "./ModelShareModal.vue";
import ModelCreatorModal from "./ModelCreatorModal.vue";

/**
 * Renders a table of project models
 */
export default Vue.extend({
  name: "ModelTable",
  components: {
    ModelShareModal,
    GenericIconButton,
    ModelCreatorModal,
    AttributeChip,
    FlexBox,
    GenericSelector,
    Typography,
  },
  data() {
    return {
      isSaveOpen: false,
      isShareOpen: false,
      headers: [
        { text: "Name", value: "name" },
        { text: "Base Model", value: "baseModel" },
        { text: "Actions", value: "actions", sortable: false },
      ],
      currentItem: undefined as TrainedModel | undefined,
    };
  },
  computed: {
    /**
     * @return All project models.
     */
    items(): TrainedModel[] {
      return projectStore.models;
    },
  },
  methods: {
    /**
     * Closes the model modal.
     */
    handleClose() {
      this.isSaveOpen = false;
      this.isShareOpen = false;
      this.currentItem = undefined;
    },
    /**
     * Opens the modal to add a model.
     */
    handleAdd() {
      modelSaveStore.baseModel = undefined;
      this.isSaveOpen = true;
    },
    /**
     * Opens the modal to edit a model.
     * @param model - The model to edit.
     */
    handleEdit(model: TrainedModel) {
      modelSaveStore.baseModel = model;
      this.currentItem = model;
      this.isSaveOpen = true;
    },
    /**
     * Opens the modal to share a model.
     * @param model - The model to share.
     */
    handleShare(model: TrainedModel) {
      this.currentItem = model;
      this.isShareOpen = true;
    },
    /**
     * Opens the modal to delete a model.
     * @param model - The model to delete.
     */
    handleDelete(model: TrainedModel) {
      handleDeleteModel(model);
    },
    /**
     * Refreshes the loaded models.
     */
    handleRefresh() {
      handleLoadModels();
    },
  },
});
</script>
