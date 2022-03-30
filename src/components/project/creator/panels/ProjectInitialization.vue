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
import JiraApi from "jira-client";
import {
  ProjectFilesInput,
  ProjectIdentifierInput,
} from "@/components/project/shared";

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
    return { tab: 0, tabs: ["Basic", "Bulk Upload", "JIRA"] };
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
    jiraLogin(): void {
      const jira = new JiraApi({
        protocol: "https",
        host: "safa-ai.atlassian.com",
        username: "tjnewman111@gmail.com",
        password: "Th1s1satlass1an",
        apiVersion: "latest",
        strictSSL: true,
      });

      jira.getProject("DRON").then((res: any) => console.log(res));
    },
  },
});
</script>
