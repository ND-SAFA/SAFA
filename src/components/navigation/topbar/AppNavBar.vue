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
import { useTheme } from "vuetify";
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { Routes } from "@/router";
import { HeaderBar } from "./header";
import { GraphBar } from "./graph";

const theme = useTheme();
const darkMode = computed(() => theme.global.current.value.dark);

const currentRoute = useRoute();
const graphVisible = ref(currentRoute.path === Routes.ARTIFACT);

watch(
  () => currentRoute.path,
  () => (graphVisible.value = currentRoute.path === Routes.ARTIFACT)
);
</script>
