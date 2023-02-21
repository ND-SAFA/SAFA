<template>
  <div class="row">
    <div class="col q-mr-md">
      <theme-controller />
      <update-password />
      <delete-account />
    </div>
    <div class="col">
      <external-links />
      <integrations-accounts />
    </div>
  </div>
</template>

<script lang="ts">
/**
 * Displays information on the current user.
 */
export default {
  name: "MyAccount",
};
</script>

<script setup lang="ts">
import ExternalLinks from "./ExternalLinks.vue";
import IntegrationsAccounts from "./IntegrationsAccounts.vue";
import DeleteAccount from "./DeleteAccount.vue";
import UpdatePassword from "./UpdatePassword.vue";
import ThemeController from "./ThemeController.vue";
</script>
