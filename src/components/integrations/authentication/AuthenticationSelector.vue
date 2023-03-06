<template>
  <stepper-list-step
    title="Integration Sources"
    :item-count="2"
    empty-message=""
  >
    <template v-slot:items>
      <under-construction-alert />
      <jira-authentication
        :inactive="inactive"
        @click="$emit('input', 'Jira')"
      />
      <git-hub-authentication
        :inactive="inactive"
        @click="$emit('input', 'GitHub')"
      />
    </template>
  </stepper-list-step>
</template>

<script lang="ts">
import Vue from "vue";
import { StepperListStep, UnderConstructionAlert } from "@/components/common";
import JiraAuthentication from "./JiraAuthentication.vue";
import GitHubAuthentication from "./GitHubAuthentication.vue";

/**
 * Allows for selecting which type of authentication to import from.
 *
 * @emits-1 `input` ("Jira" | "GitHub") - on source change.
 */
export default Vue.extend({
  name: "AuthenticationSelector",
  components: {
    GitHubAuthentication,
    JiraAuthentication,
    StepperListStep,
    UnderConstructionAlert,
  },
  props: {
    inactive: Boolean,
  },
});
</script>
