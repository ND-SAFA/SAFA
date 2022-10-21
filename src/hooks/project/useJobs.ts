import { defineStore } from "pinia";

import { JobModel } from "@/types";
import { pinia } from "@/plugins";

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
    selectedJob: -1,
  }),
  getters: {},
  actions: {
    /**
     * Adds job to list of jobs if new job, otherwise updates previous one.
     * New or updated job will be first element of the list of jobs.
     *
     * @param job - The job to update.
     */
    updateJob(job: JobModel): void {
      this.jobs = [job, ...this.jobs.filter(({ id }) => id !== job.id)];
    },
    /**
     * Selects the given job.
     *
     * @param job - The job to select.
     */
    selectJob(job: JobModel): void {
      this.jobs.forEach(({ id }, idx) => {
        if (id === job.id) {
          this.selectedJob = idx;
        }
      });
    },
    /**
     * Finds a job.
     *
     * @param jobId - The job id to get.
     * @returns The job with given id.
     */
    getJob(jobId: string): JobModel | undefined {
      return this.jobs.find(({ id }) => id === jobId);
    },
    /**
     * Removes job matching id of given job.
     *
     * @param job - The job, or id, to delete.
     */
    deleteJob(job: JobModel | string): void {
      const deleteId = typeof job === "string" ? job : job.id;

      this.$patch({
        jobs: this.jobs.filter(({ id }) => id !== deleteId),
        selectedJob: 0,
      });
    },
  },
});

export default useJobs(pinia);
