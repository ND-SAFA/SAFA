<template>
  <panel-card>
    <authentication-selector inactive />
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { AuthenticationSelector } from "@/components/integrations";
import { PanelCard } from "@/components/common";

/**
 * IntegrationsAccounts.
 */
export default Vue.extend({
  name: "IntegrationsAccounts",
  components: {
    PanelCard,
    AuthenticationSelector,
  },
});
</script>
