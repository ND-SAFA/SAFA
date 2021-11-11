<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      {{ link.source + "-" + link.target }}
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <trace-link-display
        :link="link"
        :source-body="sourceBody"
        :target-body="targetBody"
        :show-decline="showDecline"
        :show-approve="showApprove"
        @approve-link="$emit('approve-link', $event)"
        @decline-link="$emit('decline-link', $event)"
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
 * @emits `approve-link` - On Link Approval.
 * @emits `decline-link` - On Link Decline.
 */
export default Vue.extend({
  name: "trace-link-expansion-panel",
  components: { TraceLinkDisplay },
  props: {
    link: {
      type: Object as PropType<TraceLink>,
      required: true,
    },
    sourceBody: {
      type: String,
      required: true,
    },
    targetBody: {
      type: String,
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
});
</script>
