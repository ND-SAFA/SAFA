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
  private _jobs: Job[] = [];

  private _selectedJobIndex = -1;

  @Action
  /**
   * Adds job to list of jobs if new job, otherwise updates previous one.
   */
  addOrUpdateJob(job: Job): void {
    const newJobs = this._jobs.filter((j) => j.id !== job.id).concat([job]);
    this.SET_JOBS(newJobs);
  }

  @Action
  /**
   * Selects the given job if exists in jobs.
   */
  selectJob(job: Job): void {
    this._jobs.forEach((j, i) => {
      if (j.id === job.id) {
        this.SET_SELECT_JOB_INDEX(i);
      }
    });
  }

  @Action
  /**
   * Removes job matching id of given job
   */
  deleteJob(job: Job): void {
    this.SET_SELECT_JOB_INDEX(-1);
    setTimeout(() => {
      this.SET_JOBS(this._jobs.filter((j) => j.id != job.id));
    }, 500);
  }

  @Mutation
  /**
   * Sets the current user's jobs.
   */
  SET_JOBS(jobs: Job[]): void {
    this._jobs = jobs;
  }

  @Mutation
  /**
   * Sets the currently selected job index, otherwise -1.
   */
  SET_SELECT_JOB_INDEX(index: number): void {
    this._selectedJobIndex = index;
  }

  /**
   * @returns Returns job with given id if it exists.
   * IndexOutOfBounds otherwise.
   */
  get getJob(): (id: string) => Job {
    return (jobId: string) => {
      return this._jobs.filter((j) => j.id === jobId)[0];
    };
  }

  get jobs(): Job[] {
    return this._jobs;
  }

  get selectedJob(): number {
    return this._selectedJobIndex;
  }
}
