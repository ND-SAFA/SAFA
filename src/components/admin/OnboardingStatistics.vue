<template>
  <panel-card v-if="!!stats" title="Onboarding Statistics">
    <flex-box>
      <email-input
        v-model="userEmail"
        label="User Email"
        @enter="handleLoadUser"
      />
      <text-button text l="1" t="2" label="Load User" @click="handleLoadUser" />
    </flex-box>
    <div v-if="!userStats">
      <typography value="Accounts" variant="subtitle" el="h3" />
      <flex-box full-width>
        <flex-item parts="4">
          <typography value="Created" secondary el="p" />
          <typography value="Verified" secondary el="p" />
          <typography value="With Tracking" secondary el="p" />
        </flex-item>
        <flex-item>
          <typography :value="stats.accounts.created" el="p" />
          <typography :value="stats.accounts.verified" el="p" />
          <typography
            :value="stats.accounts.haveProperProgressTracking"
            el="p"
          />
        </flex-item>
      </flex-box>

      <typography value="GitHub" variant="subtitle" el="h3" />
      <flex-box full-width>
        <flex-item parts="4">
          <typography value="Accounts" secondary el="p" />
          <typography value="Percent" secondary el="p" />
          <typography value="Average Time" secondary el="p" />
        </flex-item>
        <flex-item>
          <typography
            :value="stats.github.withProperTracking.accounts"
            el="p"
          />
          <typography
            :value="convertPercent(stats.github.withProperTracking.percent)"
            el="p"
          />
          <typography
            :value="
              convertDuration(stats.github.withProperTracking.averageTime)
            "
            el="p"
          />
        </flex-item>
      </flex-box>

      <typography value="Import" variant="subtitle" el="h3" />
      <flex-box full-width>
        <flex-item parts="4">
          <typography value="Total Imports" secondary el="p" />
          <typography value="Total Accounts" secondary el="p" />
          <typography value="Total Percent" secondary el="p" />
          <typography value="Total Average Time" secondary el="p" />
          <typography value="With GitHub Accounts" secondary el="p" />
          <typography value="With GitHub Percent" secondary el="p" />
          <typography value="With GitHub Average Time" secondary el="p" />
        </flex-item>
        <flex-item>
          <typography :value="stats.imports.totalPerformed" el="p" />
          <typography :value="stats.imports.total.accounts" el="p" />
          <typography
            :value="convertPercent(stats.imports.total.percent)"
            el="p"
          />
          <typography
            :value="convertDuration(stats.imports.total.averageTime)"
            el="p"
          />
          <typography :value="stats.imports.fromGithubProper.accounts" el="p" />
          <typography
            :value="convertPercent(stats.imports.fromGithubProper.percent)"
            el="p"
          />
          <typography
            :value="convertDuration(stats.imports.fromGithubProper.averageTime)"
            el="p"
          />
        </flex-item>
      </flex-box>

      <typography value="Summarization" variant="subtitle" el="h3" />
      <flex-box full-width>
        <flex-item parts="4">
          <typography value="Total Summarizations" secondary el="p" />
        </flex-item>
        <flex-item>
          <typography :value="stats.summarizations.totalPerformed" el="p" />
        </flex-item>
      </flex-box>

      <typography value="Generation" variant="subtitle" el="h3" />
      <flex-box full-width>
        <flex-item parts="4">
          <typography value="Total Generations" secondary el="p" />
          <typography value="Total Lines Generated On" secondary el="p" />
          <typography value="Total Accounts" secondary el="p" />
          <typography value="Total Percent" secondary el="p" />
          <typography value="Total Average Time" secondary el="p" />
          <typography value="With Import Accounts" secondary el="p" />
          <typography value="With Import Percent" secondary el="p" />
          <typography value="With Import Average Time" secondary el="p" />
        </flex-item>
        <flex-item>
          <typography :value="stats.generations.totalGenerations" el="p" />
          <typography :value="stats.generations.linesGeneratedOn" el="p" />
          <typography :value="stats.generations.total.accounts" el="p" />
          <typography
            :value="convertPercent(stats.generations.total.percent)"
            el="p"
          />
          <typography
            :value="convertDuration(stats.generations.total.averageTime)"
            el="p"
          />
          <typography
            :value="stats.generations.fromImportProper.accounts"
            el="p"
          />
          <typography
            :value="convertPercent(stats.generations.fromImportProper.percent)"
            el="p"
          />
          <typography
            :value="
              convertDuration(stats.generations.fromImportProper.averageTime)
            "
            el="p"
          />
        </flex-item>
      </flex-box>
    </div>
    <div v-else>
      <typography :value="'Account: ' + userEmail" variant="subtitle" el="h3" />
      <flex-box full-width>
        <flex-item parts="4">
          <typography value="Imports" secondary el="p" />
          <typography value="Summarizations" secondary el="p" />
          <typography value="Generations" secondary el="p" />
          <typography value="Lines Generated On" secondary el="p" />
          <typography value="Created At" secondary el="p" />
          <typography value="GitHub Linked At" secondary el="p" />
          <typography value="Project Imported At" secondary el="p" />
          <typography value="Generated At" secondary el="p" />
        </flex-item>
        <flex-item>
          <typography :value="userStats.importsPerformed" el="p" />
          <typography :value="userStats.summarizationsPerformed" el="p" />
          <typography :value="userStats.generationsPerformed" el="p" />
          <typography :value="userStats.linesGeneratedOn" el="p" />
          <typography
            :value="timestampToDisplay(userStats.accountCreatedTime)"
            el="p"
          />
          <typography
            :value="timestampToDisplay(userStats.githubLinkedTime)"
            el="p"
          />
          <typography
            :value="timestampToDisplay(userStats.firstProjectImportedTime)"
            el="p"
          />
          <typography
            :value="timestampToDisplay(userStats.firstGenerationPerformedTime)"
            el="p"
          />
        </flex-item>
      </flex-box>
    </div>
  </panel-card>
</template>

<script lang="ts">
/**
 * Displays the admin page onboarding stats.
 */
export default {
  name: "OnboardingStatistics",
};
</script>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import {
  SingleUserProgressSummarySchema,
  UserProgressSummarySchema,
} from "@/types";
import { displayDuration, timestampToDisplay } from "@/util";
import { getOnboardingStatistics, getUserStatistics } from "@/api";
import {
  FlexItem,
  FlexBox,
  Typography,
  PanelCard,
  TextButton,
  EmailInput,
} from "@/components/common";

const stats = ref<UserProgressSummarySchema>();
const userEmail = ref("");
const userLoading = ref(false);
const userStats = ref<SingleUserProgressSummarySchema>();

onMounted(async () => {
  stats.value = await getOnboardingStatistics();
});

/**
 * Converts the duration (in seconds) to a human readable format.
 * @param duration - The duration in seconds.
 * @returns The human readable duration.
 */
function convertDuration(duration: number) {
  return displayDuration(duration * 1000);
}

/**
 * Converts the percent (out of 1) to a human readable format.
 * @param percent - The percent (out of 1).
 * @returns The human readable percent.
 */
function convertPercent(percent: number) {
  if (percent <= 0) return "-";
  return (percent * 100).toFixed(2) + " %";
}

/**
 * Loads the statistics for the given user.
 */
async function handleLoadUser() {
  if (userEmail.value) {
    userLoading.value = true;
    userStats.value = await getUserStatistics(userEmail.value).finally(() => {
      userLoading.value = false;
    });
  } else {
    userStats.value = undefined;
  }
}
</script>
