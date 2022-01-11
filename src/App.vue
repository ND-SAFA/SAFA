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
import { Routes } from "@/router";
import { Snackbar } from "@/components";
import { loadLastProject, logout } from "@/api";

export default Vue.extend({
  name: "app",
  components: {
    Snackbar,
  },
  async mounted() {
    const isAuthorized = await sessionModule.hasAuthorization();
    const location = window.location.href;

    if (!isAuthorized) {
      return await logout();
    } else if (isAuthorized && location.includes(Routes.ARTIFACT_TREE)) {
      await loadLastProject();
    }
  },
});
</script>

<style lang="scss">
@import "./assets/main.scss";
@import "./assets/app-styles.css";
@import "./assets/context-menu.css";
</style>
