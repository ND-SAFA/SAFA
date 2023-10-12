<template>
  <div class="full-width nav-account">
    <list-item title="" to="">
      <template #icon>
        <saving-icon />
      </template>
    </list-item>

    <notifications />

    <list-item
      v-for="option in options"
      :key="option.label"
      :color="option.color"
      :icon="option.icon"
      :subtitle="option.subtitle"
      :title="option.label"
      :to="option.path"
      :tooltip="option.tooltip"
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

<script lang="ts" setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import { NavOption } from "@/types";
import { ENABLED_FEATURES } from "@/util";
import { sessionStore } from "@/hooks";
import { Routes } from "@/router";
import { ListItem } from "@/components/common";
import SavingIcon from "./SavingIcon.vue";
import Notifications from "./Notifications.vue";

const currentRoute = useRoute();

const options = computed<NavOption[]>(() => [
  ...(ENABLED_FEATURES.ORGS
    ? [
        {
          label: "My Organization",
          icon: "organization",
          path: Routes.ORG,
          color: Routes.ORG === currentRoute.path ? "primary" : "text",
        },
      ]
    : []),
  {
    label: "My Account",
    subtitle: sessionStore.user?.email,
    icon: "account",
    path: Routes.ACCOUNT,
    color: Routes.ACCOUNT === currentRoute.path ? "primary" : "text",
    tooltip: sessionStore.userEmail,
  },
]);
</script>
