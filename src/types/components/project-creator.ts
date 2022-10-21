import { ArtifactModel, LinkModel } from "@/types/domain";
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
export type ValidPayloads = string | LinkModel;

/**
 * Defines a collection of parsed artifacts.
 */
export type ArtifactMap = Record<string, ArtifactModel>;

/**
 * Defines a panel for parsing trace link files.
 */
export type TracePanel = IGenericFilePanel<ArtifactMap, TraceFile>;

/**
 * Defines a set of panels for parsing trace link files.
 */
export type TraceUploader = IGenericUploader<ArtifactMap, LinkModel, TraceFile>;

/**
 * Defines a panel for parsing artifact files.
 */
export type ArtifactPanel = IGenericFilePanel<ArtifactMap, ArtifactFile>;

/**
 * Defines a set of panels for parsing artifact files.
 */
export type ArtifactUploader = IGenericUploader<
  ArtifactMap,
  string,
  ArtifactFile
>;

export enum CreatorTabTypes {
  standard = "standard",
  bulk = "bulk",
  jira = "jira",
  github = "github",
}
