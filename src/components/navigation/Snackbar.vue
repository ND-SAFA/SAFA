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
import { MessageType, SnackbarMessage } from "@/types";
import { appStore, logStore } from "@/hooks";
import { ServerErrorModal } from "@/components/common";

const snackbarMessage = ref("");
const messageType = ref<MessageType>(MessageType.clear);
const errors = ref<string[]>([]);

const $q = useQuasar();

const hasErrors = computed(() => errors.value.length > 0);
const isErrorOpen = computed(() => appStore.isErrorDisplayOpen);
const showAction = computed(() => messageType.value === MessageType.update);

const messageColor = computed(() => {
  switch (messageType.value) {
    case MessageType.warning:
      return "warning";
    case MessageType.error:
      return "negative";
    case MessageType.success:
      return "positive";
    default:
      return "primary";
  }
});

function buildNotification() {
  const actions = [];

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

  actions.push({
    icon: "close",
    color: "white",
    "data-cy": "button-snackbar-close",
  });

  return {
    message: snackbarMessage.value,
    color: messageColor.value,
    attrs: {
      "data-cy": `snackbar-${messageType.value}`,
    },
    actions: actions,
    multiLine: false,
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
    if (newMessage.type === MessageType.clear) return;

    handleShowMessage(newMessage);
    logStore.clearMessage();
  }
);
</script>
