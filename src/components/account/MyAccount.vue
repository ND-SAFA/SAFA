<template>
  <div>
    <flex-box justify="between" align="center">
      <typography el="h1" variant="title" value="My Account" />
      <text-button
        text
        label="Log Out"
        color="negative"
        icon="logout"
        icon-id="mdi-logout-variant"
        @click="handleLogout"
      />
    </flex-box>
    <separator b="4" />
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
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { handleLogout } from "@/api";
import { Typography, FlexBox, TextButton } from "@/components/common";
import Separator from "@/components/common/display/Separator.vue";
import ExternalLinks from "./ExternalLinks.vue";
import IntegrationsAccounts from "./IntegrationsAccounts.vue";
import DeleteAccount from "./DeleteAccount.vue";
import UpdatePassword from "./UpdatePassword.vue";
import ThemeController from "./ThemeController.vue";

/**
 * Displays information on the current user.
 */
export default defineComponent({
  name: "MyAccount",
  components: {
    Separator,
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
      handleLogout(true);
    },
  },
});
</script>
