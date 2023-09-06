<template>
  <modal :open="props.open" title="Share Model" @close="emit('close')">
    <project-input v-model="projectId" exclude-current-project />
    <select-input
      v-model="shareMethod"
      label="Share Method"
      :options="shareOptions"
      option-value="id"
      option-label="name"
      option-to-value
    />
    <template #actions>
      <text-button
        label="Share"
        :disabled="!canSave"
        color="primary"
        @click="handleSave"
      />
    </template>
  </modal>
</template>

<script lang="ts">
/**
 * A modal for sharing models.
 */
export default {
  name: "ModelShareModal",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { ModelShareType, OpenableProps, SelectOption } from "@/types";
import { createOption } from "@/util";
import { modelApiStore, modelSaveStore } from "@/hooks";
import {
  Modal,
  ProjectInput,
  SelectInput,
  TextButton,
} from "@/components/common";

const props = defineProps<OpenableProps>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

/**
 * @return display names for model share options.
 */
function modelShareOptions(): SelectOption[] {
  return [
    createOption(ModelShareType.CLONE, "Clone the model"),
    createOption(ModelShareType.REUSE, "Reuse the same model"),
  ];
}

const shareOptions = modelShareOptions();

const projectId = ref("");
const shareMethod = ref(ModelShareType.CLONE);

const model = computed(() => modelSaveStore.baseModel);
const canSave = computed(() => projectId.value !== "" && !!model.value);

/**
 * Resets the modal data.
 */
function handleReset() {
  projectId.value = "";
  shareMethod.value = ModelShareType.CLONE;
}

/**
 * Saves the current model.
 */
function handleSave() {
  if (!model.value || !projectId.value) return;

  modelApiStore.handleShare(projectId.value, model.value, shareMethod.value);

  emit("close");
}

watch(
  () => props.open,
  (open) => {
    if (!open) return;

    handleReset();
  }
);
</script>
