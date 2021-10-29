<template>
  <GenericModal
    title="Approve Link"
    :isOpen="isOpen"
    :actionsHeight="0"
    @onClose="$emit('onClose')"
  >
    <template v-slot:body>
      <TraceLinkDisplay
        :link="link"
        :sourceBody="link.sourceBody"
        :targetBody="link.targetBody"
        :showApprove="canBeApproved"
        :showDecline="canBeDeclined"
        @approveLink="onApproveLink"
        @declineLink="onDeclineLink"
      />
    </template>
  </GenericModal>
</template>

<script lang="ts">
import {
  approveLinkAPIHandler,
  declineLinkAPIHandler,
} from "@/api/handlers/trace-link-approval-handler";
import {
  TraceApproval,
  TraceLink,
  TraceLinkDisplayData,
  TraceType,
} from "@/types/domain/links";
import Vue, { PropType } from "vue";
import TraceLinkDisplay from "@/components/approve-links-view/TraceLinkDisplay.vue";
import GenericModal from "@/components/common/generic/modal/GenericModal.vue";
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
      this.$emit("onClose");
    },
    onDeclineLink(traceLink: TraceLink): void {
      declineLinkAPIHandler(traceLink, undefined);
      this.$emit("onClose");
    },
  },
});
</script>
