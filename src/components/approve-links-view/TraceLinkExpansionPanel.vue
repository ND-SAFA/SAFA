<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      {{ link.source + "-" + link.target }}
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <trace-link-display
        :link="link"
        :sourceBody="sourceBody"
        :targetBody="targetBody"
        :showDecline="showDecline"
        :showApprove="showApprove"
        @approveLink="$emit('approveLink', $event)"
        @declineLink="$emit('declineLink', $event)"
      />
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script lang="ts">
import { TraceLink } from "@/types/domain/links";
import Vue, { PropType } from "vue";
import TraceLinkDisplay from "@/components/approve-links-view/TraceLinkDisplay.vue";
export default Vue.extend({
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
