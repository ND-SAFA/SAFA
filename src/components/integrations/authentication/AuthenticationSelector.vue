<template>
  <generic-stepper-list-step
    title="Integration Sources"
    :item-count="2"
    empty-message=""
  >
    <template v-slot:items>
      <under-construction-alert />
      <jira-authentication @click="$emit('input', 'Jira')" />
      <git-hub-authentication @click="$emit('input', 'GitHub')" />
    </template>
  </generic-stepper-list-step>
</template>

<script lang="ts">
import Vue from "vue";
import {
  GenericStepperListStep,
  UnderConstructionAlert,
} from "@/components/common";
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
    GenericStepperListStep,
    UnderConstructionAlert,
  },
});
</script>
