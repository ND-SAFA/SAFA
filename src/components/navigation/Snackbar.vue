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
            @click="onSeeErrorClick"
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
import { MessageType, PanelType, SnackbarMessage } from "@/types";
import { appModule } from "@/store";
import { ServerErrorModal } from "@/components/common";

export default Vue.extend({
  name: "snackbar",
  components: {
    ServerErrorModal,
  },
  props: {
    timeout: Number,
  },
  data: () => ({
    showSnackbar: false,
    snackbarMessage: "",
    messageType: MessageType.CLEAR,
    errors: [] as string[],
  }),
  methods: {
    showMessage(snackbarMessage: SnackbarMessage) {
      this.showSnackbar = true;
      this.snackbarMessage = snackbarMessage.message;
      this.errors = snackbarMessage.errors;
      this.messageType = snackbarMessage.type;
    },
    onSeeErrorClick(): void {
      appModule.openPanel(PanelType.errorDisplay);
    },
  },
  computed: {
    hasErrors(): boolean {
      return this.errors.length > 0;
    },
    message() {
      return appModule.getMessage;
    },
    isErrorDisplayOpen(): boolean {
      return appModule.getIsErrorDisplayOpen;
    },
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
    message(newMessage: SnackbarMessage) {
      if (newMessage.type !== MessageType.CLEAR) {
        this.showMessage(newMessage);
        appModule.CLEAR_MESSAGE();
      }
    },
  },
});
</script>
