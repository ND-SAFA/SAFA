import { ArtifactType, ProjectMembership, TraceLink } from "@/types";
import { Artifact } from "./artifact";
import ArtifactTypeNode from "@/components/project/creator/tim-tree-view/ArtifactTypeNode.vue";

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
 * Enumerates the type of documents supported by SAFA
 */
export enum DocumentType {
  ARTIFACT_TREE = "ARTIFACT_TREE",
  FTA = "FTA",
}

/**
 * Defines a specific document.
 */
export interface ProjectDocument {
  /**
   * The id of this document.
   */
  documentId: string;
  /**
   * The project associated with this document.
   */
  project: ProjectIdentifier;
  /**
   * The name of the document.
   */
  name: string;
  /**
   * The description of the document.
   */
  description: string;
  /**
   * The type of document.
   */
  type: DocumentType;
  /**
   * The ids of artifacts displayed within this document.
   */
  artifactIds: string[];
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
   * Map of project members and their role.
   */
  members: ProjectMembership[];

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
}

export type VersionType = "major" | "minor" | "revision";
