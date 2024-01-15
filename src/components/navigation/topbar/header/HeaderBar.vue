<template>
  <div class="full-width">
    <flex-box full-width justify="between" align="center" y="1">
      <nav-breadcrumbs />
      <members-bar />
      <q-space />
      <project-searchbar v-if="graphVisible" />
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
import { permissionStore, sessionApiStore } from "@/hooks";
import { Routes } from "@/router";
import { FlexBox, Separator } from "@/components/common";
import { ProjectSearchbar } from "@/components/search";
import TextButton from "@/components/common/button/TextButton.vue";
import MembersBar from "./MembersBar.vue";
import NavBreadcrumbs from "./NavBreadcrumbs.vue";

const currentRoute = useRoute();

const graphVisible = computed(() => currentRoute.path === Routes.ARTIFACT);
</script>
