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
        :show-approve="canBeApproved"
        :show-decline="canBeDeclined"
        :show-delete="canBeDeleted"
        @link:approve="handleClose"
        @link:decline="handleClose"
        @link:delete="handleClose"
        @close="$emit('close')"
      />
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { ApprovalType, TraceLinkModel, TraceType } from "@/types";
import { GenericModal } from "@/components/common";
import TraceLinkDisplay from "./TraceLinkDisplay.vue";
import { deltaModule } from "@/store";

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
    link: Object as PropType<TraceLinkModel>,
  },
  computed: {
    /**
     * @return Whether this link can be deleted.
     */
    canBeDeleted(): boolean {
      return !this.canBeModified && !deltaModule.inDeltaView;
    },
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
        this.link?.approvalStatus !== ApprovalType.APPROVED
      );
    },
    /**
     * @return Whether this link can be declined.
     */
    canBeDeclined(): boolean {
      return (
        this.canBeModified &&
        this.link?.approvalStatus !== ApprovalType.DECLINED
      );
    },
  },
  methods: {
    /**
     * Closes the modal.
     */
    handleClose() {
      this.$emit("close");
    },
  },
});
</script>
