import { defineStore } from "pinia";

import { JobSchema } from "@/types";
import { pinia } from "@/plugins";

/**
 * This module tracks the jobs submitted by the user.
 */
export const useJobs = defineStore("jobs", {
  state: () => ({
    /**
     * The list of user jobs.
     */
    jobs: [] as JobSchema[],
    /**
     * The index of the selected job.
     */
    selectedJob: undefined as JobSchema | undefined,
  }),
  getters: {},
  actions: {
    /**
     * Toggles whether a job is selected.
     * @param job - The job to select.
     */
    selectJob(job: JobSchema): void {
      this.selectedJob = this.selectedJob === job ? undefined : job;
    },
    /**
     * Adds job to list of jobs if new job, otherwise updates previous one.
     * New or updated job will be first element of the list of jobs.
     *
     * @param job - The job to update.
     */
    updateJob(job: JobSchema): void {
      this.jobs = [job, ...this.jobs.filter(({ id }) => id !== job.id)];
    },
    /**
     * Removes job matching id of given job.
     *
     * @param job - The job, or id, to delete.
     */
    deleteJob(job: JobSchema | string): void {
      const deleteId = typeof job === "string" ? job : job.id;
      const jobs = this.jobs.filter(({ id }) => id !== deleteId);

      this.$patch({
        jobs,
        selectedJob: jobs[0],
      });
    },
  },
});

export default useJobs(pinia);
