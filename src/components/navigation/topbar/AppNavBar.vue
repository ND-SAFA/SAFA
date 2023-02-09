<template>
  <v-app-bar app clipped-right :color="$vuetify.theme.dark ? '' : 'primary'">
    <header-bar />
    <template v-slot:extension v-if="graphVisible">
      <graph-bar />
    </template>
  </v-app-bar>
</template>

<script lang="ts">
import Vue, { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { Routes } from "@/router";
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
  setup() {
    const currentRoute = useRoute();
    const graphVisible = ref(currentRoute.path === Routes.ARTIFACT);

    watch(
      () => currentRoute.path,
      () => (graphVisible.value = currentRoute.path === Routes.ARTIFACT)
    );

    return { graphVisible };
  },
});
</script>
