<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        @click="$emit('onClick')"
        icon
        v-bind="attrs"
        v-on="on"
        :color="color"
      >
        <v-icon>{{ iconId }}</v-icon>
      </v-btn>
    </template>
    <span>{{ tooltip }}</span>
  </v-tooltip>
</template>

<script lang="ts">
import Vue from "vue";

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
