<template>
  <generic-modal
    title="Approve Link"
    :is-open="isOpen"
    :actions-height="0"
    @close="$emit('close')"
  >
    <template v-slot:body>
      <trace-link-display
        :link="link"
        :source-body="link.sourceBody"
        :target-body="link.targetBody"
        :show-approve="canBeApproved"
        :show-decline="canBeDeclined"
        @approve-link="onApproveLink"
        @decline-link="onDeclineLink"
      />
    </template>
  </generic-modal>
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
import { GenericModal } from "@/components/common";
import TraceLinkDisplay from "./TraceLinkDisplay.vue";

/**
 * Displays trace links on a panel.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "trace-link-approval-modal",
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
    async onApproveLink(traceLink: TraceLink): Promise<void> {
      await approveLinkAPIHandler(traceLink, undefined);
      this.$emit("close");
    },
    onDeclineLink(traceLink: TraceLink): void {
      declineLinkAPIHandler(traceLink, undefined);
      this.$emit("close");
    },
  },
});
</script>
