<template>
  <div>
    <v-container>
      <flex-box justify="space-between">
        <typography el="h1" variant="title" value="My Account" />
        <v-btn text color="error" @click="handleLogout" data-cy="button-logout">
          <v-icon class="mr-1">mdi-logout-variant</v-icon>
          Log Out
        </v-btn>
      </flex-box>
      <v-divider class="mb-4" />
      <v-row>
        <v-col cols="6">
          <update-password />
          <delete-account />
        </v-col>
        <v-col cols="6">
          <integrations-accounts />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { handleLogout } from "@/api";
import { Typography, FlexBox } from "@/components/common";
import IntegrationsAccounts from "./IntegrationsAccounts.vue";
import DeleteAccount from "./DeleteAccount.vue";
import UpdatePassword from "./UpdatePassword.vue";

/**
 * Displays information on the current user.
 */
export default Vue.extend({
  name: "MyAccount",
  components: {
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
