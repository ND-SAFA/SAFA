<template>
  <server-error-modal :is-open="isErrorOpen" :errors="errors" />
</template>

<script lang="ts">
/**
 * Displays snackbar messages.
 */
export default {
  name: "Snackbar",
};
</script>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useQuasar } from "quasar";
import type { QNotifyCreateOptions } from "quasar";
import { MessageType, SnackbarMessage } from "@/types";
import { ThemeColors } from "@/util";
import { appStore, logStore } from "@/hooks";
import { ServerErrorModal } from "@/components/common";

const snackbarMessage = ref("");
const messageType = ref<MessageType>(MessageType.CLEAR);
const errors = ref<string[]>([]);

const $q = useQuasar();

const hasErrors = computed(() => errors.value.length > 0);
const isErrorOpen = computed(() => appStore.isErrorDisplayOpen);
const showAction = computed(() => messageType.value === MessageType.UPDATE);

const messageColor = computed(() => {
  switch (messageType.value) {
    case MessageType.INFO:
      return "primary";
    case MessageType.WARNING:
      return "warning";
    case MessageType.ERROR:
      return "error";
    case MessageType.SUCCESS:
      return ThemeColors.added;
    default:
      return ThemeColors.modified;
  }
});

function buildNotification(): QNotifyCreateOptions {
  const actions: QNotifyCreateOptions["actions"] = [];

  if (hasErrors.value) {
    actions.push({
      label: "See Errors",
      color: "white",
      handler: () => appStore.toggleErrorDisplay(),
    });
  }

  if (showAction.value) {
    actions.push({
      label: "Update",
      color: "white",
      handler: () => appStore.loadAppChanges(),
    });
  }

  return {
    message: snackbarMessage.value,
    color: messageColor.value,
    actions: [],
  };
}

/**
 * Displays a snackbar message.
 * @param message - The message to display.
 */
function handleShowMessage(message: SnackbarMessage) {
  snackbarMessage.value = String(message.message);
  errors.value = message.errors || [];
  messageType.value = message.type;

  $q.notify(buildNotification());
}

watch(
  () => logStore.message,
  (newMessage) => {
    if (newMessage.type === MessageType.CLEAR) return;

    handleShowMessage(newMessage);
    logStore.clearMessage();
  }
);
</script>
