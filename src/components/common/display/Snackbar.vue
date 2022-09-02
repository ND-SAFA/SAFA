<template>
  <v-snackbar
    v-model="showSnackbar"
    :timeout="timeout"
    :color="messageColor"
    bottom
    left
    outlined
  >
    <flex-box
      align="center"
      justify="space-between"
      :data-cy="`snackbar-${messageType}`"
    >
      <v-icon class="inherit-color"> {{ messageIcon }} </v-icon>
      <typography align="center" x="2" :value="snackbarMessage" />
      <flex-box align="center">
        <v-btn
          text
          v-if="hasErrors"
          :color="messageColor"
          @click="handleSeeError"
          class="ma-0"
        >
          See Errors
        </v-btn>
        <generic-icon-button
          :color="messageColor"
          icon-id="mdi-download"
          tooltip="Update"
          @click="handleAction"
        />
        <generic-icon-button
          :color="messageColor"
          icon-id="mdi-close"
          tooltip="Close"
          @click="showSnackbar = false"
        />
      </flex-box>
    </flex-box>

    <ServerErrorModal :isOpen="isErrorDisplayOpen" :errors="errors" />
  </v-snackbar>
</template>

<script lang="ts">
import Vue from "vue";
import { MessageType, SnackbarMessage } from "@/types";
import { ThemeColors } from "@/util";
import { appStore, logStore } from "@/hooks";
import { ServerErrorModal } from "@/components/common/modals";
import GenericIconButton from "@/components/common/generic/GenericIconButton.vue";
import Typography from "./Typography.vue";
import FlexBox from "./FlexBox.vue";

/**
 * Displays snackbar messages.
 */
export default Vue.extend({
  name: "Snackbar",
  components: {
    GenericIconButton,
    FlexBox,
    Typography,
    ServerErrorModal,
  },
  data() {
    return {
      timeout: 5000,
      showSnackbar: false,
      snackbarMessage: "",
      messageType: MessageType.CLEAR as MessageType,
      errors: [] as string[],
    };
  },
  methods: {
    /**
     * Displays a snackbar message.
     * @param snackbarMessage - The message to display.
     */
    showMessage(snackbarMessage: SnackbarMessage) {
      this.showSnackbar = true;
      this.snackbarMessage = String(snackbarMessage.message);
      this.errors = snackbarMessage.errors || [];
      this.messageType = snackbarMessage.type;
    },
    /**
     * Opens the error display panel.
     */
    handleSeeError(): void {
      appStore.toggleErrorDisplay();
    },
    /**
     * Runs changes that are pending.
     */
    handleAction(): void {
      this.showSnackbar = false;
      appStore.loadAppChanges();
    },
  },
  computed: {
    /**
     * @return Whether there arte any errors.
     */
    hasErrors(): boolean {
      return this.errors.length > 0;
    },
    /**
     * @return The current message.
     */
    message() {
      return logStore.message;
    },
    /**
     * @return Whether the error display is open.
     */
    isErrorDisplayOpen(): boolean {
      return appStore.isErrorDisplayOpen;
    },
    /**
     * @return The message color for the current message.
     */
    messageColor(): string {
      switch (this.messageType) {
        case MessageType.INFO:
          return "primary";
        case MessageType.WARNING:
          return "accent";
        case MessageType.ERROR:
          return "error";
        case MessageType.SUCCESS:
          return ThemeColors.added;
        default:
          return ThemeColors.modified;
      }
    },
    /**
     * @return The message icon for the current message.
     */
    messageIcon(): string {
      switch (this.messageType) {
        case MessageType.INFO:
          return "mdi-alert-circle-outline";
        case MessageType.WARNING:
          return "mdi-alert-outline";
        case MessageType.ERROR:
          return "mdi-alert-octagon-outline";
        case MessageType.SUCCESS:
          return "mdi-check-outline";
        default:
          return "mdi-alert-circle-outline";
      }
    },
    /**
     * @return Whether an action if one should be run on this notification.
     */
    showAction(): boolean {
      return this.messageType === MessageType.UPDATE;
    },
  },
  watch: {
    /**
     * When a new message is added, it will be displayed.
     */
    message(newMessage: SnackbarMessage) {
      if (newMessage.type === MessageType.CLEAR) return;

      this.showMessage(newMessage);
      logStore.clearMessage();
    },
  },
});
</script>
