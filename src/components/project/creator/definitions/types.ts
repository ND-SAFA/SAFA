import {
  ArtifactFile,
  ProjectFile,
  TraceFile,
} from "@/types/common-components";
import { Artifact } from "@/types/domain/artifact";

export interface IGenericFilePanel<Environment, F extends ProjectFile> {
  title: string;
  projectFile: F;
  entityNames: string[];
  getIsValid(): boolean;
  clearFile(): IGenericFilePanel<Environment, F>;
  parseFile(
    env: Environment,
    file: File
  ): Promise<IGenericFilePanel<Environment, F>>;
}

export interface IGenericUploader<Environment, T, F extends ProjectFile> {
  panels: IGenericFilePanel<Environment, F>[];
  createNewPanel(payload: T): IGenericFilePanel<Environment, F>;
}

export type ValidFileTypes = ArtifactFile | TraceFile;

export type ArtifactMap = Record<string, Artifact>;
