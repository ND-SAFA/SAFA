<template>
  <div style="position: absolute; bottom: 0" class="full-width">
    <v-list-item>
      <template #prepend>
        <notifications />
      </template>
      <v-list-item-title>
        <typography value="Notifications" />
      </v-list-item-title>
    </v-list-item>

    <v-divider />

    <v-list-item :to="accountPath">
      <template #prepend>
        <v-icon color="primary">mdi-account-circle</v-icon>
      </template>
      <v-list-item-title data-cy="page-account" class="ml-4 py-3">
        <typography bold value="My Account" />
      </v-list-item-title>
    </v-list-item>
  </div>
</template>

<script lang="ts">
/**
 * Renders the navigation drawer.
 */
export default {
  name: "NavAccount",
};
</script>

<script setup lang="ts">
import { Routes } from "@/router";
import { Typography } from "@/components/common";
import Notifications from "./Notifications.vue";

const accountPath = Routes.ACCOUNT;
</script>
