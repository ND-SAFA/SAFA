<template>
  <div class="full-width nav-account">
    <list-item to="" title="">
      <template #icon>
        <saving-icon />
      </template>
    </list-item>

    <list-item to="" title="Notifications">
      <template #icon>
        <notifications />
      </template>
    </list-item>

    <separator />

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
import { ListItem, Separator } from "@/components/common";
import SavingIcon from "./SavingIcon.vue";
import Notifications from "./Notifications.vue";
</script>
