import { ThemeColors } from "@/util";

export const ARTIFACT_PADDING = 50;
export const ARTIFACT_WIDTH = 105;
export const ARTIFACT_HEIGHT = (ARTIFACT_WIDTH * 9) / 16;

export const ARTIFACT_SHAPE = "rectangle";
export const ARTIFACT_BORDER_STYLE = "solid";
export const ARTIFACT_BORDER_WIDTH = 1.5;

export const ARTIFACT_BACKGROUND_COLOR = ThemeColors.artifactDefault;
export const ARTIFACT_SELECTED_COLOR = ThemeColors.primary;
export const ARTIFACT_SELECTED_BORDER_WIDTH = 6;

/**
 * Delta State.
 */
export const ARTIFACT_ADDED_COLOR = ThemeColors.artifactAdded;
export const ARTIFACT_REMOVED_COLOR = ThemeColors.artifactRemoved;
export const ARTIFACT_MODIFIED_COLOR = ThemeColors.artifactModified;
