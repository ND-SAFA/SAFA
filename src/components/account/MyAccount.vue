<template>
  <div>
    <v-container>
      <flex-box justify="space-between">
        <typography el="h1" variant="title" value="My Account" />
        <text-button
          text
          color="error"
          data-cy="button-logout"
          icon-id="mdi-logout-variant"
          @click="handleLogout"
        >
          Log Out
        </text-button>
      </flex-box>
      <v-divider class="mb-4" />
      <v-row>
        <v-col cols="6">
          <theme-controller />
          <update-password />
          <delete-account />
        </v-col>
        <v-col cols="6">
          <external-links />
          <integrations-accounts />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { handleLogout } from "@/api";
import { Typography, FlexBox, TextButton } from "@/components/common";
import ExternalLinks from "./ExternalLinks.vue";
import IntegrationsAccounts from "./IntegrationsAccounts.vue";
import DeleteAccount from "./DeleteAccount.vue";
import UpdatePassword from "./UpdatePassword.vue";
import ThemeController from "./ThemeController.vue";

/**
 * Displays information on the current user.
 */
export default Vue.extend({
  name: "MyAccount",
  components: {
    TextButton,
    ThemeController,
    ExternalLinks,
    IntegrationsAccounts,
    FlexBox,
    Typography,
    DeleteAccount,
    UpdatePassword,
  },
  methods: {
    /**
     * Logs the current user out.
     */
    handleLogout(): void {
      handleLogout();
    },
  },
});
</script>
