<template>
  <v-card outlined class="pa-2">
    <authentication-selector />
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { AuthenticationSelector } from "@/components/integrations";

/**
 * IntegrationsAccounts.
 */
export default Vue.extend({
  name: "IntegrationsAccounts",
  components: {
    AuthenticationSelector,
  },
});
</script>
