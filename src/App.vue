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
import { sessionModule } from "@/store";
import { navigateTo, Routes } from "@/router";
import { Snackbar } from "@/components";

export default Vue.extend({
  name: "app",
  components: {
    Snackbar,
  },
  mounted() {
    sessionModule.loadSession().then(() => navigateTo(Routes.HOME));
  },
});
</script>

<style lang="scss">
@import "./assets/main.scss";

@import "./assets/app-styles.css";
@import "./assets/artifact-styles.css";
@import "./assets/context-menu.css";
@import "./assets/modal-sizes.css";
</style>
