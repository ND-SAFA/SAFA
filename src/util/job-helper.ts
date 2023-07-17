import { IconVariant, JobSchema, JobStatus } from "@/types";
import { enumToDisplay, timestampToDisplay } from "@/util/string-helper";
import { getJobStatusColor } from "@/util/theme";

/**
 * Returns helpful display information about a job.
 * @param job - The job to display.
 * @return Display information
 */
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export function jobStatus(job: JobSchema) {
  return {
    isCompleted: () => job.status === JobStatus.COMPLETED,
    isInProgress: () => job.status === JobStatus.IN_PROGRESS,
    progress: () => {
      switch (job.status) {
        case JobStatus.IN_PROGRESS:
          return (
            `${job.currentProgress}% | ` +
            `${timestampToDisplay(job.lastUpdatedAt)}`
          );
        case JobStatus.COMPLETED:
          return timestampToDisplay(job.completedAt);
        case JobStatus.CANCELLED:
        case JobStatus.FAILED:
          return timestampToDisplay(job.lastUpdatedAt);
        default:
          return "";
      }
    },
    status: () => enumToDisplay(job.status || ""),
    color: () => getJobStatusColor(job.status || ""),
    icon: (): IconVariant => {
      switch (job.status) {
        case JobStatus.CANCELLED:
          return "job-cancel";
        case JobStatus.FAILED:
          return "job-fail";
        default:
          return "job-complete";
      }
    },
  };
}
