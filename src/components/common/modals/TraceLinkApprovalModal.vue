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
        @link:approve="onApproveLink"
        @link:decline="onDeclineLink"
      />
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import {
  TraceApproval,
  TraceLink,
  TraceLinkDisplayData,
  TraceType,
} from "@/types";
import { handleApproveLink, handleDeclineLink } from "@/api";
import { GenericModal } from "@/components/common/generic";
import { TraceLinkDisplay } from "@/components/common/display";

/**
 * A modal for approving trace links.
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
      await handleApproveLink(traceLink, undefined);
      this.$emit("close");
    },
    onDeclineLink(traceLink: TraceLink): void {
      handleDeclineLink(traceLink, undefined);
      this.$emit("close");
    },
  },
});
</script>
