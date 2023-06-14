import {
  ApprovalType,
  ArtifactDeltaState,
  JobStatus,
  ThemeColor,
} from "@/types";

export enum Colors {
  white = "#FFFFFF",
  black = "#1E1E1E",

  greyDarkest = "#272727",
  greyDark = "#333",
  grey = "#36405A",
  greyLight = "#94969e",
  greyLightest = "#F0F5FF",

  green = "#00AD69",
  greenLight = "#6CD8A9",
  greenDark = "#188958",

  blue = "#5975B8",
  blueLight = "#729FCF",
  blueLightest = "#8DA5D3",
  blueDark = "#204184",

  red = "#E11F26",
  redLight = "#E27171",
  redDark = "#AF001E",

  orange = "#F5B53F",
  orangeLight = "#FFD592",
  orangeDark = "#DD8300",

  // gradient1 = "#6290C3",
  // gradient2 = "#F59700",
  // gradient3 = "#5BC0BE",
  // gradient4 = "#C16200",
  // gradient5 = "#74121D",

  gradient1 = "#1e6091",
  gradient2 = "#168aad",
  gradient3 = "#52b69a",
  gradient4 = "#76c893",
  gradient5 = "#b5e48c",
}

/**
 * Defines all colors in the theme.
 */
export const ThemeColors = {
  primary: Colors.blue,
  primaryDark: Colors.blueLight,
  secondary: Colors.orange,
  accent: Colors.orangeLight,
  error: Colors.red,

  whiteBg: Colors.white,
  lightBg: Colors.greyLightest,
  lightText: Colors.grey,
  lightSelected: Colors.greyLightest,

  blackBg: Colors.black,
  darkBg: Colors.greyDark,
  darkText: Colors.white,
  darkSelected: Colors.greyLightest,

  added: Colors.green,
  addedBg: Colors.greenLight,
  addedBd: Colors.greenDark,

  modified: Colors.blue,
  modifiedBg: Colors.blueLight,
  modifiedBd: Colors.blueDark,

  removed: Colors.red,
  removedBg: Colors.redLight,
  removedBd: Colors.redDark,

  warning: Colors.orange,
  warningBg: Colors.orangeLight,
  warningBd: Colors.orangeDark,

  nodeDefaultLight: Colors.greyLight,
  nodeDefaultDark: Colors.greyLightest,
  nodeGenerated: Colors.orange,
};

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

  text: ThemeColors.lightText,
  neutral: ThemeColors.whiteBg,
  background: ThemeColors.lightBg,
  selected: ThemeColors.lightSelected,

  added: ThemeColors.added,
  addedBg: ThemeColors.addedBg,
  modified: ThemeColors.modified,
  modifiedBg: ThemeColors.modifiedBg,
  removed: ThemeColors.removed,
  removedBg: ThemeColors.removedBg,
  flagged: ThemeColors.warningBd,
  flaggedBg: ThemeColors.warningBg,

  nodeDefault: ThemeColors.nodeDefaultLight,
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

  text: ThemeColors.darkText,
  neutral: ThemeColors.blackBg,
  background: ThemeColors.darkBg,
  selected: ThemeColors.darkSelected,

  added: ThemeColors.added,
  addedBg: ThemeColors.addedBg,
  modified: ThemeColors.modified,
  modifiedBg: ThemeColors.modifiedBg,
  removed: ThemeColors.removed,
  removedBg: ThemeColors.removedBg,

  nodeDefault: ThemeColors.nodeDefaultDark,
};

const typeColorMap: Record<string, string> = {
  "": Colors.blue,
};

/**
 * Returns the color for the given type.
 * @param type - The type to get the color for.
 * @return The color.
 */
export function getTypeColor(type = ""): string {
  if (!typeColorMap[type]) {
    const remainingColors = [
      // Colors.blueLight,
      // Colors.greenLight,
      // Colors.orange,
      // Colors.orangeDark,
      // Colors.red,
      Colors.gradient1,
      Colors.gradient2,
      Colors.gradient3,
      Colors.gradient4,
      Colors.gradient5,
    ].filter((color) => !Object.values(typeColorMap).includes(color));

    typeColorMap[type] =
      remainingColors.length === 0
        ? Colors.blue
        : remainingColors[Math.floor(Math.random() * remainingColors.length)];
  }

  return typeColorMap[type];
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
