<template>
  <div :data-cy="displayNavigation ? 'is-logged-in' : ''">
    <app-nav-drawer v-if="displaySidebar" />
    <app-nav-bar v-if="displayNavigation" />
    <details-drawer v-if="displayNavigation" />
    <snackbar />
    <app-confirm-modal :message="confirmationMessage" />
    <save-project-modal />
    <delete-project-modal />
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
import { logStore, permissionStore, sessionStore } from "@/hooks";
import { AppConfirmModal } from "@/components/common";
import { SaveProjectModal, DeleteProjectModal } from "@/components/project";
import { AppNavDrawer } from "./sidebar";
import { AppNavBar } from "./topbar";
import { DetailsDrawer } from "./detailsDrawer";
import Snackbar from "./Snackbar.vue";

const displayNavigation = computed(() => sessionStore.doesSessionExist);
const displaySidebar = computed(
  () =>
    displayNavigation.value && permissionStore.organizationAllows("navigation")
);

const confirmationMessage = computed(() => logStore.confirmation);
</script>
