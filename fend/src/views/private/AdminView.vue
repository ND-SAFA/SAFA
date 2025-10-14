<template>
  <private-page>
    <sidebar-grid>
      <template #sidebar>
        <admin-controls />
      </template>
      <onboarding-statistics />
    </sidebar-grid>
  </private-page>
</template>

<script lang="ts">
/**
 * Displays the admin page.
 */
export default {
  name: "AdminView",
};
</script>

<script setup lang="ts">
import {
  PrivatePage,
  AdminControls,
  OnboardingStatistics,
  SidebarGrid,
} from "@/components";
</script>
