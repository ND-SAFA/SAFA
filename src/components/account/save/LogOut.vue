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
    <flex-box
      v-if="sessionStore.superuser"
      justify="between"
      align="center"
      t="2"
    >
      <div>
        <typography value="Superuser mode" el="div" />
        <typography secondary value="Enables all permissions" />
      </div>
      <q-toggle
        v-model="adminApiStore.activeSuperuser"
        label="Enabled"
        class="q-mr-md"
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
import { adminApiStore, sessionApiStore, sessionStore } from "@/hooks";
import {
  PanelCard,
  FlexBox,
  Typography,
  TextButton,
} from "@/components/common";

const email = computed(() => sessionStore.user?.email || "");
</script>
