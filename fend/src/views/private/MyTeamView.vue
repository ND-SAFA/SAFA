<template>
  <private-page full-window>
    <team-tabs />
  </private-page>
</template>

<script lang="ts">
/**
 * Displays the team page.
 */
export default {
  name: "MyTeamView",
};
</script>

<script setup lang="ts">
import { PrivatePage, TeamTabs } from "@/components";
</script>
