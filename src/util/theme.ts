import { ArtifactDeltaState, JobStatus } from "@/types";

/**
 * Defines all colors in the theme.
 */
export enum ThemeColors {
  primary = "#00304c",
  secondary = "#FFD740",
  accent = "#006aff",
  error = "rgb(255, 82, 82)",

  menuHighlight = "#f0f0f0",

  artifactDefault = "#F5F5F5",
  artifactBorder = "#888888",
  artifactText = "#36405a",
  artifactAdded = "#81c784",
  artifactRemoved = "#e57373",
  artifactModified = "#64b5f6",
  artifactWarning = "#EEBC3D",
}

/**
 * Returns the background color for the given delta state.
 * @param deltaState - The delta state to get the color for.
 * @return The color.
 */
export function getBackgroundColor(deltaState?: ArtifactDeltaState): string {
  switch (deltaState) {
    case ArtifactDeltaState.ADDED:
      return ThemeColors.artifactAdded;
    case ArtifactDeltaState.REMOVED:
      return ThemeColors.artifactRemoved;
    case ArtifactDeltaState.MODIFIED:
      return ThemeColors.artifactModified;
    default:
      return ThemeColors.artifactDefault;
  }
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
