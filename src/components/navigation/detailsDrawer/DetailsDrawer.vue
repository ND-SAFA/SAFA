<template>
  <v-navigation-drawer
    app
    right
    clipped
    hide-overlay
    :value="drawerOpen"
    height="100%"
    class="elevation-1"
  >
    <v-container> </v-container>
  </v-navigation-drawer>
</template>

<script lang="ts">
import Vue from "vue";

/**
 * Renders content in a right side panel.
 */
export default Vue.extend({
  name: "DetailsDrawer",
  components: {},
  data() {
    return {
      drawerOpen: false,
    };
  },
  computed: {},
  methods: {},
});
</script>

<style scoped lang="scss"></style>
