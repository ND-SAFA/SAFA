<template>
  <v-container>
    <v-row>
      <v-col cols="6">
        <h2 class="text-h4">{{ link.source }}</h2>
        <p class="text-body-1">{{ sourceBody }}</p>
      </v-col>
      <v-divider vertical />
      <v-col cols="6">
        <h2 class="text-h4">{{ link.target }}</h2>
        <p class="text-body-1">{{ targetBody }}</p>
      </v-col>
    </v-row>
    <v-row justify="center" class="pt-5">
      <v-btn
        v-if="showDecline"
        color="error"
        class="ma-1"
        @click="$emit('link:decline', link)"
      >
        <v-icon>mdi-close</v-icon> Decline
      </v-btn>
      <v-btn
        v-if="showApprove"
        color="primary"
        class="ma-1"
        @click="$emit('link:approve', link)"
      >
        <v-icon>mdi-check</v-icon>
        Approve
      </v-btn>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue, { PropType } from "vue";
import { TraceLink } from "@/types";

/**
 * Displays a trace link.
 *
 * @emits-1 `link:approve` - On Link Approval.
 * @emits-2 `link:decline` - On Link Decline.
 */
export default Vue.extend({
  name: "trace-link-display",
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
