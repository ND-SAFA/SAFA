<template>
  <panel-card title="Integration Sources">
    <jira-authentication inactive />
    <git-hub-authentication inactive />
  </panel-card>
</template>

<script lang="ts">
/**
 * IntegrationsAccounts.
 */
export default {
  name: "IntegrationsAccounts",
};
</script>

<script setup lang="ts">
import {
  JiraAuthentication,
  GitHubAuthentication,
} from "@/components/integrations";
import { PanelCard } from "@/components/common";
</script>
