import { Artifact, Link } from "@/types/domain";
import { ArtifactFile, ProjectFile, TraceFile } from "@/types/components";

export interface IGenericFilePanel<Environment, F extends ProjectFile> {
  title: string;
  projectFile: F;
  entityNames: string[];
  getIsValid(): boolean;
  clearPanel(): void;
  parseFile(env: Environment, file: File): Promise<void>;
}

export interface IGenericUploader<Environment, T, F extends ProjectFile> {
  panels: IGenericFilePanel<Environment, F>[];
  createNewPanel(payload: T): IGenericFilePanel<Environment, F>;
}

export type ValidFileTypes = ArtifactFile | TraceFile;

export type ValidPayloads = string | Link;

export type ArtifactMap = Record<string, Artifact>;

export interface TracePanel extends IGenericFilePanel<ArtifactMap, TraceFile> {
  generateTraceLinks(artifactMap: ArtifactMap): Promise<void>;
}

export type ArtifactPanel = IGenericFilePanel<ArtifactMap, ArtifactFile>;
