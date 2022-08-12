import {
  ArtifactPositions,
  ArtifactType,
  ArtifactWarning,
  MembershipModel,
  TraceLink,
} from "@/types";
import { Artifact } from "./artifact";
import { ProjectDocument } from "./document";

/**
 * Enumerates the states of parsing.
 */
export enum ApplicationActivity {
  PARSING_TIM,
  PARSING_ARTIFACTS,
  PARSING_TRACES,
  UNKNOWN,
}

/**
 * Defines a parser error.
 */
export interface ParserError {
  /**
   * The id of the error.
   */
  errorId: string;
  /**
   * The message of the error.
   */
  message: string;
  /**
   * The state of the parser when this error was encountered.
   */
  activity: ApplicationActivity;
  /**
   * The location of the error.
   */
  location: string;
}

/**
 * Defines a collection of all parser errors.
 */
export interface ProjectErrors {
  tim: ParserError[];
  artifacts: ParserError[];
  traces: ParserError[];
  allErrors: ParserError[];
}

/**
 * Defines a project.
 */
export interface ProjectIdentifier {
  /**
   * The ID of the project.
   */
  projectId: string;

  /**
   * The name of the project.
   */
  name: string;
  /**
   * The description of the project.
   */
  description: string;

  /**
   * List of members and roles in project.
   */
  members: MembershipModel[];

  /**
   * The primary owner of this project.
   */
  owner: string;
}

/**
 * Defines the version of a project.
 */
export interface ProjectVersion {
  /**
   * The project version id.
   */
  versionId: string;
  /**
   * The project.
   */
  project?: ProjectIdentifier;
  /**
   * The major version number.
   */
  majorVersion: number;
  /**
   * The minor version number.
   */
  minorVersion: number;
  /**
   * The revision version number.
   */
  revision: number;
}

/**
 * Defines a versioned and parsed project.
 */
export interface Project extends ProjectIdentifier {
  /**
   * The project's version.
   */
  projectVersion?: ProjectVersion;

  /**
   * The project's artifacts.
   */
  artifacts: Artifact[];
  /**
   * The project's traces.
   */
  traces: TraceLink[];

  /**
   * The current document id.
   */
  currentDocumentId?: string;
  /**
   * The different documents for this project.
   */
  documents: ProjectDocument[];

  /**
   * The artifact types present in the project.
   */
  artifactTypes: ArtifactType[];
  /**
   * A collection of warnings on project artifacts.
   */
  warnings: Record<string, ArtifactWarning[]>;
  /**
   * Map of artifact ids to their position in the default graph.
   */
  layout: ArtifactPositions;
}

export interface ProjectSummary {
  /**
   * The project itself.
   */
  project: Project;

  /**
   * A collection of errors on project artifacts.
   */
  errors: ProjectErrors;
}

export type VersionType = "major" | "minor" | "revision";
