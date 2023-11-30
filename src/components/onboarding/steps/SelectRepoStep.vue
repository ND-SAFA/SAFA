<template>
  <typography
    el="p"
    value="
      To import code, you will need to connect to our GitHub integration,
      and be a contributor on the repository.
      Your organization will also need to approve our integration.
    "
  />

  <git-hub-authentication inactive />

  <q-banner rounded class="bg-background q-mt-md">
    <template #avatar>
      <icon variant="security" color="secondary" size="md" class="q-mr-sm" />
    </template>
    <typography
      value="
        Our integration will only use read access from the repository you select,
        and does not train on any data you import.
        As we work toward SOC II compliance, you can track our current security practices below.
      "
    />
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
  </q-banner>
</template>

<script lang="ts">
/**
 *
 */
export default {
  name: "SelectRepoStep",
};
</script>

<script setup lang="ts">
import { SECURITY_LINK } from "@/util";
import { GitHubAuthentication } from "@/components/integrations";
import { Icon, TextButton, Typography } from "@/components";

/**
 * Opens the security practices link in a new tab.
 */
function handleViewSecurityPractices() {
  window.open(SECURITY_LINK);
}
</script>
