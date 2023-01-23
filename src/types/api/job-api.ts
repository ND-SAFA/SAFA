/**
 * Identifies a job being performed.
 */
export interface JobSchema {
  /**
   * The UUID of the job.
   */
  id: string;
  /**
   * A readable name for the job.
   */
  name: string;
  /**
   * The current step this job is on.
   */
  currentStep: number;
  /**
   * The steps names involved with this job.
   */
  steps: string[];
  /**
   * The current status of the job.
   */
  status: JobStatus;
  /**
   * Timestamp of when the job was started.
   */
  startedAt: string;
  /**
   * Timestamp of when the job was last updated.
   */
  lastUpdatedAt: string;
  /**
   * Timestamp of when the job was completed.
   */
  completedAt: string;
  /**
   * Integer percentage of current progress of the job.
   */
  currentProgress: number;
  /**
   * The UUID of the entity completed or updated by this job.
   */
  completedEntityId?: string;
}

/**
 * The state a job can be in.
 */
export enum JobStatus {
  /**
   * The job is being performed as expected.
   */
  IN_PROGRESS = "IN_PROGRESS",
  /**
   * The job has finished.
   */
  COMPLETED = "COMPLETED",
  /**
   * The job has been cancelled.
   */
  CANCELLED = "CANCELLED",
  /**
   * The job has failed.
   */
  FAILED = "FAILED",
}

/**
 * Describes an entry in the job log.
 */
export interface JobLogSchema {
  id: string;
  job: string;
  stepNum: number;
  timestamp: string;
  entry: string;
}
