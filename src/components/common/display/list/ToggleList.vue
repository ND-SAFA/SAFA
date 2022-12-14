<template>
  <v-list-group :prepend-icon="icon" :value="value">
    <template v-slot:activator>
      <v-list-item-title>
        <typography v-if="title" :value="title" data-cy="generic-list-item" />
        <slot name="activator" />
      </v-list-item-title>
    </template>
    <v-divider class="faded" />
    <slot />
    <v-divider class="faded" />
  </v-list-group>
</template>

<script lang="ts">
import Vue from "vue";
import Typography from "../Typography.vue";

/**
 * Displays a toggleable list.
 */
export default Vue.extend({
  name: "ToggleList",
  components: { Typography },
  props: {
    value: Boolean,
    icon: String,
    title: String,
  },
});
</script>
