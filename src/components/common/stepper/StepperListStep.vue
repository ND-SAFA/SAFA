<template>
  <v-container>
    <typography el="h1" variant="subtitle" :value="title" />
    <v-divider />
    <v-progress-circular
      v-if="loading"
      indeterminate
      size="48"
      class="mx-auto my-2 d-block"
    />
    <typography
      v-if="itemCount === 0 && !loading"
      variant="small"
      el="p"
      :value="emptyMessage"
    />
    <v-list>
      <v-list-item-group style="max-height: 400px" class="overflow-y-auto">
        <slot name="items" />
      </v-list-item-group>
    </v-list>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import { Typography } from "@/components/common/display";

/**
 * Presents a list in a stepper workflow for item selection.
 */
export default Vue.extend({
  name: "StepperListStep",
  components: { Typography },
  props: {
    title: {
      type: String,
      required: true,
    },
    itemCount: {
      type: Number,
      required: true,
    },
    emptyMessage: {
      type: String,
      required: true,
    },
    loading: {
      type: Boolean,
      required: false,
    },
  },
});
</script>
