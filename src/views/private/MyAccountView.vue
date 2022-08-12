<template>
  <private-page>
    <template v-slot:page>
      <back-button />
      <v-container>
        <typography el="h1" variant="title" value="My Account" />
        <v-divider />
        <update-password />
        <v-divider class="mt-4" />
        <delete-account />
      </v-container>
    </template>
  </private-page>
</template>

<script lang="ts">
import Vue from "vue";
import {
  PrivatePage,
  Typography,
  BackButton,
  DeleteAccount,
  UpdatePassword,
} from "@/components";

/**
 * Displays the account page.
 */
export default Vue.extend({
  name: "MyAccountView",
  components: {
    BackButton,
    Typography,
    PrivatePage,
    DeleteAccount,
    UpdatePassword,
  },
});
</script>
