<template>
  <div style="position: absolute; bottom: 0" class="full-width">
    <list-item to="" title="Notifications">
      <template #icon>
        <notifications />
      </template>
    </list-item>

    <q-separator />

    <list-item
      :to="Routes.ACCOUNT"
      color="primary"
      icon="account"
      title="My Account"
      class="q-py-sm"
    />
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
import { ListItem } from "@/components/common";
import Notifications from "./Notifications.vue";
</script>
