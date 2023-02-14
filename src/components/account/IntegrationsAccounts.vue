<template>
  <panel-card>
    <authentication-selector inactive />
  </panel-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { AuthenticationSelector } from "@/components/integrations";
import { PanelCard } from "@/components/common";

/**
 * IntegrationsAccounts.
 */
export default defineComponent({
  name: "IntegrationsAccounts",
  components: {
    PanelCard,
    AuthenticationSelector,
  },
});
</script>
