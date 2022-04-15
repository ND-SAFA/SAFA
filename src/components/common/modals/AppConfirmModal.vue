<template>
  <generic-modal
    size="xs"
    :isOpen="isMessageDefined"
    :title="title"
    @close="handleClose"
  >
    <template v-slot:body>{{ body }}</template>
    <template v-slot:actions>
      <v-row justify="center">
        <v-btn outlined color="primary" @click="handleConfirm">
          I accept
        </v-btn>
      </v-row>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ConfirmationType, ConfirmDialogueMessage } from "@/types";
import { logModule } from "@/store";
import { GenericModal } from "@/components/common/generic";

/**
 * Displays a modal for confirming sensitive actions.
 */
export default Vue.extend({
  name: "AppConfirmModal",
  components: { GenericModal },
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

      logModule.CLEAR_CONFIRMATION_MESSAGE();
      this.message.statusCallback(true);
    },
    /**
     * Closes the confirmation message.
     */
    handleClose(): void {
      if (!this.message) return;

      logModule.CLEAR_CONFIRMATION_MESSAGE();
      this.message.statusCallback(false);
    },
  },
});
</script>
