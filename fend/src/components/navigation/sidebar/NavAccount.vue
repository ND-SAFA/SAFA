<template>
  <div class="full-width nav-account">
    <list-item title="" to="">
      <template #icon>
        <saving-icon />
      </template>
    </list-item>

    <list-item
      to=""
      title="Send Feedback"
      icon="feedback"
      clickable
      tooltip="Send Feedback"
      @click="handleFeedback"
    />

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
      :class="option.class"
      :action-cols="2"
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
import { FEEDBACK_LINK } from "@/util";
import { orgStore, permissionStore, sessionStore } from "@/hooks";
import { Routes } from "@/router";
import { ListItem } from "@/components/common";
import SavingIcon from "./SavingIcon.vue";
import Notifications from "./Notifications.vue";

const currentRoute = useRoute();

const options = computed<NavOption[]>(() => [
  {
    label: "My Organization",
    icon: "organization",
    subtitle: orgStore.org.name,
    path: Routes.ORG,
    color: Routes.ORG === currentRoute.path ? "primary" : "text",
    tooltip: "My Organization: " + orgStore.org.name,
  },
  {
    label: "My Account",
    subtitle: sessionStore.userEmail,
    icon: "account",
    path: Routes.ACCOUNT,
    color: Routes.ACCOUNT === currentRoute.path ? "primary" : "text",
    tooltip: "My Account: " + sessionStore.userEmail,
  },
  ...(permissionStore.isSuperuser
    ? [
        {
          label: "Admin Controls",
          icon: "admin",
          path: Routes.ADMIN,
          color: permissionStore.isSuperuserActive ? "primary" : "text",
          class: permissionStore.isSuperuserActive ? "bd-primary" : "",
          tooltip: "Admin Controls",
        } as NavOption,
      ]
    : []),
]);

/**
 * Routes the user to the feedback page.
 */
function handleFeedback(): void {
  window.open(FEEDBACK_LINK);
}
</script>
