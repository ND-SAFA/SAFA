<template>
  <div class="full-width nav-account">
    <list-item to="" title="">
      <template #icon>
        <saving-icon />
      </template>
    </list-item>

    <notifications />

    <list-item
      :to="Routes.ORG"
      icon="organization"
      title="My Organization"
      class="q-py-sm"
    />

    <list-item
      :to="Routes.ACCOUNT"
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
import SavingIcon from "./SavingIcon.vue";
import Notifications from "./Notifications.vue";
</script>
