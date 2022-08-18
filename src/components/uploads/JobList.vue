<template>
  <v-expansion-panels v-model="selectedJobs" multiple>
    <div class="full-width" v-if="uploads.length > 0">
      <job-panel v-for="(upload, i) in uploads" :key="i" :job="upload" />
    </div>
    <flex-box v-else-if="isLoading" justify="center" x="2" y="2">
      <v-progress-circular size="40" indeterminate />
    </flex-box>
    <typography v-else variant="small" value="There aren't any uploads yet." />
  </v-expansion-panels>
</template>

<script lang="ts">
import Vue from "vue";
import { JobModel } from "@/types";
import { appModule, jobModule } from "@/store";
import { handleReloadJobs } from "@/api";
import { Typography } from "@/components/common";
import JobPanel from "./JobPanel.vue";
import FlexBox from "@/components/common/display/FlexBox.vue";

/**
 * Displays all jobs.
 */
export default Vue.extend({
  name: "JobList",
  components: {
    FlexBox,
    Typography,
    JobPanel,
  },
  data() {
    return {
      selectedJobs: [0] as number[],
    };
  },
  mounted() {
    this.reloadJobs();
  },
  computed: {
    /**
     * @return Whether the app is loading.
     */
    isLoading(): boolean {
      return appModule.getIsLoading;
    },
    /**
     * return The current jobs.
     */
    uploads(): JobModel[] {
      return jobModule.currentJobs;
    },
    /**
     * return The current selected job index.
     */
    selectedJobIndex(): number {
      return jobModule.selectedJobIndex;
    },
  },
  watch: {
    /**
     * Synchronizes what jobs are selected with the selected index.
     */
    selectedJobIndex(newIndex: number): void {
      if (newIndex == -1) {
        this.selectedJobs = [];
      } else {
        this.selectedJobs = [newIndex];
      }
    },
    /**
     * Selects the first job when the uploads change.
     */
    uploads(): void {
      this.selectedJobs = [0];
    },
  },
  methods: {
    /**
     * Reloads the list of jobs.
     */
    async reloadJobs() {
      await handleReloadJobs();
    },
  },
});
</script>
