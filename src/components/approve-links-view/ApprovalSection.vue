<template>
  <v-container>
    <v-row justify="center">
      <h2>{{ title }}</h2>
    </v-row>
    <SectionControls @openAll="openAll" @closeAll="closeAll" />
    <v-row class="pt-5">
      <v-expansion-panels multiple v-model="openLinks">
        <TraceLinkExpansionPanel
          v-for="link in links"
          :key="link.traceLinkId"
          :link="link"
          :sourceBody="artifacts[link.source].body"
          :targetBody="artifacts[link.target].body"
          :showApprove="showApprove"
          :showDecline="showDecline"
          @approveLink="$emit('approveLink', $event)"
          @declineLink="$emit('declineLink', $event)"
        />
      </v-expansion-panels>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceLink, Artifact } from "@/types";
import TraceLinkExpansionPanel from "./TraceLinkExpansionPanel.vue";
import SectionControls from "./TraceLinkExpansionPanel.vue";

export default Vue.extend({
  name: "ApprovalSection",
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
