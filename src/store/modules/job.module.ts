import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type { Job } from "@/types";

@Module({ namespaced: true, name: "job" })
/**
 * This module tracks the jobs submitted by the user.
 */
export default class JobModule extends VuexModule {
  /**
   * The list of user jobs.
   */
  private jobs: Job[] = [];

  @Action
  /**
   * Adds job to list of jobs if new job, otherwise updates previous one.
   */
  addOrUpdateJob(job: Job): void {
    const newJobs = this.jobs.filter((j) => j.id !== job.id).concat([job]);
    this.SET_JOBS(newJobs);
  }

  @Mutation
  /**
   * Sets the current user's jobs.
   */
  SET_JOBS(jobs: Job[]): void {
    this.jobs = jobs;
  }

  /**
   * @returns Returns job with given id if it exists.
   * IndexOutOfBounds otherwise.
   */
  get getJob(): (id: string) => Job {
    return (jobId: string) => {
      return this.jobs.filter((j) => j.id === jobId)[0];
    };
  }
}
