<template>
  <v-app-bar app color="primary">
    <header-bar />
    <template v-slot:extension v-if="graphVisible">
      <graph-bar />
    </template>
  </v-app-bar>
</template>

<script lang="ts">
import Vue from "vue";
import { Route } from "vue-router";
import { router, Routes } from "@/router";
import { HeaderBar } from "./header";
import { GraphBar } from "./graph";

/**
 * Renders the top navigation bar.
 */
export default Vue.extend({
  name: "AppNavBar",
  components: {
    HeaderBar,
    GraphBar,
  },
  data() {
    return {
      graphVisible: router.currentRoute.path === Routes.ARTIFACT,
    };
  },
  watch: {
    /**
     * Checks whether the graph buttons should be visible when the route changes.
     */
    $route(to: Route) {
      this.graphVisible = to.path === Routes.ARTIFACT;
    },
  },
  computed: {},
});
</script>

<style scoped lang="scss"></style>
