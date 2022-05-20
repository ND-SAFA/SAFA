<template>
  <generic-modal
    title="Trace Link"
    :is-open="isOpen"
    :actions-height="0"
    @close="$emit('close')"
    size="l"
  >
    <template v-slot:body>
      <trace-link-display
        v-if="!!link"
        :link="link"
        :source-body="sourceBody"
        :target-body="targetBody"
        :show-approve="canBeApproved"
        :show-decline="canBeDeclined"
        :show-delete="!canBeModified"
        @link:approve="handleApprove"
        @link:decline="handleDecline"
        @link:delete="handleDecline"
        @close="$emit('close')"
      />
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceApproval, TraceLink, TraceType } from "@/types";
import { handleApproveLink, handleDeclineLink } from "@/api";
import { GenericModal } from "@/components/common";
import TraceLinkDisplay from "./TraceLinkDisplay.vue";
import { artifactModule } from "@/store";

/**
 * A modal for approving trace links.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "TraceLinkApprovalModal",
  components: { GenericModal, TraceLinkDisplay },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    link: Object as PropType<TraceLink>,
  },
  data() {
    return {
      sourceBody: "",
      targetBody: "",
    };
  },
  watch: {
    isOpen(isOpen: boolean) {
      if (!isOpen || !this.link) return;

      const artifactsById = artifactModule.getArtifactsById;

      this.sourceBody = artifactsById[this.link.sourceId].body;
      this.targetBody = artifactsById[this.link.targetId].body;
    },
  },
  computed: {
    /**
     * @return Whether this link can be modified.
     */
    canBeModified(): boolean {
      return this.link?.traceType === TraceType.GENERATED;
    },
    /**
     * @return Whether this link can be approved.
     */
    canBeApproved(): boolean {
      return (
        this.canBeModified &&
        this.link?.approvalStatus !== TraceApproval.APPROVED
      );
    },
    /**
     * @return Whether this link can be declined.
     */
    canBeDeclined(): boolean {
      return (
        this.canBeModified &&
        this.link?.approvalStatus !== TraceApproval.DECLINED
      );
    },
  },
  methods: {
    /**
     * Approves the given link and closes the modal.
     * @param traceLink - The link to approve.
     */
    async handleApprove(traceLink: TraceLink): Promise<void> {
      await handleApproveLink(traceLink);
      this.$emit("close");
    },
    /**
     * Declines the given link and closes the modal.
     * @param traceLink - The link to decline.
     */
    handleDecline(traceLink: TraceLink): void {
      handleDeclineLink(traceLink);
      this.$emit("close");
    },
  },
});
</script>
