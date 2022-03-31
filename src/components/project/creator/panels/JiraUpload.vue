<template>
  <v-card outlined>
    <v-container>
      <v-btn block @click="jiraLogin">JIRA Test</v-btn>
    </v-container>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { sessionModule } from "@/store";

/**
 * Allows for creating a project from JIRA.
 */
export default Vue.extend({
  methods: {
    async jiraLogin(): Promise<void> {
      const clientId = "oKrINIDiMwdJTjiBsDVPTq2yhXKE6JpH";
      const redirect = "http://localhost:8080/create?mode=jira";

      window.open(
        `https://auth.atlassian.com/authorize?` +
          `audience=api.atlassian.com&` +
          `client_id=${clientId}&` +
          `scope=read&` +
          `redirect_uri=${redirect}&` +
          `state=${sessionModule.getToken}&` +
          `response_type=code&` +
          `prompt=consent`
      );
      // const basicRes = await fetch(
      //   `https://${clientId}.atlassian.net/rest/api/3/project/search`
      // );
      //
      // console.log(await basicRes.json());
      //
      // const cloudId = "xyz";
      // const authRes = await fetch(
      //   `https://api.atlassian.com/ex/jira/${cloudId}/rest/api/3/project/search`
      // );
      //
      // console.log(await authRes.json());
    },
  },
});
</script>
