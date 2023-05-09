<template>
  <private-page full-window>
    <flex-box full-width justify="center" t="10">
      <project-searchbar />
    </flex-box>
  </private-page>
</template>

<script lang="ts">
/**
 * Displays the project search page.
 */
export default {
  name: "SearchView",
};
</script>

<script setup lang="ts">
import { ProjectSearchbar } from "@/components/search";
import { PrivatePage, FlexBox } from "@/components";
</script>
