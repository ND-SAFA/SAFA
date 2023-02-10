<template>
  <v-app>
    <v-main class="primary-bg">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </v-main>
    <app-nav />
  </v-app>
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
import { AppNav } from "@/components";
</script>

<style lang="scss">
@import "assets/style/main";
</style>
