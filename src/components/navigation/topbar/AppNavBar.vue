<template>
  <q-header elevated :class="darkMode ? '' : 'bg-primary'">
    <q-toolbar>
      <div class="full-width">
        <header-bar />
        <graph-bar v-if="graphVisible" />
        <loading-bar />
      </div>
    </q-toolbar>
  </q-header>
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
import { HeaderBar, LoadingBar } from "./header";
import { GraphBar } from "./graph";

const { darkMode } = useTheme();

const currentRoute = useRoute();
const graphVisible = ref(currentRoute.path === Routes.ARTIFACT);

watch(
  () => currentRoute.path,
  () => (graphVisible.value = currentRoute.path === Routes.ARTIFACT)
);
</script>
