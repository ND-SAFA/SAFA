import {
  Artifact,
  ArtifactWarning,
  ArtifactDeltaState,
  TraceLink,
  Project,
  ProjectErrors,
  ProjectVersion,
} from "@/types";

/**
 * Defines the options for interacting with API endpoints.
 */
export interface APIOptions {
  headers?: Record<string, string>;
  method: string;
  body?: string | FormData;
}

/**
 * Defines a response from the API.
 */
export interface APIResponse<T> {
  status: number;
  body: T;
}

/**
 * Defines a error response from the API.
 */
export interface APIError {
  /**
   * The error status.
   */
  status: number;
  /**
   * The body of the error.
   */
  body: APIErrorBody;
}

/**
 * Defines an API error.
 */
export interface APIErrorBody {
  /**
   * The error details.
   */
  details: string;
  /**
   * The error message.
   */
  message: string;
  /**
   * A list of stack traces.
   */
  errors: string[];
}

/**
 * Defines the response for a created project.
 */
export interface ProjectCreationResponse {
  /**
   * The created project.
   */
  project: Project;
  /**
   * Any errors from creation.
   */
  errors: ProjectErrors;
  /**
   * The version of the project.
   */
  projectVersion: ProjectVersion;
  /**
   * A collection of warnings on project artifacts.
   */
  warnings: Record<string, ArtifactWarning[]>;
}

/**
 * Defines a toggleable item of data.
 */
export interface DataItem<T> {
  /**
   * Whether this item is enabled.
   */
  value: boolean;
  /**
   * The item of data.
   */
  item: T;
}

/**
 * Defines the response from checking if an artifact exists.
 */
export interface ArtifactNameValidationResponse {
  /**
   * Whether the artifact exists.
   */
  artifactExists: boolean;
}
/**
 * Defines a changed artifact.
 */
export interface ArtifactChange {
  /**
   * The type of change to this artifact.
   */
  revisionType:
    | ArtifactDeltaState.ADDED
    | ArtifactDeltaState.MODIFIED
    | ArtifactDeltaState.REMOVED;
  /**
   * The artifact changed.
   */
  artifact: Artifact;
}

/**
 * Defines a changed trance.
 */
export interface TraceChange {
  /**
   * The type of change to this trace.
   */
  revisionType: ArtifactDeltaState.ADDED | ArtifactDeltaState.REMOVED;
  /**
   * The trace changed.
   */
  trace: TraceLink;
}

/**
 * Defines an update to traces and artifacts within a project version.
 */
export interface ProjectVersionUpdate {
  /**
   * Whether the data modified is included in the Update.
   */
  type: "included" | "excluded";
  /**
   * The traces updated.
   */
  traces: TraceLink[];
  /**
   * The artifacts updated.
   */
  artifacts: Artifact[];
}

/**
 * The response from parsing a file.
 */
export interface ParseFileResponse {
  /**
   * Any parsing errors encountered.
   */
  errors: string[];
}

/**
 * The response from parsing an artifact file.
 */
export interface ParseArtifactFileResponse extends ParseFileResponse {
  /**
   * The artifacts parsed.
   */
  artifacts: Artifact[];
}

/**
 * The response from parsing a trace file.
 */
export interface ParseTraceFileResponse extends ParseFileResponse {
  /**
   * The traces parsed.
   */
  traces: TraceLink[];
}
