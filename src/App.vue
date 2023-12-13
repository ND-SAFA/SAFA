<template>
  <q-layout view="lHh LpR lfr" class="bg-background">
    <app-nav />
    <q-page-container>
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
/**
 * Renders the SAFA app.
 */
export default {
  name: "App",
};
</script>

<script setup lang="ts">
import { onMounted } from "vue";
import { useTheme } from "@/hooks";
import { AppNav } from "@/components";

const theme = useTheme();

onMounted(() => {
  theme.loadDarkMode();
});
</script>

<style lang="scss">
@import "assets/style/main";
</style>
