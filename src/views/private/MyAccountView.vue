<template>
  <private-page title="My Account">
    <template #actions>
      <text-button
        text
        label="Log Out"
        color="negative"
        icon="logout"
        icon-id="mdi-logout-variant"
        data-cy="button-account-logout"
        @click="handleLogoutClick"
      />
    </template>
    <my-account />
  </private-page>
</template>

<script lang="ts">
/**
 * Displays the account page.
 */
export default {
  name: "MyAccountView",
};
</script>

<script setup lang="ts">
import { handleLogout } from "@/api";
import { PrivatePage, MyAccount, TextButton } from "@/components";

/**
 * Logs out back to the login page.
 */
function handleLogoutClick() {
  handleLogout(true);
}
</script>
