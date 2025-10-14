<template>
  <private-page full-window>
    <organization-tabs />
  </private-page>
</template>

<script lang="ts">
/**
 * Displays the organization page.
 */
export default {
  name: "MyOrganizationView",
};
</script>

<script setup lang="ts">
import { PrivatePage, OrganizationTabs } from "@/components";
</script>
