<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      {{ headerName }}
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <trace-link-display
        :link="link"
        :show-decline="showDecline"
        :show-approve="showApprove"
        :show-delete="false"
        @link:approve="$emit('link:approve', $event)"
        @link:decline="$emit('link:decline', $event)"
      />
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceLink } from "@/types";
import TraceLinkDisplay from "./TraceLinkDisplay.vue";

/**
 * Displays trace links on a panel.
 *
 * @emits-1 `link:approve` - On Link Approval.
 * @emits-2 `link:decline` - On Link Decline.
 */
export default Vue.extend({
  name: "TraceLinkExpansionPanel",
  components: { TraceLinkDisplay },
  props: {
    link: {
      type: Object as PropType<TraceLink>,
      required: true,
    },
    showDecline: {
      type: Boolean,
      default: true,
    },
    showApprove: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    /**
     * @return The trace link name.
     */
    headerName(): string {
      return `${this.link.sourceName} - ${this.link.targetName}`;
    },
  },
});
</script>
