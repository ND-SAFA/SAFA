<template>
  <div class="full-width nav-account">
    <list-item to="" title="">
      <template #icon>
        <saving-icon />
      </template>
    </list-item>

    <list-item
      to=""
      title="Send Feedback"
      icon="feedback"
      clickable
      @click="handleFeedback"
    />

    <notifications />

    <list-item
      v-for="option in options"
      :key="option.label"
      :to="option.path"
      :icon="option.icon"
      :title="option.label"
      :subtitle="option.subtitle"
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
import { ENABLED_FEATURES, FEEDBACK_LINK } from "@/util";
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
  },
]);

/**
 * Routes the user to the feedback page.
 */
function handleFeedback(): void {
  window.open(FEEDBACK_LINK);
}
</script>
