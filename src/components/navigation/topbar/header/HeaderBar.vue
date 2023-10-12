<template>
  <div class="full-width">
    <flex-box
      full-width
      :wrap="smallWindow"
      justify="between"
      align="center"
      y="2"
    >
      <flex-box align="center" :b="smallWindow ? '1' : ''">
        <project-selector />
        <version-selector />
        <!--        <nav-breadcrumbs />-->
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
import { useScreen } from "@/hooks";
import { Routes } from "@/router";
import { FlexBox, Separator } from "@/components/common";
import { VersionSelector, ProjectSelector } from "@/components/project";
import { ProjectSearchbar } from "@/components/search";
// import NavBreadcrumbs from "./NavBreadcrumbs.vue";
import UpdateButton from "./UpdateButton.vue";

const currentRoute = useRoute();

const { smallWindow } = useScreen();

const graphVisible = computed(() => currentRoute.path === Routes.ARTIFACT);
</script>
