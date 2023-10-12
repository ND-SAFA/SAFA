<template>
  <div class="full-width">
    <flex-box
      :wrap="smallWindow"
      align="center"
      full-width
      justify="between"
      y="2"
    >
      <flex-box :b="smallWindow ? '1' : ''" align="center">
        <project-selector />
        <version-selector />
      </flex-box>
      <q-space />
      <project-searchbar v-if="graphVisible" />
      <q-space />
      <q-space />
      <update-button />
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
import { useScreen } from "@/hooks";
import { Routes } from "@/router";
import { FlexBox, Separator } from "@/components/common";
import { VersionSelector, ProjectSelector } from "@/components/project";
import { ProjectSearchbar } from "@/components/search";
import UpdateButton from "./UpdateButton.vue";

const currentRoute = useRoute();

const { smallWindow } = useScreen();

const graphVisible = computed(() => currentRoute.path === Routes.ARTIFACT);
</script>
