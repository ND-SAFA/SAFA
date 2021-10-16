import { Project, ProjectErrors, ProjectVersion } from "@/types/domain/project";
import { Artifact, ArtifactWarning } from "@/types/domain/artifact";
import { ArtifactDeltaState } from "@/types/domain/delta";
import { TraceLink } from "@/types/domain/links";

export interface HeaderOption {
  [key: string]: string;
}

export interface APIOptions {
  headers?: HeaderOption;
  method: string;
  body?: string | FormData;
}

export interface APIResponse<T> {
  status: number;
  body: T;
}

export interface APIError {
  status: number;
  body: APIErrorBody;
}

export interface APIErrorBody {
  message: string;
  error: string[];
}

export function isAPIError<T>(
  blob: APIResponse<T> | APIError
): blob is APIError {
  if (blob.status > 0) {
    return true;
  }
  return false;
}

export interface ProjectCreationResponse {
  project: Project;
  errors: ProjectErrors;
  projectVersion: ProjectVersion;
  warnings: Record<string, ArtifactWarning[]>;
}

export interface ProjectAndVersion {
  project: Project;
  projectVersion?: ProjectVersion;
}

export interface DataItem<T> {
  value: boolean;
  item: T;
}

export interface ArtifactNameValidationResponse {
  artifactExists: boolean;
}

export interface ArtifactChange {
  revisionType:
    | ArtifactDeltaState.ADDED
    | ArtifactDeltaState.MODIFIED
    | ArtifactDeltaState.REMOVED;
  artifact: Artifact;
}

export interface TraceChange {
  revisionType: ArtifactDeltaState.ADDED | ArtifactDeltaState.REMOVED;
  trace: TraceLink;
}

export interface Update {
  type: "included" | "excluded";
  traces: TraceLink[];
  artifacts: Artifact[];
}
