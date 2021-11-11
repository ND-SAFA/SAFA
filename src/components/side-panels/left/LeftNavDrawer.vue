<template>
  <v-navigation-drawer
    app
    clipped
    hide-overlay
    light
    left
    stateless
    v-model="isLeftOpen"
    :width="width"
    height="100%"
  >
    <SelectedNodeTab />
  </v-navigation-drawer>
</template>
<script lang="ts">
import Vue from "vue";
import SelectedNodeTab from "./SelectedNodeTab.vue";

export default Vue.extend({
  components: {
    SelectedNodeTab,
  },
  props: {
    isLeftOpen: Boolean,
    width: {
      type: Number,
      required: true,
    },
  },
});
</script>
