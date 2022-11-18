<template>
  <panel-card>
    <typography el="h2" variant="subtitle" value="Linked Integrations" />
    <v-divider class="mb-2" />
    <jira-authentication />
    <git-hub-authentication />
  </panel-card>
</template>

<script lang="ts">
import Vue from "vue";
import { PanelCard, Typography } from "@/components/common/";
import {
  JiraAuthentication,
  GitHubAuthentication,
} from "@/components/integrations";

/**
 * IntegrationsAccounts.
 */
export default Vue.extend({
  name: "IntegrationsAccounts",
  components: {
    JiraAuthentication,
    GitHubAuthentication,
    Typography,
    PanelCard,
  },
});
</script>
