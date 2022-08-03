<template>
  <generic-modal
    title="Trace Link"
    :is-open="isOpen"
    :actions-height="0"
    @close="$emit('close')"
    size="l"
  >
    <template v-slot:body> </template>
  </generic-modal>
</template>

<script lang="ts">
import Vue from "vue";
import { GenericModal } from "@/components/common";

/**
 * A modal for creating trace links.
 *
 * @emits `close` - On close.
 */
export default Vue.extend({
  name: "TraceLinkCreatorModal",
  components: { GenericModal },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
  },
  data() {
    return {};
  },
  watch: {
    isOpen(isOpen: boolean) {
      if (!isOpen) return;
    },
  },
});
</script>
