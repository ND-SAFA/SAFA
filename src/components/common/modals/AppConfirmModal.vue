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
import { ConfirmationType } from "@/types";
import { logStore } from "@/hooks";
import { Typography } from "@/components/common/display";
import TextButton from "@/components/common/button/TextButton.vue";
import Modal from "./Modal.vue";

const message = computed(() => logStore.confirmation);

const isOpen = computed(() => message.value.type !== ConfirmationType.CLEAR);

/**
 * Confirms the confirmation message.
 */
function handleConfirm(): void {
  logStore.clearConfirmation();
  message.value.statusCallback(true);
}

/**
 * Closes the confirmation message.
 */
function handleClose(): void {
  logStore.clearConfirmation();
  message.value.statusCallback(false);
}
</script>
