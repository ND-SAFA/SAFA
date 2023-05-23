<template>
  <q-header elevated class="bg-neutral">
    <q-toolbar class="nav-topbar">
      <div class="full-width">
        <header-bar />
        <graph-bar v-if="graphVisible" />
      </div>
    </q-toolbar>
    <loading-bar />
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
import { Routes } from "@/router";
import { HeaderBar, LoadingBar } from "./header";
import { GraphBar } from "./graph";

const currentRoute = useRoute();
const graphVisible = ref(currentRoute.path === Routes.ARTIFACT);

watch(
  () => currentRoute.path,
  () => (graphVisible.value = currentRoute.path === Routes.ARTIFACT)
);
</script>
