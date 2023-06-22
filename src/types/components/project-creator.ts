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
