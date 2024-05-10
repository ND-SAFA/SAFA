import { JobLogSchema, JobSchema } from "@/types";
import { buildRequest } from "@/api";

/**
 * Returns list of jobs created by user.
 *
 * @return Uses list.
 */
export async function getUserJobs(): Promise<JobSchema[]> {
  return buildRequest<JobSchema[]>("jobsUser").get();
}

/**
 * Returns list of jobs associated with project.
 * @param projectId
 */
export async function getProjectJobs(projectId: string): Promise<JobSchema[]> {
  return buildRequest<JobSchema[]>("jobsProject", { projectId }).get();
}

/**
 * Deletes the job with given id.
 *
 * @param jobId - The job to delete.
 */
export async function deleteJobById(jobId: string): Promise<void> {
  return buildRequest<void, "jobId">("job", { jobId }).delete();
}

/**
 * Returns the logs for a job.
 *
 * @param jobId - The job to get logs for.
 */
export async function getJobLog(jobId: string): Promise<JobLogSchema[][]> {
  return buildRequest<JobLogSchema[][], "jobId">("jobLogs", { jobId }).get();
}
