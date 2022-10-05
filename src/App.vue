<template>
  <v-app>
    <v-main>
      <transition name="fade" mode="out-in">
        <keep-alive>
          <router-view />
        </keep-alive>
      </transition>
    </v-main>
    <navigation />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import { Navigation } from "@/components";

/**
 * Renders the SAFA app.
 */
export default Vue.extend({
  name: "App",
  components: {
    Navigation,
  },
});
</script>

<style lang="scss">
@import "./assets/main.scss";
</style>
