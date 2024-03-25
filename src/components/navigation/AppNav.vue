<template>
  <div :data-cy="displayNavigation ? 'is-logged-in' : ''">
    <app-nav-drawer v-if="displaySidebar" />
    <app-nav-bar v-if="displayNavigation" />
    <details-drawer v-if="displayNavigation" />
    <snackbar />
    <app-confirm-modal :message="confirmationMessage" />
    <job-log-modal />
    <save-project-modal />
    <transfer-project-modal />
    <delete-project-modal />
    <onboarding-popup />
    <flex-box
      v-if="displayLoading"
      full-width
      justify="center"
      align="center"
      style="height: 100vh"
    >
      <q-spinner-ball class="nav-gradient" size="4em" />
    </flex-box>
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
import { useRoute } from "vue-router";
import {
  logStore,
  permissionStore,
  sessionApiStore,
  sessionStore,
} from "@/hooks";
import { AppConfirmModal, FlexBox } from "@/components/common";
import {
  SaveProjectModal,
  DeleteProjectModal,
  TransferProjectModal,
} from "@/components/project";
import { OnboardingPopup } from "@/components/onboarding";
import { JobLogModal } from "@/components/jobs";
import { AppNavDrawer } from "./sidebar";
import { AppNavBar } from "./topbar";
import { DetailsDrawer } from "./detailsDrawer";
import Snackbar from "./Snackbar.vue";

const currentRoute = useRoute();

const displayLoading = computed(() => sessionApiStore.authLoading);
const displayNavigation = computed(
  () =>
    sessionStore.doesSessionExist &&
    !sessionApiStore.loading &&
    !currentRoute.meta.isPublic
);
const displaySidebar = computed(
  () => displayNavigation.value && permissionStore.isAllowed("safa.view")
);

const confirmationMessage = computed(() => logStore.confirmation);
</script>
