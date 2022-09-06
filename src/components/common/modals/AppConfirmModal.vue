<template>
  <generic-modal
    size="xs"
    :isOpen="isMessageDefined"
    :title="title"
    @close="handleClose"
  >
    <template v-slot:body>
      <typography y="2" el="p" :value="body" />
    </template>
    <template v-slot:actions>
      <v-spacer />
      <v-btn
        color="primary"
        data-cy="button-confirm-modal"
        @click="handleConfirm"
      >
        I accept
      </v-btn>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ConfirmationType, ConfirmDialogueMessage } from "@/types";
import { logStore } from "@/hooks";
import Typography from "@/components/common/display/Typography.vue";
import GenericModal from "./GenericModal.vue";

/**
 * Displays a modal for confirming sensitive actions.
 */
export default Vue.extend({
  name: "AppConfirmModal",
  components: { Typography, GenericModal },
  props: {
    message: {
      type: Object as PropType<ConfirmDialogueMessage>,
      required: false,
    },
    width: {
      type: String,
      required: false,
      default: "500",
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  computed: {
    /**
     * @return Whether the current message exists.
     */
    isMessageDefined(): boolean {
      return !!this.message && this.message.type !== ConfirmationType.CLEAR;
    },
    /**
     * @return The message title.
     */
    title(): string {
      return this.message?.title || "";
    },
    /**
     * @return The message body.
     */
    body(): string {
      return this.message?.body || "";
    },
  },
  methods: {
    /**
     * Confirms the confirmation message.
     */
    handleConfirm(): void {
      if (!this.message) return;

      logStore.clearConfirmation();
      this.message.statusCallback(true);
    },
    /**
     * Closes the confirmation message.
     */
    handleClose(): void {
      if (!this.message) return;

      logStore.clearConfirmation();
      this.message.statusCallback(false);
    },
  },
});
</script>
