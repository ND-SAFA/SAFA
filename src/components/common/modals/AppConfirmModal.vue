<template>
  <generic-modal
    size="xs"
    :isOpen="isMessageDefined"
    :title="title"
    @close="onClose"
  >
    <template v-slot:body>{{ body }}</template>
    <template v-slot:actions>
      <v-row justify="center">
        <v-btn outlined color="primary" @click="onConfirm"> I accept </v-btn>
      </v-row>
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ConfirmationType, ConfirmDialogueMessage } from "@/types";
import { logModule } from "@/store";
import { GenericModal } from "@/components/common/generic";

export default Vue.extend({
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
  computed: {
    isMessageDefined(): boolean {
      return !!this.message && this.message.type !== ConfirmationType.CLEAR;
    },
    title(): string {
      return this.message?.title || "";
    },
    body(): string {
      return this.message?.body || "";
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    onConfirm(): void {
      if (this.message !== undefined) {
        logModule.CLEAR_CONFIRMATION_MESSAGE();
        this.message.statusCallback(true);
      }
    },
    onClose(): void {
      if (this.message !== undefined) {
        logModule.CLEAR_CONFIRMATION_MESSAGE();
        this.message.statusCallback(false);
      }
    },
  },
});
</script>
