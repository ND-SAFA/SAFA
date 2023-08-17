import { ArtifactSchema, ModelType, TraceLinkSchema } from "@/types/domain";

/**
 * Defines a collection of parsed artifacts.
 */
export type ArtifactMap = Record<string, ArtifactSchema>;

export enum CreatorTabTypes {
  standard = "standard",
  bulk = "bulk",
  import = "import",
}

export enum LoaderTabTypes {
  load = "load",
  uploads = "uploads",
}

/**
 * Represents a panel for uploading files in the project creator.
 */
export interface CreatorFilePanel {
  variant: "artifact" | "trace";
  name: string;
  type: string;
  open: boolean;
  valid: boolean;
  loading: boolean;
  ignoreErrors: boolean;
  itemNames: string[];
  file?: File;
  errorMessage?: string;

  // Artifacts
  artifacts?: ArtifactSchema[];

  // Traces
  toType?: string;
  isGenerated: boolean;
  generateMethod?: ModelType;
  traces?: TraceLinkSchema[];
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
   * The type of data being created.
   */
  variant: "artifact" | "trace";
  /**
   * The label for the type of panel.
   */
  label: string;
  /**
   * The panel's label to display over the panel name.
   */
  newLabel: string;
}
