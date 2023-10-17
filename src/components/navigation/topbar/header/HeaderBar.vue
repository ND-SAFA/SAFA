<template>
  <div class="full-width">
    <flex-box full-width justify="between" align="center" y="1">
      <nav-breadcrumbs />
      <members-bar />
      <q-space />
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

<script lang="ts" setup>
import { useRoute } from "vue-router";
import { computed } from "vue";
import { Routes } from "@/router";
import { FlexBox, Separator } from "@/components/common";
import { ProjectSearchbar } from "@/components/search";
import MembersBar from "./MembersBar.vue";
import NavBreadcrumbs from "./NavBreadcrumbs.vue";

const currentRoute = useRoute();

const graphVisible = computed(() => currentRoute.path === Routes.ARTIFACT);
</script>
