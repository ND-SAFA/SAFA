<template>
  <v-card outlined>
    <v-container class="d-flex justify-center">
      <v-btn class="my-10" color="primary" @click="jiraLogin">
        Connect to JIRA
      </v-btn>
    </v-container>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { getParam, QueryParams } from "@/router";
import {
  authorizeJira,
  getJiraToken,
  getJiraProjects,
  getJiraCloudSites,
} from "@/api";

/**
 * Allows for creating a project from JIRA.
 */
export default Vue.extend({
  async mounted() {
    const accessCode = getParam(QueryParams.JIRA_TOKEN);

    if (!accessCode) return;

    const token = await getJiraToken(String(accessCode));
    const sites = await getJiraCloudSites(token);
    const projects = await getJiraProjects(token, sites[0].id);

    console.log(projects);
  },
  methods: {
    jiraLogin(): void {
      authorizeJira();
    },
  },
});
</script>
