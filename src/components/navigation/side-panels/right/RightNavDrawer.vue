<template>
  <v-navigation-drawer
    app
    clipped
    hide-overlay
    light
    right
    stateless
    v-model="isRightOpen"
    :width="width"
    height="100%"
  >
    <side-panel />
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from "vue";
import SidePanel from "./SidePanel.vue";

export default Vue.extend({
  components: {
    SidePanel,
  },
  props: {
    isRightOpen: Boolean,
    width: {
      type: Number,
      required: true,
    },
  },
});
</script>
