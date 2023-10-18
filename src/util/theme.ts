import {
  ApprovalType,
  ArtifactDeltaState,
  DeltaType,
  JobStatus,
  MessageType,
  ThemeColor,
} from "@/types";

export enum Colors {
  white = "#FFFFFF",
  black = "#1E1E1E",

  grey = "#41533F",
  greyLight = "#bdbdbd",
  greyLightest = "#EDEFEB",
  greyDark = "#616161",
  greyDarkest = "#333",

  green = "#55A630",
  greenDark = "#488E27",

  blue = "#3055A6",

  red = "#E24C15", // "#A63055",
  redLight = "#E24C15", // "#D51552",

  orange = "#fb8500",

  brown = "#b6ad90",
  brownDark = "#a68a64",

  gradient1 = "#81C644",
  gradient2 = "#61AD73",
  gradient3 = "#4194A2",
  gradient4 = "#207BD0",
  gradient5 = "#0062FF",
}

/**
 * The gradient colors used in the theme.
 */
export const ThemeGradient = {
  nodeGradient1: Colors.gradient1,
  nodeGradient2: Colors.gradient2,
  nodeGradient3: Colors.gradient3,
  nodeGradient4: Colors.gradient4,
  nodeGradient5: Colors.gradient5,
};

/**
 * Defines all colors in the theme.
 */
export const ThemeColors = {
  primary: Colors.greenDark,
  primaryDark: Colors.green,
  secondary: Colors.brownDark,
  accent: Colors.green,
  error: Colors.red,
  errorDark: Colors.redLight,

  whiteBg: Colors.white,
  lightBg: Colors.greyLightest,
  lightText: Colors.grey,
  lightTextCaption: Colors.greyDark,
  lightSelected: Colors.greyLightest,

  blackBg: Colors.black,
  darkBg: Colors.greyDarkest,
  darkText: Colors.white,
  darkTextCaption: Colors.greyLight,
  darkSelected: Colors.greyLight,

  added: Colors.green,
  modified: Colors.blue,
  removed: Colors.red,
  warning: Colors.orange,
  unchanged: Colors.grey,

  nodeDefault: Colors.brownDark,
  nodeGenerated: Colors.brown,

  gradient: "", // Overwritten by `colors.scss`
  ...ThemeGradient,
};

/**
 * The colors used in light mode.
 */
export const lightPalette = {
  primary: ThemeColors.primary,
  secondary: ThemeColors.secondary,
  accent: ThemeColors.accent,

  info: ThemeColors.primary,
  warning: ThemeColors.warning,
  negative: ThemeColors.error,
  positive: ThemeColors.added,

  text: ThemeColors.lightText,
  textCaption: ThemeColors.lightTextCaption,
  neutral: ThemeColors.whiteBg,
  background: ThemeColors.lightBg,
  selected: ThemeColors.lightSelected,

  added: ThemeColors.added,
  modified: ThemeColors.modified,
  removed: ThemeColors.removed,
  flagged: ThemeColors.warning,
  unchanged: ThemeColors.unchanged,

  nodeDefault: ThemeColors.nodeDefault,
  nodeGenerated: ThemeColors.nodeGenerated,

  gradient: ThemeColors.gradient,
  ...ThemeGradient,
};

/**
 * The colors used in dark mode.
 */
export const darkPalette = {
  primary: ThemeColors.primaryDark,
  secondary: ThemeColors.secondary,
  accent: ThemeColors.accent,

  info: ThemeColors.primary,
  warning: ThemeColors.warning,
  negative: ThemeColors.errorDark,
  positive: ThemeColors.added,

  text: ThemeColors.darkText,
  textCaption: ThemeColors.darkTextCaption,
  neutral: ThemeColors.blackBg,
  background: ThemeColors.darkBg,
  selected: ThemeColors.darkSelected,

  added: ThemeColors.added,
  modified: ThemeColors.modified,
  removed: ThemeColors.removed,
  flagged: ThemeColors.warning,
  unchanged: ThemeColors.unchanged,

  nodeDefault: ThemeColors.nodeDefault,
  nodeGenerated: ThemeColors.nodeGenerated,

  gradient: ThemeColors.gradient,
  ...ThemeGradient,
};

/**
 * Returns the color code based on a type color name.
 * @param colorName - The color name to get the color for.
 * @return The color.
 */
export function convertTypeToColor(
  colorName: keyof typeof ThemeGradient | string
): string {
  return (
    (ThemeGradient as Record<string, string>)[colorName] || ThemeColors.primary
  );
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
  state:
    | ApprovalType
    | ArtifactDeltaState
    | DeltaType
    | MessageType
    | JobStatus
    | string
): ThemeColor {
  switch (state) {
    case "ADDED":
    case "APPROVED":
    case "COMPLETED":
    case "success":
    case "added":
      return "added";
    case "MODIFIED":
    case "UNREVIEWED":
    case "IN_PROGRESS":
    case "info":
    case "update":
    case "modified":
      return "modified";
    case "REMOVED":
    case "DECLINED":
    case "FAILED":
    case "error":
    case "removed":
      return "removed";
    case "warning":
      return "warning";
    default:
      return "unchanged";
  }
}
