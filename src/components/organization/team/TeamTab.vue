<template>
  <panel-card title="Teams" subtitle="Manage teams and permissions.">
    <typography value="<Team information will be displayed here>" />
  </panel-card>
</template>

<script lang="ts">
/**
 * A tab for managing teams within an organization.
 */
export default {
  name: "TeamTab",
};
</script>

<script setup lang="ts">
import { PanelCard, Typography } from "@/components/common";
</script>
