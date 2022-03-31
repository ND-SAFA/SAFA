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
import { sessionModule } from "@/store";
import { getParam, QueryParams } from "@/router";

const clientId = "oKrINIDiMwdJTjiBsDVPTq2yhXKE6JpH";
const clientSecret =
  "8c1Z8ZrlkXUkbCh3ktWayPFZMDMzjoNvAxys2mvmWPWN8vA1fSJ2oVFzoyWK7rjf";
const redirect = "http://localhost:8080/create?tab=jira";

/**
 * Allows for creating a project from JIRA.
 */
export default Vue.extend({
  async mounted() {
    const accessCode = getParam(QueryParams.JIRA_TOKEN);

    if (!accessCode) return;

    const authRes = await fetch("https://auth.atlassian.com/oauth/token", {
      method: "POST",
      body: JSON.stringify({
        grant_type: "authorization_code",
        client_id: clientId,
        client_secret: clientSecret,
        code: accessCode,
        redirect_uri: redirect,
      }),
    });

    const accessToken = (await authRes.json()).access_token as string;

    const cloudRes = await fetch(
      "https://api.atlassian.com/oauth/token/accessible-resources",
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    const cloudId = (await cloudRes.json())[0].id as string;

    const projectsRes = await fetch(
      `https://api.atlassian.com/ex/jira/${cloudId}/rest/api/3/project/search`
    );

    const projects = await projectsRes.json();

    console.log(projects);
  },
  methods: {
    async jiraLogin(): Promise<void> {
      window.open(
        `https://auth.atlassian.com/authorize?` +
          `audience=api.atlassian.com&` +
          `client_id=${clientId}&` +
          `scope=read%3Ajira-work&` +
          `redirect_uri=${redirect}&` +
          `state=${sessionModule.getToken}&` +
          `response_type=code&` +
          `prompt=consent`
      );
    },
  },
});
</script>
