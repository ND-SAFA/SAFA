<template>
  <div>
    <v-container>
      <flex-box justify="space-between">
        <typography el="h1" variant="title" value="My Account" />
        <v-btn text color="error" @click="handleLogout">
          <v-icon>mdi-logout-variant</v-icon>
          Log Out
        </v-btn>
      </flex-box>
      <v-divider />
      <v-container>
        <update-password />
        <delete-account />
      </v-container>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { handleLogout } from "@/api";
import { Typography, FlexBox } from "@/components/common";
import DeleteAccount from "./DeleteAccount.vue";
import UpdatePassword from "./UpdatePassword.vue";

/**
 * Displays information on the current user.
 */
export default Vue.extend({
  name: "MyAccount",
  components: {
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
