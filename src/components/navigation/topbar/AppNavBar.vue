<template>
  <v-app-bar clipped-right :color="darkMode ? '' : 'primary'">
    <header-bar />
    <template v-if="graphVisible" #extension>
      <graph-bar />
    </template>
  </v-app-bar>
</template>

<script lang="ts">
/**
 * Renders the top navigation bar.
 */
export default {
  name: "AppNavBar",
};
</script>

<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useTheme } from "@/hooks";
import { Routes } from "@/router";
import { HeaderBar } from "./header";
import { GraphBar } from "./graph";

const { darkMode } = useTheme();

const currentRoute = useRoute();
const graphVisible = ref(currentRoute.path === Routes.ARTIFACT);

watch(
  () => currentRoute.path,
  () => (graphVisible.value = currentRoute.path === Routes.ARTIFACT)
);
</script>
