<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        icon
        v-on="on"
        v-bind="attrs"
        :color="color"
        @click="$emit('click')"
      >
        <v-icon>{{ iconId }}</v-icon>
      </v-btn>
    </template>
    <span>{{ tooltip }}</span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * A generic icon button.
 *
 * @emits `click` - On button click.
 */
export default Vue.extend({
  name: "generic-icon-button",
  props: {
    tooltip: {
      type: String,
      required: true,
    },
    iconId: {
      type: String,
      required: true,
    },
    color: {
      type: String,
      required: false,
    },
  },
});
</script>
