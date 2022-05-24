import { JobStatus } from "@/types";

/**
 * Defines all colors in the theme.
 */
export enum ThemeColors {
  primary = "#00304c",
  secondary = "#FFD740",
  accent = "#006aff",
  error = "rgb(255, 82, 82)",

  menuHighlight = "#f0f0f0",

  artifactDefault = "#fafafa",
  artifactBorder = "#888888",
  artifactAdded = "#81c784",
  artifactRemoved = "#e57373",
  artifactModified = "#64b5f6",
}

/**
 * Returns the color of a job status.
 *
 * @param status - The job status to get the color of.
 * @returns The display color.
 */
export function getJobStatusColor(status: JobStatus): string {
  switch (status) {
    case JobStatus.COMPLETED:
      return ThemeColors.artifactModified;
    case JobStatus.IN_PROGRESS:
      return "#EEBC3D";
    case JobStatus.CANCELLED:
      return ThemeColors.artifactRemoved;
    default:
      return "";
  }
}
