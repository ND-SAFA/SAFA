<template>
  <div
    style="position: absolute; bottom: 0"
    class="full-width"
  >
    <v-list-item>
      <template #prepend>
        <notifications />
      </template>
      <v-list-item-title>
        <typography
          value="Notifications"
          l="3"
        />
      </v-list-item-title>
    </v-list-item>

    <v-divider />

    <v-list-item
      :to="accountPath"
      color="primary"
    >
      <template #prepend>
        <icon variant="account" />
      </template>
      <v-list-item-title
        data-cy="page-account"
        class="py-3"
      >
        <typography
          bold
          value="My Account"
        />
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
import { Typography, Icon } from "@/components/common";
import Notifications from "./Notifications.vue";

const accountPath = Routes.ACCOUNT;
</script>
