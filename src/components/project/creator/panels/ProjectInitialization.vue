<template>
  <div>
    <v-tabs v-model="tab">
      <v-tab v-for="item in tabs" :key="item">
        {{ item }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item key="1">
        <project-identifier-input
          v-bind:name.sync="currentName"
          v-bind:description.sync="currentDescription"
        />
      </v-tab-item>

      <v-tab-item key="2">
        <project-identifier-input
          v-bind:name.sync="currentName"
          v-bind:description.sync="currentDescription"
        />
        <project-files-input
          v-bind:name.sync="currentName"
          v-bind:description.sync="currentDescription"
        />
      </v-tab-item>
      <v-tab-item key="3">
        <v-btn @click="jiraLogin">JIRA</v-btn>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import {
  ProjectFilesInput,
  ProjectIdentifierInput,
} from "@/components/project/shared";
import { sessionModule } from "@/store";

/**
 * Input fields for editing a project.
 *
 * @emits-1 `update:name` (string) - On name updated.
 * @emits-2 `update:description` (string) - On description updated.
 * @emits-3 `close` - On close.
 */
export default Vue.extend({
  components: {
    ProjectFilesInput,
    ProjectIdentifierInput,
  },
  props: {
    name: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      required: true,
    },
  },
  data() {
    return { tab: 0, tabs: ["Standard Upload", "Bulk Upload", "JIRA Upload"] };
  },
  computed: {
    currentName: {
      get(): string {
        return this.name;
      },
      set(newName: string): void {
        this.$emit("update:name", newName);
      },
    },
    currentDescription: {
      get(): string {
        return this.description;
      },
      set(newDescription: string): void {
        this.$emit("update:description", newDescription);
      },
    },
  },
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
