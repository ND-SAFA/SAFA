<template>
  <div class="full-width nav-account">
    <list-item to="" title="">
      <template #icon>
        <saving-icon />
      </template>
    </list-item>

    <notifications />

    <list-item
      v-for="option in options"
      :key="option.label"
      :to="option.path"
      :icon="option.icon"
      :title="option.label"
      :color="option.color"
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
import { computed } from "vue";
import { useRoute } from "vue-router";
import { NavOption } from "@/types";
import { Routes } from "@/router";
import { ListItem } from "@/components/common";
import SavingIcon from "./SavingIcon.vue";
import Notifications from "./Notifications.vue";

const currentRoute = useRoute();

const options = computed<NavOption[]>(() => [
  {
    label: "My Organization",
    icon: "organization",
    path: Routes.ORG,
    color: Routes.ORG === currentRoute.path ? "primary" : "text",
  },
  {
    label: "My Account",
    icon: "account",
    path: Routes.ACCOUNT,
    color: Routes.ACCOUNT === currentRoute.path ? "primary" : "text",
  },
]);
</script>
