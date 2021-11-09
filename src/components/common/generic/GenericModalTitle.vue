<template>
  <v-row justify="space-between" class="pb-1">
    <label>{{ title }}</label>
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn @click="$emit('onClose')" icon v-bind="attrs" v-on="on">
          <v-icon id="close-button">mdi-close</v-icon>
        </v-btn>
      </template>
      <span>Close</span>
    </v-tooltip>
  </v-row>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  props: {
    title: {
      type: String,
      required: true,
    },
  },
});
</script>
