<template>
  <div style="position: absolute; bottom: 0" class="full-width">
    <q-item>
      <q-item-section avator>
        <notifications />
      </q-item-section>
      <q-item-section>
        <typography value="Notifications" l="3" />
      </q-item-section>
    </q-item>

    <q-separator />

    <q-item clickable :to="accountPath" color="primary">
      <q-item-section avatar>
        <icon variant="account" />
      </q-item-section>
      <q-item-section data-cy="page-account" class="py-3">
        <typography bold value="My Account" />
      </q-item-section>
    </q-item>
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
