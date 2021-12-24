<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      {{ link.sourceName + "-" + link.targetName }}
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <trace-link-display
        :link="link"
        :source-body="sourceBody"
        :target-body="targetBody"
        :show-decline="showDecline"
        :show-approve="showApprove"
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
