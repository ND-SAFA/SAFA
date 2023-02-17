<template>
  <q-layout>
    <q-page-container>
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
      <app-nav />
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
import { AppNav } from "@/components";
</script>

<style lang="scss">
@import "assets/style/main";
</style>
