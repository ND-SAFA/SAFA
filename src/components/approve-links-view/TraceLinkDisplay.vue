<template>
  <v-container>
    <v-row>
      <v-col cols="6">
        <h3>{{ link.source }}</h3>
        <p>{{ sourceBody }}</p>
      </v-col>
      <v-divider vertical />
      <v-col cols="6">
        <h3>{{ link.target }}</h3>
        <p>{{ targetBody }}</p>
      </v-col>
    </v-row>
    <v-row justify="center" class="pb-5">
      <v-btn
        v-if="showDecline"
        small
        color="error"
        class="ma-1"
        @click="$emit('declineLink', link)"
      >
        <v-icon>mdi-close</v-icon> Decline
      </v-btn>
      <v-btn
        v-if="showApprove"
        small
        color="primary"
        class="ma-1"
        @click="$emit('approveLink', link)"
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

export default Vue.extend({
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
