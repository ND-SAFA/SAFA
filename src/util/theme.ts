import { ApprovalType, ArtifactDeltaState, JobStatus } from "@/types";

/**
 * Defines all colors in the theme.
 */
export enum ThemeColors {
  primary = "#5975B8",
  primaryDark = "#729FCF",
  secondary = "#F5B53F",
  accent = "#FFD592",
  error = "#E11F26",

  white = "#FFFFFF", // Text
  black = "#000000", // Text
  lightGrey = "#EEEEEE", // Backgrounds
  grey = "#DDDDDD",
  darkGrey = "#969696", // Borders

  textLight = "#36405A",
  textDark = "#FFF",
  backgroundLight = "#F0F5FF",
  backgroundDark = "#333",
  selectedLight = "#EEE",
  selectedDark = "#EEE",

  added = "#00AD69", // Text
  addedLight = "#6CD8A9", // Backgrounds
  addedDark = "#188958", // Borders

  modified = "#5975B8", // Text
  modifiedLight = "#8DA5D3", // Backgrounds
  modifiedDark = "#204184", // Borders

  removed = "#E11F26", // Text
  removedLight = "#E27171", // Backgrounds
  removedDark = "#AF001E", // Borders

  warning = "#F5B53F", // Text
  warningLight = "#FFD592", // Backgrounds
  warningDark = "#DD8300", // Borders
}

/**
 * Returns the background color for the given state.
 * @param state - The state to get the color for.
 * @param dark - Whether the app is in dark mode.
 * @return The color.
 */
export function getBackgroundColor(
  state: ArtifactDeltaState | ApprovalType | string,
  dark: boolean
): string {
  switch (state) {
    case ApprovalType.APPROVED:
      return ThemeColors.added;
    case ArtifactDeltaState.ADDED:
      return ThemeColors.addedLight;
    case ApprovalType.UNREVIEWED:
      return ThemeColors.modified;
    case ArtifactDeltaState.MODIFIED:
      return ThemeColors.modifiedLight;
    case ApprovalType.DECLINED:
      return ThemeColors.removed;
    case ArtifactDeltaState.REMOVED:
      return ThemeColors.removedLight;
    default:
      return dark ? ThemeColors.backgroundDark : ThemeColors.backgroundLight;
  }
}

/**
 * Returns the border color for the given state.
 * @param state - The state to get the color for.
 * @return The color.
 */
export function getBorderColor(state?: ArtifactDeltaState | string): string {
  switch (state) {
    case ArtifactDeltaState.ADDED:
      return ThemeColors.addedDark;
    case ArtifactDeltaState.MODIFIED:
      return ThemeColors.modifiedDark;
    case ArtifactDeltaState.REMOVED:
      return ThemeColors.removedDark;
    default:
      return ThemeColors.modifiedLight;
  }
}

/**
 * Returns the background color for the given confidence score.
 * @param score - The score to get the color for.
 * @return The color.
 */
export function getScoreColor(score: number | string): string {
  const [ints, decimals] = String(score).split(".");
  const tenths = decimals[0];

  if (ints === "1" || ["8", "9"].includes(tenths)) {
    return ThemeColors.added;
  } else if (["6", "7"].includes(tenths)) {
    return ThemeColors.secondary;
  } else if (["4", "5"].includes(tenths)) {
    return ThemeColors.warning;
  } else {
    return ThemeColors.error;
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
