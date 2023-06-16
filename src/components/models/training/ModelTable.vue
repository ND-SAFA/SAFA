<template>
  <panel-card
    title="Trace Prediction Models"
    subtitle="Create a new model below, or expand one of the models to continue and view past training."
  >
    <model-creator-modal :open="saveOpen" @close="handleClose" />
    <model-share-modal :open="shareOpen" @close="handleClose" />
    <selector-table
      v-model:expanded="expanded"
      class="model-table"
      :columns="modelColumns"
      :rows="rows"
      row-key="id"
      addable
      editable
      deletable
      @row:add="handleAdd"
      @row:edit="handleEdit"
      @row:delete="handleDelete"
      @refresh="handleRefresh"
    >
      <template #expanded-item="{ row }">
        <model-training :model="row" />
      </template>
      <template #[`item.actions`]="{ item }">
        <icon-button
          icon="share"
          tooltip="Share Model"
          @click="handleShare(item)"
        />
      </template>
    </selector-table>
  </panel-card>
</template>

<script lang="ts">
/**
 * Renders a table of project models.
 */
export default {
  name: "ModelTable",
};
</script>

<script setup lang="ts">
import { computed, ref } from "vue";
import { GenerationModelSchema } from "@/types";
import { modelColumns } from "@/util";
import { modelApiStore, modelSaveStore, projectStore } from "@/hooks";
import { IconButton, PanelCard, SelectorTable } from "@/components/common";
import { ModelTraining } from "./editor";
import ModelShareModal from "./ModelShareModal.vue";
import ModelCreatorModal from "./ModelCreatorModal.vue";

const saveOpen = ref(false);
const shareOpen = ref(false);
const expanded = ref<GenerationModelSchema[]>([]);

const rows = computed(() => projectStore.models);

/**
 * Closes the model modal.
 */
function handleClose() {
  saveOpen.value = false;
  shareOpen.value = false;
  modelSaveStore.baseModel = undefined;
}

/**
 * Opens the modal to add a model.
 */
function handleAdd() {
  modelSaveStore.baseModel = undefined;
  saveOpen.value = true;
}

/**
 * Opens the modal to edit a model.
 * @param model - The model to edit.
 */
function handleEdit(model: GenerationModelSchema) {
  modelSaveStore.baseModel = model;
  saveOpen.value = true;
}

/**
 * Opens the modal to share a model.
 * @param model - The model to share.
 */
function handleShare(model: GenerationModelSchema) {
  modelSaveStore.baseModel = model;
  shareOpen.value = true;
}

/**
 * Opens the modal to delete a model.
 * @param model - The model to delete.
 */
function handleDelete(model: GenerationModelSchema) {
  modelApiStore.handleDeleteModel(model);
}

/**
 * Refreshes the loaded models.
 */
function handleRefresh() {
  modelApiStore.handleLoadModels();
}
</script>
