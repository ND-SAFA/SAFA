<template>
  <div :data-cy="isLoggedIn ? 'is-logged-in' : ''">
    <app-nav-drawer v-if="isLoggedIn" />
    <app-nav-bar v-if="isLoggedIn" />
    <details-drawer v-if="isLoggedIn" />
    <snackbar />
    <app-confirm-modal :message="logStore.confirmation" />
  </div>
</template>

<script lang="ts">
/**
 * Renders all app navigation components.
 */
export default {
  name: "AppNav",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { logStore, sessionStore } from "@/hooks";
import { AppConfirmModal } from "@/components/common";
import { AppNavDrawer } from "./sidebar";
import { AppNavBar } from "./topbar";
import { DetailsDrawer } from "./detailsDrawer";
import Snackbar from "./Snackbar.vue";

const isLoggedIn = computed(() => sessionStore.doesSessionExist);
</script>
