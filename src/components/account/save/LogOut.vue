<template>
  <panel-card title="My Account">
    <flex-box justify="between" align="center">
      <typography :value="email" />
      <text-button
        text
        label="Log Out"
        icon="logout"
        data-cy="button-account-logout"
        @click="sessionApiStore.handleLogout(true)"
      />
    </flex-box>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays an action to log out of the app.
 */
export default {
  name: "LogOut",
};
</script>

<script setup lang="ts">
import { computed } from "vue";
import { sessionApiStore, sessionStore } from "@/hooks";
import {
  PanelCard,
  FlexBox,
  Typography,
  TextButton,
} from "@/components/common";

const email = computed(() => sessionStore.user?.email || "");
</script>
