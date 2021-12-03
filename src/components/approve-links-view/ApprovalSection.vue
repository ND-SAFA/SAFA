<template>
  <v-container>
    <h1 class="text-h4 text-center">{{ title }}</h1>

    <section-controls @open:all="openAll" @close:all="closeAll" />

    <v-row class="pt-5">
      <v-expansion-panels multiple v-model="openLinks">
        <trace-link-expansion-panel
          v-for="link in links"
          :key="link.traceLinkId"
          :link="link"
          :source-body="artifacts[link.source].body"
          :target-body="artifacts[link.target].body"
          :show-approve="showApprove"
          :show-decline="showDecline"
          @link:approve="$emit('link:approve', $event)"
          @link:decline="$emit('link:decline', $event)"
        />
      </v-expansion-panels>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceLink, Artifact } from "@/types";
import TraceLinkExpansionPanel from "./TraceLinkExpansionPanel.vue";
import SectionControls from "./SectionControls.vue";

/**
 * Displays link approvals.
 *
 * @emits-1 `link:approve` - On Link Approval.
 * @emits-2 `link:decline` - On Link Decline.
 */
export default Vue.extend({
  name: "approval-section",
  components: { TraceLinkExpansionPanel, SectionControls },
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
    links: Array as PropType<TraceLink[]>,
    artifacts: Object as PropType<Record<string, Artifact>>,
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
    links(newLinks: TraceLink[]) {
      if (this.isOpen) {
        this.$nextTick(
          () => (this.openLinks = newLinks.map((_, index) => index))
        );
      }
    },
  },
  methods: {
    openAll() {
      this.openLinks = this.links.map((_, index) => index);
      this.isOpen = true;
    },
    closeAll() {
      this.openLinks = [];
      this.isOpen = false;
    },
  },
});
</script>
