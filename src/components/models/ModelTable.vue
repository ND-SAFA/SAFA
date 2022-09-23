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
      <model-creator-modal
        :model="currentItem"
        :is-open="isModalOpen"
        @close="isModalOpen = false"
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
  </generic-selector>
</template>

<script lang="ts">
import Vue from "vue";
import { TrainedModel } from "@/types";
import { projectStore } from "@/hooks";
import { handleDeleteModel, handleLoadModels } from "@/api";
import {
  AttributeChip,
  FlexBox,
  GenericSelector,
  Typography,
} from "@/components/common";
import ModelCreatorModal from "./ModelCreatorModal.vue";

/**
 * Renders a table of project models
 */
export default Vue.extend({
  name: "ModelTable",
  components: {
    ModelCreatorModal,
    AttributeChip,
    FlexBox,
    GenericSelector,
    Typography,
  },
  data() {
    return {
      isModalOpen: false,
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
      this.isModalOpen = false;
    },
    /**
     * Opens the modal to add a model.
     */
    handleAdd() {
      this.isModalOpen = true;
    },
    /**
     * Opens the modal to edit a model.
     * @param model - The model to edit.
     */
    handleEdit(model: TrainedModel) {
      this.currentItem = model;
      this.isModalOpen = true;
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
