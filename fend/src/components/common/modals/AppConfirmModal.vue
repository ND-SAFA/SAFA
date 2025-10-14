<template>
  <modal
    size="sm"
    :open="isOpen"
    :title="message.title"
    :subtitle="message.body"
    @close="handleClose"
  >
    <template #actions>
      <text-button
        label="Confirm"
        color="primary"
        data-cy="button-confirm-modal"
        @click="handleConfirm"
      />
    </template>
  </modal>
</template>

<script lang="ts">
/**
 * Displays a modal for confirming sensitive actions.
 */
export default {
  name: "AppConfirmModal",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { logStore } from "@/hooks";
import { TextButton } from "@/components/common/button";
import Modal from "./Modal.vue";

const message = computed(() => logStore.confirmation);

const isOpen = computed(() => message.value.type !== "clear");

/**
 * Confirms the confirmation message.
 */
function handleConfirm(): void {
  message.value.statusCallback(true);
  logStore.clearConfirmation();
}

/**
 * Closes the confirmation message.
 */
function handleClose(): void {
  message.value.statusCallback(false);
  logStore.clearConfirmation();
}
</script>
