import { Action, Module, Mutation, VuexModule } from "vuex-module-decorators";

import type { JobModel } from "@/types";

@Module({ namespaced: true, name: "job" })
/**
 * This module tracks the jobs submitted by the user.
 */
export default class JobModule extends VuexModule {
  /**
   * The list of user jobs.
   */
  private jobs: JobModel[] = [];
  /**
   * The index of the selected job.
   */
  private selectedJob = -1;

  @Action
  /**
   * Adds job to list of jobs if new job, otherwise updates previous one.
   * New or updated job will be first element of the list of jobs.
   */
  addOrUpdateJob(job: JobModel): void {
    const newJobs = [job].concat(this.jobs.filter((j) => j.id !== job.id));
    this.SET_JOBS(newJobs);
  }

  @Action
  /**
   * Selects the given job if exists in jobs.
   */
  selectJob(job: JobModel): void {
    this.jobs.forEach((j, i) => {
      if (j.id === job.id) {
        this.SET_SELECT_JOB_INDEX(i);
      }
    });
  }

  @Action
  /**
   * Removes job matching id of given job.
   */
  deleteJob(job: JobModel): void {
    this.SET_SELECT_JOB_INDEX(-1);
    setTimeout(() => {
      this.SET_JOBS(this.jobs.filter((j) => j.id != job.id));
    }, 500);
  }

  @Mutation
  /**
   * Sets the current user's jobs.
   */
  SET_JOBS(jobs: JobModel[]): void {
    this.jobs = jobs;
  }

  @Mutation
  /**
   * Sets the currently selected job index, otherwise -1.
   */
  SET_SELECT_JOB_INDEX(index: number): void {
    this.selectedJob = index;
  }

  /**
   * @returns The job with given id.
   */
  get getJob(): (id: string) => JobModel {
    return (jobId: string) => {
      return this.jobs.filter((j) => j.id === jobId)[0];
    };
  }

  /**
   * @returns All current jobs.
   */
  get currentJobs(): JobModel[] {
    return this.jobs;
  }

  /**
   * @returns The index of the selected job.
   */
  get selectedJobIndex(): number {
    return this.selectedJob;
  }
}
