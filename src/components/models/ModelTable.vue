<template>
  <v-container>
    <typography
      el="p"
      b="4"
      value="Create a new model below, or expand one of the models to view past training and add new steps."
    />
    <generic-selector
      is-open
      show-expand
      :has-select="false"
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
        <ModelEditor :model="item" />
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <generic-icon-button
          icon-id="mdi-share-variant"
          tooltip="Share Model"
          @click="handleShare(item)"
        />
      </template>
    </generic-selector>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { GenerationModel } from "@/types";
import { modelSaveStore, projectStore } from "@/hooks";
import { handleDeleteModel, handleLoadModels } from "@/api";
import {
  GenericSelector,
  GenericIconButton,
  Typography,
} from "@/components/common";
import ModelShareModal from "./ModelShareModal.vue";
import ModelCreatorModal from "./ModelCreatorModal.vue";
import { ModelEditor } from "./editor";

/**
 * Renders a table of project models.
 */
export default Vue.extend({
  name: "ModelTable",
  components: {
    ModelShareModal,
    ModelCreatorModal,
    GenericIconButton,
    ModelEditor,
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
      currentItem: undefined as GenerationModel | undefined,
    };
  },
  computed: {
    /**
     * @return All project models.
     */
    items(): GenerationModel[] {
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
    handleEdit(model: GenerationModel) {
      modelSaveStore.baseModel = model;
      this.currentItem = model;
      this.isSaveOpen = true;
    },
    /**
     * Opens the modal to share a model.
     * @param model - The model to share.
     */
    handleShare(model: GenerationModel) {
      this.currentItem = model;
      this.isShareOpen = true;
    },
    /**
     * Opens the modal to delete a model.
     * @param model - The model to delete.
     */
    handleDelete(model: GenerationModel) {
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
