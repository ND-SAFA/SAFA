<template>
  <v-container>
    <flex-box justify="space-between" full-width>
      <typography el="h1" variant="title" :value="title" />
      <section-controls @open:all="openAll" @close:all="closeAll" />
    </flex-box>
    <v-divider class="mb-2" />
    <v-expansion-panels multiple v-model="openLinks">
      <trace-link-expansion-panel
        v-for="link in links"
        :key="link.traceLinkId"
        :link="link"
        :show-approve="showApprove"
        :show-decline="showDecline"
        @link:approve="$emit('link:approve', $event)"
        @link:decline="$emit('link:decline', $event)"
      />
    </v-expansion-panels>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceLinkModel } from "@/types";
import { Typography, FlexBox } from "@/components/common";
import TraceLinkExpansionPanel from "./TraceLinkExpansionPanel.vue";
import SectionControls from "./SectionControls.vue";

/**
 * Displays link approvals.
 *
 * @emits-1 `link:approve` - On Link Approval.
 * @emits-2 `link:decline` - On Link Decline.
 */
export default Vue.extend({
  name: "ApprovalSection",
  components: { FlexBox, Typography, TraceLinkExpansionPanel, SectionControls },
  props: {
    title: String,
    showApprove: {
      type: Boolean,
      default: true,
    },
    showDecline: {
      type: Boolean,
      default: true,
    },
    links: Array as PropType<TraceLinkModel[]>,
    startOpen: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      openLinks: [] as number[],
      isOpen: this.startOpen,
    };
  },
  watch: {
    /**
     * When trace links change, sets all panels to open.
     */
    links(newLinks: TraceLinkModel[]) {
      if (!this.isOpen) return;

      this.$nextTick(
        () => (this.openLinks = newLinks.map((_, index) => index))
      );
    },
  },
  methods: {
    /**
     * Opens all trace link panels.
     */
    openAll() {
      this.openLinks = this.links.map((_, index) => index);
      this.isOpen = true;
    },
    /**
     * Closes all trace link panels.
     */
    closeAll() {
      this.openLinks = [];
      this.isOpen = false;
    },
  },
});
</script>
