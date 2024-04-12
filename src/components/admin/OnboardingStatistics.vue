<template>
  <panel-card v-if="!!stats" title="Onboarding Statistics">
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
        <typography :value="stats.accounts.haveProperProgressTracking" el="p" />
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
        <typography :value="stats.github.withProperTracking.accounts" el="p" />
        <typography
          :value="stats.github.withProperTracking.percent + ' %'"
          el="p"
        />
        <typography
          :value="convertDuration(stats.github.withProperTracking.averageTime)"
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
        <typography :value="stats.imports.total.percent + ' %'" el="p" />
        <typography
          :value="convertDuration(stats.imports.total.averageTime)"
          el="p"
        />
        <typography :value="stats.imports.fromGithubProper.accounts" el="p" />
        <typography
          :value="stats.imports.fromGithubProper.percent + ' %'"
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
        <typography :value="stats.generations.total.percent + ' %'" el="p" />
        <typography
          :value="convertDuration(stats.generations.total.averageTime)"
          el="p"
        />
        <typography
          :value="stats.generations.fromImportProper.accounts"
          el="p"
        />
        <typography
          :value="stats.generations.fromImportProper.percent + ' %'"
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
import { UserProgressSummarySchema } from "@/types";
import { displayDuration } from "@/util";
import { getOnboardingStatistics } from "@/api";
import { FlexItem, FlexBox, Typography, PanelCard } from "@/components/common";

const stats = ref<UserProgressSummarySchema>();

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
</script>
