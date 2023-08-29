<template>
  <panel-card title="My Organization">
    <typography value="<Organization information will be displayed here>" />
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays an organization.
 */
export default {
  name: "OrganizationDisplay",
};
</script>

<script setup lang="ts">
import { PanelCard, Typography } from "@/components/common";
</script>
