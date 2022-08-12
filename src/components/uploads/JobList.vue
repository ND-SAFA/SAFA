<template>
  <v-expansion-panels v-model="selectedJobs" multiple>
    <typography
      v-if="uploads.length === 0"
      variant="small"
      value="There aren't any uploads yet."
    />
    <job-panel v-for="(upload, i) in uploads" :key="i" :job="upload" />
  </v-expansion-panels>
</template>

<script lang="ts">
import Vue from "vue";
import { JobModel } from "@/types";
import { jobModule } from "@/store";
import { connectAndSubscribeToJob, getUserJobs } from "@/api";
import JobPanel from "./JobPanel.vue";
import { Typography } from "@/components/common";

/**
 * Displays all jobs.
 */
export default Vue.extend({
  name: "JobList",
  components: {
    Typography,
    JobPanel,
  },
  data() {
    return {
      selectedJobs: [] as number[],
    };
  },
  mounted() {
    this.reloadJobs();
  },
  computed: {
    /**
     * Returns the current jobs.
     */
    uploads(): JobModel[] {
      return jobModule.currentJobs;
    },
    /**
     * Returns the current selected job index.
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
  },
  methods: {
    /**
     * Reloads the list of jobs.
     */
    async reloadJobs() {
      const jobs = await getUserJobs();

      for (const job of jobs) {
        await connectAndSubscribeToJob(job.id);
      }

      jobModule.SET_JOBS(jobs);
      jobModule.selectJob(jobs[0]);
    },
  },
});
</script>
