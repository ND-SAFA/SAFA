import { ClickableProps, ColorProps, StyleProps, TestableProps } from "@/types";

/**
 * Enumerates the types of icons.
 */
export type IconVariant =
  | "add"
  | "edit"
  | "save"
  | "saving"
  | "delete"
  | "cancel"
  | "leave"
  | "info"
  | "update"
  | "success"
  | "error"
  | "artifact"
  | "trace"
  | "upload"
  | "download"
  | "sync"
  | "integrate"
  | "warning"
  | "back"
  | "account"
  | "search"
  | "generate"
  | "generateArtifacts"
  | "notification"
  | "share"
  | "logs"
  | "more"
  | "undo"
  | "redo"
  | "logout"
  | "file"
  | "down"
  | "up"
  | "arrow-down"
  | "arrow-up"
  | "fullscreen"
  | "fullscreen-exit"
  | "home-list"
  | "home-add"
  | "job-complete"
  | "job-cancel"
  | "job-fail"
  | "trace-approve"
  | "trace-decline"
  | "trace-decline-all"
  | "trace-unreview"
  | "view-tim"
  | "view-tree"
  | "view-table"
  | "view-delta"
  | "graph-zoom-in"
  | "graph-zoom-out"
  | "graph-center"
  | "graph-refresh"
  | "nav-toggle"
  | "nav-home"
  | "nav-create"
  | "nav-open"
  | "nav-uploads"
  | "nav-artifact"
  | "nav-trace"
  | "nav-settings"
  | "filter-open"
  | "filter-close"
  | "group-open"
  | "group-open-all"
  | "group-close"
  | "group-close-all";

/**
 * Defines props for an icon.
 */
export interface IconDisplayProps
  extends ColorProps,
    StyleProps,
    TestableProps {
  /**
   * The icon variant to render.
   */
  variant?: IconVariant;
  /**
   * The id of an icon, if not rendering a preset variant.
   */
  id?: string;
  /**
   * The size of the icon.
   */
  size?: "sm" | "md" | "lg";
  /**
   * How much to rotate the icon (in degrees).
   */
  rotate?: number;
}

/**
 * Defines props for the safa icon.
 */
export interface SafaIconProps extends ClickableProps {
  /**
   * Whether to hide the icon.
   */
  hidden?: boolean;
}
