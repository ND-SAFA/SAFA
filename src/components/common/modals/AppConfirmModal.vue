<template>
  <GenericModal
    size="xs"
    :isOpen="isMessageDefined"
    :title="title"
    @onClose="onClose"
  >
    <template v-slot:body>{{ body }}</template>
    <template v-slot:actions>
      <v-row justify="center">
        <v-btn outlined color="primary" @click="onConfirm"> I accept </v-btn>
      </v-row>
    </template>
  </GenericModal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import GenericModal from "@/components/common/generic/GenericModal.vue";
import { ConfirmationType, ConfirmDialogueMessage } from "@/types";
import { appModule } from "@/store";

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
      return this.message.type !== ConfirmationType.CLEAR;
    },
    title(): string {
      if (this.isMessageDefined) {
        return this.message.title;
      } else {
        return "";
      }
    },
    body(): string {
      if (this.isMessageDefined) {
        return this.message.body;
      } else {
        return "";
      }
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
        appModule.CLEAR_CONFIRMATION_MESSAGE();
        this.message.statusCallback(true);
      }
    },
    onClose(): void {
      if (this.message !== undefined) {
        appModule.CLEAR_CONFIRMATION_MESSAGE();
        this.message.statusCallback(false);
      }
    },
  },
});
</script>
