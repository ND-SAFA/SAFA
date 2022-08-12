<template>
  <v-chip small class="mr-1" :color="color" outlined>
    <typography :value="text" inherit-color />
  </v-chip>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceLinkModel } from "@/types";
import { capitalize, getBackgroundColor } from "@/util";
import Typography from "@/components/common/display/Typography.vue";

/**
 * Renders a chip for the delta state of this artifact.
 */
export default Vue.extend({
  name: "ApprovalChip",
  components: { Typography },
  props: {
    link: Object as PropType<TraceLinkModel>,
  },
  computed: {
    /**
     * @return The text to display on this chip.
     */
    text(): string {
      return capitalize(this.link.approvalStatus);
    },
    /**
     * @return The color to display for this chip.
     */
    color(): string {
      return getBackgroundColor(this.link.approvalStatus);
    },
  },
});
</script>
