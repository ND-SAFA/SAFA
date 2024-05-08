import {
  ArtifactSchema,
  ArtifactTypeSchema,
  AttributeLayoutSchema,
  AttributeSchema,
  ViewSchema,
  LayoutPositionsSchema,
  MembershipSchema,
  PermissionType,
  SubtreeMapSchema,
  TraceLinkSchema,
  TraceMatrixSchema,
} from "@/types";

/**
 * Defines a project.
 */
export interface IdentifierSchema {
  /**
   * The ID of the project.
   */
  projectId: string;
  /**
   * The organization that owns the project
   */
  orgId: string;
  /**
   * The team that owns the project.
   */
  teamId: string;

  /**
   * The name of the project.
   */
  name: string;
  /**
   * The description of the project.
   */
  description: string;
  /**
   * The AI generated summary of the most recent project version.
   */
  specification?: string;

  /**
   * List of members and their roles in the project.
   */
  members: MembershipSchema[];

  /**
   * The primary owner of this project.
   */
  owner: string;
  /**
   * The permissions of the current user on this project.
   */
  permissions: PermissionType[];
}

/**
 * Defines the version of a project.
 */
export interface VersionSchema {
  /**
   * The project version id.
   */
  versionId: string;
  /**
   * The project.
   */
  project?: IdentifierSchema;
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
export interface ProjectSchema extends IdentifierSchema {
  /**
   * The project's version.
   */
  projectVersion?: VersionSchema;

  /**
   * The project's artifacts.
   */
  artifacts: ArtifactSchema[];
  /**
   * The project's traces.
   */
  traces: TraceLinkSchema[];
  /**
   * The artifact types in the project.
   */
  artifactTypes: ArtifactTypeSchema[];
  /**
   * The trace matrices in the project.
   */
  traceMatrices: TraceMatrixSchema[];
  /**
   * The current document id.
   */
  currentDocumentId?: string;
  /**
   * The different documents for this project.
   */
  documents: ViewSchema[];

  /**
   * Map of artifact ids to their position in the default graph.
   */
  layout: LayoutPositionsSchema;
  /**
   * Map of artifact ids to their subtree information.
   */
  subtrees: SubtreeMapSchema;
  /**
   * A list of custom attributes used on this project.
   */
  attributes?: AttributeSchema[];
  /**
   * Layouts for displaying this project's custom attributes.
   */
  attributeLayouts?: AttributeLayoutSchema[];
}

/**
 * Represents a minimal project schema, to ensure that the main project store does
 * not have stale data retrieved from it. All omitted fields should be retrieved from their
 * own respective stores.
 */
export type MinimalProjectSchema = Omit<
  ProjectSchema,
  | "layout"
  | "artifacts"
  | "traces"
  | "artifactTypes"
  | "traceMatrices"
  | "attributes"
  | "attributeLayouts"
>;

export type VersionType = "major" | "minor" | "revision";
