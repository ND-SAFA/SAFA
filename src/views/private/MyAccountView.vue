<template>
  <private-page>
    <template v-slot:page>
      <v-btn text @click="handleGoBack">
        <v-icon left> mdi-arrow-left </v-icon>
        Go Back
      </v-btn>
      <v-container>
        <h1 class="text-h4">My Account</h1>
        <v-divider class="mb-4" />

        <div style="max-width: 300px">
          <h2 class="text-h6 mb-2">Password</h2>
          <password-field label="Current Password" v-model="oldPassword" />
          <password-field label="New Password" v-model="newPassword" />
          <v-btn outlined @click="handleEditPassword">Update Password</v-btn>
        </div>
      </v-container>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import { PrivatePage, PasswordField } from "@/components";
import { navigateBack } from "@/router";
import { logModule } from "@/store";

/**
 * Displays the account page.
 */
export default Vue.extend({
  name: "MyAccountView",
  components: {
    PasswordField,
    PrivatePage,
  },
  data() {
    return {
      oldPassword: "",
      newPassword: "",
    };
  },
  methods: {
    /**
     * Called to navigate back to the previous page.
     */
    handleGoBack() {
      navigateBack();
    },
    /**
     * Handles an password edit.
     */
    handleEditPassword(): void {
      logModule.onInfo("Account editing is not yet available.");
    },
  },
});
</script>
