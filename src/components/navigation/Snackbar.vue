<template>
  <v-snackbar
    v-model="showSnackbar"
    :timeout="timeout"
    :color="messageColor"
    bottom
  >
    <flex-box
      align="center"
      justify="space-between"
      :data-cy="`snackbar-${messageType}`"
    >
      <icon color="white" :variant="iconVariant" />
      <typography color="white" align="center" x="2" :value="snackbarMessage" />
      <flex-box align="center">
        <text-button
          v-if="hasErrors"
          text
          color="white"
          class="ma-0"
          @click="handleSeeError"
        >
          See Errors
        </text-button>
        <icon-button
          v-if="showAction"
          color="white"
          icon-variant="download"
          tooltip="Update"
          @click="handleAction"
        />
        <icon-button
          color="white"
          icon-variant="cancel"
          tooltip="Close"
          data-cy="button-snackbar-close"
          @click="showSnackbar = false"
        />
      </flex-box>
    </flex-box>

    <ServerErrorModal :is-open="isErrorOpen" :errors="errors" />
  </v-snackbar>
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
import { IconVariant, MessageType, SnackbarMessage } from "@/types";
import { ThemeColors } from "@/util";
import { appStore, logStore } from "@/hooks";
import {
  ServerErrorModal,
  IconButton,
  Typography,
  FlexBox,
  TextButton,
  Icon,
} from "@/components/common";

const timeout = 5000;

const showSnackbar = ref(false);
const snackbarMessage = ref("");
const messageType = ref<MessageType>(MessageType.CLEAR);
const errors = ref<string[]>([]);

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

const iconVariant = computed<IconVariant>(() => {
  switch (messageType.value) {
    case MessageType.WARNING:
      return "warning";
    case MessageType.ERROR:
      return "error";
    case MessageType.SUCCESS:
      return "success";
    default:
      return "info";
  }
});
/**
 * Displays a snackbar message.
 * @param message - The message to display.
 */
function handleShowMessage(message: SnackbarMessage) {
  showSnackbar.value = true;
  snackbarMessage.value = String(message.message);
  errors.value = message.errors || [];
  messageType.value = message.type;
}

/**
 * Opens the error display panel.
 */
function handleSeeError(): void {
  appStore.toggleErrorDisplay();
}

/**
 * Runs changes that are pending.
 */
function handleAction(): void {
  showSnackbar.value = false;
  appStore.loadAppChanges();
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
