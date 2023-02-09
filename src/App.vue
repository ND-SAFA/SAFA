<template>
  <v-app>
    <v-main class="primary-bg">
      <transition name="fade" mode="out-in">
        <keep-alive>
          <router-view />
        </keep-alive>
      </transition>
    </v-main>
    <app-nav />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import { AppNav } from "@/components";

/**
 * Renders the SAFA app.
 */
export default Vue.extend({
  name: "App",
  components: {
    AppNav,
  },
});
</script>

<style lang="scss">
@import "assets/style/main";
</style>
