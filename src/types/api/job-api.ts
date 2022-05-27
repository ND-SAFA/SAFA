/**
 * Identifies a job being performed.
 */
export interface Job {
  /**
   * The UUID of the job.
   */
  id: string;
  /**
   * A readable name for the job.
   */
  name: string;
  /**
   * The type of job being performed.
   */
  jobType: JobType;
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
 * Enumerates the jobs that can be performed
 */
export enum JobType {
  /**
   * Parsing and uploading entities via flat files.
   */
  FLAT_FILE_PROJECT_CREATION = "FLAT_FILE_PROJECT_CREATION",
  /**
   * Scraping and uploading entities from a JIRA project.
   */
  JIRA_PROJECT_CREATION = "JIRA_PROJECT_CREATION",
  /**
   * Creating a project via JSON.
   */
  PROJECT_CREATION = "PROJECT_CREATION",
  /**
   * Updating changed entities from jira projects
   */
  PROJECT_SYNC = "PROJECT_SYNC",
  /**
   * Generating set of trace links.
   */
  GENERATE_LINKS = "GENERATE_LINKS",
  /**
   * Training Bert model for trace link prediction on some domain.
   */
  TRAIN_MODEL = "TRAIN_MODEL",
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
