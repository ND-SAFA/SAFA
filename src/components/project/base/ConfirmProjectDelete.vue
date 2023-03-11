<template>
  <modal
    :loading="loading"
    :open="props.open"
    title="Delete Project"
    subtitle="Are you sure you want to delete this project? Type in the project's name to confirm deletion."
    data-cy="modal-project-delete"
    @close="handleCancel"
  >
    <text-input
      v-model="confirmText"
      :label="label"
      data-cy="input-project-delete-name"
    />
    <template #actions>
      <text-button
        color="negative"
        label="Delete"
        :disabled="!canDelete"
        :loading="loading"
        data-cy="button-project-delete"
        @click="handleConfirm"
      />
    </template>
  </modal>
</template>

<script lang="ts">
/**
 * A modal for confirming project deletion.
 */
export default {
  name: "ConfirmProjectDelete",
};
</script>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { identifierSaveStore } from "@/hooks";
import { handleDeleteProject } from "@/api";
import { Modal, TextInput, TextButton } from "@/components/common";

const props = defineProps<{
  open: boolean;
}>();

const emit = defineEmits<{
  (e: "confirm"): void;
  (e: "close"): void;
}>();

const confirmText = ref("");
const loading = ref(false);

const projectName = computed(
  () => identifierSaveStore.baseIdentifier?.name || ""
);
const label = computed(() => `Type "${projectName.value}"`);
const canDelete = computed(() => confirmText.value === projectName.value);

/**
 * Clears the modal data.
 */
function handleClear(): void {
  confirmText.value = "";
}

/**
 * Cancels the project deletion.
 */
function handleCancel(): void {
  emit("close");
  handleClear();
}

/**
 * Confirms the project deletion.
 */
function handleConfirm(): void {
  loading.value = true;

  handleDeleteProject({
    onSuccess: () => {
      emit("confirm");
      handleClear();
    },
    onComplete: () => (loading.value = false),
  });
}

watch(
  () => props.open,
  (open) => {
    if (!open) return;

    handleClear();
  }
);
</script>
