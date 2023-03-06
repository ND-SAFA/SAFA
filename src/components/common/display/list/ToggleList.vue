<template>
  <v-list-group :prepend-icon="icon" :value="value" @click="$emit('click')">
    <template v-slot:activator>
      <v-list-item-title>
        <slot name="activator" />
        <typography v-if="title" :value="title" data-cy="generic-list-item" />
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
 *
 * @emits-1 `click` - On activator click.
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
