<template>
  <generic-modal
    title="Trace Link"
    :is-open="isOpen"
    :actions-height="0"
    @close="$emit('close')"
    size="l"
    data-cy="modal-trace-approve"
  >
    <template v-slot:body>
      <trace-link-display
        v-if="!!link"
        :link="link"
        @link:approve="handleClose"
        @link:decline="handleClose"
        @link:unreview="handleClose"
        @link:delete="handleClose"
        @close="$emit('close')"
      />
    </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceLinkModel } from "@/types";
import { GenericModal } from "@/components/common";
import TraceLinkDisplay from "../TraceLinkDisplay.vue";

/**
 * A modal for approving trace links.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "TraceLinkApprovalModal",
  components: {
    GenericModal,
    TraceLinkDisplay,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    link: Object as PropType<TraceLinkModel>,
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
