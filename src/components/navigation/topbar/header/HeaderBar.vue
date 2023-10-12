<template>
  <div class="full-width">
    <flex-box full-width justify="between" align="center" y="1">
      <nav-breadcrumbs v-if="ENABLED_FEATURES.NAV_BREADCRUMBS" />
      <flex-box v-else align="center">
        <project-selector />
        <version-selector />
      </flex-box>
      <q-space />
      <update-button />
      <project-searchbar v-if="graphVisible" />
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

<script setup lang="ts">
import { useRoute } from "vue-router";
import { computed } from "vue";
import { ENABLED_FEATURES } from "@/util";
import { Routes } from "@/router";
import { FlexBox, Separator } from "@/components/common";
import { VersionSelector, ProjectSelector } from "@/components/project";
import { ProjectSearchbar } from "@/components/search";
import NavBreadcrumbs from "./NavBreadcrumbs.vue";
import UpdateButton from "./UpdateButton.vue";

const currentRoute = useRoute();

const graphVisible = computed(() => currentRoute.path === Routes.ARTIFACT);
</script>
