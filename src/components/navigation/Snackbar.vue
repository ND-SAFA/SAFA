<template>
  <v-snackbar v-model="showSnackbar" :timeout="timeout" :color="color">
    <v-alert :type="messageType" class="pa-0 ma-0" dense>
      <v-row align="center" justify="center">
        <v-col class="grow">
          {{ snackbarMessage }}
        </v-col>
        <v-col class="shrink pa-0 ma-0">
          <v-btn text @click="showSnackbar = false"> Close </v-btn>
        </v-col>
      </v-row>
    </v-alert>
  </v-snackbar>
</template>

<script lang="ts">
import Vue from "vue";
import { MessageType, SnackbarMessage } from "@/types/store";
import { appModule } from "@/store";

export default Vue.extend({
  name: "snackbar",
  props: {
    timeout: Number,
  },
  data: () => ({
    showSnackbar: false,
    snackbarMessage: "",
    color: "green",
    messageType: "success",
  }),
  methods: {
    getMessageColor(messageType: MessageType) {
      switch (messageType) {
        case MessageType.INFO:
          return ["blue", "info"];
        case MessageType.WARNING:
          return ["orange", "warning"];
        case MessageType.ERROR:
          return ["red", "error"];
        case MessageType.SUCCESS:
          return ["green", "success"];
        default:
          return ["blue", "info"];
      }
    },
    showMessage(snackbarMessage: SnackbarMessage) {
      this.showSnackbar = true;
      this.snackbarMessage = snackbarMessage.message;
      const [color, type] = this.getMessageColor(snackbarMessage.type);
      this.color = color;
      this.messageType = type;
    },
  },
  computed: {
    message() {
      return appModule.getMessage;
    },
  },
  watch: {
    message(newMessage: SnackbarMessage | undefined) {
      if (newMessage !== undefined) {
        this.showMessage(newMessage);
        appModule.CLEAR_MESSAGE();
      }
    },
  },
});
</script>
