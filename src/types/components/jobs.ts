import { JobSchema } from "@/types";

/**
 * The props for displaying a row in the job table.
 */
export interface JobRowProps {
  /**
   * Props passed in from the quasar table.
   */
  quasarProps: Record<string, unknown>;
  /**
   * The job to render.
   */
  job: JobSchema;
  /**
   * Whether the row is expanded.
   */
  expanded: boolean;
}

export interface JobTableProps {
  /**
   * Whether to show project jobs. Otherwise, user jobs are shown.
   */
  displayProjectJobs: boolean;
}
