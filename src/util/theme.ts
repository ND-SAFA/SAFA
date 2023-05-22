import {
  ApprovalType,
  ArtifactDeltaState,
  JobStatus,
  ThemeColor,
} from "@/types";

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
  black = "#1E1E1E", // Text
  darkGrey = "#272727", // Backgrounds

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
 * The colors used in light mode.
 */
export const lightPalette: Record<string, string> = {
  primary: ThemeColors.primary,
  secondary: ThemeColors.secondary,
  accent: ThemeColors.accent,

  info: ThemeColors.primary,
  warning: ThemeColors.warning,
  negative: ThemeColors.error,
  positive: ThemeColors.added,

  text: ThemeColors.textLight,
  neutral: ThemeColors.white,
  background: ThemeColors.backgroundLight,
  selected: ThemeColors.selectedLight,

  addedLight: ThemeColors.addedLight,
  modifiedLight: ThemeColors.modifiedLight,
  removedLight: ThemeColors.removedLight,
};

/**
 * The colors used in dark mode.
 */
export const darkPalette: Record<string, string> = {
  primary: ThemeColors.primaryDark,
  secondary: ThemeColors.secondary,
  accent: ThemeColors.accent,

  info: ThemeColors.primary,
  warning: ThemeColors.warning,
  negative: ThemeColors.error,
  positive: ThemeColors.added,

  text: ThemeColors.textDark,
  neutral: ThemeColors.black,
  background: ThemeColors.backgroundDark,
  selected: ThemeColors.selectedDark,

  addedLight: ThemeColors.addedLight,
  modifiedLight: ThemeColors.modifiedLight,
  removedLight: ThemeColors.removedLight,
};

const typeColorMap: Record<string, string> = {
  "": ThemeColors.modifiedLight,
};

/**
 * Returns the color for the given type.
 * @param type - The type to get the color for.
 * @return The color.
 */
export function getTypeColor(type = ""): string {
  if (!typeColorMap[type]) {
    const remainingColors = [
      ThemeColors.addedLight,
      ThemeColors.removedLight,
      ThemeColors.secondary,
      ThemeColors.accent,
      ThemeColors.modified,
    ].filter((color) => !Object.values(typeColorMap).includes(color));

    typeColorMap[type] =
      remainingColors.length === 0
        ? ThemeColors.modifiedLight
        : remainingColors[Math.floor(Math.random() * remainingColors.length)];
  }

  return typeColorMap[type];
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
export function getBorderColor(
  state: ArtifactDeltaState | string = ""
): string {
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
export function getScoreColor(score: number | string): ThemeColor {
  const [ints, decimals = "0"] = String(score).split(".");
  const tenths = decimals[0];

  if (ints === "1" || ["8", "9"].includes(tenths)) {
    return "positive";
  } else if (["6", "7"].includes(tenths)) {
    return "secondary";
  } else {
    return "negative";
  }
}

/**
 * Returns the background color for an approval state.
 * @param state - The state to get the color for.
 * @return The color.
 */
export function getEnumColor(
  state: ApprovalType | ArtifactDeltaState | string
): ThemeColor {
  switch (state) {
    case ArtifactDeltaState.ADDED:
    case ApprovalType.APPROVED:
      return "positive";
    case ArtifactDeltaState.MODIFIED:
    case ApprovalType.UNREVIEWED:
      return "primary";
    case ArtifactDeltaState.REMOVED:
    case ApprovalType.DECLINED:
      return "negative";
    default:
      return "";
  }
}

/**
 * Returns the color of a job status.
 *
 * @param status - The job status to get the color of.
 * @returns The display color.
 */
export function getJobStatusColor(status: JobStatus): ThemeColor {
  switch (status) {
    case JobStatus.COMPLETED:
      return "primary";
    case JobStatus.IN_PROGRESS:
      return "secondary";
    case JobStatus.FAILED:
      return "negative";
    default:
      return "";
  }
}
