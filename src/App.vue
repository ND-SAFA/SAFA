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
import { LocalStorageKeys } from "@/types";
import { useTheme } from "@/hooks";
import { AppNav } from "@/components";

const theme = useTheme();

onMounted(() => {
  const now = new Date();
  const hour = now.getHours();
  const isNight = hour < 6 || hour > 18; // Assuming night is from 6PM to 6AM

  const storedDarkMode = localStorage.getItem(LocalStorageKeys.darkMode);

  theme.darkMode.value = storedDarkMode ? storedDarkMode === "true" : isNight;
});
</script>

<style lang="scss">
@import "assets/style/main";
</style>
