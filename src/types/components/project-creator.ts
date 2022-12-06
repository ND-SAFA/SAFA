import { ArtifactSchema, LinkSchema } from "@/types/domain";
import { ArtifactFile, ProjectFile, TraceFile } from "@/types/components";

/**
 * Defines a panel for parsing files.
 */
export interface ParseFilePanel<Environment, F extends ProjectFile> {
  title: string;
  projectFile: F;
  entityNames: string[];
  getIsValid(): boolean;
  clearPanel(): void;
  parseFile(env: Environment, file: File): Promise<void>;
}

/**
 * Defines a set of panels for uploading multiple types of files.
 */
export interface FileUploader<Environment, T, F extends ProjectFile> {
  panels: ParseFilePanel<Environment, F>[];
  createNewPanel(payload: T): ParseFilePanel<Environment, F>;
}

/**
 * Defines the types of objects that can be uploaded.
 */
export type ValidFileTypes = ArtifactFile | TraceFile;

/**
 * Defines the types of parsed objects used in upload verification as
 * either an artifact id or a trace link.
 */
export type ValidPayloads = string | LinkSchema;

/**
 * Defines a collection of parsed artifacts.
 */
export type ArtifactMap = Record<string, ArtifactSchema>;

/**
 * Defines a panel for parsing trace link files.
 */
export type TracePanel = ParseFilePanel<ArtifactMap, TraceFile>;

/**
 * Defines a set of panels for parsing trace link files.
 */
export type TraceUploader = FileUploader<ArtifactMap, LinkSchema, TraceFile>;

/**
 * Defines a panel for parsing artifact files.
 */
export type ArtifactPanel = ParseFilePanel<ArtifactMap, ArtifactFile>;

/**
 * Defines a set of panels for parsing artifact files.
 */
export type ArtifactUploader = FileUploader<ArtifactMap, string, ArtifactFile>;

export enum CreatorTabTypes {
  standard = "standard",
  bulk = "bulk",
  import = "import",
}
