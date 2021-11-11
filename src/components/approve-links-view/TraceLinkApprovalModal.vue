<template>
  <GenericModal
    title="Approve Link"
    :is-open="isOpen"
    :actions-height="0"
    @onClose="$emit('close')"
  >
    <template v-slot:body>
      <TraceLinkDisplay
        :link="link"
        :source-body="link.sourceBody"
        :target-body="link.targetBody"
        :show-approve="canBeApproved"
        :show-decline="canBeDeclined"
        @approve-link="onApproveLink"
        @decline-link="onDeclineLink"
      />
    </template>
  </GenericModal>
</template>

<script lang="ts">
import { approveLinkAPIHandler, declineLinkAPIHandler } from "@/api";
import {
  TraceApproval,
  TraceLink,
  TraceLinkDisplayData,
  TraceType,
} from "@/types";
import Vue, { PropType } from "vue";
import { TraceLinkDisplay, GenericModal } from "@/components";

/**
 * Displays trace links on a panel.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  components: { GenericModal, TraceLinkDisplay },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    link: {
      type: Object as PropType<TraceLinkDisplayData>,
      required: true,
    },
  },
  computed: {
    canBeModified(): boolean {
      const traceLink: TraceLink = this.$props.link;
      return traceLink.traceType === TraceType.GENERATED;
    },
    canBeApproved(): boolean {
      const traceLink: TraceLink = this.$props.link;
      return (
        this.canBeModified &&
        traceLink.approvalStatus !== TraceApproval.APPROVED
      );
    },
    canBeDeclined(): boolean {
      const traceLink: TraceLink = this.$props.link;
      return (
        this.canBeModified &&
        traceLink.approvalStatus !== TraceApproval.DECLINED
      );
    },
  },
  methods: {
    onApproveLink(traceLink: TraceLink): void {
      approveLinkAPIHandler(traceLink, undefined);
      this.$emit("close");
    },
    onDeclineLink(traceLink: TraceLink): void {
      declineLinkAPIHandler(traceLink, undefined);
      this.$emit("close");
    },
  },
});
</script>
