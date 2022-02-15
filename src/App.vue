<template>
  <v-app>
    <v-main>
      <transition name="fade" mode="out-in">
        <keep-alive>
          <router-view />
        </keep-alive>
      </transition>
    </v-main>

    <snackbar :timeout="5000" />
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import { verifyAuthentication } from "@/api";
import { Snackbar } from "@/components";

export default Vue.extend({
  name: "app",
  components: {
    Snackbar,
  },
  async mounted() {
    await verifyAuthentication();
  },
});
</script>

<style lang="scss">
@import "./assets/main.scss";
</style>
