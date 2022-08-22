import { defineStore } from "pinia";

import { pinia } from "@/plugins";
import { JobModel } from "@/types";

/**
 * This module tracks the jobs submitted by the user.
 */
export const useJobs = defineStore("jobs", {
  state: () => ({
    /**
     * The list of user jobs.
     */
    jobs: [] as JobModel[],
    /**
     * The index of the selected job.
     */
    selectedJob: 0,
  }),
  getters: {},
  actions: {
    /**
     * Adds job to list of jobs if new job, otherwise updates previous one.
     * New or updated job will be first element of the list of jobs.
     */
    updateJob(job: JobModel): void {
      this.jobs = [job, ...this.jobs.filter(({ id }) => id !== job.id)];
    },
    /**
     * Selects the given job.
     */
    selectJob(job: JobModel): void {
      this.jobs.forEach(({ id }, idx) => {
        if (id === job.id) {
          this.selectedJob = idx;
        }
      });
    },
    /**
     * @returns The job with given id.
     */
    getJob(jobId: string): JobModel | undefined {
      return this.jobs.find(({ id }) => id === jobId);
    },
    /**
     * Removes job matching id of given job.
     */
    deleteJob(job: JobModel): void {
      this.jobs = this.jobs.filter(({ id }) => id !== job.id);
      this.selectedJob = 0;
    },
  },
});

export default useJobs(pinia);
