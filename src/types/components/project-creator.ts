import { Artifact, Link } from "@/types/domain";
import { ArtifactFile, ProjectFile, TraceFile } from "@/types/components";

/**
 * Defines a panel for parsing files.
 */
export interface IGenericFilePanel<Environment, F extends ProjectFile> {
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
export interface IGenericUploader<Environment, T, F extends ProjectFile> {
  panels: IGenericFilePanel<Environment, F>[];
  createNewPanel(payload: T): IGenericFilePanel<Environment, F>;
}

/**
 * Defines the types of objects that can be uploaded.
 */
export type ValidFileTypes = ArtifactFile | TraceFile;

/**
 * Defines the types of parsed objects used in upload verification as
 * either an artifact id or a trace link.
 */
export type ValidPayloads = string | Link;

/**
 * Defines a collection of parsed artifacts.
 */
export type ArtifactMap = Record<string, Artifact>;

/**
 * Defines a panel for parsing trace link files.
 */
export interface TracePanel extends IGenericFilePanel<ArtifactMap, TraceFile> {
  generateTraceLinks(artifactMap: ArtifactMap): Promise<void>;
}

/**
 * Defines a panel for parsing artifact files.
 */
export type ArtifactPanel = IGenericFilePanel<ArtifactMap, ArtifactFile>;

export enum CreatorTypes {
  standard = "standard",
  bulk = "bulk",
  jira = "jira",
  github = "github",
}
