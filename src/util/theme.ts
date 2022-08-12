import { ApprovalType, ArtifactDeltaState, JobStatus } from "@/types";

/**
 * Defines all colors in the theme.
 */
export enum ThemeColors {
  primary = "#5975B8",
  secondary = "#F5B53F",
  accent = "#F5871F",
  error = "#E11F26",

  white = "#FFFFFF", // Text
  black = "#000000", // Text
  lightGrey = "#DDDDDD", // Backgrounds
  darkGrey = "#969696", // Borders

  added = "#00AD69",
  modified = "#5975B8",
  removed = "#E11F26",
  warning = "#F5B53F",
}

/**
 * Returns the background color for the given state.
 * @param state - The state to get the color for.
 * @return The color.
 */
export function getBackgroundColor(
  state?: ArtifactDeltaState | ApprovalType
): string {
  switch (state) {
    case ApprovalType.APPROVED:
    case ArtifactDeltaState.ADDED:
      return ThemeColors.added;
    case ApprovalType.UNREVIEWED:
    case ArtifactDeltaState.MODIFIED:
      return ThemeColors.modified;
    case ApprovalType.DECLINED:
    case ArtifactDeltaState.REMOVED:
      return ThemeColors.removed;
    default:
      return ThemeColors.lightGrey;
  }
}

/**
 * Returns the text color for the given delta state.
 * @param deltaState - The delta state to get the color for.
 * @return The color.
 */
export function getTextColor(deltaState?: ArtifactDeltaState): string {
  if (!deltaState || deltaState === ArtifactDeltaState.NO_CHANGE) {
    return ThemeColors.black;
  } else {
    return ThemeColors.white;
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
      return ThemeColors.modified;
    case JobStatus.IN_PROGRESS:
      return "#EEBC3D";
    case JobStatus.CANCELLED:
      return ThemeColors.removed;
    default:
      return "";
  }
}
