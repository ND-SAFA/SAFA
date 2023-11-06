import { TimJsonSchema } from "@/types";
import { ArtifactSchema, TraceLinkSchema } from "@/types/domain";

/**
 * Defines a collection of parsed artifacts.
 */
export type ArtifactMap = Record<string, ArtifactSchema>;

/**
 * The types of create project tabs.
 */
export type UploadPanelType = "artifact" | "trace" | "bulk" | "github" | "jira";

/**
 * The types of create project tabs.
 */
export type CreatorTab = "standard" | "bulk" | "import";

/**
 * The types of create project tabs.
 */
export type CreatorSectionTab = "name" | "data";

/**
 * The types of load project tabs.
 */
export type LoaderTab = "load" | "project" | "user";

/**
 * Represents a panel for uploading files in the project creator.
 */
export interface CreatorFilePanel {
  variant: UploadPanelType;
  name: string;
  type: string;
  open: boolean;
  valid: boolean;
  loading: boolean;
  ignoreErrors: boolean;
  itemNames: string[];
  file?: File;
  errorMessage?: string;
  parseErrorMessage?: string;

  // Artifacts
  artifacts?: ArtifactSchema[];
  summarize: boolean;

  // Traces
  toType?: string;
  isGenerated: boolean;
  traces?: TraceLinkSchema[];

  // Bulk
  bulkFiles: File[];
  tim?: TimJsonSchema;
  emptyFiles: boolean;
}

/**
 * The props for displaying a file upload panel.
 */
export interface FilePanelProps {
  /**
   * The panel being edited.
   */
  panel: CreatorFilePanel;
  /**
   * The panel index.
   */
  index: number;
  /**
   * If true, the upload type editor will be hidden.
   */
  hideUploadType?: boolean;
}
