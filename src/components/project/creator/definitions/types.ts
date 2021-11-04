import {
  ArtifactFile,
  ProjectFile,
  TraceFile,
} from "@/types/common-components";
import { Artifact } from "@/types/domain/artifact";
import { TracePanel } from "@/components/project/creator/definitions/trace-uploader";

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

export type ArtifactMap = Record<string, Artifact>;

export function isTraceFile(obj: ProjectFile): obj is TraceFile {
  return (
    "source" in obj &&
    "target" in obj &&
    "isGenerated" in obj &&
    "traces" in obj
  );
}

export function isTracePanel(
  obj: IGenericFilePanel<any, any>
): obj is TracePanel {
  return isTraceFile(obj.projectFile);
}
