<template>
  <modal :open="props.open" :title="modalTitle" @close="emit('close')">
    <flex-box>
      <text-input
        v-model="editedModel.name"
        label="Model Name"
        class="q-mr-md"
      />
      <gen-method-input
        v-if="!isUpdate"
        v-model="editedModel.baseModel"
        only-trainable
      />
    </flex-box>
    <template #actions>
      <text-button
        label="Save"
        :disabled="!canSave"
        color="primary"
        @click="handleSave"
      />
    </template>
  </modal>
</template>

<script lang="ts">
/**
 * A modal for creating and editing models.
 */
export default {
  name: "ModelCreatorModal",
};
</script>

<script setup lang="ts">
import { computed, watch } from "vue";
import { modelApiStore, modelSaveStore } from "@/hooks";
import {
  Modal,
  GenMethodInput,
  FlexBox,
  TextInput,
  TextButton,
} from "@/components/common";

const props = defineProps<{
  open: boolean;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const isUpdate = computed(() => modelSaveStore.isUpdate);
const editedModel = computed(() => modelSaveStore.editedModel);
const modalTitle = computed(() =>
  isUpdate.value ? "Edit Model" : "Create Model"
);
const canSave = computed(() => modelSaveStore.canSave);

/**
 * Saves the current model.
 */
function handleSave() {
  modelApiStore.handleSaveModel({
    onSuccess: () => emit("close"),
  });
}

watch(
  () => props.open,
  (open) => {
    if (!open) return;

    modelSaveStore.resetModel();
  }
);
</script>
