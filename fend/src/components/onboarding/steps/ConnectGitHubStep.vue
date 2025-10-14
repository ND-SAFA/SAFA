<template>
  <typography el="p" :value="ONBOARDING_GITHUB_IMPORT" />

  <git-hub-authentication inactive />

  <flex-box
    v-if="ENABLED_FEATURES.ONBOARDING_PUBLIC_REPOS"
    align="center"
    justify="center"
    full-width
  >
    <separator style="width: 40px" />
    <typography secondary el="div" class="q-ma-sm" value="OR" />
    <separator style="width: 40px" />
  </flex-box>

  <flex-box
    v-if="ENABLED_FEATURES.ONBOARDING_PUBLIC_REPOS"
    t="4"
    justify="center"
  >
    <text-button
      outlined
      icon="changelog"
      @click="onboardingApiStore.handleLoadNextStep('connect')"
    >
      Upload Public Repo
    </text-button>
  </flex-box>

  <callout-sub-step icon="security" :message="ONBOARDING_GITHUB_SECURITY">
    <template #action>
      <text-button
        text
        color="secondary"
        icon="changelog"
        @click="handleViewSecurityPractices"
      >
        Security Practices
      </text-button>
    </template>
  </callout-sub-step>

  <flex-box
    v-if="integrationsStore.validGitHubCredentials"
    t="4"
    justify="center"
  >
    <text-button
      outlined
      @click="onboardingApiStore.handleLoadNextStep('connect')"
    >
      Continue
    </text-button>
  </flex-box>
</template>

<script lang="ts">
/**
 * Connects to GitHub to import code during onboarding.
 */
export default {
  name: "ConnectGitHubStep",
};
</script>

<script setup lang="ts">
import {
  ENABLED_FEATURES,
  ONBOARDING_GITHUB_IMPORT,
  ONBOARDING_GITHUB_SECURITY,
  SECURITY_LINK,
} from "@/util";
import { integrationsStore, onboardingApiStore } from "@/hooks";
import { GitHubAuthentication } from "@/components/integrations";
import {
  TextButton,
  Typography,
  FlexBox,
  Separator,
} from "@/components/common";
import CalloutSubStep from "./CalloutSubStep.vue";

/**
 * Opens the security practices link in a new tab.
 */
function handleViewSecurityPractices() {
  window.open(SECURITY_LINK);
}
</script>
