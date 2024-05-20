import { IconVariant } from "@/types";

export const DefaultTypeIcon = "mdi-alpha-a-box-outline";

export const TypeIcons = [
  "mdi-clipboard-text",
  "mdi-math-compass",
  "mdi-hazard-lights",
  "mdi-pine-tree-fire",
  "mdi-alpha-a-box",
  "mdi-text-box-multiple",
  "mdi-code-braces-box",
  "mdi-drawing-box",
  "mdi-folder",
  "mdi-file-table",
  "mdi-database",
  "mdi-application-cog",
  "mdi-account-box-multiple",
  "mdi-book-lock",
  "mdi-message",
  "mdi-book-open",
];

/**
 * Returns the icon id for the given variant.
 * @param variant - The icon variant.
 * @return The corresponding icon id.
 */
export function getIcon(variant?: IconVariant): string {
  switch (variant) {
    case "add":
      return "mdi-plus";
    case "edit":
      return "mdi-pencil";
    case "save":
      return "mdi-content-save";
    case "saving":
      return "mdi-cloud-upload-outline";
    case "delete":
      return "mdi-delete";
    case "cancel":
      return "mdi-close";
    case "leave":
      return "mdi-tab-remove";
    case "info":
      return "mdi-alert-circle-outline";
    case "error":
      return "mdi-alert-circle-outline";
    case "invite":
      return "mdi-account-plus";
    case "success":
      return "mdi-check-circle-outline";
    case "artifact":
      return "mdi-alpha-a-box-outline";
    case "trace":
      return "mdi-ray-start-arrow";
    case "upload":
      return "mdi-folder-arrow-up-outline";
    case "download":
      return "mdi-download";
    case "sync":
      return "mdi-cloud-sync-outline";
    case "integrate":
      return "mdi-transit-connection-variant";
    case "warning":
      return "mdi-hazard-lights";
    case "back":
      return "mdi-arrow-left";
    case "forward":
      return "mdi-arrow-right";
    case "account":
      return "mdi-account-circle";
    case "organization":
      return "mdi-domain";
    case "permission":
      return "mdi-account-cog";
    case "search":
      return "mdi-magnify";
    case "code":
      return "mdi-code-json";
    case "create-artifact":
      return "mdi-folder-plus-outline";
    case "create-trace":
      return "mdi-ray-start-end";
    case "graph-add":
    case "generate":
      return "mdi-creation";
    case "generate-artifacts":
      return "mdi-monitor-shimmer";
    case "generate-summaries":
      return "mdi-shimmer";
    case "generate-traces":
      return "mdi-chart-timeline-variant-shimmer";
    case "notification":
      return "mdi-bell-outline";
    case "feedback":
      return "mdi-comment-quote";
    case "share":
      return "mdi-share-variant";
    case "logs":
      return "mdi-post-outline";
    case "more":
      return "mdi-dots-horizontal";
    case "undo":
      return "mdi-undo";
    case "redo":
      return "mdi-redo";
    case "logout":
      return "mdi-logout-variant";
    case "file":
      return "mdi-paperclip";
    case "calendar":
      return "mdi-calendar";
    case "down":
      return "mdi-chevron-down";
    case "up":
      return "mdi-chevron-up";
    case "arrow-down":
      return "mdi-arrow-down";
    case "arrow-up":
      return "mdi-arrow-up";
    case "fullscreen":
      return "mdi-fullscreen";
    case "fullscreen-exit":
      return "mdi-fullscreen-exit";
    case "home-list":
      return "mdi-view-list";
    case "home-add":
      return "mdi-folder-plus-outline";
    case "job-complete":
      return "mdi-check-circle-outline";
    case "job-cancel":
      return "mdi-minus-circle-outline";
    case "job-fail":
      return "mdi-close-circle-outline";
    case "trace-approve":
      return "mdi-check-circle-outline";
    case "trace-decline":
      return "mdi-close-circle-outline";
    case "trace-decline-all":
      return "mdi-close-circle-multiple-outline";
    case "trace-unreview":
      return "mdi-checkbox-blank-circle-outline";
    case "view-tim":
      return "mdi-ballot";
    case "view-tree":
      return "mdi-family-tree";
    case "view-table":
      return "mdi-table-multiple";
    case "view-delta":
      return "mdi-compare";
    case "graph-zoom-in":
      return "mdi-magnify-plus";
    case "graph-zoom-out":
      return "mdi-magnify-minus";
    case "graph-center":
      return "mdi-image-filter-center-focus-strong";
    case "graph-refresh":
      return "mdi-refresh";
    case "nav-toggle":
      return "mdi-menu-open";
    case "nav-home":
      return "mdi-home";
    case "nav-create":
      return "mdi-folder-plus";
    case "nav-open":
      return "mdi-list-box";
    case "nav-uploads":
      return "mdi-folder-upload";
    case "nav-artifact":
      return "mdi-family-tree";
    case "nav-trace":
      return "mdi-link-box";
    case "nav-settings":
      return "mdi-cog-box";
    case "filter-open":
      return "mdi-filter-menu";
    case "filter-close":
      return "mdi-filter-minus";
    case "group-open":
      return "mdi-chevron-up";
    case "group-open-all":
      return "mdi-arrow-expand-all";
    case "group-close":
      return "mdi-chevron-down";
    case "group-close-all":
      return "mdi-arrow-collapse-all";
    case "member-add":
      return "mdi-account-plus";
    case "member-delete":
      return "mdi-account-remove";
    case "project-add":
      return "mdi-briefcase-plus";
    case "project-delete":
      return "mdi-briefcase-remove";
    case "project-edit":
      return "mdi-briefcase-edit";
    case "version-add":
      return "mdi-folder-plus";
    case "version-delete":
      return "mdi-folder-remove";
    case "pw-show":
      return "mdi-eye";
    case "pw-hide":
      return "mdi-eye-off";
    case "connected":
      return "mdi-network";
    case "disconnected":
      return "mdi-network-off";
    case "onboarding":
      return "mdi-map-legend";
    case "changelog":
      return "mdi-file-document-multiple";
    case "security":
      return "mdi-shield-lock";
    case "payment":
      return "mdi-credit-card-outline";
    case "admin":
      return "mdi-account-supervisor-circle";
    case "comment":
      return "mdi-comment-text-outline";
    case "comment-resolve":
      return "mdi-comment-check-outline";
    case "flag":
      return "mdi-flag";
    case "health":
      return "mdi-heart-pulse";
    case "health-unknown":
      return "mdi-help";
    case "health-concept":
      return "mdi-file-document";
    case "health-concept-multiple":
      return "mdi-file-document-multiple";
    case "health-conflict":
      return "mdi-compare-remove";
    case "link":
      return "mdi-link";
    default:
      return "";
  }
}
