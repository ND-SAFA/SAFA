<template>
  <div class="full-width">
    <flex-box full-width justify="between" align="center" y="1">
      <icon v-if="permissionStore.isDemo" variant="safa" class="q-mr-md" />
      <nav-breadcrumbs />
      <members-bar />
      <q-space />
      <project-searchbar v-if="graphVisible && !permissionStore.isDemo" />
      <text-button
        v-if="permissionStore.isDemo"
        text
        color="primary"
        class="q-ml-md"
        icon="calendar"
        label="Contact Us"
        @click="onboardingStore.handleScheduleCall(false)"
      />
      <text-button
        v-if="permissionStore.isDemo"
        text
        color="gradient"
        class="q-ml-md bd-gradient"
        icon="member-add"
        label="Sign Up"
        @click="sessionApiStore.handleLogout(true, true)"
      />
    </flex-box>
    <separator v-if="graphVisible" nav />
  </div>
</template>

<script lang="ts">
/**
 * Renders the top navigation bar header.
 */
export default {
  name: "HeaderBar",
};
</script>

<script lang="ts" setup>
import { useRoute } from "vue-router";
import { computed } from "vue";
import { onboardingStore, permissionStore, sessionApiStore } from "@/hooks";
import { Routes } from "@/router";
import { FlexBox, Separator } from "@/components/common";
import { ProjectSearchbar } from "@/components/search";
import TextButton from "@/components/common/button/TextButton.vue";
import Icon from "@/components/common/display/icon/Icon.vue";
import MembersBar from "./MembersBar.vue";
import NavBreadcrumbs from "./NavBreadcrumbs.vue";

const currentRoute = useRoute();

const graphVisible = computed(() => currentRoute.path === Routes.ARTIFACT);
</script>
