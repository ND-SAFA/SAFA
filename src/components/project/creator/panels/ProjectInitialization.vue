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
    jiraLogin(): void {},
  },
});
</script>
