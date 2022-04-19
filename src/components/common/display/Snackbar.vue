<template>
  <v-snackbar v-model="showSnackbar" :timeout="timeout" :color="messageColor">
    <v-row class="ma-0 pa-0" justify="space-around">
      <v-col cols="1" class="ma-0 pa-0" align-self="center">
        <v-icon> {{ messageIcon }} </v-icon>
      </v-col>
      <v-col
        :cols="hasErrors ? 6 : 9"
        class="ma-1 pa-0 text-center white--text"
        align-self="center"
      >
        {{ snackbarMessage }}
      </v-col>
      <v-col :cols="hasErrors ? 3 : 0" class="ma-0 pa-0" align-self="center">
        <v-row justify="end" class="ma-0 pa-0">
          <v-btn
            v-if="hasErrors"
            :color="messageColor"
            @click="handleSeeError"
            class="ma-0"
          >
            See Errors
          </v-btn>
        </v-row>
      </v-col>
      <v-col cols="1" class="ma-0 pa-0" align-self="center">
        <v-btn icon @click="showSnackbar = false">
          <v-icon> mdi-close </v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <ServerErrorModal :isOpen="isErrorDisplayOpen" :errors="errors" />
  </v-snackbar>
</template>

<script lang="ts">
import Vue from "vue";
import { MessageType, SnackbarMessage } from "@/types";
import { appModule, logModule } from "@/store";
import { ServerErrorModal } from "@/components/common/modals";

/**
 * Displays snackbar messages.
 */
export default Vue.extend({
  name: "Snackbar",
  components: {
    ServerErrorModal,
  },
  props: {
    timeout: Number,
  },
  data() {
    return {
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
      this.snackbarMessage = snackbarMessage.message;
      this.errors = snackbarMessage.errors || [];
      this.messageType = snackbarMessage.type;
    },
    /**
     * Opens the error display panel.
     */
    handleSeeError(): void {
      appModule.openErrorDisplay();
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
      return logModule.getMessage;
    },
    /**
     * @return Whether the error display is open.
     */
    isErrorDisplayOpen(): boolean {
      return appModule.getIsErrorDisplayOpen;
    },
    /**
     * @return The message color for the current message.
     */
    messageColor(): string {
      switch (this.messageType) {
        case MessageType.INFO:
          return "blue";
        case MessageType.WARNING:
          return "orange";
        case MessageType.ERROR:
          return "red";
        case MessageType.SUCCESS:
          return "green";
        default:
          return "info";
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
  },
  watch: {
    /**
     * When a new message is added, it will be displayed.
     */
    message(newMessage: SnackbarMessage) {
      if (newMessage.type === MessageType.CLEAR) return;

      this.showMessage(newMessage);
      logModule.CLEAR_MESSAGE();
    },
  },
});
</script>
