import { IconVariant, JobSchema } from "@/types";
import { enumToDisplay, timestampToDisplay } from "@/util/string-helper";
import { getEnumColor } from "@/util/theme";

/**
 * Returns helpful display information about a job.
 * @param job - The job to display.
 * @return Display information
 */
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export function jobStatus(job: JobSchema) {
  return {
    isCompleted: () => job.status === "COMPLETED",
    isInProgress: () => job.status === "IN_PROGRESS",
    progress: () => {
      switch (job.status) {
        case "IN_PROGRESS":
          return (
            `${job.currentProgress}% | ` +
            `${timestampToDisplay(job.lastUpdatedAt)}`
          );
        case "COMPLETED":
          return timestampToDisplay(job.completedAt);
        case "CANCELLED":
        case "FAILED":
          return timestampToDisplay(job.lastUpdatedAt);
        default:
          return "";
      }
    },
    status: () => enumToDisplay(job.status || ""),
    color: () => getEnumColor(job.status || ""),
    icon: (): IconVariant => {
      switch (job.status) {
        case "CANCELLED":
          return "job-cancel";
        case "FAILED":
          return "job-fail";
        default:
          return "job-complete";
      }
    },
  };
}
