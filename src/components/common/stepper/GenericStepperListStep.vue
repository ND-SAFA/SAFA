<template>
  <v-container>
    <h1 class="text-h5">{{ title }}</h1>
    <v-divider />
    <v-progress-circular
      v-if="loading"
      indeterminate
      size="48"
      class="mx-auto my-2 d-block"
    />
    <p v-if="itemCount === 0 && !loading" class="text-caption">
      {{ emptyMessage }}
    </p>
    <v-list>
      <v-list-item-group style="max-height: 400px" class="overflow-y-auto">
        <slot name="items" />
      </v-list-item-group>
    </v-list>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Presents a list in a stepper workflow for item selection.
 */
export default Vue.extend({
  name: "GenericStepperListStep",
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
